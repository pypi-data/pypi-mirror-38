# Compare Microsoft Spreadsheet Files

Look for instances of plagiarism. 

* Compare file meta data
    * File creation time stamp
    * File modification time stamp
    * Author of file creation 
    * Author of last modification of file
* Cell values
    * Non-formula strings
    * Cell-by-cell values
* Cell layout
    * Check locations of filled/unfilled cells

Spreadsheet files must be of type `.xlsx`

# Installation and Setup

To install run `pip install --user compsheet` from the terminal. 

To run type 

```bash
python3 -m compsheet
```

followed by the various inputs and flags. It is recommended that the user establish the alias `compsheet` for easy usage. 
To do this, edit the file `.bashrc` from the home directory and add the line 

```bash
alias compsheet='python3 -m compsheet'
```

to the end. One can do this in their favourite editor or simply open a terminal and type 

```bash
echo "alias compsheet='python3 -m compsheet'" >> .bashrc
```
into the prompt and press enter. 

# Some basic examples of usage:

```bash
python3 -m compsheet    # show help message with no alias
compsheet -h            # show help message
compsheet               # compare all files in current directory
compsheet ./dirname     # compare all files in directory 'dirname'
compsheet -d ./dirname  # do a dry run: write no files. 
compsheet --explain     # print description of table headers
```
