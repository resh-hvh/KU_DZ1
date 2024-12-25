import os
import sys
import zipfile
import tempfile
import shutil

current_path = ""
base_path = ""
history = []

def ls():
    """List directory contents."""
    try:
        contents = os.listdir(current_path)
        return "\n".join(contents) if contents else "(empty)"
    except FileNotFoundError:
        return f"Error: Directory '{current_path}' not found."

def cd(directory):
    """Change directory."""
    global current_path
    if not directory:
        return "Error: Directory not specified."
    
    new_path = os.path.abspath(os.path.join(current_path, directory))
    
    if os.path.isdir(new_path) and new_path.startswith(base_path):
        current_path = os.path.normpath(new_path)
        return ""
    return f"Error: Directory '{directory}' does not exist."

def uname():
    """Print system information."""
    return "EmulatorShell v1.0"

def history_cmd():
    """Show command history."""
    return "\n".join(history)

def tac(file):
    """Print file contents in reverse order."""
    file_path = os.path.join(current_path, file)
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return "".join(reversed(lines))
    except FileNotFoundError:
        return f"Error: File '{file}' not found."

def exit_cmd():
    """Exit the emulator."""
    print("Exiting emulator...")
    sys.exit(0)

def execute_command(command):
    """Parse and execute a command."""
    history.append(command)
    parts = command.strip().split()
    if not parts:
        return ""

    cmd, *args = parts
    if cmd == "ls":
        return ls()
    elif cmd == "cd":
        return cd(args[0] if args else "")
    elif cmd == "uname":
        return uname()
    elif cmd == "history":
        return history_cmd()
    elif cmd == "tac":
        return tac(args[0] if args else "")
    elif cmd == "exit":
        exit_cmd()
    else:
        return f"Error: Command '{cmd}' not recognized."

def setup_virtual_fs(zip_path):
    """Extract virtual filesystem from ZIP archive."""
    if not zipfile.is_zipfile(zip_path):
        print(f"Error: {zip_path} is not a valid ZIP file.")
        sys.exit(1)

    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(temp_dir)

    return os.path.abspath(temp_dir)


def main():
    if len(sys.argv) < 3:
        print("Usage: emulator.py <path_to_zip> <path_to_script>")
        sys.exit(1)

    zip_path = sys.argv[1]
    script_path = sys.argv[2]

    global current_path, base_path
    base_path = setup_virtual_fs(zip_path)
    current_path = base_path

    if os.path.isfile(script_path):
        with open(script_path, 'r') as script:
            for line in script:
                output = execute_command(line.strip())
                if output:
                    print(output)

    try:
        while True:
            command = input(f"{current_path} $ ")
            output = execute_command(command)
            if output:
                print(output)
    except KeyboardInterrupt:
        print("\nExiting emulator...")
    finally:
        shutil.rmtree(base_path)

if __name__ == "__main__":
    main()
