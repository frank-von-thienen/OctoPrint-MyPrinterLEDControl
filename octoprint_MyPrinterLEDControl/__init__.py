# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import logging
import os

logger = logging.getLogger (__name__)

# defining global static variables
class StatusTrigger:
    PRINTING = False

class MyPrinterLEDControlPlugin(octoprint.plugin.StartupPlugin,
                                octoprint.plugin.TemplatePlugin):
    # initialize variables and register callback
    def on_after_startup(self):
        StatusTrigger.PRINTING = False
        callback = MyPrinterCallback(self._printer)
        self._printer.register_callback(callback)

        # doing some WEBCAM adjustments
        os.system ("uvcdynctrl -s 'Power Line Frequency' 1")
        os.system ("uvcdynctrl -s 'White Balance Temperature, Auto' 0")
        os.system ("uvcdynctrl -s 'White Balance Temperature' 5700")
        os.system ("uvcdynctrl -s 'Exposure, Auto' 0")
        os.system ("uvcdynctrl -s 'Exposure (Absolute)' 120")
        os.system ("uvcdynctrl -s 'Contrast' 155")
        os.system ("uvcdynctrl -s 'Brightness' 175")
        os.system ("uvcdynctrl -s 'Focus, Auto' 0") 
        os.system ("uvcdynctrl -s 'Focus (absolute)' 30")

class MyPrinterCallback(octoprint.printer.PrinterCallback):
    def __init__(self, printer):
        self._printer = printer

    # compare some flag to see if the printer is printing in real
    def on_printer_send_current_data(self, data):
        if data["state"]["flags"]["printing"] == True and data["currentZ"] > 0 and StatusTrigger.PRINTING == False:
            StatusTrigger.PRINTING = True
            self._printer.commands ("M420 R1 E1 B1")

#    def on_printer_add_message(self, data):
#        logger.info ("add message %s", data)
__plugin_name__ = "My Printer LED Control"
__plugin_implementation__ = MyPrinterLEDControlPlugin()
