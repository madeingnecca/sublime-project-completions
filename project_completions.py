import sublime
import sublime_plugin
import glob
import json


class ProjectCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        l = []
        folders = view.window().folders()

        for folder in folders:
            files = glob.glob(folder + "/*.sublime-completions")
            for filename in files:
                l.extend(self.load_completion_file(view, prefix, locations, filename))

        return l

    def load_completion_file(self, view, prefix, locations, filename):
        result = []

        f = open(filename)
        try:
            content = f.read() or '{}'
            data = json.loads(content)
        except:
            return []
        finally:
            f.close()

        if "scope" in data:
            pt = view.sel()[0].b
            score = view.score_selector(pt, data["scope"])
            if score == 0:
                return []

        if "completions" in data:
            for compl in data["completions"]:
                if type(compl) is dict:
                    result.append((compl["trigger"], compl["contents"]))
                else:
                    result.append((compl, compl))

        return result
