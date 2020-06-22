# comparesc
### CSV Comparison on steriods 

## Usage

```console
comparesv [-h] [-v] [--enc1 ENCODING] [--enc2 ENCODING] [-i]
              [-rm ROW_MATCH] [-cm COLUMN_MATCH] [-sm STRING_MATCH] [-ir]
              [-ic] [-is] [-s]
              [FILE1] [FILE2]

CSV files comparison

positional arguments:
  FILE1                 the first CSV file
  FILE2                 the second CSV file

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --enc1 ENCODING       encoding of the first file (default is to autodetect)
  --enc2 ENCODING       encoding of the second file (default is to autodetect)
  -i, --ignore-case     ignore case (default is case-sensitive)
  -rm ROW_MATCH, --row-match ROW_MATCH
                        Logic to be used to identify the rows. Possible
                        options 'order', 'fuzzy', 'deep' (default is order)
  -cm COLUMN_MATCH, --column-match COLUMN_MATCH
                        Logic to be used to identify the columns. Possible
                        options 'exact','fuzzy' (default is exact)
  -sm STRING_MATCH, --string-match STRING_MATCH
                        Logic to be used to identify the columns. Possible
                        options 'exact','fuzzy' (default is exact)
  -ir, --include-addnl-rows
                        Include added additional added rows from second file
                        (default is false)
  -ic, --include-addnl-columns
                        Include added additional columns from second file
                        (default is false)
  -is, --include-stats  Include stats (default is false)
  -s, --save-output     Save output to file
```

## Description



