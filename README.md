Console Wrap
================

<p>
    <img src="https://img.shields.io/github/release/unknownuser88/consolewrap.svg" alt="Release version">
    <img src="https://img.shields.io/badge/stability-stable-brightgreen.svg" alt="Stability: Stable">
    <img src="https://img.shields.io/packagecontrol/dt/Console%20Wrap.svg" alt="Package Control">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" alt="License: MIT">
</p>

This plugin helps you easily create (comment, remove, show all) log statements (console.log, print etc.)

It places selected variable in log statement like console.log("variable", variable);

*This is not a snippet.* 

#### Supported languages

* Javascript
* Python
* Php

## Usage

First you need to select a variable (or put cursor on it) and press `"ctrl+shift+q"`. The log line will appear on the next line. Press `"ctrl+shift+q"` again to change wrapping (info,warn etc.)

You can Also remove, comment or remove commented log statements from your selsection or from all document
you can find that functionality in context menu (right click) or Command Palette (command+shift+p on OS X, control+shift+p on Linux/Windows).


## Screenshots

| Javascript |
| ---------- |
| ![Javascript](https://github.com/unknownuser88/consolewrap/raw/demo/images/js.gif) |

| Python |
| ------ |
| ![Python](https://github.com/unknownuser88/consolewrap/raw/demo/images/py.gif)  |

| Php |
| --- |
| ![Php](https://github.com/unknownuser88/consolewrap/raw/demo/images/php.gif) |

| All Logs |
| -------- |
| ![All Logs](https://github.com/unknownuser88/consolewrap/raw/demo/images/list.gif)  |


## Key Binding

The default key binding is `"ctrl+shift+q"` and `"ctrl+shift+alt+q"` (insert before selection).

```javascript
{ 
    "keys": ["ctrl+shift+q"], 
    "command": "console_wrap",
    "args": {"insert_before": false}
},
{ 
    "keys": ["ctrl+shift+alt+q"], 
    "command": "console_wrap",
    "args": {"insert_before": true}
}
```

## Commands

```javascript
{
    "caption": "Console Wrap: Create logs",
    "command": "console_wrap"
}, {
    "caption": "Console Wrap: Remove logs",
    "command": "console_action",
    "args": {"action": "remove"}
}, {
    "caption": "Console Wrap: Remove Commented logs",
    "command": "console_action",
    "args": {"action": "remove_commented"}
}, {
    "caption": "Console Wrap: Comment logs",
    "command": "console_action",
    "args": {"action": "comment"}
}, {
    "caption": "Console Wrap: Show all logs",
    "command": "console_action",
    "args": {"action": "show_quick_nav"}
}
```

## Settings

```javascript
{
    "js": {
        "consoleStr"   : "{title}, {variable}", // "{title}, tmpVal = {variable}" to assigne value to temporary parameter output: console.log('title', tmpVal = variable);
        "consoleFunc"  : ["console", "log"],    // You can change default log statement for example ["logger", "info"] output: logger.info('title', variable);
        "single_quotes": false,                 // If true output: console.log('title', variable);
        "semicolon"    : true,                  // If false, will not add semicolon at end of line
        "log_types"    : ["log", "info", "warn", "error"]
    },
    "py": {
        "consoleStr"   : "{title}, {variable}",
        "consoleFunc"  : ["print"],
        "single_quotes": false
    },
    "php": {
        "consoleFunc"  : ["print_r"],   // var_dump or if you have custom logger ["$logger", "debug"] output: $logger->debug($variable);
        "preTag"       : true,          // Put log in pre tag like echo '<pre>'; print_r($variable); echo '</pre>';
        "dieAfterLog"  : false          // echo '<pre>'; print_r($variable); echo '</pre>'; die();
    },
    "fileTypeMap" : {                   // Maps file type to wrapper. For example "text.html.vue": "js" means use js wrapper in vue js files
        "text.html.vue"  : "js",        // php,python,js is included by dafault ("embedding.php": "php", "source.js": "js", "source.python": "py")
        "source.ts"      : "js",
        "source.tsx"     : "js",
        "source.coffee"  : "js",
        "text.html.basic": "js",
        "text.html.blade": "js",
        "text.html.twig" : "js"
    }
}

```

## How to install

With [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run “Package Control: Install Package” command, find and install `Console Wrap` plugin.
2. Restart Sublime Text editor (if required)

Manually:

1. Clone or [download](https://github.com/unknownuser88/consolewrap/archive/master.zip) git repo into your packages folder (in Sublime Text, find Browse Packages... menu item to open this folder)
2. Restart Sublime Text editor (if required)

---
