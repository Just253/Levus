from command import Command
import zipfile

class BotCommand(Command):
    name = "ZipFuntions"
    description = "This command executes zip operations"
    
    def compress_files(self, zipname, *filenames):
        with zipfile.ZipFile(zipname, 'w') as zipf:
            for filename in filenames:
                zipf.write(filename)

    def decompress_file(self, zipname, extract_dir='.'):
        with zipfile.ZipFile(zipname, 'r') as zipf:
            zipf.extractall(path=extract_dir)