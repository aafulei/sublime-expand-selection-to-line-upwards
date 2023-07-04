"""
MIT License

Copyright (c) 2020 Aaron Fu Lei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sublime
import sublime_plugin


class ExpandSelectionToLineAtomicCommand(sublime_plugin.TextCommand):
    def run(self, edit, upwards):
        for region in self.view.sel():
            region_begin = region.begin()
            region_end = region.end()
            line_begin = self.view.line(region_begin).begin()
            line_end = self.view.line(region_end).end()
            # expand to one line above / below if this line has been covered
            covered = line_begin == region_begin and line_end == region_end
            if upwards:
                line_begin = self.view.line(region_begin - covered).begin()
                new_region = sublime.Region(line_end, line_begin)
            else:
                line_end = self.view.line(region_end + covered).end()
                new_region = sublime.Region(line_begin, line_end)
            self.view.sel().add(new_region)


class ExpandSelectionToLineUpwardsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def callback():
            cmd = "expand_selection_to_line_atomic"
            args = {"upwards": True}
            self.view.run_command(cmd, args)
        # enable soft undo line by line
        delay = 0
        sublime.set_timeout(callback, delay)


class ExpandSelectionToLineDownwardsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def callback():
            cmd = "expand_selection_to_line_atomic"
            args = {"upwards": False}
            self.view.run_command(cmd, args)
        # enable soft undo line by line
        delay = 0
        sublime.set_timeout(callback, delay)


class ShrinkSelectionByLineAtomicCommand(sublime_plugin.TextCommand):
    def run(self, edit, upwards):
        old_sel = list(self.view.sel())
        new_sel = []
        for region in old_sel:
            b = region.begin()
            e = region.end()
            begin_line = self.view.line(b)
            end_line = self.view.line(e)
            if begin_line == end_line:
                b = begin_line.begin()
                e = b
            elif upwards:
                e = end_line.begin() - 1
            else:
                b = begin_line.end() + 1
                b, e = e, b
            new_region = sublime.Region(b, e)
            new_sel.append(new_region)
        self.view.sel().clear()
        self.view.sel().add_all(new_sel)


class ShrinkSelectionByLineUpwardsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def callback():
            cmd = "shrink_selection_by_line_atomic"
            args = {"upwards": True}
            self.view.run_command(cmd, args)
        # enable soft undo line by line
        delay = 0
        sublime.set_timeout(callback, delay)


class ShrinkSelectionByLineDownwardsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def callback():
            cmd = "shrink_selection_by_line_atomic"
            args = {"upwards": False}
            self.view.run_command(cmd, args)
        # enable soft undo line by line
        delay = 0
        sublime.set_timeout(callback, delay)
