# Board 6 - Teilnehmer-Board, zwei LED-Streifen
#   Grove 2 (GP3)       = Grove Button
#   Grove 3 (GP5)       = Ultraschall Grove Ranger
#   Grove 4 (GP17/GP16) = Streifen 1, Feuerball (orange-weiss)
#   Grove 5 (GP26)      = Streifen 2, Blitz (lila-blau)
#   Grove 6 (GP27)      = Grove Buzzer
# Knopfdruck ODER Kugel vor dem Ultraschall -> beide Streifen schiessen gleichzeitig los.
# Sie sind unterschiedlich lang, laufen aber synchron und kommen zusammen an.

import board, digitalio, neopixel, pwmio, random, time

N1 = 60                    # LEDs Streifen 1 an Grove 4
N2 = 104                   # LEDs Streifen 2 an Grove 5 (nachzaehlen!)
HELL = 0.8                 # beide Streifen zusammen, daher etwas unter Vollgas
SCHWEIF1 = 12              # Flammenschweif
SCHWEIF2 = 14              # Blitzschweif, laenger weil der Streifen laenger ist
SCHRITTE = 110             # Bilder pro Schuss; mehr = langsamer und weicher
START_TEMPO = 0.020        # Sekunden pro Bild am Anfang
END_TEMPO = 0.007          # Sekunden pro Bild am Ende (beschleunigt)
MAX_WARTEND = 3            # so viele Ausloeser werden hoechstens gemerkt
SCHWELLE_CM = 12.0         # alles naeher als 12 cm zaehlt als Kugel
MESSPAUSE = 0.15           # Sekunden zwischen zwei Ultraschall-Messungen
TON_START = 1500           # Hz beim Abschuss
TON_ENDE = 260             # Hz kurz vor dem Einschlag
LAUT = 32768               # 32768 = volle Lautstaerke, kleiner = leiser

# Streifen 1 wird auf beiden moeglichen Pins getrieben, Streifen 2 nur auf GP26
s1a = neopixel.NeoPixel(board.GP17, N1, brightness=HELL, auto_write=False)
s1b = neopixel.NeoPixel(board.GP16, N1, brightness=HELL, auto_write=False)
s2 = neopixel.NeoPixel(board.GP26, N2, brightness=HELL, auto_write=False)

taste = digitalio.DigitalInOut(board.GP3)      # Grove Button an Grove 2
taste.switch_to_input(pull=digitalio.Pull.DOWN)   # Modul liefert HIGH bei Druck

sig = digitalio.DigitalInOut(board.GP5)        # Ultraschall an Grove 3, einmal anlegen
sig.switch_to_input(pull=digitalio.Pull.DOWN)

pwm = pwmio.PWMOut(board.GP27, frequency=880, duty_cycle=0, variable_frequency=True)

wartend = 0                # gemerkte Ausloeser
gedrueckt = False          # Knopfzustand beim letzten Blick

def knopf_pruefen():       # zaehlt jeden neuen Druck, auch waehrend der Animation
    global wartend, gedrueckt
    jetzt = taste.value
    if jetzt and not gedrueckt:
        wartend = min(wartend + 1, MAX_WARTEND)
    gedrueckt = jetzt

# ---------------- Ultraschall ----------------
def abstand_cm(limit=30_000_000):
    sig.switch_to_output(False)
    time.sleep(0.000005)
    sig.value = True
    time.sleep(0.00002)                        # 20 us Trigger
    sig.value = False
    sig.switch_to_input(pull=digitalio.Pull.DOWN)
    t = time.monotonic_ns()
    while not sig.value:
        if time.monotonic_ns() - t > limit: return None
    t = time.monotonic_ns()
    while sig.value:
        if time.monotonic_ns() - t > limit: return None
    return (time.monotonic_ns() - t) / 1000 / 58

def messen():
    try:
        return abstand_cm()
    except Exception:
        return None

# ---------------- Ton ----------------
def ton(f, laut):
    pwm.frequency = max(60, min(20000, int(f))); pwm.duty_cycle = int(laut)

def still():
    pwm.duty_cycle = 0

def rauschen(basis, laut, dauer, breite=0.7):
    """Wartezeit in kurze Stuecke zerhacken, jedes mit anderer Tonhoehe = Fauchen."""
    ende = time.monotonic() + dauer
    while time.monotonic() < ende:
        ton(basis * (1 - breite + random.random() * breite * 2), laut)
        time.sleep(0.004)

