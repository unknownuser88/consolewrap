import sublime


class settings(object):
    loaded_settings = sublime.load_settings('consolewrap.sublime-settings')

    get = loaded_settings.get
    set = loaded_settings.set

