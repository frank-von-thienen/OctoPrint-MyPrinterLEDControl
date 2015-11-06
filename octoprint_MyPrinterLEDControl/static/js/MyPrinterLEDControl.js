/*
 * View model for MyPrinterLEDControl
 *
 * Author: Frank von Thienen
 * License: AGPLv3
 */
$(function() {
    function MyprinterledcontrolViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        MyprinterledcontrolViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        [ /* "loginStateViewModel", "settingsViewModel" */ ],

        // e.g. #settings_plugin_MyPrinterLEDControl, #tab_plugin_MyPrinterLEDControl, ...
        [ /* ... */ ]
    ]);
});
