from .command import Command
import zipfile

class BotCommand(Command):
    name = "ZipFunctions"
    description = "This command executes zip operations"
    
    def execute(self, operation: str, zipname: str, *args: list):
        """
        :param operation: La operación a realizar {Comprimir, Descomprimir}
        :type operation: string
        :param zipname: El nombre del archivo zip + su extensión de formato
        :type zipname: string
        :param args: Los argumentos necesarios para la operación {Comprimir: lista de archivos, Descomprimir: directorio de extracción}
        :type args: list
        """
        if operation == 'compress':
            self.compress_files(zipname, *args)
        elif operation == 'decompress':
            self.decompress_file(zipname, *args[0] if args else '.')
        else:
            print(f"Unknown operation: {operation}")

    def compress_files(self, zipname, *filenames):
        with zipfile.ZipFile(zipname, 'w') as zipf:
            for filename in filenames:
                zipf.write(filename)

    def decompress_file(self, zipname, extract_dir='.'):
        with zipfile.ZipFile(zipname, 'r') as zipf:
            zipf.extractall(path=extract_dir)