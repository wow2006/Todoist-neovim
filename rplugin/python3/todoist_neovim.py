import os
import json
import neovim
import tempfile


@neovim.plugin
class Todoist(object):
    def __init__(self, vim):
        self.vim = vim
        if(os.path.exists("TODO.json")):
            with open("TODO.json", "r") as f:
                self.preview_tasks = json.loads(f.read())
        else:
            self.preview_tasks = []
        self.file_name = self.create_temp_file()

    def __del__(self):
        os.remove(self.file_name)
        with open('TODO.json', 'w', encoding='utf-8') as f:
            json.dump(self.preview_tasks, f, ensure_ascii=False, indent=4)

    def update(self):
        with open(self.file_name, "w") as f:
            # TODO(Hussein): split tasks to projects
            f.write("Project:\n")
            width = self.vim.current.window.width
            f.write("=" * width + "\n")
            for task in self.preview_tasks:
                f.write("\t[ ] " + task + "\n")
                f.write("-" * width + "\n")
        self.vim.command("view " + self.file_name)

    @neovim.command('TodoistAddTest', range='', nargs='*')
    def add_test(self, args, nargs='*'):
        if args:
            task_name = " ".join(args)
            self.preview_tasks.append(task_name)
            self.update()

    @neovim.command('TodoistShow', range='', nargs='*')
    def show_window(self, args, nargs='*'):
        self.vim.command("vsplit")
        self.update()

    def create_temp_file(self):
        fp = tempfile.NamedTemporaryFile(mode="w", suffix="TODO", delete=False)
        file_name = fp.name
        fp.close()
        return file_name
