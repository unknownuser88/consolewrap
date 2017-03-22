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
wrapConnector['py'] = PyWrapp()
print(" -- wrapConnector", wrapConnector)

def getSupportedFileTypes():
    supportedFileTypes = {#settings().get('supportedFileTypesa') or {
        "embedding.php"  : "py",
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
    return supportedFileTypes


class ConsoleWrapCommand(sublime_plugin.TextCommand):
    def run(self, edit, insert_before=False):

        view = self.view
        cursors = view.sel() if insert_before else reversed(view.sel())

        supportedFileTypes = getSupportedFileTypes()
        lastPos = float("inf")

        for cursor in cursors:
            scope_name = view.scope_name(cursor.begin())
            fileTypeIntersect = list(set(scope_name.split(' ')).intersection(supportedFileTypes))

            if not fileTypeIntersect:
                sublime.status_message('Console Wrap: Not work in this file type ( {} )'.format(scope_name.split(' ')[0]))
                continue


            wrapperType = supportedFileTypes.get(fileTypeIntersect[0], False)

            if view.match_selector(cursor.begin(), 'source.js'):
                wrapperType = 'js'
            
            wrapper = wrapConnector.get(wrapperType, None)

            if wrapper:
                end = wrapper.create(view, edit, cursor,insert_before)
                lastPos = end if end < lastPos else lastPos

        if lastPos > 0 and lastPos < float("inf"):
            view.sel().clear()
            view.sel().add(sublime.Region(lastPos, lastPos))
            self.view.run_command("move_to", {"to": "eol"})

class ConsoleCleanCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        if not checkFileType(self.view):
            return False
        return True

    def run(self, edit, action=False):
        view = self.view
        cursors = view.sel()
        supportedFileTypes = getSupportedFileTypes()

        for cursor in cursors:
            scope_name = view.scope_name(cursor.begin())
            fileTypeIntersect = list(set(scope_name.split(' ')).intersection(supportedFileTypes))
            print(" -- fileTypeIntersect", fileTypeIntersect)

            if not fileTypeIntersect:
                continue

            wrapperType = supportedFileTypes.get(fileTypeIntersect[0], False)

            if view.match_selector(cursor.begin(), 'source.js'):
                wrapperType = 'js'

            wrapper = wrapConnector.get(wrapperType, None)

            if wrapper:
                getattr(wrapper, action)(self.view, edit)


