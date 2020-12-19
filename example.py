"""
Example for the use of `csvloader`.
"""

import csvloader

with open('example-data.csv') as f:
    for row in csvloader.load(f):
        print(row)
