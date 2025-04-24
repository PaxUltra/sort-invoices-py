import sys
import os
import shutil
import fitz
import logging
import argparse
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from dateutil import parser
from datetime import datetime

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = logging.FileHandler("sort_invoices.log")
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger

def normalize_date(raw_date):
    try:
        parsed = parser.parse(raw_date)
        return parsed.strftime("%Y-%m-%d") # YYYY-MM-DD
    except (ValueError, TypeError):
        return "Unknown"

def process_args():
    arg_parser = argparse.ArgumentParser(description="Sort and organize invoices.")
    arg_parser.add_argument("source", nargs="?", default="", help="Source directory")
    arg_parser.add_argument("destination", nargs="?", default="", help="Destination directory")

    return arg_parser.parse_args()

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

def get_client_and_date_from_string(content):
    client = None
    date = None

    for line in content.splitlines():
                line = line.strip()

                if line.lower().startswith("client:"):
                    client = line.split(":", 1)[1].strip()
                elif line.lower().startswith("date:"):
                    date = normalize_date(line.split(":", 1)[1].strip())

                # Breakout early if we find what we are looking for
                if client and date:
                    break

    return client, date

def extract_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return get_client_and_date_from_string(content)
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

def extract_from_pdf(file_path):
    try:
        with fitz.open(file_path) as f:
            content = ""
            for page in f:
                content += page.get_text()
            return get_client_and_date_from_string(content)
    except RuntimeError:
        raise RuntimeError(f"Error: File '{file_path}' unreadable.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")
    except PermissionError:
        raise PermissionError(f"Error: Permission denied for '{file_path}'.")
    except TypeError:
        raise TypeError(f"Error: '{file_path}' is an invalid argument for fitz.open().")

def extract_from_docx(file_path):
    try:
        doc = Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs])
        return get_client_and_date_from_string(content)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")
    except PermissionError:
        raise PermissionError(f"Error: Permission denied for '{file_path}'.")
    except PackageNotFoundError:
        raise PackageNotFoundError(f"Error: '{file_path}' is not a valid .docx file.")
    except (TypeError, AttributeError) as e:
        raise TypeError(f"Error: '{file_path}' content is malformed -")

def process_files(files):
    data = []
    supported_mimetypes = {
        ".txt": extract_from_txt,
        ".pdf": extract_from_pdf,
        ".docx": extract_from_docx
    }

    for file in files:
        _, extension = os.path.splitext(file)
        client, date = supported_mimetypes.get(extension, lambda *args: ("Unknown", "Unknown"))(file)
        data.append({
                "path": file,
                "client": client,
                "date": date
            })

    return data

def rename_and_move_files(destination_path, invoice_data_dict):
    for invoice in invoice_data_dict:
        source_path = invoice.get("path")
        _, extension = os.path.splitext(source_path)
        client = invoice.get("client", "Unsorted").strip().title()
        date = invoice.get("date", "Unknown")
        timestamp = datetime.now().strftime("%H%M%S")

        # Create Client folder
        client_folder = os.path.join(destination_path, client)
        os.makedirs(client_folder, exist_ok=True)

        # Save new file with Client Name and Date
        new_file_name = f"{date}_Invoice_{timestamp}{extension}"
        new_file_path = os.path.join(client_folder, new_file_name)
        shutil.copy2(source_path, new_file_path)

def main():
    # Configure logging
    logger = configure_logger()

    try:
        # Accept file path
        # The source will always be the first argument, and the destination will be the second
        args = process_args()
        source_arg = args.source
        destination_arg = args.destination
        source_path, destination_path = get_file_paths(source_arg, destination_arg)

        # Read files
        files = get_file_names(source_path)

        # Parse Client Name and Date
        invoice_data = process_files(files)

        # Create Client folder
        rename_and_move_files(destination_path, invoice_data)

    except Exception as e:
        logger.exception(e)
    
if __name__ == "__main__":
    main()