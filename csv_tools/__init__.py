#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import six

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"


class CSVToolsReader(six.Iterator):
    """
    A wrapper around Python 3's builtin :func:`csv.reader`.
    """

    def __init__(self, f, **kwargs):
        self.reader = csv.reader(f, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.reader)

    @property
    def dialect(self):
        return self.reader.dialect

    @property
    def line_num(self):
        return self.reader.line_num


class CSVToolsWriter(object):
    """
    A wrapper around Python 3's builtin :func:`csv.writer`.
    """

    def __init__(self, f, line_numbers=False, **kwargs):
        self.row_count = 0
        self.line_numbers = line_numbers

        if 'lineterminator' not in kwargs:
            kwargs['lineterminator'] = '\n'

        self.writer = csv.writer(f, **kwargs)

    def _append_line_number(self, row):
        if self.row_count == 0:
            row.insert(0, 'line_number')
        else:
            row.insert(0, self.row_count)

        self.row_count += 1

    def writerow(self, row):
        if self.line_numbers:
            row = list(row)
            self._append_line_number(row)

        # Convert embedded Mac line endings to unix style line endings so they get quoted
        row = [i.replace('\r', '\n') if isinstance(i, six.string_types) else i for i in row]

        self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writer.writerow(row)


class CSVToolsDictReader(csv.DictReader):
    """
    A wrapper around Python 3's builtin :class:`csv.DictReader`.
    """
    pass


class CSVToolsDictWriter(csv.DictWriter):
    """
    A wrapper around Python 3's builtin :class:`csv.DictWriter`.
    """

    def __init__(self, f, fieldnames, line_numbers=False, **kwargs):
        self.row_count = 0
        self.line_numbers = line_numbers

        if 'lineterminator' not in kwargs:
            kwargs['lineterminator'] = '\n'

        csv.DictWriter.__init__(self, f, fieldnames, **kwargs)

    def _append_line_number(self, row):
        if self.row_count == 0:
            row['line_number'] = 0
        else:
            row['line_number'] = self.row_count

        self.row_count += 1

    def writerow(self, row):
        if self.line_numbers:
            row = list(row)
            self._append_line_number(row)

        # Convert embedded Mac line endings to unix style line endings so they get quoted
        row = dict([(k, v.replace('\r', '\n')) if isinstance(v, six.string_types) else (k, v) for k, v in row.items()])

        csv.DictWriter.writerow(self, row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def reader(*args, **kwargs):
    """
    A drop-in replacement for Python's :func:`csv.reader`.t
    """
    return CSVToolsReader(*args, **kwargs)


def writer(*args, **kwargs):
    """
    A drop-in replacement for Python's :func:`csv.writer`.
    """
    return CSVToolsWriter(*args, **kwargs)
