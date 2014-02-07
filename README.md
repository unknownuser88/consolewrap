ConsoleWrap
================

## Summary
This plugin places your selected variable in console.log as console.log('variable' , variable); 
THIS IS NOT A SNIPPET.

## Screenshot

![ScreenShot](https://raw.github.com/unknownuser88/consolewrap/master/screenshot.PNG)

## Install

#### Git Clone
Clone this repository in to the Sublime Text "Packages" directory, which is located where ever the
"Preferences" -> "Browse Packages" option in sublime takes you.

## Key Binding

The default key binding is "ctrl+shift+q".

## Key Binding Conflicts

Unfortunately there are other plugins that use "ctrl+shift+q", this is a hard problem to solve. If consolewrap doesn't work, then you have two options:

1. Add ```{"keys": ["ctrl+shift+q"],  "command": "consolewrap"}``` to your user keybindings file. This will override anything specifid by a plugin.
2. Find the offending plugin, and change the shortcut in its sublime-keymap file (will revert on updates).


## Usage

First you need to select a variable and press "ctrl+shift+q". The cosole.log line will appear on the next line. 

---
