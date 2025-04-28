import unittest
from sort_invoices import normalize_date

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