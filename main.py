import cmd
import sys
import os
import zipfile
import configparser

class MyCLI(cmd.Cmd):
    config = configparser.ConfigParser()
    config.read("config.ini")
    print(config['bitbucket.org'])
    prompt = '>> '  # Change the prompt text
    intro = 'Welcome to CLI by Boyko Danimir'

    def __init__(self, zip_path):
        super().__init__()
        self.zip_path = zip_path
        self.current_directory = ''  # Start at the root of the zip
        try:
            self.zip_file = zipfile.ZipFile(self.zip_path, 'r')
        except FileNotFoundError:
            print(f"Error: File '{self.zip_path}' not found.")
            sys.exit(1)

    def do_ls(self, line):
        """List files and directories in the current directory."""
        path = self.current_directory or ''  # Root if empty
        contents = [name for name in self.zip_file.namelist() if name.startswith(path) and name != path]
        for item in contents:
            # Show only files and directories directly under the current directory
            item_name = item[len(path):].strip('/')
            if '/' not in item_name:
                print(item_name)

    def do_cd(self, directory):
        """Change the current directory."""
        new_dir = os.path.join(self.current_directory, directory).rstrip('/') + '/'
        if any(name.startswith(new_dir) for name in self.zip_file.namelist()):
            self.current_directory = new_dir
            print(f"Current directory changed to {self.current_directory}")
        else:
            print(f"Directory '{directory}' does not exist.")

    def do_cat(self, filename):
        """Read the contents of a file inside the zip."""
        file_path = os.path.join(self.current_directory, filename)
        try:
            with self.zip_file.open(file_path) as file:
                print(file.read().decode())
        except KeyError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_pwd(self, line):
        """Print the current directory in the virtual file system."""
        print(f"Current directory: {self.current_directory or '/'}")

    def do_quit(self, line):
        """Exit the CLI."""
        print("Exiting...")
        return True

    def postcmd(self, stop, line):
        print()
        return stop

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <virtual_fs.zip>")
        sys.exit(1)
    zip_path = sys.argv[1]
    MyCLI(zip_path).cmdloop()
