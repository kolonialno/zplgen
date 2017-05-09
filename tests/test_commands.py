# encoding: utf-8

from unittest import TestCase

from zplgen import Command, Font


class CommandsTestCase(TestCase):
    """
    Tests for the interesting command types.
    """

    def test_field_encoding(self):
        """
        Tests that Command.field handles unicode characters by encoding
        in cp1252 and returning the command as the bytes type.
        """

        data = u'håhå'

        expected_bytes = (
            '^FO0,0' '^FD' + data + '^FS'
        ).encode('cp1252')

        encoded_field = Command.field(data)

        self.assertIsInstance(encoded_field, bytes)
        self.assertEqual(encoded_field, expected_bytes)

    def test_field_minimal(self):
        """
        Tests the minimal set of arguments to Command.field.
        """

        data = 'data'

        expected_command = (
            '^FO0,0' '^FD' + data + '^FS'
        ).encode('cp1252')

        minimal_field = Command.field(data)

        self.assertEqual(minimal_field, expected_command)

    def test_field_maximal(self):
        """
        Tests that Command.field generates the expected set of commands
        when given the full set of arguments.
        """

        data = '123'
        x = 12
        y = 13
        font = Font('0', 10)
        block = '^FB200,1'
        barcode = '^BE3,1'
        invert = '^FR'

        expected_command = (
            font +
            '^FO{},{}'.format(x, y) +
            block +
            barcode +
            invert +
            '^FD{}'.format(data) +
            '^FS'
        ).encode('cp1252')

        maximal_field = Command.field(
            data, x=x, y=y,
            font=font, block=block,
            barcode=barcode, invert=True,
        )

        self.assertEqual(maximal_field, expected_command)

    def test_argument_trimming(self):
        """
        Tests that insignificant argument trimming works as expected for
        the Command.block method.
        """

        # If given only the first arg, the trailing commas should not
        # be included.

        width = '100'
        expected_trimmed_command = (
            '^FB' + width
        ).encode('cp1252')

        trimmed_command = Command.block(width)

        self.assertEqual(trimmed_command, expected_trimmed_command)

        # If given extra args, the commas should not be trimmed

        extra_args = (2, 3, 'R', 2)

        expected_untrimmed_command = (
            '^FB{},{},{},{},{}'.format(width, *extra_args)
        ).encode('cp1252')

        untrimmed_command = Command.block(width, *extra_args)

        self.assertEqual(untrimmed_command, expected_untrimmed_command)


class FontTestCase(TestCase):
    """
    Tests the essential functionality of the Font utility class.
    """

    def setUp(self):
        self.font = Font('0', 3, 4, orientation='N')

    def test_str(self):
        "Tests that the string representation uses the default height/width."
        self.assertEqual(self.font, '^A0N,3,4')
        self.assertEqual(str(self.font), '^A0N,3,4')

    def test_call(self):
        "Tests that calling the object scales it."
        self.assertEqual(self.font(100, 200), '^A0N,100,200')
