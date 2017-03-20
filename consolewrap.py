import sublime
import sublime_plugin

try:
    from .core.settings import *
    from .core.js_wrapper import *
    from .core.py_wrapper import *
except ValueError:
    from core.settings import *
    from core.js_wrapper import *
    from core.py_wrapper import *

def plugin_loaded():
    msg('*' * 30 + ' start ' + '*' * 30)


def checkFileType(view):
    supportedFileTypes = settings().get('supportedFileTypesa') or {
        "embedding.php"  : "js",
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
    return (list(set(view.scope_name(0).split(' ')).intersection(supportedFileTypes)), supportedFileTypes)


def getWrapperType(view):
    fileTypeIntersect, supportedFileTypes = checkFileType(view)

    wrapperType = supportedFileTypes.get(fileTypeIntersect[0], False)

    return wrapperType


class ConsoleWrapCommand(sublime_plugin.TextCommand):
    def run(self, edit, insert_before=False):
        wrapper = getWrapperType(self.view)

        if not wrapper:
            return sublime.status_message('Console Wrap: Not work in this file type')
        self.view.run_command(wrapper + '_wrapp_create', {'insert_before': insert_before})


class ConsoleCleanCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        if not checkFileType(self.view):
            return False
        return True

    def run(self, edit, action=False):
        self.view.run_command(getWrapperType(self.view) + '_wrapp_' + action)


