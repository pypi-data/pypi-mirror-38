# Compare all spreadsheets in directory to each other
# Derek Fujimoto
# Nov 2018

import compsheet.multifile_comparer as mc
import os, argparse

# run if main
if __name__ == '__main__':
    
    # set up argument parser
    parser = argparse.ArgumentParser(description='Run a pairwise comparison '+\
        'of all spreadsheets on target PATH. Look for pairs with common'+\
        ' features indicative of plagiarism.')

    # directory
    parser.add_argument("PATH",
                        help='evaluate spreadsheets found on PATH',
                        action='store',
                        default='.',
                        nargs="?")

    # dry-run don't save spreadsheet
    parser.add_argument("-d", "--dry",
                        help="Dry run, don't write to speadsheet",
                        dest='dry',
                        action='store_true',
                        default=False)

    # explain headers
    parser.add_argument("--explain",
                        help='Print calculation methodology of table values',
                        dest='explain',
                        action='store_true',
                        default=False)

    # log
    parser.add_argument("-l", "--log",
                        help='write print out table to text file',
                        dest='logfile',
                        action='store',
                        default='')
    
    # options
    opt_help="comma-separated list of items to compare "+\
             "(possible: 'meta,exact,string,geo')"
                    
    parser.add_argument("-o", "--options",
                        help=opt_help,
                        dest='options',
                        action='store',
                        default='meta')
    
    # print lines
    parser.add_argument("-f", "--full",
                        help='Print full detailed summary of each comparison',
                        dest='full',
                        action='store_true',
                        default=False)
    
    # print table
    parser.add_argument("-t", "--table",
                        help='Print summary table of all comparisons',
                        dest='table',
                        action='store_true',
                        default=False)
    
    # verbose mode
    parser.add_argument("-v", "--verbose",
                        help='Print output to stdout',
                        dest='verbose',
                        action='store_true',
                        default=False)
    
    # save as spreadsheet
    parser.add_argument("-s", "--save",
                        help='write printout to xlsx file',
                        dest='savefile',
                        action='store',
                        default='')

    # number of processors
    parser.add_argument("-n", "--nproc",
                        help='choose number of processors',
                        dest='nproc',
                        action='store',
                        default=1)
    
    # parse
    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # Set up and run comparison
    if args.explain:
        print(mc.explanation)
    
    else:
        c = mc.multifile_comparer(args.PATH,int(args.nproc))
        c.compare(options=args.options,do_print=args.full,do_verbose=args.verbose)
        
        if args.table:
            c.print_table(filename=args.logfile)
            
        if not args.dry:
            c.print_spreadsheet(filename=args.savefile)
