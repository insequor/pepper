console.log("commandprompt.js is loaded and more");

const KeyCodes = {
    // Modifier keys
    SHIFT: 16,
    CTRL: 17,
    ALT: 18,
    META: 91, // Windows/Command key
    CONTEXT_MENU: 93,
  
    // Special keys
    ENTER: 13,
    ESCAPE: 27,
    SPACE: 32,
    BACKSPACE: 8,
    TAB: 9,
    CAPS_LOCK: 20,
    NUM_LOCK: 144,
    SCROLL_LOCK: 145,
    INSERT: 45,
    DELETE: 46,
    HOME: 36,
    END: 35,
    PAGE_UP: 33,
    PAGE_DOWN: 34,
    
    // Arrow keys
    ARROW_UP: 38,
    ARROW_DOWN: 40,
    ARROW_LEFT: 37,
    ARROW_RIGHT: 39,
  
    // Function keys
    F1: 112,
    F2: 113,
    F3: 114,
    F4: 115,
    F5: 116,
    F6: 117,
    F7: 118,
    F8: 119,
    F9: 120,
    F10: 121,
    F11: 122,
    F12: 123,
  };


class KeyInfo {
    constructor() {

    }

    static modifiers = [
        KeyCodes.SHIFT, 
        KeyCodes.CTRL, 
        KeyCodes.META,
        KeyCodes.CONTEXT_MENU,
    ];

    static autoComplate = [KeyCodes.ARROW_RIGHT];
    static previous = [KeyCodes.ARROW_UP];
    static next = [KeyCodes.ARROW_DOWN];
    static back = [KeyCodes.ARROW_LEFT];
    static ignored = [KeyCodes.ARROW_RIGHT];
    static cancel = "";
    static enter = "";

    static hasModifiers() {
    }

}

window.onload = function() {
    let commandElement = document.querySelector("#command");
    let optionsElement = document.querySelector("#options");
    var current = -1;
    var currentOptions = [];
    commandElement.focus();
    commandElement.addEventListener('keydown', function (e) {
        return;
        console.log("keydown", e.key, e.which, commandElement.value);
        currentOptions = getFilteredOptions(commandElement.value);
        updateOptions();
    });
    commandElement.addEventListener('keyup', function (e) {
        console.log("keyup", e.key, e.which, commandElement.value);
        handleSpecialKey(e, commandElement.value);
    });

    function getFilteredOptions(value) {
        var options = [];
        if(!value){
            options = Array.from(allOptions);
        }
        else {
            for(let option of allOptions){
                if(option.toLowerCase().indexOf(value.toLowerCase()) >= 0){
                    options.push(option);
                }
            }
        }
        options.sort();
        if(options != [] && value) {
            current = 0;
        }
        else {
            current = -1;
        }
        return options;
    }
    function updateOptions() {
        // Use the given value to filter out the options and show the remaining ones only
        const options_ = Array.from(currentOptions);
        if(current >= 0 && current < options_.length) {
            options_[current] = "* " + options_[current];
        }
        optionsElement.innerHTML = options_.join("<br/>");
    }
    function handleSpecialKey(key, value) {
        switch(key.which) {
            case KeyCodes.ARROW_DOWN: {
                console.log("Select the next item");
                if (current == currentOptions.length - 1){
                    current = 0;
                }
                else {
                    current += 1;
                }
                break;
            }
            case KeyCodes.ARROW_UP: {
                console.log("Select the previous item");
                if(current <= 0) {
                    current = currentOptions.length - 1;
                }
                else {
                    current -= 1;
                }
                
                break;
            }
            case KeyCodes.ESCAPE: {
                exitCommand();
                return;
            }
            case KeyCodes.ENTER: {
                executeCommand(value, currentOptions[current]);
                return;
            }
            default: {
                currentOptions = getFilteredOptions(commandElement.value);
            }
        }
        updateOptions();
    }
    currentOptions = getFilteredOptions(); 
    updateOptions();
};

function showResponse(response) {
    console.log(response);
}
function executeCommand(value, selection) {
    console.log("Execute command", value, selection);
    try{
        pywebview.api.execute(value, selection).then(showResponse)
    }
    catch(error) {
        showResponse(error);
    }
    
}

function exitCommand() {
    console.log("Exit command");
    try {
        pywebview.api.cancel().then(showResponse);
    }
    catch(error) {
        showResponse(error);
    }
}

