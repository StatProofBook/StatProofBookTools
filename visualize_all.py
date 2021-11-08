#!/usr/bin/env python
"""
Visualize all items in the StatProofBook
_
This script prepares a Python dictionary coding the entire table of contents
that is later to be used for interactive visualization of the StatProofBook.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-08-25 19:25:00
 Last edit: 2021-11-08 23:02:00
"""


# Import modules
#-----------------------------------------------------------------------------#
# import os
import BookTools as spbt

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')
toc_md  = '/I/ToC.md'

# Load "Table of Contents"
#-----------------------------------------------------------------------------#
toc_obj = open(rep_dir + toc_md, 'r')
toc_txt = toc_obj.readlines()
toc_obj.close()

# Browse through files
#-----------------------------------------------------------------------------#
StatProofBook     = dict()
nums, tocs, files = spbt.get_all_items(toc_txt)
for toc,file_md in zip(tocs,files):
    file = file_md[0:-3]
    if toc[0] not in StatProofBook:
        StatProofBook[toc[0]] = dict()
    if toc[1] not in StatProofBook[toc[0]]:
        StatProofBook[toc[0]][toc[1]] = dict()
    if toc[2] not in StatProofBook[toc[0]][toc[1]]:
        StatProofBook[toc[0]][toc[1]][toc[2]] = dict()
    if toc[3] not in StatProofBook[toc[0]][toc[1]][toc[2]]:
        StatProofBook[toc[0]][toc[1]][toc[2]][toc[3]] = ''
    StatProofBook[toc[0]][toc[1]][toc[2]][toc[3]] = 'https://statproofbook.github.io' + file