import re
import sublime
import sublime_plugin

try:
    from .settings import *
except ValueError:
    from settings import *

def plugin_loaded():
    global settings
    settings = sublime.load_settings('consolewrap.sublime-settings')

def getConsoleFunc():
    return settings.get('consoleFunc') or ['console','log']

def getConsoleLogTypes():
    return settings.get('log_types') or ['log', 'info', 'warn', 'error']

def getConsoleStr():
    return settings.get('consoleStr') or "{title}, {variable}"

def getConsoleSingleQuotes():
    return settings.get('single_quotes') or False

def msg(msg):
    print ("[Console Wrap] %s" % msg)


def get_indent(view, region, insert_before):
    matches = re.findall(r'^(\s*)[^\s]', view.substr(region))
    indent_str = matches and len(matches) and matches[0] or ''
    if insert_before:
        return indent_str
    indent_line = view.substr(find_next_line(view, region)).strip()
    need_indent = [True for i in ['{', '=', ':', '->', '=>'] if indent_line.endswith(i)]
    indent_line.lstrip('{}[]() \t')
    if need_indent:
        indent_str += len(indent_str) and indent_str[0] == '\t' and '\t' or '    '
    return indent_str

def checkQuotes(cmd):
    matches = re.search(r"console\.(\w+)\((\\\"|\\\'|\'|\")", cmd)
    if not matches:
        return "'";
    return matches.group(2);

def find_next_line(view, region):
    while 0 < region.a and region.b < view.size() and view.classify(region.a) is sublime.CLASS_EMPTY_LINE:
        region = view.line(region.a - 1)
    return region

def get_wrapper(view, var, indent_str, insert_before):
    consoleStr = getConsoleStr()
    single_quotes = getConsoleSingleQuotes()
    consoleFunc = getConsoleFunc()
    separator = ", "

    if single_quotes:
        text = var.replace("'", "\\'")
    else:
        text = var.replace('"', '\\"')

    consoleArr = consoleStr.split(separator)

    t = consoleArr[0]

    if len(consoleArr) >= 2:
        v = ', '.join(consoleArr[1:])
    else:
        v = t

    tmpl = indent_str if insert_before else ("\n" + indent_str)

    quotes = "'" if single_quotes else "\""
    a = "{4}({0}{1}{0}{2}{3});".format(quotes, t, separator, v , ".".join(consoleFunc))
    a = a.format(title=text, variable=var)

    tmpl += a

    tmpl += "\n" if insert_before else ""

    return tmpl

def is_log_string(line):
    log_types =  getConsoleLogTypes()
    logFunc = getConsoleFunc()[0]
    return True in [line.strip().startswith(logFunc+'.' + i) for i in log_types]

def change_log_type(view, edit, line_region, line):
    log_types =  getConsoleLogTypes()
    logFunc = getConsoleFunc()[0]
    current_type = None
    matches = re.match(r'^\s*'+logFunc+'\.(\w+)', line)
    if not matches: return
    current_type = matches.group(1)
    if current_type not in log_types: return
    inc = True and 1 or -1
    next_type = log_types[(log_types.index(current_type) + 1) % len(log_types)]
    new_line = line.replace(logFunc + '.' + current_type, logFunc + '.' + next_type)
    view.replace(edit, line_region, new_line)

def get_selections(s):
    selections = s.view.sel()
    has_selections = False
    for sel in selections:
        if sel.empty() == False:
            has_selections = True
    if not has_selections:
        full_region = sublime.Region(0, s.view.size())
        selections.add(full_region)
    return selections

def checkFileType(view):
    supportedFileTypes = settings.get('supportedFileTypes') or [
        'text.html.vue',
        'source.ts',
        'source.tsx',
        'source.coffee',
        'source.js',
        'text.html.basic',
        'text.html.blade',
        'text.html.twig'
    ]
    return set(view.scope_name(0).split(' ')).intersection(supportedFileTypes)

def comment_log(self, edit):
    logFunc = getConsoleFunc()[0]
    get_selections(self)
    cursor = self.view.sel()[0]
    line_region = self.view.line(cursor)
    string = self.view.substr(line_region)
    matches = re.finditer(r"(?<!\/\/\s)"+logFunc+"\..*?\);?", string, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        string = string.replace(match.group(0), "// "+match.group(0))

    self.view.replace(edit, line_region, string)
    self.view.sel().clear()

def remove_log(self, edit):
    logFunc = getConsoleFunc()[0]
    get_selections(self)
    cursor = self.view.sel()[0]
    line_region = self.view.line(cursor)
    string = self.view.substr(line_region)
    newstring = re.sub(r"(\/\/\s)?"+logFunc+"\..*?\);?", '', string)
    self.view.replace(edit, line_region, newstring)
    self.view.sel().clear()

class ConsoleWrapCommand(sublime_plugin.TextCommand):

    def run(self, edit, insert_before=False):

        if not checkFileType(self.view):
            return sublime.status_message('Console Wrap: Not work in this file type')

        view = self.view
        cursors = view.sel() if insert_before else reversed(view.sel())

        for cursor in cursors:
            line_region = view.line(cursor)
            string = view.substr(line_region)
            match = re.search(r"(\s*)", string)

            if is_log_string(string):
                return change_log_type(view, edit, line_region, string)

            if match:
                # check if cursor is on the word and trying to get that word 
                if cursor.begin() == cursor.end():
                    word = view.word(cursor)
                else:
                    word = cursor

                var_text = view.substr(word).strip()

                # if selection is empty and there is no word under cursor use clipboard
                if not var_text:
                    var_text = sublime.get_clipboard()

                if var_text[-1:] == ";":
                    var_text = var_text[:-1]

                if len(var_text) == 0:
                    return sublime.status_message('Console Wrap: Please make a selection or copy something.')
                else:
                    indent_str = get_indent(view, line_region,insert_before)
                    text = get_wrapper(view, var_text, indent_str, insert_before)
                    # msg('text', text)
                    if insert_before:
                        lineReg = line_region.begin()
                    else:
                        lineReg = line_region.end()
                    view.insert(edit, lineReg, text)
                    end = view.line(lineReg + 1).end()

        if not is_log_string(string):
            view.sel().clear()
            view.sel().add(sublime.Region(end, end)) 

class ConsoleCleanCommand(sublime_plugin.TextCommand):

    def is_enabled(self):
        if not checkFileType(self.view):
            return False
        return True

    def run(self, edit, action=False):
        globals()[action + "_log"](self, edit)

