#!/usr/bin/env python
"""
Replace affiliation and e-mail address in certain Proofs/Definitions.
_
This script takes all Proofs and Definitions written by Joram Soch after
2024-01-01, changes their affiliation to "OvGU Magdeburg" and their e-mail
address to "joram.soch@ovgu.de".

Author: Joram Soch, OvGU Magdeburg
E-Mail: joram.soch@ovgu.de

First edit: 2025-10-31 16:28:00
 Last edit: 2025-10-31 16:28:00
"""


# Import modules
#-----------------------------------------------------------------------------#
# import os
import BookTools as spbt
from datetime import datetime

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')

# Load "Table of Contents"
#-----------------------------------------------------------------------------#
toc_md  = '/I/ToC.md'
toc_obj = open(rep_dir + toc_md, 'r')
toc_txt = toc_obj.readlines()
toc_obj.close()

# Read all proofs/definitions
#-----------------------------------------------------------------------------#
nums, tocs, files = spbt.get_all_items(toc_txt)
date0             = datetime(2024, 1, 1, 0, 0, 0)

# Browse through files
#-----------------------------------------------------------------------------#
pr_edited  = []
def_edited = []
item_msg   = '   - {} "{}"'
print('\n-> Editing proofs and definitions (in order of ToC):')
for file in files:
    
    # Load proof/definition
    #---------------------------------------------------------------------#
    file_obj = open(rep_dir + file, 'r')
    file_txt = file_obj.readlines()
    file_obj.close()
    
    # Get date and info
    #---------------------------------------------------------------------#
    file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
    chapter, section, topic, item            = spbt.get_toc_info(file_txt)
    
    # If this proof/definition is eligible
    #---------------------------------------------------------------------#
    if username == 'JoramSoch' and date > date0:
        
        # store file ID
        if file_id[0] == 'P':
            pr_edited.append(file_id)
            print(item_msg.format('Proof', title))
        if file_id[0] == 'D':
            def_edited.append(file_id)
            print(item_msg.format('Definition', title))
        
        # write new file
        file_obj = open(rep_dir + file, 'w')
        for line in file_txt:
            if line.startswith('author:'):
                file_obj.write(line)
            elif line.startswith('affiliation:'):
                file_obj.write('affiliation: "OvGU Magdeburg"\n')
            elif line.startswith('e_mail:'):
                file_obj.write('e_mail: "joram.soch@ovgu.de"\n')
            else:
                file_obj.write(line)
        file_obj.close()

# Report edited files
#-----------------------------------------------------------------------------#      
print('\n-> The following proofs were edited:')
print(sorted(pr_edited))
print('\n-> The following definitions were edited:')
print(sorted(def_edited))