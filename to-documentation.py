
import sys
import re
import argparse

# Global Vars
CodeBlockName = ""
EndCode = ""
Header = ""
Footer = ""
# start in document Mode
Mode = 'document' # document or code

# get the arguments from the command line
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="lesen source file to be converted to documentation or code")

parser.add_argument("-d", "--doctype", help="the type of document to export to",
                        choices=['tex', 'md'])

args = parser.parse_args()

if args.filename is not None:
    fileName = args.filename
else:
    fileName = 'example.lsn'

markdownPattern = re.compile(".md")
latexPattern = re.compile(".tex")

# TODO: check extension to see what type, accept overrides, and write up a default to do minimal
if latexPattern.match(fileName):
    docType = 'tex'
elif markdownPattern.match(fileName):
    docType = 'md'

if args.doctype is not None:
    if (args.doctype == 'tex') or (args.doctype == 'md'):
        docType = args.doctype
    else:
        sys.exit('Error! Doctype of ' + args.doctype + ' is not known.')
else:
    docType = 'default'



if (docType == 'tex'):
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

elif (docType == 'md'):
    MarkDownHeadingLevel = 1
    def startCode(codeBlockName):
        heading = '#' * (MarkDownHeadingLevel + 1)
        return heading + codeBlockName + '\n'

    # ``` oriented markdown, Github's flavor
    # def startCode(codeBlockName):
    #     heading = '#' * (MarkDownHeadingLevel + 1)
    #     return heading + codeBlockName + '\n```'
    # EndCode = '```'

elif (docType == 'default'):
    def startCode(codeBlockName):
        return '<<' + codeBlockName + '>>='

def iterateMarkdownHeadingLevel(start, line):
     MarkDownHeadingLevel = 1
     for i in range(start, len(line)):
         if (line[i] != '#'):
             return MarkDownHeadingLevel
         else:
             MarkDownHeadingLevel += 1


if fileName is not None:
    file = open(fileName)

    for line in file:
        if (line[0] == '@'): # if document block starts
            if (Mode == 'code'):
                sys.stdout.write(EndCode) # if latex, end code block formatting
            elif (docType == 'md') and (Mode == 'document') and (line[1] == '#'):
                MarkDownHeadingLevel = iterateMarkdownHeadingLevel(2, line)
            sys.stdout.write(line[1:])
            Mode = 'document'
        elif (line[0] == '<') and (line[1] == '<'):
            previousCodeBlockName = CodeBlockName # backup the code block name
            CodeBlockName = ""

            for i in range(2,len(line)): # parse out the name of the code chunk
                #print 'i: ' + str(i)
                if (line[i] == '>'): # check to see if it's the end of the name chunk
                    i += 1
                    if (line[i] == '>'): # it's either a reference or an addition to code chunk
                        i += 1
                        # print 'DEBUG: >> i: ' + str(i)
                        if (line[i] == '='): # it's an addition
                            Mode = 'code'
                            print(startCode(CodeBlockName))
                            #sys.stdout.write(line)
                            # print 'DEBUG: >>= i: ' + str(i)
                            # new code block definition
                            # print 'DEBUG: new code block: ' + CodeBlockName
                            break
                        else: # does not end in =, it's just a reference
                            if (docType == 'md') and (Mode == 'code'):
                              sys.stdout.write('    ' + line)
                            else:
                              sys.stdout.write(line)
                            referenceCodeBlockName = CodeBlockName # save the reference code-block name as such
                            CodeBlockName = previousCodeBlockName # set the code-block name back to what it was
                            # print 'DEBUG: >> not = i: ' + str(i)
                            # print 'DEBUG: embed code'
                            break
                    else: # does not have second > of >>
                        CodeBlockName += line[i]
                else: # does not have second > of >>
                    CodeBlockName += line[i]


        else: # does not start with << or @
                if (line[0] == '#') and (docType == 'md'):
                    MarkDownHeadingLevel = iterateMarkdownHeadingLevel(1, line)
                if (docType == 'md') and (Mode == 'code'):
                  sys.stdout.write('    ' + line)
                else:
                  sys.stdout.write(line)
                # print 'DEBUG: ' + Mode
    file.close()


if(Mode == 'code'):
    print(EndCode)

sys.stdout.write(Footer)
