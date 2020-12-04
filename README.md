## StatProofBookTools

[![DOI](https://zenodo.org/badge/238672483.svg)](https://zenodo.org/badge/latestdoi/238672483)

Tools for [The Book of Statistical Proofs](https://statproofbook.github.io/)

### Getting Started

To configure everything, proceed as follows:
1. clone the repositories [StatProofBook.github.io](https://github.com/StatProofBook/StatProofBook.github.io) and [StatProofBookTools](https://github.com/StatProofBook/StatProofBookTools) to your local machine;
2. replace the first line of `init_tools.txt` by the path to your local *StatProofBook.github.io* repository;
3. run any of the Python scripts (ending on `.py`) in your local *StatProofBookTools* repository.

### The Tools

In more details, the tools allow you to:
* `write_book.py`: write all StatProofBook content into a [LaTeX source file](https://github.com/StatProofBook/StatProofBookTools/blob/master/write_book/StatProofBook.tex) that results in a [PDF of the book](https://github.com/StatProofBook/StatProofBookTools/blob/master/write_book/StatProofBook.pdf);
* `report_links.py`: create a [list of dead links](https://github.com/StatProofBook/StatProofBookTools/blob/master/report_links/Dead_Links.txt), i.e. a list of pages which are referenced but non-existing;
* `find_conflicts.py`: display a list of conflicts, i.e. mismatches between table of contents and proofs/definitions;
* `replace_string.py`: replace an arbitrary string with another predefined string in all proofs and definitions;
* `display_content.py`: display some stats regarding [content](https://github.com/StatProofBook/StatProofBookTools/blob/master/display_content/Content.png), [development](https://github.com/StatProofBook/StatProofBookTools/blob/master/display_content/Development.png), [proofs](https://github.com/StatProofBook/StatProofBookTools/blob/master/display_content/Topic_Proofs.png) and [definitions](https://github.com/StatProofBook/StatProofBookTools/blob/master/display_content/Topic_Definitions.png);
* `visualize_all.py`: create a nested dictionary that can be used for interactive visualization.
