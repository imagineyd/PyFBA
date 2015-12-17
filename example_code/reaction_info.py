import argparse
import os
import sys
import PyFBA
__author__ = 'Rob Edwards'

parser = argparse.ArgumentParser(description='Print information about a reaction')
parser.add_argument('-r', help='reaction(s) to print information about', action='append', required=True)
args = parser.parse_args()

compounds, reactions, enzymes = PyFBA.parse.compounds_reactions_enzymes('gramnegative')

for r in args.r:
    print("{}: {}".format(r, reactions[r].equation))