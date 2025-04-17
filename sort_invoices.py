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
            raise ValueError(f"Source path '{source_arg}' not found, or inaccessible.")
    else:
        source_path = current_dir

    if destination_arg:
        if os.path.exists(destination_arg):
                destination_path = os.path.abspath(destination_arg)
        else:
            raise ValueError(f"Destination path '{destination_arg}' not found, or inaccessible.")
    else:
        destination_path = current_dir

    
    return source_path, destination_path

def main(args):
    try:
        # The source will always be the first argument, and the destination will be the second
        source_arg, destination_arg = process_args(args)
        source_path, destination_path = get_file_paths(source_arg, destination_arg)

        print(source_path)
        print(destination_path)
    except ValueError as e:
        print(e)
    


if __name__ == "__main__":
    # Accept file path

    # Read files

    # Parse Client Name and Date

    # Create Client folder

    # Save new file with Client Name and Date

    main(sys.argv)