import sublime
import sublime_plugin

try:
    from .core.tools import *
    from .core.settings import *
    from .core.js_wrapper import *
    from .core.py_wrapper import *
    from .core.php_wrapper import *
except ValueError:
    from core.tools import *
    from core.settings import *
    from core.js_wrapper import *
    from core.py_wrapper import *
    from core.php_wrapper import *


def plugin_loaded():
    msg('*' * 30 + ' start ' + '*' * 30)


wrapConnector = {}

wrapConnector['js'] = JsWrapp()
wrapConnector['py'] = PyWrapp()
wrapConnector['php'] = PhpWrapp()


def getSupportedFileTypes():
    supportedFileTypes = settings().get('supportedFileTypesa') or {
        "embedding.php": "php",
        "text.html.vue": "js",
        "source.ts": "js",
        "source.tsx": "js",
        "source.coffee": "js",
        "source.js": "js",
        "text.html.basic": "js",
        "text.html.blade": "js",
        "text.html.twig": "js",
        "source.python": "py"
    }
    return supportedFileTypes


def supportedFile(view):
    supported = False
    supportedFileTypes = getSupportedFileTypes()

    cursors = view.sel()

    if not list(cursors):
        view.sel().add(0)

    for cursor in cursors:
        scope_name = view.scope_name(cursor.begin())
        fileTypeIntersect = list(set(scope_name.split(' ')).intersection(supportedFileTypes))

        if fileTypeIntersect:
            supported = True

    return supported


def runCommand(view, edit, action, insert_before=False):
    cursors = view.sel()

    supportedFileTypes = getSupportedFileTypes()
    lastPos = float("inf")

    if not list(cursors):
        view.sel().add(0)

    for cursor in cursors:
        scope_name = view.scope_name(cursor.begin())

        fileTypeIntersect = list(set(scope_name.split(' ')).intersection(supportedFileTypes))[::-1]

        if not fileTypeIntersect:
            fileType = scope_name.split(' ')[0]
            msg = 'Console Wrap: Not work in this file type ( {} )'.format(fileType)
            sublime.status_message(msg)
            continue

        wrapperType = supportedFileTypes.get(fileTypeIntersect[0], False)

        if view.match_selector(cursor.begin(), 'source.php'):
            wrapperType = 'php'

        if view.match_selector(cursor.begin(), 'source.js'):
            wrapperType = 'js'

        wrapper = wrapConnector.get(wrapperType, None)

        if wrapper:
            if action == 'create':
                end = getattr(wrapper, action)(view, edit, cursor, insert_before)
            else:
                end = getattr(wrapper, action)(view, edit, cursor)
        if end:
            lastPos = end if end < lastPos else lastPos

    return lastPos


class ConsoleWrapCommand(sublime_plugin.TextCommand):
    def run(self, edit, insert_before=False):
        view = self.view
        lastPos = runCommand(view, edit, 'create', insert_before)

        if lastPos > 0 and lastPos < float("inf"):
            view.sel().clear()
            view.sel().add(sublime.Region(lastPos, lastPos))
            self.view.run_command("move_to", {"to": "eol"})


class ConsoleActionCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return supportedFile(self.view)

    def run(self, edit, action=False):
        runCommand(self.view, edit, action)
