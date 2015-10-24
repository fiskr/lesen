
import sys
import re
import argparse
from pprint import pprint # take this out before releasing - this is for tests

# get the arguments from the command line
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="lesen source file to be converted to code")

parser.add_argument("-n", "--blockname", help="the top level code block to export to the source file")

args = parser.parse_args()

if args.blockname is not None:
    MasterBlockName = args.blockname
else:
    MasterBlockName = "*"

if args.filename is not None:
    fileName = args.filename

# Global vars
CodeBlockName = ''
Mode = 'document'

# blindly going to use a dictionary to store the  code chunks
# this might need to be changed later

codeChunks = {}

if fileName is not None:
    file = open(fileName)

    for line in file: # run through the document once to setup the code chunks
        if (line[0] == '@'):
            Mode = 'document'
        if (line[0] == '<') and (line[1] == '<'):
            previousCodeBlockName = CodeBlockName # backup the code block name
            CodeBlockName = ""

            for i in range(2,len(line)): # parse out the name of the code chunk
                if (line[i] == '>'): # check to see if it's the end of the name chunk
                    i += 1
                    if (line[i] == '>'): # it's either a reference or an addition to code chunk
                        i += 1
                        if (line[i] == '='): # it's an addition
                            Mode = 'code'
                            if CodeBlockName not in codeChunks:
                                codeChunks[CodeBlockName] = []
                            break
                        else: # does not end in =, it's just a reference
                            referenceCodeBlockName = CodeBlockName # save the reference code-block name as such
                            CodeBlockName = previousCodeBlockName # set the code-block name back to what it was
                            codeChunks[CodeBlockName].append(line)
                            break
                    else: # does not have second > of >>
                        CodeBlockName += line[i]
                else: # does not have second > of >>
                    CodeBlockName += line[i]


        else: # does not start with << or @
            if (Mode == 'code') and (CodeBlockName is not None) and (CodeBlockName != ''):
                codeChunks[CodeBlockName].append(line)

    def processChunk(codeChunkName):
        for chunk in codeChunks[codeChunkName]:
            codeChunkMatches = re.match('^.*<<([^>]+)>>.*$', chunk)
            surroundingMatches = re.match('^(.*?)<<[^>]+>>(.*)$', chunk)
            if codeChunkMatches is not None:
                codeChunkReferenceNames = codeChunkMatches.groups() # even though it's "names", you should expect only one group - use item [0]
                referencePadding = surroundingMatches.groups()
                if (codeChunkReferenceNames is not None) and (len(codeChunkReferenceNames) > 0):
                    processChunk(codeChunkReferenceNames[0])
            else:
                sys.stdout.write(chunk)

    processChunk(MasterBlockName)

    file.close()

# codeChunks
# pprint(codeChunks)
