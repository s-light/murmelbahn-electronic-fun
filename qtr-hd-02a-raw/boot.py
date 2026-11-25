import usb_cdc

# console: REPL, status messages and commands
# data:    second serial port, only plot data (for SerialPlot)
# takes effect after a hard reset
usb_cdc.enable(console=True, data=True)
