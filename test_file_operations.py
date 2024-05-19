import unittest
from kursinis import ReadFileOperation, WriteFileOperation, FileOperationFactory, is_valid_date

class TestFileOperations(unittest.TestCase):
    
    def test_read_file_not_found(self):
        operation = ReadFileOperation()
        result = operation.execute('non_existent_file.txt')
        self.assertEqual(result, "File not found.")

    def test_read_file_success(self):
        operation = ReadFileOperation()
        test_content = "Hello, world!"
        with open('test_file.txt', 'w') as file:
            file.write(test_content)
        result = operation.execute('test_file.txt')
        self.assertEqual(result, test_content)

    def test_write_file_success(self):
        operation = WriteFileOperation()
        test_content = "New content"
        result = operation.execute('test_write_file.txt', test_content)
        self.assertEqual(result, "Data successfully written to file.")
        with open('test_write_file.txt', 'r+') as file:
            content = file.read().strip()
            self.assertEqual(content, test_content)
            file.truncate(0)

    def test_write_file_exception(self):
        operation = WriteFileOperation()
        result = operation.execute('/invalid_path/test_write_file.txt', 'data')
        self.assertIn("Error writing to file:", result)

    def test_invalid_date(self):
        self.assertFalse(is_valid_date('2023-13-01'))
        self.assertFalse(is_valid_date('2023-00-01'))
        self.assertFalse(is_valid_date('2023-01-32'))
        self.assertFalse(is_valid_date('invalid_date'))

    def test_valid_date(self):
        self.assertTrue(is_valid_date('2023-05-18'))
        self.assertTrue(is_valid_date('2024-02-29'))  # Leap year

if __name__ == '__main__':
    unittest.main()