# -*- encoding: utf-8 -*-
import datetime as dt
import dateutil.parser

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
import logging
import os
from os import lstat
import dill

import pycdlib

from .consts import *
from .disc_info import DiscInfo
from .file_db import FileDatabase
from .hash_db import *
from .hash_file_entry import iso9660_dir, HashFileEntry


# import tarfile
# import tempfile
# from datetime import datetime
# from getpass import getpass
# import hashlib
# import uuid
# import socket
# import re
# import fnmatch
# import mimetypes
# import calendar
# import functools
# from contextlib import closing  # for Python2.6 compatibility
# from gzip import GzipFile
#
# import yaml
# from beefish import decrypt, encrypt_file
# import grandfatherson
# from byteformat import ByteFormatter
#
# from bakthat.backends import GlacierBackend, S3Backend, RotationConfig, SwiftBackend
# from bakthat.conf import config, events, load_config, DEFAULT_DESTINATION, DEFAULT_LOCATION, CONFIG_FILE, EXCLUDE_FILES
# from bakthat.utils import _interval_string_to_seconds
# from bakthat.models import Backups
# from bakthat.sync import BakSyncer, bakmanager_hook, bakmanager_periodic_backups
# from bakthat.plugin import setup_plugins, plugin_setup
#
# __version__ = "0.6.0"
#
#
log = logging.getLogger("odarchive")


def archive():
    pass


class odarchiveFilter(logging.Filter):

    def filter(self, rec):
        if rec.name.startswith("odarchive") or rec.name == "root":
            return True
        else:
            return rec.levelno >= logging.WARNING


#!/usr/bin/env python3
from argparse import ArgumentParser
from fnmatch import fnmatch
from os import fsdecode, fsencode, getcwd, lstat, readlink, stat_result
from pathlib import Path
import re


# fnmatch patterns, specifically:
IMPORT_FILENAME_PATTERNS = [
    DB_FILENAME,
    HASH_FILENAME,
    HASH_FILENAME + ".asc",
    "*.sha512sum",
    "*.sha512sum.asc",
    "DIGESTS",
    "DIGESTS.asc",
]
SURROGATE_ESCAPES = re.compile(r"([\udc80-\udcff])")

ADDED_COLOR = "\033[01;32m"
REMOVED_COLOR = "\033[01;34m"
MODIFIED_COLOR = "\033[01;31m"
NO_COLOR = "\033[00m"


def find_external_hash_files(path: Path):
    for dirpath_str, _, filenames in walk(str(path)):
        dirpath = Path(dirpath_str).absolute()
        for filename in filenames:
            if any(fnmatch(filename, pattern) for pattern in IMPORT_FILENAME_PATTERNS):
                yield dirpath / filename


def print_file_list(files):
    for filename in sorted(files):
        printable_filename = SURROGATE_ESCAPES.sub("\ufffd", str(filename))
        print(printable_filename)
    print()

def print_file_lists(added, removed, modified):
    if added:
        print(ADDED_COLOR + "Added files:" + NO_COLOR)
        print_file_list(added)
    if removed:
        print(REMOVED_COLOR + "Removed files:" + NO_COLOR)
        print_file_list(removed)
    if modified:
        print(MODIFIED_COLOR + "Modified files:" + NO_COLOR)
        print_file_list(modified)


def list_dirs(files):
    for filename in sorted(files):
        printable_filename = SURROGATE_ESCAPES.sub("\ufffd", str(filename))
        print(printable_filename)
    print()


def load_archiver_from_dill(filename="archiver.dill"):
    with open(filename, "rb") as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        archiver = dill.load(f)
    return archiver


def load_archiver_from_json(filename=None, json_data=None):
    """Load an archive from a catalogue.jsno file eg from an written CD.
    If filename is none, can load the json directly.  Note the filename takes precedence over json_data"""
    ar = Archiver()
    def parse_json(json_data):
        d = json_data
        for attribute in ('client_name', 'job_name', 'iso_path_root', 'source_path', 'version'):
            try:
                setattr(ar, attribute, d[attribute])
            except KeyError:
                pass
        try:
            ar.client_name = uuid.UUID(d["job_id"])
        except KeyError:
            pass  # Ignore missing client names.  Missisn from frist version
        # fill the has_db from the d['files'] entry.
        ar.hash_db = HashDatabase(None, ar.iso_path_root)
        ar.hash_db.entries = HashFileEntries.create_from_json(ar.iso_path_root, d['files'], ar.hash_db)
        """Save the current catalogue to file as a JSON file.
        It should be possible to reread this file later and recreate this record."""
        ar.guid = uuid.UUID(d["guid"])
        if int(d['version']) != ar.hash_db.version:
            raise odarchiveError(f"Version of Catalogue ({d['version']} " +
                                 " does not match that of software ({ar.version})." +
                                 "Upgrading version not currently possible. Contact supplier")
        try:
            date_str = d['date']
            ar.archive_date = dateutil.parser.parse(date_str) # This a read only value after an archive has been
            # created
        except:
            raise odarchiveError('Date string malformed or not found in catalogue.json')
        try:
            ar.hash_db.str_segment_size = d['segment_size_str']
        except:
            ar.hash_db.str_segment_size = 'bd'
        try:
            ar.hash_db.int_segment_size = d['segment_size_int']
        except:
            ar.hash_db.int_segment_size = 25000000000
    if filename:
        with open(filename) as json_data_from_file:
            parse_json(json.load(json_data_from_file))
        ar.hash_db.catalogue_size = os.path.getsize(filename)
    else:
        parse_json(json.loads(json_data))
        ar.hash_db.catalogue_size = len(json_data)
    return ar


