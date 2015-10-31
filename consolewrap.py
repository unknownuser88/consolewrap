import re
import sublime
import sublime_plugin
class ConsolewrapCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        cursor = view.sel()[0]
        line_region = view.line(cursor)
        string = view.substr(line_region)
        match = re.search(r"(\s*)", string)

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
                text = ConsolewrapCommand.get_wrapper(extension, match.group(1), var_text, var_text_escaped)
                view.insert(edit, line_region.end(), text)
                end = view.line(line_region.end() + 1).end()
                view.sel().clear()
                view.sel().add(sublime.Region(end, end))

    @staticmethod
    def get_wrapper(lang, spaces, var_text, var_text_escaped):
        if lang == 'rb':
            return "\n%sputs '-----------------------------[log][auto][%s]:';p %s" % (spaces, var_text_escaped, var_text)
        elif lang == 'erb':
            return "\n%s<%% puts '-----------------------------[log][auto][%s]:';p %s %%>" % (spaces, var_text_escaped, var_text)
        else:
            return "\n%sconsole.log('%s', %s);" % (spaces, var_text_escaped, var_text)


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
