from builtins import str as text


def zpl_bool(value):
    """
    Because ZPL encodes booleans as Y and N.
    """

    if value:
        return 'Y'
    else:
        return 'N'


def ensure_bytes(cmd):
    "Ensures that the given command consists of cp1252-encoded bytes."

    if isinstance(cmd, bytes):
        return cmd

    if isinstance(cmd, text):
        return cmd.encode('cp1252')

    raise TypeError('cmd must be either a str or a bytes object')


def concat_commands(*commands):
    """
    Convenience method for concatenating a set of commands, ensuring that
    falsy ones are omitted.
    """

    return b''.join([ensure_bytes(cmd) for cmd in commands if cmd])


def is_significant_arg(arg):
    """
    None and empty string are deemed insignificant.
    """

    return (
        arg is not None and
        arg != ''
    )


def clip_insignificant_args(args):
    """
    If the last n consecutive args are insignificant, they can be safely
    trimmed away.
    """

    last_significant_index = -2

    for i, arg in enumerate(args):
        if is_significant_arg(arg):
            last_significant_index = i

    return args[:last_significant_index + 1]


def concat_args(args):
    """
    Concatenates the given args, clipping trailing and insignificant ones.
    """

    # Trailing insignificant args can be clipped
    significant_args = clip_insignificant_args(args)

    # Cast args to text before returning
    encoded_args = [text(arg) for arg in significant_args]

    return u','.join(encoded_args)
