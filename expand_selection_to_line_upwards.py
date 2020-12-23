import sublime
import sublime_plugin

class ExpandSelectionToLineUpwardsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.set_timeout(lambda: self.view.run_command("expand_selection_to_line_upwards_atomic"), 0)

class ExpandSelectionToLineUpwardsAtomicCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for se in self.view.sel():
            beg = se.begin()
            end = se.end()
            linbeg = self.view.line(beg).begin()
            linend = self.view.line(end).end()
            if linbeg == beg and linend == end:
                linbeg = self.view.line(beg-1).begin()
            self.view.sel().add(sublime.Region(linend, linbeg))
