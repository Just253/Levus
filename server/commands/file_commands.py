from command import Command
import os
import shutil

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

    def execute(self, operation, *args):
        func = self.operations.get(operation)
        if func:
            func(*args)
        else:
            print(f"Unknown operation: {operation}")

    def read_file(self, filename):
        with open(filename, 'r') as file:
            print(file.read())

    def create_file(self, filename, content=''):
        with open(filename, 'w') as file:
            file.write(content)

    def delete_file(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)
        else:
            print(f"{filename} not found.")

    def copy_file(self, source_filename, destination_filename):
        shutil.copy(source_filename, destination_filename)

    def move_file(self, source_filename, destination_filename):
        shutil.move(source_filename, destination_filename)

    def list_files(self, directory):
        files = os.listdir(directory)
        for file in files:
            print(file)

    def file_size(self, filename):
        size = os.path.getsize(filename)
        print(f"The size of {filename} is {size} bytes.")