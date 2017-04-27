from .utils import concat_args, concat_commands, zpl_bool


class Command(bytes):
    """
    Convenience class for generating bytes to be sent to a ZPL2 printer.
    """

    ENCODING = 'cp1252'

    COMMAND_TYPE_CONTROL = b'~'
    COMMAND_TYPE_FORMAT = b'^'

    FIELD_BLOCK = 'FB'
    FIELD_DATA = 'FD'
    FIELD_INVERT = 'FR'
    FIELD_ORIGIN = 'FO'
    FIELD_SEPARATOR = 'FS'

    LABEL_END = 'XZ'
    LABEL_HOME = 'LH'
    LABEL_START = 'XA'

    FONT = 'A'

    BARCODE_EAN = 'BE'
    BARCODE_FIELD_DEFAULT = 'BY'

    def __new__(cls, name, *args, **options):
        """
        Constructor for a command returning bytes in an acceptable encoding.

        The following options are available:

            command_type
                Either Command.TYPE_FORMAT or Command.TYPE_CONTROL.
                (Defaults to Command.TYPE_FORMAT.)

            encoding
                The encoding to use for the returned bytes.
        """

        options.setdefault('encoding', cls.ENCODING)

        return cls.to_bytes(
            cls.get_command_type(options) +
            name +
            concat_args(args)
        )

    ######################
    # Command primitives #
    ######################

    @classmethod
    def field_block(
            cls, width, n_lines='',
            line_spacing='', justify='', left_margin=''):
        "A bounding box for the printed field data."

        return cls(
            cls.FIELD_BLOCK,
            width, n_lines, line_spacing, justify, left_margin,
        )

    block = field_block

    @classmethod
    def field_data(cls, data):
        "The content data of the field."
        return cls(cls.FIELD_DATA, data)

    @classmethod
    def field_invert(cls):
        "Prints the field black-on-white."
        return cls(cls.FIELD_INVERT)

    @classmethod
    def field_origin(cls, x, y):
        "Sets the origin coordinates of a field."
        return cls(cls.FIELD_ORIGIN, x, y)

    @classmethod
    def field_separator(cls):
        "Must be placed between separate field definitions."
        return cls(cls.FIELD_SEPARATOR)

    @classmethod
    def label_end(cls):
        "Ends a series of label print commands."
        return cls(cls.LABEL_END)

    @classmethod
    def label_home(cls, x, y):
        "Sets the origin for an entire label."
        return cls(cls.LABEL_HOME, x, y)

    @classmethod
    def label_start(cls):
        "Starts a series of label print commands."
        return cls(cls.LABEL_START)

    @classmethod
    def font(cls, name, height, width=None, orientation=''):
        """
        Sets the current font.

            name
                The name of a font available to the printer. Typically
                indicated by 0-9 or A-Z.

            height
                The height of the font in points.

            width
                The width of the font in points. Defaults to matching
                the height.

            orientation
                The direction of the text. See ORIENTATION_*.
        """

        if width is None:
            width = height

        # Font name and orientation are not comma-separated
        name_with_orientation = ''.join((str(name), orientation))

        return cls(cls.FONT, name_with_orientation, height, width)

    @classmethod
    def barcode_ean(
            cls, orientation='', height='',
            interpretation_line=True, interpretation_line_is_above=True):
        """
        Indicates that the current field is an EAN-13 barcode.

            orientation
                The direction of the barcode. See ORIENTATION_*.

            height
                The height of the barcode.

            interpretation_line
                Indicates whether the barcode numbers should be printed.

            interpretation_line_is_above
                Indicates that the barcode numbers should be printed above
                the barcode, not below.
        """

        return cls(
            cls.BARCODE_EAN, orientation, height,
            zpl_bool(interpretation_line),
            zpl_bool(interpretation_line_is_above),
        )

    @classmethod
    def barcode_field_default(cls, width, heigth='', ratio=''):
        "Sets barcode field defaults. Applied until new defaults are applied."
        return cls(cls.BARCODE_FIELD_DEFAULT, width, ratio, heigth)

    ####################
    # Complex commands #
    ####################

    @classmethod
    def field(
            cls, text, x=0, y=0, font=None,
            block=None, barcode=None, invert=False):
        """
        Convenience method for generating a field, which is basically
        a concatenation of several related subcommands.

            text
                Field data -- e.g. text or a barcode value.

            x, y
                Placement within the label.

            invert
                Inverts the colors of the printed text.
        """

        invert_cmd = cls.field_invert() if invert else None

        return concat_commands(
            font,
            cls.field_origin(x, y),
            block,
            barcode,
            invert_cmd,
            cls.field_data(text),
            cls.field_separator(),
        )

    #############
    # Utilities #
    #############

    @classmethod
    def get_command_type(cls, options):
        """
        Gets the command type from the options, verifying that it is valid.
        """

        valid_command_types = [
            cls.COMMAND_TYPE_CONTROL,
            cls.COMMAND_TYPE_FORMAT,
        ]

        # Get the command type from options
        command_type = options.pop('type', cls.COMMAND_TYPE_FORMAT)
        if command_type not in valid_command_types:
            raise TypeError('command_type must be in {}'.format(
                ', '.join(valid_command_types)
            ))

        return command_type

    @classmethod
    def to_bytes(cls, data):
        """
        Encodes the given data in an encoding understood by the printer.
        """

        return unicode(data).encode(cls.ENCODING)


class Font(object):
    """
    Utility object for defining fonts, then scaling them in later use.
    """

    def __init__(
            self, name, default_height=30,
            default_width=None, orientation=''):

        self.name = name
        self.default_height = default_height
        self.default_width = default_width
        self.orientation = orientation

    def scaled(self, height, width=None):
        """
        Returns the current font, scaled to the given height and width.
        """

        return self.as_command(
            name=self.name,
            height=height,
            width=width,
            orientation=self.orientation,
        )

    @staticmethod
    def as_command(name, height, width, orientation):
        """
        Returns the font as a Command.
        """

        return Command.font(
            name=name,
            height=height,
            width=width,
            orientation=orientation,
        )

    def __call__(self, *args, **kwargs):
        return self.scaled(*args, **kwargs)

    def __str__(self):
        return self.scaled(self.default_height, self.default_width)
