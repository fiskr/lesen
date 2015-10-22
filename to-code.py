
import sys
import argparse


# get the arguments from the command line
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="lesen source file to be converted to code")

parser.add_argument("-s", "--sourcetype", help="the type of source file to export to")

args = parser.parse_args()
