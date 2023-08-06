import re


def csv_repair(infile, outfile):
    with open(infile, 'r') as csv:
        with open(outfile, 'w') as new:
            for line in csv:
                if line.endswith('...\n'):
                    line = re.sub(';\.*', '', line)
                    print(line.split(';'))
                new.write(line)


filename = '/home/john/Desktop/box005_update_2018_MINUS_ISSUE.csv'
repair = '/home/john/Desktop/box005_update_2018_MINUS_ISSUE_repair.csv'

csv_repair(filename, repair)
