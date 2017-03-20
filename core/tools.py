def msg(*msg):
    print ("[Console Wrap] " , msg)

def get_selections(s, sublime):
    selections = s.view.sel()
    has_selections = False
    for sel in selections:
        if sel.empty() == False:
            has_selections = True
    if not has_selections:
        full_region = sublime.Region(0, s.view.size())
        selections.add(full_region)
    return selections