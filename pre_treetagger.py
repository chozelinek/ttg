#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import time
import fnmatch
from lxml import etree
import re


def timeit(method):
    """Time methods."""
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r %2.2f sec' %
              (method.__name__, te-ts))
        return result

    return timed


class PreTokenizer(object):
    """Normalize characters for better tokenization."""

    @timeit
    def __init__(self):
        """Constructor."""
        self.cli()
        self.ifiles = self.get_files(self.idir, self.pattern)
        self.counter = 0
        self.main()

    def __str__(self):
        """Print The End message."""
        message = ["{} files processed!".format(self.counter)]
        return " ".join(message)

    def get_files(self, directory, fileclue):
        """Get all files in a directory matching a pattern.

        Keyword arguments:
        directory -- a string for the input folder path
        fileclue -- a string as glob pattern
        """
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, fileclue):
                matches.append(os.path.join(root, filename))
        return matches

    def read_xml(self, ifile):
        """Parse a XML file.

        Keyword arguments:
        ifile -- path to the input file as string
        """
        parser = etree.XMLParser(remove_blank_text=True, encoding='utf-8')
        with open(ifile, encoding='utf-8', mode='r') as input:
            return etree.parse(input, parser)

    def serialize(self, tree_as_string, ifile):
        """Serialize output.

        Keyword arguments:
        tree_as_string -- tree as string
        ifile -- path to the input file as string
        """
        if not os.path.exists(self.odir):
            os.makedirs(self.odir)
        outpath = os.path.join(  # output path
            self.odir,
            os.path.splitext(os.path.basename(ifile))[0]+'.xml')
        with open(outpath, mode='w', encoding='utf-8') as outfile:
            outfile.write(tree_as_string)
        pass

    def unprettify(self, tree):
        """Remove any indentation introduced by pretty print."""
        tree = etree.tostring(  # convert XML tree to string
            tree,
            encoding="UTF-8",
            method="xml",
            xml_declaration=True).decode(encoding='UTF-8')
        tree = re.sub(  # remove trailing spaces before tag
            r"(\n) +(<)",
            r"\1\2",
            tree)
        tree = re.sub(  # put each XML element in a different line
            r"> *<",
            r">\n<",
            tree)
        tree = re.sub(
            r"(>)([^.])",
            r"\1\n\2",
            tree)
        tree = re.sub(  # remove unnecessary empty lines
            r"\n\n+",
            r"\n",
            tree)
        return tree
    
    def search_and_replace(self, tc):
        tc = re.sub(r"(\s)-+(\w)", r"\1—\2", tc)
        tc = re.sub(r"(\w)-+(\s)", r"\1—\2", tc)
        tc = re.sub(r"(\s)-(\s)", r"\1—\2", tc)
        return tc

    def main(self):
        for ifile in self.ifiles:
            print(ifile)
            tree = self.read_xml(ifile)
            text_containers = tree.xpath('.//{}//text()'.format(self.text))
            for tc in text_containers:
#                 text = tc.text
#                 tc = re.sub(r"(\s)-+(\w)", r"\1—\2", tc)
#                 tc = re.sub(r"(\w)-+(\s)", r"\1—\2", tc)
#                 tc = re.sub(r"(\s)-(\s)", r"\1—\2", tc)
#                 tc.text = text
                tc_is_text = tc.is_text
                tc_is_tail = tc.is_tail
                parent = tc.getparent()
                tc = self.search_and_replace(tc)
                if tc_is_text:
                    parent.text = tc
                elif tc_is_tail:
                    parent.tail = tc
            output = self.unprettify(tree)
            self.serialize(output, ifile)
            self.counter += 1
        pass

    def cli(self):
        """Parse command-line arguments."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-i",
            "--input",
            required=True,
            help="input directory.")
        parser.add_argument(
            "-o",
            "--output",
            required=True,
            help="output directory.")
        parser.add_argument(
            "-t",
            "--text",
            required=False,
            default="s",
            help="element containing text to be kept (by default 's').")
        parser.add_argument(
            "-g",
            "--glob_pattern",
            required=False,
            default="*.xml",
            help="glob pattern to filter files.")
        args = parser.parse_args()
        self.idir = args.input
        self.odir = args.output
        self.text = args.text
        self.pattern = args.glob_pattern
        pass


print(PreTokenizer())
