##############################################################
## Program takes in search location and outputs location of ##
## all the files matching the search string a csv file.     ## 
##############################################################
import argparse
import os
from pathlib import Path
import sys
import csv

def main():
    #set of input arguments
    replace_file = False
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--in_folder', default=os.getcwd(),
                        help='Specify the full input search folder')
    parser.add_argument('-o','--o_file', required=True,
                        help='Specify the full output file location')
    #default search string is set such that
    #output will contain all files in the given input dir 
    parser.add_argument('-p','--pattern', default='**/*',
                        help='Specify the search pattern')
    
    #error checks
    args = parser.parse_args()
    if Path(args.o_file).exists():
        if Path(args.o_file).is_file():
            if os.access(str(args.o_file),os.W_OK):
                pass
            else:
                #error for no write access
                print('Dont have write access for the output file')
        else:
            #error for wrong output file
            sys.stdout.write('Output File specified is a directory, please specify a file')
            quit()

    #error for incorrect outout file format
    if Path(args.o_file).suffix != '.csv':
        print('Output file should csv file')
        quit()
    
    #calling function to get all the paths
    getPaths(args)


def getPaths(args):
    inp = args.in_folder
    opf = args.o_file
    pat = args.pattern

    paths = []
    filename = []
    sizes = []
    write_access = []
    read_access = []

    #using glob to navigate through the folders
    for path in Path(inp).glob(pat):
        paths.append(str(path))
        filename.append(path.name)
        sizes.append(os.stat(str(path)).st_size)
        write_access.append(str(os.access(str(path),os.W_OK)))
        read_access.append(str(os.access(str(path),os.R_OK)))
    
    #write file location in a csv folder
    with open(opf,'w') as f:
        fieldnames = ['filePath','filename','Size','ReadAccess','WriteAccess']
        csv_writer = csv.DictWriter(f,fieldnames=fieldnames,delimiter=',')

        csv_writer.writeheader()

        for i in range(len(paths)):
            csv_writer.writerow({'filePath':paths[i],'filename':filename[i],'Size':sizes[i],
                        'ReadAccess': read_access[i],'WriteAccess':write_access[i]})

if __name__ == '__main__':
    main()
