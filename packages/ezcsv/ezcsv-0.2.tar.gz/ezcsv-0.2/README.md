# EZCSV

Some utility functions to do the obvious things you want to do with CSV files.

`csv` is easy, this is EZ.

Install it: `pip install ezcsv`

Should be compatible with Python 2.5+ and 3.x

I say "should be" because there are no tests! Please see 'Contributing', below.


## Reference

#### `read_dicts(file_path)`

Returns the data at `file_path` as a list of dicts.

- **`file_path`** `string | Path`

#### `read_lists(file_path)`

Returns the data at `file_path` as a list of lists. Ignores blank lines.

- **`file_path`** `string | Path`
   
Example Usage:
```
>>> from easycsv import csv_as_list
>>> filepath = 'C:\\path\\to\\file.csv'
>>> print(filepath)
C:\path\to\file.csv
>>> l = csv_as_list(filepath)
>>> print(l[0])
First,Line,Of,File,Prints,Here
```

#### `write_dicts(data, csv_path, mkdir=False, silent_fail=False)`

Writes the input data to a CSV file

Always produces a Unix-style CSV file, regardless of whether on
Windows or not.

- **`data`** `list[dict]`

   One dict per line. The first dict is expected to contain all of the
keys that will form the header line, unless `fieldnames` is provided.
- **`csv_path`** `string | Path`

   Should have a .csv extension. `mkdir` will malfunction if it doesn't.
- **`mkdir`** `bool`

   If true, creates the directory tree leading up to `csv_path`, ignoring
if directories already exist. Default: `False`
- **`silent_fail`**: `bool`

    If `true`, causes the method to do nothing if `data` happens
to be empty. Default: `False`
- **`fieldnames`**: `list[str]`

    If set, provides the list of field names to be passed to `csv.DictWriter`.
These are written as the header, regardless of what keys are present in
the first dict in `data`. Default: `None`
    

#### `write_lists(data, csv_path, mkdir=False)`

Writes the input data to a CSV file

Always produces a Unix-style CSV file, regardless of whether on
Windows or not.

- **`data`** `list[list]`

   - **`csv_path`** `string | Path`

Should have a .csv extension. `mkdir` will malfunction if it doesn't.
- **`mkdir`** `bool`

   If true, creates the directory tree leading up to `csv_path`, ignoring
if directories already exist.


## Contributing

This could really use some tests!

Feel free to fork and open a pull request. Please, one pull request per
functional change.

