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


wrapConnector = {}

wrapConnector['js'] = JsWrapp()



def checkFileType(view):
    supportedFileTypes = {#settings().get('supportedFileTypesa') or {
        "source.php"     : "js",
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

        view = self.view
        cursors = view.sel() if insert_before else reversed(view.sel())

        for cursor in cursors:
            a = view.scope_name(cursor.begin())
            b = view.match_selector(cursor.begin(), 'source.js')
            print(" -- b", b)
            print('a', a)

        wrapperType = getWrapperType(self.view)
        print("wrapperType", wrapperType);

        wrapper = wrapConnector.get(wrapperType, None)
        print("wrapper", wrapper);

        if not wrapper:
            return sublime.status_message('Console Wrap: Not work in this file type')

        wrapper.create(view, edit, insert_before)
        print(" -- jsWrapp", jsWrapp)
        # self.view.run_command(wrapper + '_wrapp_create', {'insert_before': insert_before})


class ConsoleCleanCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        if not checkFileType(self.view):
            return False
        return True

    def run(self, edit, action=False):
        self.view.run_command(getWrapperType(self.view) + '_wrapp_' + action)


