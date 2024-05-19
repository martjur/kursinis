import unittest
from unittest.mock import patch, mock_open
from kursinis import (
    ReadFileOperation,
    WriteFileOperation,
    FileOperationFactory,
    DateUtils
)

class TestFileOperations(unittest.TestCase):

    def test_read_file_operation_success(self):
        mock_file_data = "Sample file content."
        with patch("builtins.open", mock_open(read_data=mock_file_data)):
            operation = ReadFileOperation()
            result = operation.execute("dummy_path")
            self.assertEqual(result, mock_file_data)

    def test_read_file_operation_file_not_found(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = FileNotFoundError
            operation = ReadFileOperation()
            result = operation.execute("dummy_path")
            self.assertEqual(result, "File not found.")

    def test_write_file_operation_success(self):
        mock_file_data = "New content"
        with patch("builtins.open", mock_open()) as mocked_open:
            operation = WriteFileOperation()
            result = operation.execute("dummy_path", mock_file_data)
            mocked_open().write.assert_called_once_with(mock_file_data + '\n')
            self.assertEqual(result, "Data successfully written to file.")

    def test_write_file_operation_exception(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = IOError("mocked IO error")
            operation = WriteFileOperation()
            result = operation.execute("dummy_path", "data")
            self.assertEqual(result, "Error writing to file: mocked IO error")

class TestFileOperationFactory(unittest.TestCase):

    def test_create_read_operation(self):
        operation = FileOperationFactory.create_operation("read")
        self.assertIsInstance(operation, ReadFileOperation)

    def test_create_write_operation(self):
        operation = FileOperationFactory.create_operation("write")
        self.assertIsInstance(operation, WriteFileOperation)

    def test_create_invalid_operation(self):
        with self.assertRaises(ValueError):
            FileOperationFactory.create_operation("invalid")

class TestUtilityFunctions(unittest.TestCase):

    def test_is_valid_date_valid(self):
        self.assertTrue(DateUtils.is_valid_date("2023-05-19"))

    def test_is_valid_date_invalid_format(self):
        self.assertFalse(DateUtils.is_valid_date("19-05-2023"))

    def test_is_valid_date_invalid_date(self):
        self.assertFalse(DateUtils.is_valid_date("2023-13-01"))  # Invalid month
        self.assertFalse(DateUtils.is_valid_date("2023-00-01"))  # Invalid month
        self.assertFalse(DateUtils.is_valid_date("2023-05-32"))  # Invalid day
        self.assertFalse(DateUtils.is_valid_date("2023-05-00"))  # Invalid day

if __name__ == "__main__":
    unittest.main()