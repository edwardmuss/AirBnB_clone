#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import console
from contextlib import contextmanager
from datetime import datetime
import inspect
from io import StringIO
import models
import pep8
import sys
from os import environ, stat
import unittest
from unittest.mock import patch


Place = models.Place
State = models.State
User = models.User
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')
HBNBCommand = console.HBNBCommand
storage = console.storage
CNC = models.CNC


@contextmanager
def redirect_streams():
    """function redirects streams: stdout & stderr for testing purposes
    first creates StringIO obj, then saves / updates stdout & stderr"""
    new_stdout, new_stderr = StringIO(), StringIO()
    old_stdout, sys.stdout = sys.stdout, new_stdout
    old_stderr, sys.stderr = sys.stderr, new_stderr
    try:
        # returns new file streams
        yield new_stdout, new_stderr
    finally:
        # restore std streams to the previous value
        sys.stdout, sys.stderr = old_stdout, old_stderr


class TestHBNBcmdDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def test_help_quit(self):
        h = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h, output.getvalue().strip())

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())

    def setUpClass(cls):
        """init: prints output to mark new tests"""
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......  For the Console  .......')
        print('.................................\n\n')
        cls.all_funcs = inspect.getmembers(console.HBNBCommand,
                                           inspect.isfunction)

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nCommand interpreter for Holberton AirBnB project\n'
        actual = console.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = '\n    Command inerpreter class\n    '
        actual = HBNBCommand.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in console file"""
        AF = TestHBNBcmdDocs.all_funcs
        for f in AF:
            if "_HBNBCommand_" in f[0]:
                self.assertIsNotNone(f[1].__doc__)

    def test_pep8_console(self):
        """... console.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['console.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

if __name__ == '__main__':
    unittest.main