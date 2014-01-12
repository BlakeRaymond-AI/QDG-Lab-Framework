Range = {
# Format (FormatNumber, Low Voltage, High Voltage)
'BIP20VOLTS': (15, -20, 20),
'BIP10VOLTS': (1, -10, 10), # Only channel usable in single-ended mode.
'BIP5VOLTS': (0, -5, 5),
'BIP4VOLTS': (16, -4, 4),
'BIP2PT5VOLTS': (2, -2.5, 2.5),
'BIP2VOLTS': (14, -2.0, 2.0),
'BIP1PT25VOLTS': (3, -1.25, 1.25),
'BIP1VOLTS': (4, -1, 1),
}

TrigType = {'GATE_HIGH': 8,
            'GATE_LOW': 9,
            'TRIG_HIGH': 10,
            'TRIG_LOW': 11,
            'TRIG_POS_EDGE': 12,
            'TRIG_NEG_EDGE': 13
}

Options = {
'FOREGROUND': 0x0000, # Run in foreground, don't return till done
'BACKGROUND': 0x0001, # Run in background, return immediately
'SINGLEEXEC': 0x0000, # One execution
'CONTINUOUS': 0x0002, # Run continuously until cbstop() called
'TIMED': 0x0000, # Time conversions with internal clock
'EXTCLOCK': 0x0004, # Time conversions with external clock
'NOCONVERTDATA': 0x0000, # Return raw data
'CONVERTDATA': 0x0008, # Return converted A/D data
'NODTCONNECT': 0x0000, # Disable DT Connect
'DTCONNECT': 0x0010, # Enable DT Connect
'SCALEDATA': 0x0010, # Scale scan data to engineering units
'DEFAULTIO': 0x0000, # Use whatever makes sense for board
'SINGLEIO': 0x0020, # Interrupt per A/D conversion
'DMAIO': 0x0040, # DMA transfer
'BLOCKIO': 0x0060, # Interrupt per block of conversions
'BURSTIO': 0x10000, # Transfer upon scan completion
'RETRIGMODE': 0x20000, # Re-arm trigger upon acquiring trigger count samples
'NONSTREAMEDIO': 0x040000, # Non-streamed D/A output
'ADCCLOCKTRIG': 0x080000, # Output operation is triggered on ADC clock
'ADCCLOCK': 0x100000, # Output operation is paced by ADC clock
'HIGHRESRATE': 0x200000, # Use high resolution rate
'SHUNTCAL': 0x400000, # Enable Shunt Calibration
'BYTEXFER': 0x0000, # Digital IN/OUT a byte at a time
'WORDXFER': 0x0100, # Digital IN/OUT a word at a time
'INDIVIDUAL': 0x0000, # Individual D/A output
'SIMULTANEOUS': 0x0200, # Simultaneous D/A output
'FILTER': 0x0000, # Filter thermocouple inputs
'NOFILTER': 0x0400, # Disable filtering for thermocouple
'NORMMEMORY': 0x0000, # Return data to data array
'EXTMEMORY': 0x0800, # Send data to memory board ia DT-Connect
'BURSTMODE': 0x1000, # Enable burst mode
'NOTODINTS': 0x2000, # Disbale time-of-day interrupts
'EXTTRIGGER': 0x4000, # A/D is triggered externally
'NOCALIBRATEDATA': 0x8000, # Return uncalibrated PCM data
'CALIBRATEDATA': 0x0000, # Return calibrated PCM A/D data
'CTR16BIT': 0x0000, # Return 16-bit counter data
'CTR32BIT': 0x0100, # Return 32-bit counter data
'CTR48BIT': 0x0200, # Return 48-bit counter data
'ENABLED': 1,
'DISABLED': 0,
'UPDATEIMMEDIATE': 0,
'UPDATEONCOMMAND': 1,
}