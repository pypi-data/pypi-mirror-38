#!/usr/bin/env python3
from sys import stderr
from typing import List

from hog.utils.args import parse_args
from hog.utils.get_filenames import get_filenames
from hog.utils.get_logcategory import list_logcategories, get_logcategory
from hog.utils.print_logs import print_logs


def main() -> None:
    args = parse_args()
    if args.is_verbose:
        print(f"---hog logcategory specifier: {args.logcategory}", file=stderr)
        print(f"---hog interval specifier: {args.interval}", file=stderr)
    logcategories = list_logcategories()
    logcategory: str = get_logcategory(
        query=args.logcategory, logcategories=logcategories
    )
    if args.is_verbose:
        print(f"---hog logcategory: {logcategory}", file=stderr)
    filenames: List[str] = get_filenames(
        logcategory=logcategory, interval=args.interval
    )
    if args.is_verbose:
        print("---hog filenames:", file=stderr)
        for filename in filenames:
            print(filename, file=stderr)
        print("---hog file contents:", file=stderr)
    print_logs(logcategory, filenames)


if __name__ == "__main__":
    main()
