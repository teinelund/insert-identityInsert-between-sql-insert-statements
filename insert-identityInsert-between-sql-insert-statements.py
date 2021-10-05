#!/usr/bin/env python3


import sys, getopt
import re
import os

def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = False
    arguments = len(sys.argv) - 1

    #
    # Parse options

    try:
        opts, args = getopt.getopt(argv,"hvVi:o:",["help", "version", "verbose", "input=", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for (opt, value) in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-v', '--version'):
            print('insert-identityInsert-between-sql-insert-statements.py version 1.0.0 - 2021 Henrik Teinelund.', end='\n')
            sys.exit()
        elif opt in ('-V', '--verbose'):
            verbose = True
        elif opt in ('-i', '--input'):
            inputfile = value
        elif opt in ('-o', '--output'):
            outputfile = value

    #
    # Parse options
    if inputfile == '':
        print('[ERROR] Option --input is mandatory. Type --help to display help page.', end='\n')
        sys.exit(1)
    if not os.path.exists(inputfile):
        print('[ERROR] input file "' + inputfile + '" does not exist. Check spelling.', end='\n')
        sys.exit(1)
    if not os.path.isfile(inputfile):
        print('[ERROR] input file is not a regular file. Check spelling.', end='\n')
        sys.exit(1)
    if outputfile == '':
        outputfile = inputfile
    if os.path.isdir(outputfile):
        print('[ERROR] output file is a folder. Not allowed. Check spelling.', end='\n')
        sys.exit(1)

    if verbose:
        print('Verbose output is enabled.', end='\n')
    
    if os.path.exists(outputfile):
        print('[WARNING] output file does exist. File content will be overwritten.', end='\n')

    set_identity_insert = 'set identity_insert '
    current_table = ''
    table_line_above = ''
    pattern = '^INSERT\s+INTO\s+dbo.(\w+)\s*\W.*$'
    output_content = []

    #
    # Open and read input file. Line by line
    # process the content. Place 'set identity insert'
    # between different table insert blocks.
    with open(inputfile, 'r', encoding='UTF-8') as file:
        for line in file:
            
            match = re.search(pattern, line.rstrip())
            if match:
                current_table = match.group(1)

            if table_line_above == '':
                output_content.append(set_identity_insert + current_table + " on;")
            elif table_line_above != '' and table_line_above != current_table:
                output_content.append(set_identity_insert + table_line_above + " off;")
                output_content.append('')
                output_content.append(set_identity_insert + current_table + " on;")
            
            output_content.append(line.rstrip())
            table_line_above = current_table;
        
        output_content.append(set_identity_insert + table_line_above + " off;")

    if verbose:
        print('[VERBOSE] Output content:', end='\n')
        print(output_content, end='\n')
    
    #
    # Read list, line by line, and write content to file.
    with open(outputfile, mode='wt', encoding='utf-8') as ofile:
        for line in output_content:
            print(line, file = ofile)
    ofile.close

    print('[INFO] Output file "' + outputfile + '" written.', end='\n')

def usage():
    print('This command takes an input file (containing SQL insert statements) and inserts', end='\n')
    print('"set identity_insert TABLE on/off" between SQL inserts blocks.', end='\n')
    print('', end='\n')
    print('Syntax:', end='\n')
    print('insert-identityInsert-between-sql-insert-statements [OPTIONS]', end='\n')
    print('Options: --help | --version | [--verbose] --input FILE [--output FILE]', end='\n')
    print('', end='\n')
    print('-i --input FILE                 File to read (containing SQL insert statements). Mandatory.', end='\n')
    print('-o --output FILE                File to write. Optional. If omitted, input file will be overwritten.', end='\n')
    print('-h --help                       Display this output.', end='\n')
    print('-v --version                    Display application version.', end='\n')
    print('-V --verbose                    Verbose output enabled.', end='\n')
    sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
