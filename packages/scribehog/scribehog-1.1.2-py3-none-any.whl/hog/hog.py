#!/usr/bin/env python3
from sys import stderr

from hog.utils.args import parse_args
from hog.utils.get_filenames import get_filenames
from hog.utils.get_logcategory import list_logcategories, get_logcategory
from hog.utils.print_logs import print_logs


def main() -> None:
    args = parse_args()
    if args.is_verbose:
        print("---hog logcategory specifier: {}".format(args.logcategory), file=stderr)
        print("---hog interval specifier: {}".format(args.interval), file=stderr)
    logcategories = list_logcategories()
    logcategory = get_logcategory(query=args.logcategory, logcategories=logcategories)
    if args.is_verbose:
        print("---hog logcategory: {}".format(logcategory), file=stderr)
    filenames = get_filenames(logcategory=logcategory, interval=args.interval)
    if args.is_verbose:
        print("---hog filenames:", file=stderr)
        for filename in filenames:
            print(filename, file=stderr)
        print("---hog file contents:", file=stderr)
    print_logs(logcategory, filenames)


if __name__ == "__main__":
    main()
