# TreeTaggerWrapper of TreeTaggerWrapper

**T**ree**T**agger**W**rapper **o**f **T**ree**T**agger**W**rapper is a wrapper to annotate XML files with TreeTagger. The goal is to get always well-formed XML and to customize TreeTagger behaviour as needed.

This script bundle relies on a [modified version](https://github.com/chozelinek/mytreetaggerwrapper) of [Laurent Pointal's treetaggerwrapper](https://pypi.python.org/pypi/treetaggerwrapper).

## Contents

```text
├── LICENSE: GPL-3.0
├── README.md: this file
├── post_treetagger.py: script to fix annotation
├── pre_treetagger.py: script to normalize characters
├── requirements.txt: Python dependencies
├── spanish-abbreviations: one token per line, true case and punctuation (TreeTagger expected format)
└── treetagger.py: the wrapper of the wrapper
```

## Requirements

In order to use the `TTWoTTW` you will need to:

1. clone this repository
1. install python dependencies `pip install -r requirements.txt`
1. install [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)

## Usage

### Help

Run `python treetagger.py -h`:

```text
usage: treetagger.py [-h] -i INPUT -o OUTPUT -l {en,es,de} [-e ELEMENT]
                     [-p PATTERN] [-s] [--tokenize] [-a ABBREVIATION]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the input directory.
  -o OUTPUT, --output OUTPUT
                        path to the output directory.
  -l {en,es,de}, --language {en,es,de}
                        language of the version to be processed.
  -e ELEMENT, --element ELEMENT
                        XML element containing the text to be split in
                        sentences.
  -p PATTERN, --pattern PATTERN
                        glob pattern to filter files.
  -s, --sentence        if provided, it splits text in sentences.
  --tokenize            if provided, it tokenizes the text, else, it expects
                        one token per line.
  -a ABBREVIATION, --abbreviation ABBREVIATION
                        path to the abbreviation file, if not provided uses
                        default TreeTagger's abbreviation file.
```

### Example

```shell
python treetagger.py -i input/directory/ -o output/directory/ -l es -e s --tokenize -p "*.xml" -a spanish-abbreviations
```

### A pipeline for Spanish

```shell
# preprocess files
python pre_treetagger.py -i input/directory/ -o output/directory/ -t s -g "*.xml"
# tag files with TTWoTTW
python treetagger.py -i input/directory/ -o output/directory/ -l es -e s --tokenize -a spanish-abbreviations -p "*.xml"
# postprocess files
python post_treetagger.py -i input/directory/ -o output/directory/ -l es -g "*.vrt"
```
