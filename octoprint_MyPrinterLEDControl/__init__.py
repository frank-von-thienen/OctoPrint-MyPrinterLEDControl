# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import logging
import os

logger = logging.getLogger (__name__)

# defining global static variables
class StatusTrigger:
    PRINTING = False

# Plugin reacts on different printer status
class MyPrinterLEDControlPlugin(octoprint.plugin.StartupPlugin,
                                octoprint.plugin.TemplatePlugin):
    # initialize variables and register callback
    def on_after_startup(self):
        StatusTrigger.PRINTING = False
        callback = MyPrinterCallback(self._printer)
        self._printer.register_callback(callback)

        # doing some WEBCAM adjustments
        os.system ("uvcdynctrl -s 'Power Line Frequency' 1")            # setting frequency to 50Hz
        os.system ("uvcdynctrl -s 'White Balance Temperature, Auto' 0") # switching off AUTO WBT
        os.system ("uvcdynctrl -s 'White Balance Temperature' 5700")
        os.system ("uvcdynctrl -s 'Exposure, Auto' 0")                  # swithing off AUTO Exposure
        os.system ("uvcdynctrl -s 'Exposure (Absolute)' 120")
        os.system ("uvcdynctrl -s 'Contrast' 155")
        os.system ("uvcdynctrl -s 'Brightness' 175")
        os.system ("uvcdynctrl -s 'Focus, Auto' 0")                      # switching off AUTO Focus
        os.system ("uvcdynctrl -s 'Focus (absolute)' 30")

class MyPrinterCallback(octoprint.printer.PrinterCallback):
    def __init__(self, printer):
        self._printer = printer

    # Compare some flag to see if the printer is printing in real
    # If the printer starts heating the FLAG:PRINTING is set
    # I use this information in Octoprint GCODE script:BEFORE PRINT JOB STARTS to set the LEDs to RED
    # Unfortunately, this is not an indication for printing th eobject.
    # The "real" printing starts, if the bed is move in Z direction (first layer hight)
    # This is the  indicator for starting the print and setting the LEDs to white
    # Setting the LEDs to GREEN is handled by OctoPrint GCODE script:AFTER PRINT JOB COMPLETES

    def on_printer_send_current_data(self, data):
        if data["state"]["flags"]["printing"] == True and data["currentZ"] > 0 and StatusTrigger.PRINTING == False:
            StatusTrigger.PRINTING = True
            self._printer.commands ("M420 R1 E1 B1")



#plugin settings
__plugin_name__           = "My Printer LED Control"
__plugin_description__    = "Plugin switching LEDS depending on the printer status"
__plugin_author__         = "Frank von Thienen"
__plugin_version__        = "0.9.3"

__plugin_implementation__ = MyPrinterLEDControlPlugin()
