#!/usr/bin/env python
"""
Run all StatProofBook tools
_
This script runs all updating Python scripts in this folder.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-05-18 19:58:00
 Last edit: 2020-08-25 15:49:00
"""


import os
cwd = os.getcwd()

# Write "The Book of Statistical Proofs"
#-----------------------------------------------------------------------------#
runfile('write_book.py', wdir=cwd)

# Report dead links in the StatProofBook
#-----------------------------------------------------------------------------#
runfile('report_links.py', wdir=cwd)

# Find ToC conflicts in the StatProofBook
#-----------------------------------------------------------------------------#
runfile('find_conflicts.py', wdir=cwd)

# Display content in the StatProofBook
#-----------------------------------------------------------------------------#
runfile('display_content.py', wdir=cwd)