# from https://github.com/mmdbalkhi/Flask-tinydb

# tinydb_flask.py
import io
import os
import sys
import tinydb
from flask import Flask
from typing import Any
from typing import Dict
from typing import Optional
from tinydb import Storage as _Storage
from tinydb.storages import JSONStorage
from tinydb.storages import MemoryStorage
from tinydb.storages import touch

__all__ = (
    "JSONStorage",
    "MemoryStorage",
    "YAMLStorage",
    "TinyDB",
)

class Storage(_Storage):
    def __init__(
        self, path: str, create_dirs=False, encoding=None, access_mode="r+", **kwargs
    ) -> None:
        """
        Create a new instance.

        Also creates the storage file, if it doesn't exist and the access mode is appropriate for writing.

        :param path: Where to store the JSON data.
        :param access_mode: mode in which the file is opened(r, r+, w, a, x, b, t, +, U)
        :type access_mode: str
        """

        super().__init__()

        self._mode = access_mode
        self.kwargs = kwargs

        # Create the file if it doesn't exist and creating is allowed by the
        # access mode
        if any(
            [character in self._mode for character in ("+", "w", "a")]
        ):  # any of the writing modes
            touch(path, create_dirs=create_dirs)

        # Open the file for reading/writing
        self._handle = open(path, mode=self._mode, encoding=encoding)

    def close(self) -> None:
        self._handle.close()


try:
    import yaml
except ImportError:  # pragma: no cover
    import warnings

    warnings.warn(
        "pyyaml lib is Not Installed. If you want to use yaml,"
        "you must be install pyyaml via this command: \n"
        "pip install Flask-TinyDB[yaml]"
    )
    sys.exit(1)


class YAMLStorage(Storage):
    """Store the data in a Yaml file.

    usage:
        ...
        >>> app.config["TINYDB_DATABASE_STORAGE"] = YAMLStorage
        >>> db = TinyDB(app)
        ...
    """

    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:

        # Get the file size by moving the cursor to the file end and reading
        # its location
        self._handle.seek(0, os.SEEK_END)
        size = self._handle.tell()

        if not size:
            # File is empty, so we return ``None`` so TinyDB can properly
            # initialize the database
            return None

        self._handle.seek(0)
        return yaml.safe_load(self._handle.read())

    def write(self, data: Dict[str, Dict[str, Any]]) -> None:
        # Move the cursor to the beginning of the file just in case
        self._handle.seek(0)

        # Serialize the database state using the user-provided arguments
        serialized = yaml.dump(data, **self.kwargs)

        # Write the serialized data to the file
        try:
            self._handle.write(serialized)
        except io.UnsupportedOperation as err:  # pragma: no cover
            raise OSError(
                f'Cannot write to the database. Access mode is "{self._mode}"'
            ) from err

        # Ensure the file has been written
        self._handle.flush()
        os.fsync(self._handle.fileno())

        # Remove data that is behind the new cursor in case the file has
        # gotten shorter
        self._handle.truncate()

class TinyDB:
    """tinydb class for flask"""

    def __init__(self, app: Flask) -> None:
        self.app = app
        self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.config.setdefault("TINYDB_DATABASE_PATH", "flask.db")
        app.config.setdefault("TINYDB_DATABASE_TABLE", "app")
        app.config.setdefault("TINYDB_DATABASE_STORAGE", tinydb.storages.JSONStorage)
        #print(app.config["TINYDB_DATABASE_STORAGE"])
        self.db = tinydb.TinyDB(
            app.config["TINYDB_DATABASE_PATH"],
            storage=app.config["TINYDB_DATABASE_STORAGE"],
        )
        self.table = self.db.table(
            app.config["TINYDB_DATABASE_TABLE"],
        )

    def get_db(self) -> tinydb.TinyDB:
        """Get the underlying TinyDB instance."""
        return self.db

    def get_table(self) -> tinydb.table.Table:
        """Get the underlying TinyDB Table instance."""
        return self.table