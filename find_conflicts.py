#!/usr/bin/env python
"""
Find conflicts in Table of Contents
_
This script loads all content from the proof/definition/index directories and
produces warnings about ToC mismatches between index and proofs/definitions.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-08-25 15:55:00
 Last edit: 2021-11-08 23:00:00
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

# Prepare finding conflicts
#-----------------------------------------------------------------------------#
print('\n-> Find ToC conflicts in the StatProofBook:')
conf_found = False

# Set chapter and section names
#-----------------------------------------------------------------------------#
chapters  = ['I', 'II', 'III', 'IV']
num_chap  = 0;
num_sect  = 0;
num_ssec  = 0;
num_ssse  = 0;
curr_chap = '';
curr_sect = '';
curr_ssec = '';
curr_ssse = '';

# Parse "Table of Contents"
#-----------------------------------------------------------------------------#
for entry in toc_txt:
    
    # If there is a new chapter
    #-------------------------------------------------------------------------#
    if entry.count('.') == 0 and entry.find('<h3>') > -1:
        
        num_sect  = 0
        num_chap  = num_chap + 1
        curr_chap = entry[entry.find('<h3>')+4:entry.find('</h3>')]
        curr_chap = curr_chap[curr_chap.find(': ')+2:]
    
    # If there is a new section
    #-------------------------------------------------------------------------#
    if entry.count('.') == 1 and entry.find(str(num_sect+1) + '. ') > -1:
                
        num_ssec  = 0
        num_sect  = num_sect + 1        
        curr_sect = entry[entry.find('. ')+2:entry.find('\n')]
        
    # If there is a new subsection
    #-------------------------------------------------------------------------#
    if entry.count('.') == 2 and entry.find(str(num_sect) + '.' + str(num_ssec+1) + '. ') > -1:
        
        num_ssse  = 0
        num_ssec  = num_ssec + 1
        curr_ssec = entry[entry.find('. ')+2:entry.find('<br>')]
        if curr_ssec[-1] == ' ': curr_ssec = curr_ssec[0:-1]
        
    # If there is a new subsubsection
    #-------------------------------------------------------------------------#
    if entry.count('.') >= 3 and entry.find(str(num_sect) + '.' + str(num_ssec) + '.' + str(num_ssse+1) + '. ') > -1:
        
        num_ssse  = num_ssse + 1
        curr_ssse = entry[entry.find('[')+1:entry.find(']')]
        file      = entry[entry.find('(', entry.find(']'))+1:entry.find(')', entry.find(']'))]
        file_md   = file + '.md'
        
        # Read proof or definition
        if file_md.find('/P/') > -1:
            item_type = 'Proof'
        if file_md.find('/D/') > -1:
            item_type = 'Definition'
        file_obj = open(rep_dir + file_md, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Extract ToC information
        file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
        chapter, section, topic, item            = spbt.get_toc_info(file_txt)
        
        # Compare ToC information
        if chapter != curr_chap or section != curr_sect or topic != curr_ssec or item != curr_ssse:
            print('   - Warning: ' + item_type + ' "' + shortcut + '" (' + chapters[num_chap-1] + '/' + str(num_sect) + '.' + str(num_ssec) + '.' + str(num_ssse) + '. ' + title + '):')
            print('     - categoized in file as "' + chapter + '" >> "' + section + '" >> "' + topic + '" >> "' + item + '".')
            print('     - referenced in ToC  as "' + curr_chap + '" >> "' + curr_sect + '" >> "' + curr_ssec + '" >> "' + curr_ssse + '".')
            conf_found = True
 
# Finalize treatment
#-----------------------------------------------------------------------------#
if not conf_found:
    print('   - no conflicts found.')