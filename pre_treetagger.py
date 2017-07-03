#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import time
import fnmatch
from lxml import etree
import regex as re


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
        # replace unicode punctuation
        tc = re.sub(r'，', r',', tc)
        tc = re.sub(r'。', r'. ', tc)
        tc = re.sub(r'、', r',', tc)
        tc = re.sub(r'”', r'"', tc)
        tc = re.sub(r'“', r'"', tc)
        tc = re.sub(r'∶', r':', tc)
        tc = re.sub(r'：', r':', tc)
        tc = re.sub(r'？', r'?', tc)
        tc = re.sub(r'《', r'"', tc)
        tc = re.sub(r'》', r'"', tc)
        tc = re.sub(r'）', r')', tc)
        tc = re.sub(r'！', r'!', tc)
        tc = re.sub(r'（', r'(', tc)
        tc = re.sub(r'；', r';', tc)
        tc = re.sub(r'１', r'"', tc)
        tc = re.sub(r'」', r'"', tc)
        tc = re.sub(r'「', r'"', tc)
        tc = re.sub(r'０', r'0', tc)
        tc = re.sub(r'３', r'3', tc)
        tc = re.sub(r'２', r'2', tc)
        tc = re.sub(r'５', r'5', tc)
        tc = re.sub(r'６', r'6', tc)
        tc = re.sub(r'９', r'9', tc)
        tc = re.sub(r'７', r'7', tc)
        tc = re.sub(r'８', r'8', tc)
        tc = re.sub(r'４', r'4', tc)
        tc = re.sub(r'．', r'. ', tc)
        tc = re.sub(r'～', r'~', tc)
        tc = re.sub(r'’', r'\'', tc)
        tc = re.sub(r'…', r'\.\.\.', tc)
        tc = re.sub(r'━', r'-', tc)
        tc = re.sub(r'〈', r'<', tc)
        tc = re.sub(r'〉', r'>', tc)
        tc = re.sub(r'【', r'[', tc)
        tc = re.sub(r'】', r']', tc)
        tc = re.sub(r'％', r'%', tc)
        # normalize punctuation
        tc = re.sub(r"(\s)-+(\w)", r"\1—\2", tc)
        tc = re.sub(r"(\w)-+(\s)", r"\1—\2", tc)
        tc = re.sub(r"(\s)-+(\s)", r"\1—\2", tc)
        tc = re.sub(r"\r", r"", tc)
        # remove extra spaces
        tc = re.sub(r'\(', r' (', tc)
        tc = re.sub(r'\)', r') ', tc)
        tc = re.sub(r' +', r' ', tc)
        tc = re.sub(r'\) ([\.\!\:\?\;\,])', r')\1', tc)
        tc = re.sub(r'\( ', r'(', tc)
        tc = re.sub(r' \)', r')', tc)
        tc = re.sub(r'(\d) \%', r'\1%', tc)
        tc = re.sub(r' :', r':', tc)
        tc = re.sub(r' ;', r';', tc)
        # normalize unicode punctuation
        tc = re.sub(r'\`', r'\'', tc)
        tc = re.sub(r'\'\'', r' " ', tc)
        tc = re.sub(r'„', r'"', tc)
        tc = re.sub(r'“', r'"', tc)
        tc = re.sub(r'”', r'"', tc)
        tc = re.sub(r'–', r'-', tc)
#         tc = re.sub(r'—', r' - ', tc)
        tc = re.sub(r' +', r' ', tc)
        tc = re.sub(r'´', r'\'', tc)
        tc = re.sub(r'(\p{L})‘(\p{L})', r'\1\'\2', tc)
        tc = re.sub(r'(\p{L})’(\p{L})', r'\1\'\2', tc)
        tc = re.sub(r'‘', r'"', tc)
        tc = re.sub(r'‚', r'"', tc)
        tc = re.sub(r'’', r'"', tc)
        tc = re.sub(r'\'\'', r'"', tc)
        tc = re.sub(r'´´', r'"', tc)
        tc = re.sub(r'…', r'...', tc)
        # French quotes
        tc = re.sub(r' « ', r' "', tc)
        tc = re.sub(r'« ', r'"', tc)
        tc = re.sub(r'«', r'"', tc)
        tc = re.sub(r' » ', r'" ', tc)
        tc = re.sub(r' »', r'"', tc)
        tc = re.sub(r'»', r'"', tc)
        # handle pseudo-spaces
        tc = re.sub(r' \%', r'\%', tc)
        tc = re.sub(r'nº ', r'nº ', tc)
        tc = re.sub(r' :', r':', tc)
        tc = re.sub(r' ºC', r' ºC', tc)
        tc = re.sub(r' cm', r' cm', tc)
        tc = re.sub(r' \?', r'\?', tc)
        tc = re.sub(r' \!', r'\!', tc)
        tc = re.sub(r' ;', r';', tc)
        tc = re.sub(r', ', r', ', tc)
        tc = re.sub(r' +', r' ', tc)
        # English "quotation," followed by comma, style
        if self.lang is "en":
            tc = re.sub(r'\"([,\.]+)', r'\1"', tc)
        # German/Spanish/French "quotation", followed by comma, style
        else:
            tc = re.sub(r',\"', r'",', tc)    
            tc = re.sub(r'(\.+)\"(\s*[^<])', r'"\1\2', tc)
        # Numbers
        tc = re.sub(r' (\p{P})?(\d{1,3}) (\d{3}) ?(\d{3})? ?(\d{3})? ?(\d{3})? ?', r' \1\2\3\4\5\6 ', tc)
        # remove non-printing characters
        tc = re.sub(r"\p{C}", r" ", tc)
        # remove too many white spaces
        tc = re.sub(r" {2,}", r" ", tc)
        return tc
    
    def main(self):
        for ifile in self.ifiles:
            print(ifile)
            tree = self.read_xml(ifile)
            if self.strip is True:
                elements = tree.xpath('.//{}'.format(self.text))
                for e in elements:
                    e.text = e.text.strip()
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
#             output = self.unprettify(tree)
            output = etree.tostring(
                tree,
                encoding='UTF-8',
                method='xml',
                xml_declaration=True,
                pretty_print=True).decode()
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
            "-l",
            "--language",
            required=True,
            choices=['es', 'en', 'de'],
            help="language of the version to be processed.")
        parser.add_argument(
            "-g",
            "--glob_pattern",
            required=False,
            default="*.xml",
            help="glob pattern to filter files.")
        parser.add_argument(
            "-s",
            "--strip",
            required=False,
            default=False,
            action="store_true",
            help="strip empty lines and white spaces for text. False by default.")
        args = parser.parse_args()
        self.idir = args.input
        self.odir = args.output
        self.text = args.text
        self.pattern = args.glob_pattern
        self.strip = args.strip
        self.lang = args.language
        pass


print(PreTokenizer())