class Archiver:
    """This holds the information on the archiving project - potentially should keep state over multiple
    invocations.  This means that you do not have to hold in memory a temporary copy of all discs but
    can do them one by one.  For a 10TB archiving to 25GB drives this is a big saving."""

    def __init__(self):
        # This is some default data which should be overwritten.
        self.iso_path_root = PurePosixPath("/DATA")
        self.client_name = 'Unknown client'
        self.job_name = 'Unamed job'
        self.job_id = uuid.uuid4()  # The job_id should only be changed when reading a job from an old catalogue.
        self.version = DATABASE_VERSION
        self.guid = None


    def save_as_dill(self, filename="archiver.dill"):
        """Saving using dill is really a lazy way of saving the archive (which works).  It should be replaced
        by saving as a json file.  'catalogue.json'  This should be transportable over time.  The reason is that
        you want to be able to work with the archive when you read it back in.  This could be part of a restore
        or verification process."""
        with open(filename, "wb") as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            dill.dump(self, f, dill.HIGHEST_PROTOCOL)

    def save(self, catalogue_name=DB_FILENAME):
        """Save the current catalogue to file as a JSON file.
        It should be possible to reread this file later and recreate this record and a complete archive."""
        if not hasattr(self, "hash_db"):
            raise odarchiveError('Trying to save an archive which has not yet calculated the hashes for all the files.')
        self.guid = uuid.uuid4()  # a second save will have a different guid as the structure is mutable and this
        # ensures that each saved file is uniquely identifiable.
        filename = Path(getcwd()) / catalogue_name
        data = {
            "client_name": self.client_name,  # date of saving the file
            "date": str(dt.datetime.utcnow().isoformat()),  # date of saving the file
            "guid": str(self.guid),
            "job_name" : self.job_name,
            "job_id" : str(self.job_id),
            "iso_path_root" : str(self.iso_path_root),
            "segment_size" : self.hash_db.segment_size,
            "source_path" : str(self.source_path), # Where did the data come from
            "version": self.version,
            "files": json.loads(self.hash_db.entries.to_json()),
            # List of directories are derived from file paths
        }
        with filename.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)

    def create_file_database(self, usb_path, job_name=None, client_name = None):
        # Create database
        self.file_db = FileDatabase(usb_path)
        if job_name:
            self.job_name = job_name
        if client_name:
            self.client_name = client_name
        self.source_path = usb_path
        # Check to make sure not overwriting database
        print("Initializing file database")
        self.file_db.update(
            usb_path
        )  # Scan directory to add files
        # Need to load the hash files into the Has list

    def convert_to_hash_database(self, verbose=False):
        if not self.is_locked:
            self.file_db.calculate_file_hash(verbose)
            # Create database
            self.hash_db = HashDatabase(self.file_db, self.iso_path_root)
        else:
            raise odarchiveError('Archive locked so cannot calculate hashes')

    def create_catalogue(self, verbose=False):
        """Creates a catalogue file catalogue.json on disc."""
        self.hash_db.save()  # Creates catalogue.json
        self.save()


    def write_iso(self, pretend=False, disc_num=None, job_name="new"):
        """No ISO file will be created if there are not files in it.  Eg using a disc num that is
        not being used."""
        try:
            if disc_num is None and self.hash_db.last_disc_number is not None:
                raise odarchiveError("disc_num is None but archive has been segmented")
            elif self.hash_db.last_disc_number is None and disc_num is not None:
                raise odarchiveError(
                    f"disc_num is {disc_num} but archive has not been segmented"
                )
            else:
                # Create ISO file
                iso = pycdlib.PyCdlib()
                if disc_num is None:  # Assuming standard is one based.
                    seqnum = 0
                else:
                    seqnum = disc_num
                if self.last_disc_num is None:  # Has not been segmented
                    set_size = 1
                else:
                    set_size = self.last_disc_num
                print(f'Disc num = |{disc_num}|')
                iso.new(
                    interchange_level=3,
                    udf="2.60",
                    app_ident_str="odarchive (C) 2018 drummonds.net",
                    abstract_file="README.MKD",
                    set_size=set_size,  # This is the size of the set of discs ie the number of disck
                    # eg 2 of set_size
                    seqnum=seqnum,
                )
        except AttributeError:
            raise odarchiveError(
                f"Probably have not yet created hash db"
            )

        # The readme file is created fresh for each disc created.  It should consist of specific information about
        # this disc and also information about the archive process
        readme = f"""# Archive File created by www.drummonds.net
This archive was created {dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}

The data for this archive is stored in the directory /DATA.
There is a catalogue of this archive stored in catalogue.json.  
This catalogue has a list of all the files archived in this run 
and on which disc they are stored.  
The same catalogue is written to each disc in the archive series."""
        readme_bytes = readme.encode("utf-8")
        iso.add_fp(
            BytesIO(readme_bytes),
            len(readme_bytes),
            "/README.MKD;1",
            udf_path="/readme.mkd",
        )
        iso.add_file(
            str(DB_FILENAME),
            f"/{DB_FILENAME.upper()};1",
            udf_path=f"/{DB_FILENAME}"  # Same catalogue for each disc
            # So that you can go to single disc and then find where to go next - which disc to read rather than
            # having to read all the files.
        )
        di = DiscInfo()
        di.setup(disc_num, set_size)
        disk_info_bytes = di.get_json().encode("utf-8")
        iso.add_fp(
            BytesIO(disk_info_bytes),
            len(disk_info_bytes),
            f"/{DISC_INFO_FILENAME.upper()};1",
            udf_path=f"/{DISC_INFO_FILENAME}",
        )
        dir_count = 0
        for this_dir in self.hash_db.entries.dir_entries(disc_num=disc_num):
            # Todo add Bridge format and iso9660
            # iso.add_directory(iso9660_dir(this_dir), udf_path=this_dir)
            # After 10^8 directories (which breaks a standard ISO 9660 the formatting will vary
            if this_dir == "/DATA":
                iso.add_directory(
                    "/DATA", udf_path="/DATA"
                )  # Add root data directory to both ISO and UDF
            else:
                iso.add_directory(
                    f"/DATA/{dir_count:08}", udf_path=this_dir
                )  # Note can't use "/" as ISO 9660 root as we are adding
                # a directory and this would only be the root
            dir_count += 1
        any_files = False
        file_count = 0
        for this_file in self.hash_db.files(disc_num=disc_num):
            # Todo add Bridge format and iso9660
            # iso.add_file(
            #     str(this_file.filename),
            #     this_file.iso9660_path,
            #     udf_path=str(this_file.udf_absolute_path),
            # )
            iso.add_file(
                str(this_file.file_system_path),
                f"/DATA/{file_count:08}",  # All data files in same directory and anonymise names :(
                udf_path=str(this_file.udf_absolute_path),
            )
            any_files = True
            file_count += 1
        if (
            not pretend and any_files
        ):  # Will not write out a cataloge with no files in it
            if disc_num is None:
                filename = f"{job_name}.iso"
            else:
                filename = f"{job_name}_{disc_num:04}.iso"
            # If file exists then iso.write will just overwrite part of it so need to delete it first.
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass
            iso.write(filename)
            iso.close()

    @property
    def is_locked(self):
        """Once you have successfully written the first ISO then you should lock the archive.
        This should prevent operations such as segmenting if the archive is locked."""
        try:
            return self.locked
        except AttributeError:  # NO hash db so not segmented
            return False

    def segment(self, size):
        """Segment an archive.  This is mainly"""
        if not self.is_locked:
            catalogue_size = (
                (2048 + lstat(str(str(DB_FILENAME))).st_size) // 2048
            ) * 2048  # Account for sector size
            self.hash_db.segment(size, catalogue_size)
        else:
            raise odarchiveError('Archive is locked so cannot resegment')

    @property
    def is_segmented(self):
        try:
            return self.hash_db.is_segmented
        except AttributeError:  # NO hash db so not segmented
            return False

    def get_info(self):
        """Returns summary information on archive"""
        try:
            result = self.hash_db.get_info()
        except:
            result = self.file_db.get_info()
        # Add archive specific info
        if hasattr(self,'guid'):
            result += (
                f"guid = {self.guid}\n"
            )
        return result

    def print_files(self):
        self.file_db.print_files()

    @property
    def last_disc_num(self):
        return self.hash_db.last_disc_number

    def get_disc_info(self, disc_num):
        """Returns summary information on a single disc"""
        return self.hash_db.get_info(disc_num)

    def get_all_disc_info(self):
        """Returns summary information on all discs"""
        result = ''
        for i in range(self.last_disc_num):
            result += self.get_disc_info(i)
        return result


