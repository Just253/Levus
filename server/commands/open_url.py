from command import Command

class BotCommand(Command):
    name = "open_url"
    description = "Opens a URL in the default browser"
    def execute(self, url):
        import os
        os.system(f"start {url}")