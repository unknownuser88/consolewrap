import re
import sublime
import sublime_plugin

LOG_TYPES = ['log', 'info', 'warn', 'error']

def get_indent(view, region):
    matches = re.findall(r'^(\s*)[^\s]', view.substr(region))
    indent_str = matches and len(matches) and matches[0] or ''
    indent_line = view.substr(find_next_line(view, region)).strip()
    need_indent = [True for i in ['{', '=', ':', '->', '=>'] if indent_line.endswith(i)]
    indent_line.lstrip('{}[]() \t')
    if need_indent:
        indent_str += len(indent_str) and indent_str[0] == '\t' and '\t' or '    '
    return indent_str

def find_next_line(view, region):
    while 0 < region.a and region.b < view.size() and view.classify(region.a) is sublime.CLASS_EMPTY_LINE:
        region = view.line(region.a - 1)
    return region

def get_wrapper(view, var_text, indent_str):
    text_escaped = var_text.replace("'", "\\'")
    tmpl = "\n" + indent_str
    
    if 'source.coffee' in view.scope_name(0):
        tmpl += "console.log '%s', %s" % (text_escaped, var_text)
    else:
        tmpl += "console.log('%s', %s);" % (text_escaped, var_text)

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

class ConsolewrapCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        cursors = view.sel()

        for cursor in cursors:
            line_region = view.line(cursor)
            string = view.substr(line_region)
            match = re.search(r"(\s*)", string)

            if is_log_string(string):
                change_log_type(view, edit, line_region, string)
            else: 
                if match:
                    if cursor.empty():
                        var_text = sublime.get_clipboard()
                    else:
                        var_text = view.substr(cursor)
                    if var_text[-1:] == ";":
                        var_text = var_text[:-1]

                    if len(var_text) == 0:
                        sublime.status_message('Please make a selection or copy something.')
                    else:
                        indent_str = get_indent(view, line_region)
                        text = get_wrapper(view, var_text, indent_str)
                        view.insert(edit, line_region.end(), text)
                        end = view.line(line_region.end() + 1).end()

        if not is_log_statement(string):
            view.sel().clear()
            view.sel().add(sublime.Region(end, end))


class ConsoleremoveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.get_selections()
        cursor = self.view.sel()[0]
        line_region = self.view.line(cursor)
        string = self.view.substr(line_region)
        newstring = re.sub(r"(?m)^((?!//|/\*).)*console\.log.*", '', string)
        self.view.replace(edit, line_region, newstring)
        self.view.sel().clear()

    def get_selections(self):
        selections = self.view.sel()
        has_selections = False
        for sel in selections:
            if sel.empty() == False:
                has_selections = True
        if not has_selections:
            full_region = sublime.Region(0, self.view.size())
            selections.add(full_region)
        return selections
