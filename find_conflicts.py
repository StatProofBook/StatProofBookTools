#!/usr/bin/env python
"""
Find conflicts in Table of Contents
_
This script loads all content from the proof/definition/index directories and
produces warnings about ToC mismatches between index and proofs/definitions.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-08-25 15:55:00
 Last edit: 2024-10-04 11:52:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import BookTools as spbt

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')
www_dir = spbt.get_rep_dir('online')
toc_md  = '/I/ToC.md'

# Read "Table of Contents"
#-----------------------------------------------------------------------------#
toc_obj = open(rep_dir + toc_md, 'r')
toc_txt = toc_obj.readlines()
toc_obj.close()

# Parse "Table of Contents"
#-----------------------------------------------------------------------------#
chapters          = ['I', 'II', 'III', 'IV']
nums, tocs, files = spbt.get_all_items(toc_txt)

# Prepare finding conflicts
#-----------------------------------------------------------------------------#
print('\n-> Find ToC conflicts in the StatProofBook:')
num_conf = 0

# Perform finding conflicts
#-----------------------------------------------------------------------------#
for num, toc, file_md in zip(nums, tocs, files):
    
    # Read proof or definition
    if file_md.find('/P/') > -1:
        item_type = 'Proof'
    if file_md.find('/D/') > -1:
        item_type = 'Definition'
    file_obj = open(rep_dir + file_md, 'r')
    file_txt = file_obj.readlines()
    file_obj.close()
    
    # Extract ToC information (from file)
    file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
    chapter, section, topic, item            = spbt.get_toc_info(file_txt)
    
    # Extract ToC information (from ToC)
    num_chap  = num[0]
    num_sect  = num[1]
    num_ssec  = num[2]
    num_ssse  = num[3]
    curr_chap = toc[0]
    curr_sect = toc[1]
    curr_ssec = toc[2]
    curr_ssse = toc[3]
    
    # Compare ToC information
    if chapter != curr_chap or section != curr_sect or topic != curr_ssec or item != curr_ssse:
        print('   - Warning: ' + item_type + ' "' + shortcut + '" (' + chapters[num_chap-1] + '/' + str(num_sect) + '.' + str(num_ssec) + '.' + str(num_ssse) + '. ' + title + '):')
        print('     - categoized in file as "' + chapter + '" >> "' + section + '" >> "' + topic + '" >> "' + item + '".')
        print('     - referenced in ToC  as "' + curr_chap + '" >> "' + curr_sect + '" >> "' + curr_ssec + '" >> "' + curr_ssse + '".')
        num_conf = num_conf + 1

# Finalize treatment
#-----------------------------------------------------------------------------#
if num_conf == 0:
    print('   - no conflicts found.')
else:
    print('\n-> Number of conflicts found: {}.'.format(num_conf))