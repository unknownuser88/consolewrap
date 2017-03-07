import re
import sublime
import sublime_plugin
import sys

PY3 = sys.version > '3'
if PY3:
    from .settings import *
else:
    from settings import *

LOG_TYPES = ['log', 'info', 'warn', 'error']

def plugin_loaded():
    settings.loaded_settings = sublime.load_settings('consolewrap.sublime-settings')
    settings.get = settings.loaded_settings.get
    settings.set = settings.loaded_settings.set

def get_indent(view, region):
    matches = re.findall(r'^(\s*)[^\s]', view.substr(region))
    indent_str = matches and len(matches) and matches[0] or ''
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

def get_wrapper(view, variable, indent_str, insert_before):
    cmd = settings.get('consoleStr') or "\"console.log('%s', %s);\" % (text, variable)"
    if checkQuotes(cmd) == '"':
        text = variable.replace('"', '\\"')
    else:
        text = variable.replace("'", "\\'")
    tmpl = indent_str if insert_before else ("\n" + indent_str)
    
    tmpl += eval(cmd)

    tmpl += "\n" if insert_before else ""
    return tmpl

def is_log_string(line):
    return True in [line.strip().startswith('console.' + i) for i in LOG_TYPES]

def change_log_type(view, edit, line_region, line):
    current_type = None
    matches = re.match(r'^\s*console\.(\w+)', line)
    if not matches: return
    current_type = matches.group(1)
    if current_type not in LOG_TYPES: return
    inc = True and 1 or -1
    next_type = LOG_TYPES[(LOG_TYPES.index(current_type) + 1) % len(LOG_TYPES)]
    new_line = line.replace('console.' + current_type, 'console.' + next_type)
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

class ConsolewrapCommand(sublime_plugin.TextCommand):

    def checkFileType(self, view):
        return set(self.view.scope_name(0).split(' ')).intersection(['text.html.vue', 'source.ts', 'source.tsx' ,'source.coffee', 'source.js', 'text.html.basic', 'text.html.blade', 'text.html.twig'])

    def run(self, edit, insert_before=False):

        if not self.checkFileType(self.view):
            return sublime.status_message('Console Wrap: Not work in this file type')

        view = self.view
        cursors = view.sel()

        for cursor in cursors:
            line_region = view.line(cursor)
            string = view.substr(line_region)
            match = re.search(r"(\s*)", string)

            if is_log_string(string):
                return change_log_type(view, edit, line_region, string)

            if match:
                if cursor.empty():
                    var_text = sublime.get_clipboard()
                else:
                    var_text = view.substr(cursor)

                if var_text[-1:] == ";":
                    var_text = var_text[:-1]

                if len(var_text) == 0:
                    return sublime.status_message('Console Wrap: Please make a selection or copy something.')
                else:
                    indent_str = get_indent(view, line_region)
                    text = get_wrapper(view, var_text, indent_str, insert_before)
                    if insert_before:
                        lineReg = line_region.begin()
                    else:
                        lineReg = line_region.end()
                    view.insert(edit, lineReg, text)
                    end = view.line(lineReg + 1).end()

        if not is_log_string(string):
            view.sel().clear()
            view.sel().add(sublime.Region(end, end)) 

class ConsolecommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        get_selections(self)
        cursor = self.view.sel()[0]
        line_region = self.view.line(cursor)
        string = self.view.substr(line_region)
        matches = re.finditer(r"(?<!\/\/\s)console\..*?\);?", string, re.MULTILINE)

        for matchNum, match in enumerate(matches):
            # matchNum = matchNum + 1
            # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group(0)))
            string = string.replace(match.group(0), "// "+match.group(0))

        self.view.replace(edit, line_region, string)
        self.view.sel().clear() 


class ConsoleremoveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        get_selections(self)
        cursor = self.view.sel()[0]
        line_region = self.view.line(cursor)
        string = self.view.substr(line_region)
        newstring = re.sub(r"(\/\/\s)?console\..*?\);?", '', string)
        self.view.replace(edit, line_region, newstring)
        self.view.sel().clear()

   