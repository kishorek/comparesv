# comparesv
### Python CSV Comparison on steriods 

## Installation

```console
pip install comparesv
```

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

## Examples

### Scenario 1: Simple direct comparison

|id |first   |last    |age|
|---|--------|--------|---|
|432|Roy     |Aguilar |46 |
|914|Janie   |Bowman  |24 |
|021|Grace   |Copeland|53 |
|708|Louise  |Franklin|25 |
|850|Gertrude|Carr    |60 |

vs

|id |first   |last    |age|
|---|--------|--------|---|
|432|Roy     |Aguilar |46 |
|914|Janie   |Bowman  |24 |
|021|Grace   |Copeland|53 |
|708|Louise  |Franklin|25 |
|850|Gertrude|Carr    |60 |

```console
comparesv file1 file2
```

Will provide:

|S.No|id      |first   |last|age |
|----|--------|--------|----|----|
|1   |True    |True    |True|True|
|2   |True    |True    |True|True|
|3   |True    |True    |True|True|
|4   |True    |True    |True|True|
|5   |True    |True    |True|True|

and

|S.No|id      |first   |last|age |
|----|--------|--------|----|----|
|1   |[432]:[432]|[Roy]:[Roy]|[Aguilar]:[Aguilar]|[46]:[46]|
|2   |[914]:[914]|[Janie]:[Janie]|[Bowman]:[Bowman]|[24]:[24]|
|3   |[021]:[021]|[Grace]:[Grace]|[Copeland]:[Copeland]|[53]:[53]|
|4   |[708]:[708]|[Louise]:[Louise]|[Franklin]:[Franklin]|[25]:[25]|
|5   |[850]:[850]|[Gertrude]:[Gertrude]|[Carr]:[Carr]|[60]:[60]|

---
### Scenario 2: Fuzzy column names

|id |first   |last    |age of student|
|---|--------|--------|--------------|
|432|Roy     |Aguilar |46            |
|914|Janie   |Bowman  |24            |

and 

|id |first   |last    |age|
|---|--------|--------|---|
|432|Roy     |Aguilar |46 |
|914|Janie   |Bowman  |24 |

```console
comparesv file1.csv file2.csv --column-match 'fuzzy'
```

will provide
|S.No|id      |first   |last|age |
|----|--------|--------|----|----|
|1   |True    |True    |True|True|
|2   |True    |True    |True|True|
---
### Scenario 3: Fuzzy row order - Differnt ordered textual data

|id |first   |last    |age|
|---|--------|--------|---|
|432|Roy     |Aguilar |46 |
|914|Janie   |Bowman  |24 |
|021|Grace   |Copeland|53 |

and

|id |first   |last    |age of student|
|---|--------|--------|--------------|
|021|Grace   |Copeland|53            |
|432|Roy     |Aguilar |46            |
|914|Janie   |Bowman  |24            |

```console
comparesv file1.csv file2.csv --column-match 'fuzzy' --row-match 'fuzzy'
```
will provide

|S.No|id      |first   |last|age |
|----|--------|--------|----|----|
|1   |True    |True    |True|True|
|2   |True    |True    |True|True|
|3   |True    |True    |True|True|
--- 
### Scenario 3: Deep row order - Different ordered numerical data

|year1|year2   |year3   |year|
|-----|--------|--------|----|
|751  |609     |590     |930 |
|417  |501     |441     |763 |
|691  |621     |941     |563 |
|179  |781     |335     |225 |
|961  |530     |433     |571 |

and

|year1|year2   |year3   |year|
|-----|--------|--------|----|
|961  |530     |433     |571 |
|751  |609     |590     |930 |
|691  |621     |941     |563 |
|179  |781     |335     |225 |
|417  |501     |441     |763 |

```console
comparesv file1.csv file2.csv --row-match 'deep'
```

|S.No|year1   |year2   |year3|year|
|----|--------|--------|-----|----|
|1   |True    |True    |True |True|
|2   |True    |True    |True |True|
|3   |True    |True    |True |True|
|4   |True    |True    |True |True|
|5   |True    |True    |True |True|

---
### Scenario n: Unlimited options. Please explore the options below
---
## Description

The first file is considered as the source file. It will be compared against the second file. Refer the below options to finetune the way it works.

### Row Match (-rm)

This will define the way how the rows between the files will be identified for comparison

`order` - This is the default option, This will compare the rows by their position between the files. This can be used if the records in both the files are in same order

`fuzzy` - This will use fuzzy logic to identify the matching row on second file. This can be used if the records are not in order and most of the data are **text**.

`deep` - This will use fuzzy logic to identify the matching row on second file. This can be used if the records are not in order and it has **numeric** data. This will look for each row in file1 against all the rows in file2 to find a potential match

### Column Match (-rm)

This will define the way how the columns between the files will be identified for comparison

`exact` - This is the default option, This will compare the columns between the files by their headers for an exact match and select it for comparison. eg. 'Age' and 'Age' columns across the files will be selected for comparison.

`fuzzy` - This will use fuzzy logic to identify the matching column on second file. This can be used if the column headers across the files are not exactly same by somehow closer. eg. 'age' and 'age of student' columns may be selected for comparison.

### String Match (-sm)

This will define the way how the textual data is compared.

`exact` - This is the default option, This will compare the exact text.

`fuzzy` - This will use fuzzy logic to find if the texts are closer to each other and identifies the match.

### Include Additional Rows (-ir)

If the second file contains more rows than the first file, this option will enable the comparison output to include the remaining rows (uncompared ones).

### Include Additional Columns (-ic)

If the second file contains more columns than the first file, this option will enable the comparison output to include the remaining columms.

### Ignore case (-i)

This option will ignore the case while comparing the strings.

### Include Stats (-is)

This option is enabled by default and it outputs the comparison stats (in percentage) on the console

### Save Output (-s)

This option will save the result & values comparison in the current directory. This is enabled by default.
