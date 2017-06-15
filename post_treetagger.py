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


class PostTagger(object):
    """Correct POS tagging."""

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
            os.path.splitext(os.path.basename(ifile))[0]+'.vrt')
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

    def main(self):
        for ifile in self.ifiles:
            print(ifile)
            tree = self.read_xml(ifile)
            text_containers = tree.xpath('.//{}'.format(self.text))
            for tc in text_containers:
                text = tc.text
                if self.lang == 'es':
                    text = re.sub(
                        r"\nSr\.\t.+?\n", r"\nSr.\tNC\tseñor\n", text)
                    text = re.sub(
                        r"\nSra\.\t.+?\n", r"\nSra.\tNC\tseñora\n", text)
                tc.text = text
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
        parser.add_argument(
            "-l",
            "--language",
            required=True,
            choices=['es'],
            help="language."
        )
        args = parser.parse_args()
        self.idir = args.input
        self.odir = args.output
        self.text = args.text
        self.pattern = args.glob_pattern
        self.lang = args.language
        pass


print(PostTagger())
