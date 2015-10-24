
import sys
import re
import argparse

# Global Vars
CodeBlockName = ""
EndCode = ""
Header = ""
Footer = ""
DocType = None
# start in document Mode
Mode = 'document' # document or code
Choices = ['tex', 'md']

# get the arguments from the command line
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="lesen source file to be converted to documentation or code")

parser.add_argument("-t", "--doctype", help="the type of document to export to",
                        choices=Choices)

args = parser.parse_args()



if args.filename is not None:
    fileName = args.filename
else:
    fileName = None

if fileName is not None:
    # TODO: check extension to see what type, accept overrides, and write up a default to do minimal
    for typeChoice in Choices:
        if re.match('.*\.' + typeChoice + '.*', fileName):
            DocType = typeChoice

if args.doctype is not None:
    DocType = args.doctype
else:
    if DocType is None:
        DocType = 'default'




if (DocType == 'tex'):
    Header = """\\documentclass{article}
\\usepackage{listings}
\\usepackage{color}
\\usepackage{xcolor}
\\usepackage{caption}
\\DeclareCaptionFont{white}{\\color{white}}
\\DeclareCaptionFormat{listing}{\\colorbox{gray}{\\parbox{\\textwidth}{#1#2#3}}}
\\captionsetup[lstlisting]{format=listing,labelfont=white,textfont=white}

\\begin{document}"""
    def startCode(codeBlockName):
        label = codeBlockName.lower()
        label = label.replace(' ', '-')
        return '\\noindent\\begin{lstlisting}[label=' + label + ',caption=' + codeBlockName + ']'

    Footer = '\\end{document}' # ends the document

    EndCode = '\\end{lstlisting}'
    print(Header)

elif (DocType == 'md'):
    MarkDownHeadingLevel = 1
    def startCode(codeBlockName):
        heading = '#' * (MarkDownHeadingLevel + 1)
        return heading + codeBlockName + '\n'

    # ``` oriented markdown, Github's flavor
    # def startCode(codeBlockName):
    #     heading = '#' * (MarkDownHeadingLevel + 1)
    #     return heading + codeBlockName + '\n```'
    # EndCode = '```'

elif (DocType == 'default'):
    def startCode(codeBlockName):
        return '<<' + codeBlockName + '>>='

def iterateMarkdownHeadingLevel(start, line):
     MarkDownHeadingLevel = 1
     for i in range(start, len(line)):
         if (line[i] != '#'):
             return MarkDownHeadingLevel
         else:
             MarkDownHeadingLevel += 1

def processLine(line):
    global Mode
    global CodeBlockName
    global DocType
    global startCode
    if (line[0] == '@'): # if document block starts
        if (Mode == 'code'):
            sys.stdout.write(EndCode) # if latex, end code block formatting
        elif (DocType == 'md') and (Mode == 'document') and (line[1] == '#'):
            MarkDownHeadingLevel = iterateMarkdownHeadingLevel(2, line)
        sys.stdout.write(line[1:])
        Mode = 'document'
    elif (line[0] == '<') and (line[1] == '<'):
        previousCodeBlockName = CodeBlockName # backup the code block name
        CodeBlockName = ""

        for i in range(2,len(line)): # parse out the name of the code chunk
            if (line[i] == '>'): # check to see if it's the end of the name chunk
                i += 1
                if (line[i] == '>'): # it's either a reference or an addition to code chunk
                    i += 1
                    if (line[i] == '='): # it's an addition
                        Mode = 'code'
                        print(startCode(CodeBlockName))
                        break
                    else: # does not end in =, it's just a reference
                        if (DocType == 'md') and (Mode == 'code'):
                          sys.stdout.write('    ' + line)
                        else:
                          sys.stdout.write(line)
                        referenceCodeBlockName = CodeBlockName # save the reference code-block name as such
                        CodeBlockName = previousCodeBlockName # set the code-block name back to what it was
                        break
                else: # does not have second > of >>
                    CodeBlockName += line[i]
            else: # does not have second > of >>
                CodeBlockName += line[i]


    else: # does not start with << or @
            if (line[0] == '#') and (DocType == 'md'):
                MarkDownHeadingLevel = iterateMarkdownHeadingLevel(1, line)
            if (DocType == 'md') and (Mode == 'code'):
              sys.stdout.write('    ' + line)
            else:
              sys.stdout.write(line)


if fileName is not None:
    file = open(fileName)
    for line in file:
        processLine(line)
    file.close()
else:
    for line in sys.stdin:
        processLine(line)

if(Mode == 'code'):
    print(EndCode)

sys.stdout.write(Footer)
