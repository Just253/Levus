from .command import Command
from os import path, listdir, remove
import shutil
# from pyttsx3 import init 

class BotCommand(Command):
    name="Files commands"
    description="This command executes file operations"
    
    def __init__(self):
        self.operations = {
            'read': self.read_file,
            'create': self.create_file,
            'delete': self.delete_file,
            'copy': self.copy_file,
            'move': self.move_file,
            'list': self.list_files,
            'size': self.file_size
        }

    def execute(self, operation: str, *args: list):
        """
        :param operation: La operación a realizar {read, create, delete, copy, move, list, size}
        :type operation: string
        :param args: Los argumentos necesarios para la operación
        :type args: list {read: filename, create: filename, content, delete: filename, copy: source_filename, destination_filename, move: source_filename, destination_filename, list: directory, size: filename}
        """
        func = self.operations.get(operation)
        if func:
            func(*args)
        else:
            print(f"Unknown operation: {operation}")

    def read_file(self, filename):
        with open(filename, 'r') as file:
            print(file.read())
        
            #content = file.read()

        #engine = init()
        #engine.say(content)
        #engine.runAndWait()
        
    def create_file(self, filename, content=''):
        with open(filename, 'w') as file:
            file.write(content)

    def delete_file(self, filename):
        if path.isfile(filename):
            remove(filename)
        else:
            print(f"{filename} not found.")

    def copy_file(self, source_filename, destination_filename):
        shutil.copy(source_filename, destination_filename)

    def move_file(self, source_filename, destination_filename):
        shutil.move(source_filename, destination_filename)

    def list_files(self, directory):
        files = listdir(directory)
        for file in files:
            print(file)
        
        # message = f"Los archivos en el directorio {directory} son: {files}"
        
        # engine = init()
        # engine.say(message)
        # engine.runAndWait()

    def file_size(self, filename):
        size = path.getsize(filename) / (1024 * 1024)
        print(f"El tamaño del archivo, {filename} es de {size} megabytes")
        
        # message = f"El tamaño del archivo, {filename} es de {size} megabytes"
        
        # engine = init()
        # engine.say(message)
        # engine.runAndWait()