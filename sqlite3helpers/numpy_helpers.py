import io
import os

import numpy
import sqlite3


def adapt_array_to_binary(array: numpy.array) -> sqlite3.Binary:
    """Convert a numpy array object to a binary object

    Used to store numpy arrays to the database
    """
    out = io.BytesIO()
    numpy.save(out, array)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_binary_to_array(bytes_string: bytes) -> numpy.array:
    """Convert a bytes binary object to a numpy array

    Used to retreive numpy arrays from the database
    """
    out = io.BytesIO(bytes_string)
    out.seek(0)
    return numpy.load(out)


def sqlite3_register_numpy_array_type() -> None:
    """Registers adapter and converter to sqlite3 module"""
    sqlite3.register_adapter(numpy.ndarray, adapt_array_to_binary)
    sqlite3.register_converter("array", convert_binary_to_array)


def connect(database: str | os.PathLike,
            register_numpy_array_type=True,
            **kwargs,
            ) -> sqlite3.Connection:
    """Wrapper around sqlite3.connect

    By default sets `detect_types` to sqlite3.PARSE_DECLTYPES
    which ensures SQLite returns a numpy array when fetching
    data. The user can override this behaviour by setting
    `detect_types` themselves.

    If `detect_types` is not set to sqlite3.PARSE_DECLTYPES,
    the database will return a binary object on fetching,
    which can be parsed using the convert_array function.

    Also by default registers the numpy array type to the
    sqlite3 module using the sqlite3_register_numpy_array_type()
    function.

    For more information see documentation on sqlite3.connect()

    Args:
        database (str | os.PathLike):
            Database file path. See sqlite3 documentation for more
            information.
        **kwargs:
            sqlite3.connect() kwargs. See sqlite3.connect()
            documentation

    Returns:
        sqlite3.Connection
    """
    if register_numpy_array_type:
        sqlite3_register_numpy_array_type()
    if "detect_types" in kwargs.keys():
        return sqlite3.connect(database,
                               **kwargs)
    return sqlite3.connect(database,
                           detect_types=sqlite3.PARSE_DECLTYPES,
                           **kwargs)
