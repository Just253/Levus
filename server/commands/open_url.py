from .command import Command
class BotCommand(Command):
    name = "open_url"
    description = "Abre una url en el navegador"
    def execute(self, url: str, new_tab: bool = False):
        """
        :param url: Url a abrir
        :type url: string
        :param new_tab: Abre en una nueva pestaña
        :type new_tab: boolean
        """
        import os
        os.system(f"start {url}")