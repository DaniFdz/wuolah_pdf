#! /usr/bin/env python3
# coding: utf-8

import os
import argparse
import time

from colorama import Fore

from PyPDF2 import PdfReader, PdfWriter, errors

def get_parser() -> argparse.ArgumentParser:
    """
    This function will create the parser of the arguments that the program will receive
    This arguments are:
        -o, --output: The name of the output file, if not specified it will be the name of the first file with _merged.pdf at the end
        -r, --remove-ads: Remove the ads from the pdf
        -v, --verbose: Verbose mode, show more info about the process
        -l, --log: File to save the logs of the operations
        input: The input file
    :return: The parser of the arguments
    """
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
    """
    This function will check if the arguments are correct
    :param args: The arguments that the program received
    :return: None
    """
    if args.log:
        if args.verbose:
            print(f"{Fore.CYAN}[V]{Fore.RESET} Checking if the log file exists...")

        if not os.path.exists("./logs"):
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Creating the log directory...")
            os.makedirs("./logs")
            os.chmod("./logs", 0o777) # Give read, write and execute permissions to everyone

        log_file = open(f"./logs/log_{os.getpid()}.txt", "w")
        log_file.write(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] Log file created")
        log_file.close()
                

    if args.verbose:
        print(f"{Fore.CYAN}[V]{Fore.RESET} Checking if the output file exists...")

    if args.output is None:
        args.output = "".join(args.input[0].split(".")[:-1]) + "_merged.pdf"

    if os.path.exists(args.output):
        if(input("The file \"{}\" already exists, do you want to overwrite it? [y/N]: "
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
    """
    Main function of the program
    :return: None
    """
    parser = get_parser()

    args = parser.parse_args()

    check_args(args)
    
    try:
        if args.log:
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Opening the log file...")
            log_file = open(f"./logs/log_{os.getpid()}.txt", "a+")
            
        if args.log:
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Opening the log file...")
        if args.verbose:
            print(f"{Fore.CYAN}[V]{Fore.RESET} Opening the output file...")

        with open(args.output, 'wb') as f:
            f.write(b'')
            f.close()

        output_file = open(args.output, "wb")
        writer = PdfWriter(output_file)

        if args.verbose:
            print(f"{Fore.CYAN}[V]{Fore.RESET} Output file opened")
        if args.log:
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Output file opened")

        for file in args.input:
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Opening the input file \"{file}\"...")
            input_file = open(file, "rb")
            reader = PdfReader(input_file)
            if args.verbose:
                print(f"{Fore.GREEN}[i]{Fore.RESET} Number of pages in \"{file}\": {len(reader.pages)}")
            for page in reader.pages:
                if page.extract_text() != "":
                    writer.add_page(page)
            input_file.close()
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Pages from \"{file}\" added to the output file")
            if args.log:
                log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Pages from \"{file}\" added to the output file")
            
        if args.verbose:
            print(f"{Fore.CYAN}[V]{Fore.RESET} Closing the output file...")
        if args.log:
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Closing the output file")

        writer.write(output_file)
        output_file.close()

        if args.verbose:
            print(f"{Fore.CYAN}[V]{Fore.RESET} Output file closed")
        if args.log:
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Output file closed")

        if args.remove_ads:
            from gulagcleaner.gulagcleaner_extract import deembed
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Removing the ads from the output file...")
            if args.log:
                log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Removing the ads from the output file...")
            resp = deembed(args.output, True)
            if not resp["Success"]:
                print(f"{Fore.RED}Error:{Fore.RESET} {resp['Error']}")
                if args.log:
                    log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Closing the log file...")
                    log_file.close()
                exit(1)

        if args.log:
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Closing the log file...")
            log_file.close()
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Log file closed")

        print(f"\n{Fore.GREEN}Operation completed successfully{Fore.RESET}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by the user")
        print(Fore.RED + "\tExiting..." + Fore.RESET)
        if args.log:
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Closing the log file...")
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Operation cancelled by the user")
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Closing the log file...")
            log_file.close()
        exit(1)
    except Exception as e:
        print("\nAn error has occurred")
        print(Fore.RED + "\tExiting..." + Fore.RESET)
        if args.log:
            if args.verbose:
                print(f"{Fore.CYAN}[V]{Fore.RESET} Closing the log file...")
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] An error has occurred")
            log_file.write(f"\n[{time.strftime('%d/%m/%Y %H:%M:%S')}] Closing the log file...")
            log_file.close()
        raise e


if __name__ == "__main__":
    main()