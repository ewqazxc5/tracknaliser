from argparse import ArgumentParser
from .tracknaliser import greentrack

def process():
    parser = ArgumentParser(description="Request generated tracks")

    parser.add_argument('--start', '-S', type=str, metavar ='', nargs='+', required= True, help ='Start coordinates as x y seperated by space')
    parser.add_argument('--end', '-E', type=str, metavar ='', nargs='+', required= True, help ='End coordinates as x y seperated by space')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-b', '--simple', action='store_true', help ='print simple/basic')
    group.add_argument('-v', '--verbose', action='store_true', help ='print verbose')

    arguments = parser.parse_args()

    greentrack_output = greentrack(arguments.start, arguments.end, arguments.verbose)
    print(greentrack_output)

if __name__ == "__main__":

    process()


    