import unittest
import os
import shutil
import tempfile
from shell_emulator import execute_command, setup_virtual_fs, base_path, current_path

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Set up a virtual filesystem for testing."""
        global current_path, base_path
        self.temp_dir = tempfile.mkdtemp()
        self.test_dir = os.path.join(self.temp_dir, "test_dir")
        os.mkdir(self.test_dir)
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("Line 1\\nLine 2\\nLine 3\\n")

        base_path = self.temp_dir
        current_path = base_path

    def tearDown(self):
        """Clean up the temporary filesystem."""
        shutil.rmtree(self.temp_dir)

    def test_ls(self):
        """Test the ls command."""
        output = execute_command("ls")
        self.assertIn("test_dir", output)

    def test_cd(self):
        """Test the cd command."""
        output = execute_command("cd test_dir")
        self.assertEqual(output, "")
        self.assertEqual(current_path, os.path.join(base_path, "test_dir"))

    def test_uname(self):
        """Test the uname command."""
        output = execute_command("uname")
        self.assertEqual(output, "EmulatorShell v1.0")

    def test_history(self):
        """Test the history command."""
        execute_command("uname")
        execute_command("ls")
        output = execute_command("history")
        self.assertIn("uname", output)
        self.assertIn("ls", output)

    def test_tac(self):
        """Test the tac command."""
        execute_command("cd test_dir")
        output = execute_command("tac test_file.txt")
        self.assertEqual(output, "Line 3\\nLine 2\\nLine 1\\n")

    def test_exit(self):
        """Test the exit command."""
        with self.assertRaises(SystemExit):
            execute_command("exit")

if __name__ == "__main__":
    unittest.main()
