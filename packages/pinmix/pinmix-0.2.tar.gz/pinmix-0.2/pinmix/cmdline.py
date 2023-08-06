from pinmix.filler import process_to_print, process_file_to_odt
import sys


def main():
    args = sys.argv
    if len(args) == 2:
        filename = args[1]
        process_to_print(filename)
    elif len(args) > 2:
        filename = args[1]
        output_odt = args[2]
        print('Saving to ODT file, name %s' % output_odt)
        process_file_to_odt(filename, output_odt)
    else:
        raise Exception("Pass arguments to script!")