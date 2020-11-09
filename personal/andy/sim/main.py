import sys

def print_word(args):
    for a in args:
        print(a)


def main(argv):
    if len(argv) < 2:
        print(sys.stderr, 'Usage: python main.py <arg1> <arg2>')
        sys.exit(1)
    # loops over all .json files in the argument
    print_word(argv[1:])

    print("Success generating plot")


if __name__ == '__main__':
    main(sys.argv)
