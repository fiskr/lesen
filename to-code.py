
import sys
import argparse


# get the arguments from the command line
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="lesen source file to be converted to code")

parser.add_argument("-s", "--sourcetype", help="the type of source file to export to")

parser.add_argument("-n", "--blockname", help="the top level code block to export to the source file")

args = parser.parse_args()

if args.blockname is not None:
    MasterBlockName = args.blockname
else:
    MasterBlockName = "*"

if args.filename is not None:
    fileName = args.filename

Mode = 'document'

# blindly going to use a dictionary to store the  code chunks
# this might need to be changed later

codeChunks = {}

if fileName is not None:
    file = open(fileName)

    for line in file:
        if (line[0] == '<') and (line[1] == '<'):

    file.close()
