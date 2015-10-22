

fileName = 'example.lsn'
mode = 'document' # document or code


file = open(fileName)

for line in file:
    print line
    if (line[0] == '@'):
        mode = 'document'

file.close()
