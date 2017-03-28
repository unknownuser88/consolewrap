ConsoleWrap for JS
================

## Summary
This plugin places your selected variable in console.log as console.log('variable' , variable);
THIS IS NOT A SNIPPET.

## Screenshot
![ScreenShot](https://raw.github.com/unknownuser88/consolewrap/master/images/demo.gif)

## Install

#### Git Clone
Clone this repository in to the Sublime Text "Packages" directory, which is located where ever the
"Preferences" -> "Browse Packages" option in sublime takes you.

## Key Binding

The default key binding is "ctrl+shift+q" and "ctrl+shift+alt+q" (insert before selection).

## Key Binding Conflicts

Unfortunately there are other plugins that use "ctrl+shift+q", this is a hard problem to solve. If consolewrap doesn't work, then you have two options:

1. Add ```{"keys": ["ctrl+shift+q"],  "command": "consolewrap"}``` to your user keybindings file. This will override anything specifid by a plugin.
2. Find the offending plugin, and change the shortcut in its sublime-keymap file (will revert on updates).


## Usage

First you need to select a variable and press "ctrl+shift+q". The console.log line will appear on the next line. Press "ctrl+shift+q" again to change wrapping (info,warn etc.)

You can Also remove or comment all console.logs from your selsection or from all document

Edit settings to format output

```javascript
{
    "js": {
        "consoleStr"   : "{title}, {variable}", // "{title}, tmpVal = {variable}" to assigne value to temporary parameter output: console.log('title', tmpVal = variable);
        "consoleFunc"  : ["console", "log"],    // you can change default log statement for example ["logger", "info"] output: logger.info('title', variable);
        "single_quotes": false,                 // if true output: console.log('title', variable);
        "semicolon"    : true,                  // if false, will not add semicolon at end of line
        "log_types"    : ["log", "info", "warn", "error"],
    },
    "py": {
        "consoleStr"   : "{title}, {variable}",
        "consoleFunc"  : ["print"],
        "single_quotes": false
    },
    "php": {
        "consoleFunc"  : ["print_r"],   // var_dump or if you have custom logger ["$logger", "debug"] output: $logger->debug($variable);
        "preTag"       : true,          // put log in pre tag like echo '<pre>'; print_r($variable); echo '</pre>';
        "dieAfterLog"  : false          // echo '<pre>'; print_r($variable); echo '</pre>'; die();
    },
    "supportedFileTypes" : {
        "embedding.php"  : "php",
        "text.html.vue"  : "js",
        "source.ts"      : "js",
        "source.tsx"     : "js",
        "source.coffee"  : "js",
        "source.js"      : "js",
        "text.html.basic": "js",
        "text.html.blade": "js",
        "text.html.twig" : "js",
        "source.python"  : "py"
    }
}
```

---
