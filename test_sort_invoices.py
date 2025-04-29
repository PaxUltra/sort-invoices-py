import unittest
import os
from unittest.mock import patch
from sort_invoices import normalize_date, get_file_paths, get_file_names, get_client_and_date_from_string, process_files

class TestInvoiceFunctions(unittest.TestCase):
    def test_normalize_date(self):
        # Success
        valid_date = "December 15, 2023"
        expected_output = "2023-12-15"
        output_date = normalize_date(valid_date)
        self.assertEqual(output_date, expected_output)

        # Invalid date
        invalid_date = "This is not a date"
        output_date = normalize_date(invalid_date)
        self.assertEqual(output_date, "Unknown")

    def test_get_file_paths(self):
        # No arguments
        # Should return the current directory
        current_dir = os.getcwd()
        source_path, destination_path = get_file_paths("", "")
        self.assertEqual(source_path, current_dir)
        self.assertEqual(destination_path, current_dir)

        # A directory that exists
        source_arg = "."
        destination_arg = "."
        expected_source = os.path.abspath(".")
        expected_destination = os.path.abspath(".")
        source_path, destination_path = get_file_paths(source_arg, destination_arg)
        self.assertEqual(source_path, expected_source)
        self.assertEqual(destination_path, expected_destination)

        # Directory that doesn't exist
        # Source doesn't exist
        source_arg = "sfsdfs"
        destination_arg = "sdfsfsfds"
        with self.assertRaises(ValueError) as context:
            source_path, destination_path = get_file_paths(source_arg, destination_arg)
        self.assertEqual(str(context.exception), "Error: Source path 'sfsdfs' not found, or inaccessible.")

        # Source exists, but destination doesn't
        source_arg = "."
        destination_arg = "sdfsfsfds"
        with self.assertRaises(ValueError) as context:
            source_path, destination_path = get_file_paths(source_arg, destination_arg)
        self.assertEqual(str(context.exception), "Error: Destination path 'sdfsfsfds' not found, or inaccessible.")

    @patch("os.path.isfile")
    @patch("os.listdir")
    def test_get_file_names(self, mock_listdir, mock_isfile):
        # Valid directory, with supported extensions
        # For this test, we are going to pretend that everything is a file
        mock_listdir.return_value = [
            "invoice1.pdf", "invoice2.docx", "notes.txt",
            "image.jpg", "README.md", "folder"
        ]
        mock_isfile.return_value = True
        expected_output = [
            "some/fake/path/invoice1.pdf",
            "some/fake/path/invoice2.docx",
            "some/fake/path/notes.txt"
        ]
        result = get_file_names("some/fake/path")
        self.assertEqual(result, expected_output)

        # No files present
        # Should return an empty list
        mock_listdir.return_value = [
            "foo", "bar", "notes",
            "Desktop", "Documents", "folder"
        ]
        mock_isfile.return_value = False
        expected_output = []
        result = get_file_names("some/fake/path")
        self.assertEqual(result, expected_output)

        # FileNotFound error
        mock_listdir.side_effect = FileNotFoundError("Error: Directory 'some/fake/path' not found.")
        with self.assertRaises(FileNotFoundError) as context:
            get_file_names("some/fake/path")
        self.assertEqual(str(context.exception), "Error: Directory 'some/fake/path' not found.")

        # NotADirectory error
        mock_listdir.side_effect = NotADirectoryError("Error: 'some/fake/path.txt' is not a directory.")
        with self.assertRaises(NotADirectoryError) as context:
            get_file_names("some/fake/path.txt")
        self.assertEqual(str(context.exception), "Error: 'some/fake/path.txt' is not a directory.")

    def test_get_client_and_date_from_string(self):
        # Client and date present
        # Function hinges on 'Client:' and 'Date:' being present
        test_content = "Client: Beta LLC\n \
                        Date: 2023-12-15\n \
                        Amount: $1800"
        expected_client = "Beta LLC"
        expected_date = "2023-12-15"
        client, date = get_client_and_date_from_string(test_content)
        self.assertEqual(client, expected_client)
        self.assertEqual(date, expected_date)

        # Weird formatting
        test_content = "asdfasdfaksfdafjd;k\n" \
        "cLiEnT: Beta LLC\n" \
        "asdfasdfasdfasdgfdger3435234\n" \
        "DaTe: 2023-12-15\n" \
        "3574274hfh23974hf82y349yhf"
        expected_client = "Beta LLC"
        expected_date = "2023-12-15"
        client, date = get_client_and_date_from_string(test_content)
        self.assertEqual(client, expected_client)
        self.assertEqual(date, expected_date)

        # Client and date not present
        # Should return None for both values
        test_content = "Client and date are : not present : here."
        expected_client = None
        expected_date = None
        client, date = get_client_and_date_from_string(test_content)
        self.assertEqual(client, expected_client)
        self.assertEqual(date, expected_date)

    @patch("sort_invoices.extract_from_docx")
    @patch("sort_invoices.extract_from_pdf")
    @patch("sort_invoices.extract_from_txt")
    def test_process_files(self, mock_extract_from_txt, mock_extract_from_pdf, mock_extract_from_docx):
        # Valid list of file paths
        test_files = [
            "some/fake/path/foo.txt",
            "some/fake/path/bar.pdf",
            "another/fake/path/hehe.exe",
            "another/fake/path/nothehe.docx"
        ]
        mock_extract_from_txt.return_value = ("Big Company", "2025-04-12")
        mock_extract_from_pdf.return_value = ("Another Company", "2025-05-22")
        mock_extract_from_docx.return_value = ("Wacky Woohoo Pizza", "2024-10-02")
        expected_output = [
            {
                "path": "some/fake/path/foo.txt",
                "client": "Big Company",
                "date": "2025-04-12"
            },
            {
                "path": "some/fake/path/bar.pdf",
                "client": "Another Company",
                "date": "2025-05-22"
            },
            {
                "path": "another/fake/path/hehe.exe",
                "client": "Unknown",
                "date": "Unknown"
            },
            {
                "path": "another/fake/path/nothehe.docx",
                "client": "Wacky Woohoo Pizza",
                "date": "2024-10-02"
            }
        ]
        result = process_files(test_files)
        self.assertEqual(result, expected_output)

        # Empty file list
        test_files = []
        expected_output = []
        result = process_files(test_files)
        self.assertEqual(result, expected_output)