# ---------------- Licht ----------------
def setze1(i, c):
    s1a[i] = c; s1b[i] = c

def loesche():
    s1a.fill(0); s1b.fill(0); s2.fill(0)

def zeige():
    s1a.show(); s1b.show(); s2.show()

def flamme(h):                                 # Streifen 1: weissgluehend -> Asche
    if h > 0.85: return (255, 255, 210)
    if h > 0.60: return (255, int(200 * h), 20)
    if h > 0.30: return (255, int(110 * h), 0)
    return (int(255 * h * 2.5), 0, 0)

def blitz(h):                                  # Streifen 2: weissblau -> lila -> tiefblau
    if h > 0.85: return (210, 200, 255)
    if h > 0.60: return (int(190 * h), int(60 * h), 255)
    if h > 0.30: return (int(110 * h), 0, int(255 * h + 60))
    return (int(40 * h * 2.5), 0, int(255 * h * 2.2))

def schuss():
    # 1. Zuendung: beide Streifen gluehen am Start auf
    loesche()
    setze1(0, (255, 255, 210))
    if N1 > 1: setze1(1, (255, 160, 20))
    s2[0] = (210, 200, 255)
    if N2 > 1: s2[1] = (150, 60, 255)
    zeige()
    for i in range(14):
        ton(180 + i * 130, LAUT)
        time.sleep(0.007)

    # 2. Flug: ein Takt fuer beide Streifen, jeder rechnet seine Position selbst aus
    for f in range(SCHRITTE + 1):
        frac = f / SCHRITTE
        loesche()
        kopf1 = int(frac * (N1 + SCHWEIF1))
        for k in range(SCHWEIF1 + 1):
            i = kopf1 - k
            if 0 <= i < N1:
                setze1(i, flamme(1.0 if k == 0 else (SCHWEIF1 - k + 1) / SCHWEIF1))
        kopf2 = int(frac * (N2 + SCHWEIF2))
        for k in range(SCHWEIF2 + 1):
            i = kopf2 - k
            if 0 <= i < N2:
                s2[i] = blitz(1.0 if k == 0 else (SCHWEIF2 - k + 1) / SCHWEIF2)
        zeige()
        knopf_pruefen()
        basis = TON_START * (TON_ENDE / TON_START) ** frac
        rauschen(basis, LAUT * (1 - 0.55 * frac),
                 START_TEMPO + (END_TEMPO - START_TEMPO) * frac,
                 breite=0.35 + 0.4 * frac)

    # 3. Einschlag: beide Enden gluehen aus, tiefes Grollen
    for c1, c2, l in (((255, 230, 180), (220, 210, 255), 1.0),
                      ((255, 140, 0), (150, 70, 255), 0.85),
                      ((200, 50, 0), (90, 20, 200), 0.6),
                      ((90, 15, 0), (40, 0, 110), 0.35),
                      ((30, 0, 0), (12, 0, 40), 0.15)):
        loesche()
        setze1(N1 - 1, c1)
        if N1 > 1: setze1(N1 - 2, c1)
        s2[N2 - 1] = c2
        if N2 > 1: s2[N2 - 2] = c2
        zeige()
        knopf_pruefen()
        rauschen(95, LAUT * l, 0.07, breite=0.85)
    still()
    loesche(); zeige()

# ---------------- Start ----------------
loesche()
for i in range(N1): setze1(i, (0, 40, 0))      # Selbsttest Streifen 1: gruen
for i in range(N2): s2[i] = (0, 0, 40)         # Selbsttest Streifen 2: blau
zeige(); ton(660, LAUT); time.sleep(0.15); still()
time.sleep(0.35)
loesche(); zeige()
gedrueckt = taste.value                        # Startzustand merken, kein Fehlstart
naechste_messung = time.monotonic()

while True:
    knopf_pruefen()                            # Knopf an Grove 2

    if time.monotonic() >= naechste_messung:   # Ultraschall an Grove 3
        naechste_messung = time.monotonic() + MESSPAUSE
        d = messen()
        if d is not None and d < SCHWELLE_CM:  # Kugel im Kegel
            wartend = min(wartend + 1, MAX_WARTEND)
            naechste_messung = time.monotonic() + 0.5

    if wartend > 0:
        wartend -= 1
        schuss()
        naechste_messung = time.monotonic() + 0.5   # nach dem Flug kurz nicht messen

    time.sleep(0.01)