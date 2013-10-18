#!/usr/bin/env python
r"""
TODO 1. read config through configpack module
TODO 2. locate log , if can generate one big file, proceed, else, stop.
TODO 3. after generate one big file, start to use Parser.
TODO 4. Parser will take config object and sift each line before write the result
TODO 5. the result will be at the same directory as log files
TODO 6. the result will have the file name format: *.spl => *_spl.log
TODO 7. before proceed, check *_spl.log exist, if more than dayoffset day, 
   regenerate, else stop.
TODO 8. if force generate, spl will generate anyway
TODO 9. if Parse demand is from command line, {opid, etc / phase II} , splresult_{nu}.log
   file is generated.
"""









"""
import argparse
parser = argparse.ArgumentParser(description='SRM Log Parser Lite')

parser.add_argument("pp_start_time", help="Start Time of Primary Site Log Section")
parser.add_argument("pp_end_time", help="End Time of Primary Site Log Section")
parser.add_argument("ss_start_time", help="Start Time of Secondary Site Log Section")
parser.add_argument("ss_end_time", help="End Time of Secondary Site Log Section")

parser.add_argument("pp_dir", help="Primary Site Log Directory")
parser.add_argument("ss_dir", help="Secondary Site Log Directory")

parser.add_argument("tag_keys", help="Secondary Site Log Directory")
parser.add_argument("search_regex", help="Secondary Site Log Directory")

parser.parse_args()
"""
