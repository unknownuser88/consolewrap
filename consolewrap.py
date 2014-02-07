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
        if match:
            if cursor.empty():
                sublime.status_message('Please Make A Selection');
            else:
                var_text = view.substr(cursor)
                view.insert(edit, line_region.end(), "\n%sconsole.log('%s ' , %s);" % (match.group(1), var_text, var_text))
                end = view.line(line_region.end() + 1).end()
                view.sel().clear()
                view.sel().add(sublime.Region(end, end))