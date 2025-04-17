import sys
import os

def process_args(args):
    source_arg = args[1] if len(args) > 1 else ""
    destination_arg = args[2] if len(args) > 2 else ""
    return source_arg, destination_arg

def get_file_paths(source_arg, destination_arg):
    current_dir = os.getcwd()
    if source_arg:
        if os.path.exists(source_arg):
            source_path = os.path.abspath(source_arg)
        else:
            raise ValueError(f"Error: Source path '{source_arg}' not found, or inaccessible.")
    else:
        source_path = current_dir

    if destination_arg:
        if os.path.exists(destination_arg):
                destination_path = os.path.abspath(destination_arg)
        else:
            raise ValueError(f"Error: Destination path '{destination_arg}' not found, or inaccessible.")
    else:
        destination_path = current_dir

    
    return source_path, destination_path

def get_file_names(source_path):
    supported_extensions = [".pdf", ".docx", ".txt"]

    try:
        file_names = [
            file for file in os.listdir(source_path)
            if os.path.isfile(os.path.join(source_path, file))
            and os.path.splitext(file)[1].lower() in supported_extensions
        ]
        return file_names
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Directory '{source_path}' not found.")
    except NotADirectoryError:
        raise NotADirectoryError(f"Error: '{source_path}' is not a directory.")

def main(args):
    try:
        # Accept file path
        # The source will always be the first argument, and the destination will be the second
        source_arg, destination_arg = process_args(args)
        source_path, destination_path = get_file_paths(source_arg, destination_arg)

        print(source_path)
        print(destination_path)

        # Read files
        files = get_file_names(source_path)

        print(files)

    except ValueError as e:
        print(e)
    


if __name__ == "__main__":
    # Read files

    # Parse Client Name and Date

    # Create Client folder

    # Save new file with Client Name and Date

    main(sys.argv)