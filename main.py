import argparse
import csv
from apriori import *

def read(datafile):
    transactions = []

    with open(datafile, 'r') as data:
        transactions = list(csv.reader(data))
    return transactions


def main():
    """
    Main (Controller) function responsible for executing the project.
    """

    # Parsing the argument parameters
    parser = argparse.ArgumentParser(description='Key arguments')
    parser.add_argument('datafile', type=str)
    parser.add_argument('min_sup', type=float)
    parser.add_argument('min_conf', type=float)

    args = parser.parse_args()

    datafile = args.datafile
    min_sup = args.min_sup
    min_conf = args.min_conf

    transactions = read(datafile)

    rules = apriori_algorithm(transactions, min_sup, min_conf)

    return rules



if __name__ == '__main__':
    main()