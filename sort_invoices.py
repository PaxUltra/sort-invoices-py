import sys
import os
import mimetypes

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
            os.path.join(source_path, file) for file in os.listdir(source_path)
            if os.path.isfile(os.path.join(source_path, file))
            and os.path.splitext(file)[1].lower() in supported_extensions
        ]
        return file_names
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Directory '{source_path}' not found.")
    except NotADirectoryError:
        raise NotADirectoryError(f"Error: '{source_path}' is not a directory.")

def extract_from_txt(file_path):
    client = None
    date = None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            for line in content.splitlines():
                line = line.strip()

                if line.lower().startswith("client:"):
                    client = line.split(":", 1)[1].strip()
                elif line.lower().startswith("date:"):
                    date = line.split(":", 1)[1].strip()

                # Breakout early if we find what we are looking for
                if client and date:
                    break

            return client, date
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")
    except PermissionError:
        raise PermissionError(f"Error: Permission denied for '{file_path}'.")
    except IsADirectoryError:
        raise IsADirectoryError(f"Error: Expected a file, but found a directory - '{file_path}'")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Error: Cannot decode file '{file_path}'.")
    except (IOError, OSError) as e:
        raise RuntimeError(f"Error: An I/O error occurred while reading '{file_path}' - {e}")

def get_client_and_date(files):
    data = []

    for file in files:
        mime_type, _ = mimetypes.guess_type(file)
        if mime_type == "text/plain":
            client, date = extract_from_txt(file)
            data.append({
                "path": file,
                "client": client,
                "date": date
            })

    return data

def main(args):
    try:
        # Accept file path
        # The source will always be the first argument, and the destination will be the second
        source_arg, destination_arg = process_args(args)
        source_path, destination_path = get_file_paths(source_arg, destination_arg)

        # Read files
        files = get_file_names(source_path)

        # Parse Client Name and Date
        invoice_data = get_client_and_date(files)

        print(invoice_data)

    except ValueError as e:
        print(e)
    


if __name__ == "__main__":
    # Create Client folder

    # Save new file with Client Name and Date

    main(sys.argv)