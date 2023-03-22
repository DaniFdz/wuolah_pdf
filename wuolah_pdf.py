#! /usr/bin/env python3
# coding: utf-8
"""

"""

import os
import argparse

from colorama import Fore

from PyPDF2 import PdfFileReader, PdfFileWriter

def get_parser():
    parser = argparse.ArgumentParser(
        description="This program will merge the pdf files that you pass as arguments into one file and will remove the ads from the pdf if you want to",
        epilog="This program was made by @DaniFdz",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-o", "--output", help="Output file name, if not specified it will be the name of the first file with _merged.pdf at the end", required=False)
    parser.add_argument("-r", "--remove-ads", help="Remove the ads from the pdf", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose mode, show more info about the process", action="store_true")
    parser.add_argument("-l", "--log", help="File to save the logs of the operations", action="store_true")
    parser.add_argument("input", help="Input file", nargs="+")

    return parser

def check_args(args):
    if args.verbose:
        print(f"{Fore.CYAN}[V]{Fore.RESET} Checking if the output file exists...")

    if args.output is None:
        args.output = "".join(args.input[0].split(".")[:-1]) + "_merged.pdf"

    if os.path.exists(args.output):
        if(input("The file {} already exists, do you want to overwrite it? [y/N]: "
                 .format(args.output)).lower() != "y"):
            print("\nOperation cancelled by the user")
            print(Fore.RED + "\tExiting..." + Fore.RESET)
            exit(1)

    for file in args.input:
        if args.verbose:
            print(f"{Fore.CYAN}[V]{Fore.RESET} Checking if the file {file} exists...")
        if not os.path.exists(file):
            print(f"\nThe file {Fore.YELLOW}{file}{Fore.RESET} does not exist")
            print(Fore.RED + "\tExiting..." + Fore.RESET)
            exit(1)

def main():
    parser = get_parser()

    args = parser.parse_args()

    check_args(args)
     

if __name__ == "__main__":
    main()