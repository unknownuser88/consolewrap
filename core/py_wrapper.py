import re
import sublime
import sublime_plugin

try:
    from .settings import settings
    from .tools import *
except ValueError:
    from settings import settings
    from tools import *

class PySettings():

    def getConsoleFunc(self):
        return settings().get('py').get('consoleFunc', ['print'])

    def getConsoleLogTypes(self):
        return settings().get('py').get('log_types', ["debug", "info", "warn", "error", "critical"])

    def getConsoleStr(self):
        return settings().get('py').get('consoleStr', "{title}, {variable}")

    def getConsoleSingleQuotes(self):
        return settings().get('py').get('single_quotes', False)


class PyWrapp(PySettings):

    def create(self, view, edit, cursor, insert_before):

        line_region = view.line(cursor)
        string = view.substr(line_region)
        match = re.search(r"(\s*)", string)
        end = 0

        if self.is_log_string(string):
            self.change_log_type(view, edit, line_region, string)
            return end

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
                indent_str = self.get_indent(view, line_region,insert_before)
                text = self.get_wrapper(view, var_text, indent_str, insert_before)
                # msg('text', text)
                if insert_before:
                    lineReg = line_region.begin()
                else:
                    lineReg = line_region.end()
                view.insert(edit, lineReg, text)
                end = view.line(lineReg + 1).end()
            view.sel().subtract(sublime.Region(cursor.begin(), cursor.end()))

        return end

    def is_log_string(self, line):
        log_types =  self.getConsoleLogTypes()
        logFunc = self.getConsoleFunc()[0]
        return True in [line.strip().startswith(logFunc) for i in log_types]

    def change_log_type(self, view, edit, line_region, line):
        log_types =  self.getConsoleLogTypes()
        logFunc = self.getConsoleFunc()[0]
        current_type = None
        matches = re.findall(r'('+logFunc+')(\.?)(\w+)?', line)
        if not matches: return
        func, dot, method = matches[0]

        if dot:
            if method not in log_types: return
            inc = True and 1 or -1
            next_type = log_types[(log_types.index(method) + 1) % len(log_types)]
            new_line = line.replace(logFunc + '.' + method, logFunc + '.' + next_type)
            view.replace(edit, line_region, new_line)

    def get_indent(self, view, region, insert_before):
        matches = re.findall(r'^(\s*)[^\s]', view.substr(region))
        indent_str = matches and len(matches) and matches[0] or ''
        if insert_before:
            return indent_str
        indent_line = view.substr(self.find_next_line(view, region)).strip()
        need_indent = [True for i in ['{', '=', ':', '->', '=>'] if indent_line.endswith(i)]
        indent_line.lstrip('{}[]() \t')
        if need_indent:
            indent_str += len(indent_str) and indent_str[0] == '\t' and '\t' or '    '
        return indent_str

    def find_next_line(self, view, region):
        while 0 < region.a and region.b < view.size() and view.classify(region.a) is sublime.CLASS_EMPTY_LINE:
            region = view.line(region.a - 1)
        return region

    def get_wrapper(self, view, var, indent_str, insert_before):
        consoleStr = self.getConsoleStr()
        single_quotes = self.getConsoleSingleQuotes()
        consoleFunc = self.getConsoleFunc()
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
        a = "{4}({0}{1}{0}{2}{3})".format(quotes, t, separator, v , ".".join(consoleFunc))
        a = a.format(title=text, variable=var)

        tmpl += a

        tmpl += "\n" if insert_before else ""

        return tmpl

    def comment(self, view, edit, cursor):
        logFunc = self.getConsoleFunc()[0]
        get_selections(view, sublime)
        cursor = view.sel()[0]
        line_region = view.line(cursor)
        string = view.substr(line_region)
        matches = re.finditer(r"(?<!#\s)"+logFunc+".*?\);?", string, re.MULTILINE)

        for matchNum, match in enumerate(matches):
            string = string.replace(match.group(0), "# "+match.group(0))

        view.replace(edit, line_region, string)
        view.sel().clear()

    def remove(self, view, edit, cursor):
        logFunc = self.getConsoleFunc()[0]
        get_selections(view, sublime)
        cursor = view.sel()[0]
        line_region = view.line(cursor)
        string = view.substr(line_region)
        newstring = re.sub(r"(#\s)?"+logFunc+".*?(\n);?", '\n', string)
        view.replace(edit, line_region, newstring)
        view.sel().clear()

    def quick_nav_done(self, view, index, regions, showOnly=False):
        region = sublime.Region(regions[index].b)
        if not showOnly: 
            view.sel().add(region)
        view.show_at_center(region)

    def show_quick_nav(self, view, edit, cursor):
        tags = []
        regions = []

        logFunc = self.getConsoleFunc()[0]
        get_selections(view, sublime)
        counter = 1
        regex = re.compile(r"(\/\/\s)?("+logFunc+")(\.?)(\w+)?\((.+)?\);?", re.UNICODE|re.DOTALL)
        for comment_region in view.sel():
            for splited_region in view.split_by_newlines(comment_region):
                m = regex.search(view.substr(splited_region))
                if m:
                    # Add a counter for faster selection
                    tag = m.group(0)
                    tags.append(str(counter) + '. ' + tag)
                    regions.append(splited_region)
                    counter += 1

        if (len(tags)):
            view.window().show_quick_panel(tags, lambda index : self.quick_nav_done(view, index, regions), 0, 0, lambda index : self.quick_nav_done(view, index, regions, True))
        else:
            sublime.status_message("Console Wrap: No 'logs' found")

        view.sel().clear()

    def remove_commented(self, view, edit, cursor):
        print('remove_commented')
