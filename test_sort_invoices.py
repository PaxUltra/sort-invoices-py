import unittest
import os
from unittest.mock import patch
from sort_invoices import normalize_date, get_file_paths, get_file_names

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