"""
Provides functions for loading CSV files.
"""

from collections import namedtuple
from csv import reader

def load(csvfile, delimiter=',', usebuiltin=True, **kwargs):
    """
    Iterable for loading CSV files.

    :param csvfile: file-like object that represents
        the underlying CSV file
    :param delimiter: character used to split the line
    :param kwargs: key-value pairs to be handed to the
        underlying csv.reader function
    :param usebuiltin: determines whether to use
        csv.reader or String.split (simplier, less robust)
        to underly the file parsing

    :raises ValueError: when a line is not parsable

    usage::
        > with open('example-data.csv') as f:
        >     for row in csvloader.load(f):
        >         pass # do your stuff here
    """
    if usebuiltin:
        csvreader = reader(csvfile, delimiter=delimiter, **kwargs)
        header = next(csvreader)
        csvrow = namedtuple('csvrow', header)
        for lineno, line in enumerate(csvreader):
            try:
                yield csvrow(*line)
            except:
                raise ValueError({
                    'header':header,
                    'line':line,
                    # account for header line
                    # and Natural over Whole numbering
                    'lineno':lineno + 2
                })
    else:
        header = csvfile.readline().strip().split(delimiter)
        csvrow = namedtuple('csvrow', header)
        for lineno, line in enumerate(csvfile.readlines()):
            line = line.strip().split(delimiter)
            try:
                yield csvrow(*line)
            except:
                raise ValueError({
                    'header':header,
                    'line':line,
                    # account for header line
                    # and Natural over Whole numbering
                    'lineno':lineno + 2
                })

def loadall(csvfile, delimiter=',', usebuiltin=True, **kwargs):
    """
    Loads the whole file into memory

    :param csvfile: file-like object that represents
        the underlying CSV file
    :param delimiter: character used to split the line
    :param kwargs: key-value pairs to be handed to the
        underlying csv.reader function

    usage::
        > with open('example-data.csv') as f:
        >     data = csvloader.loadall(f)
        > pass # do your stuff here with `data`
    """
    return [
        row
        for row
        in load(csvfile, delimiter, **kwargs, usebuiltin=usebuiltin)
    ]
