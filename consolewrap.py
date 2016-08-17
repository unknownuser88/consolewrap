import re
import sublime
import sublime_plugin
class ConsolewrapCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        cursors = view.sel()
        
        def get_indent(region):
            matches = re.findall(r'^(\s*)[^\s]', view.substr(region))
            return matches and len(matches) and matches[0] or ''

        def find_next_line(region):
            while 0 < region.a and region.b < view.size() and view.classify(region.a) is sublime.CLASS_EMPTY_LINE:
                region = view.line(region.a - 1)
            return region

        for cursor in cursors:
            line_region = view.line(cursor)
            string = view.substr(line_region)
            match = re.search(r"(\s*)", string)

            indent_str = get_indent(line_region)

            indent_line = view.substr(find_next_line(line_region)).strip()
            need_indent = [True for i in ['{', '=', ':', '->', '=>'] if indent_line.endswith(i)]
            indent_line.lstrip('{}[]() \t')
            if need_indent:
                indent_str += len(indent_str) and indent_str[0] == '\t' and '\t' or '  '

            file_name = view.file_name()
            if file_name is None:
                extension = None
            else:
                extension = file_name[file_name.rfind('.') + 1:]

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
                    var_text_escaped = var_text.replace("'", "\\'")
                    text = ConsolewrapCommand.get_wrapper(self, extension,var_text, var_text_escaped, indent_str)
                    view.insert(edit, line_region.end(), text)
                    end = view.line(line_region.end() + 1).end()

        view.sel().clear()
        view.sel().add(sublime.Region(end, end))


    @staticmethod
    def get_wrapper(self, lang, var_text, var_text_escaped, indent_str):
        tmpl = "\n" + indent_str
        if lang == 'rb':
            tmpl += "puts '-----------------------------[log][auto][%s]:';p %s" % (var_text_escaped, var_text)
        elif lang == 'erb':
            tmpl += "<%% puts '-----------------------------[log][auto][%s]:';p %s %%>" % (var_text_escaped, var_text)
        else:
            if 'source.coffee' in self.view.scope_name(0):
                tmpl += "console.log '%s', %s" % (var_text_escaped, var_text)
            else:
                tmpl += "console.log('%s', %s);" % (var_text_escaped, var_text)
            return tmpl


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
