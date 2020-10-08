#!/usr/bin/env python
"""
Find and replace string in the StatProofBook
_
This script goes through all proofs and definitions and
replaces a string str1 with another string str2.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-04-14 17:48:00
 Last edit: 2020-10-08 08:18:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import re
import BookTools as spbt

# Define settings
#-----------------------------------------------------------------------------#
str1r= '.*.*Definition.*.*:'    # should be identical to str1, unless str1
str1 = '**Definition**:'        # contains regexp-problematic characters 
str2 = '**Definition:**'

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')

# Start replacement
#-----------------------------------------------------------------------------#
print('\n-> Replace "' + str1 + '" by "' + str2 + '":')
file_found = False

# Browse through proofs
#-----------------------------------------------------------------------------#
files = os.listdir(rep_dir + '/P/')
for file in files:
    if '.md' in file:
        
        # Read proof file
        #---------------------------------------------------------------------#
        file_obj = open(rep_dir + '/P/' + file, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Search proof text
        #---------------------------------------------------------------------#
        str_found = False
        for i, line in enumerate(file_txt):
            if line.find(str1) > -1:
                str_found   = True
                file_txt[i] = re.sub(str1r, str2, line)
        
        # Write proof file
        #---------------------------------------------------------------------#
        if str_found:
            print('   - in "/P/' + file + '"')
            file_new = open(rep_dir + '/P/' + file, 'w')
            for line in file_txt:
                file_new.write(line)
            file_new.close()
            file_found = True
            
# Browse through definitions
#-----------------------------------------------------------------------------#
files = os.listdir(rep_dir + '/D/')
for file in files:
    if '.md' in file:
        
        # Read definition file
        #---------------------------------------------------------------------#
        file_obj = open(rep_dir + '/D/' + file, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Search definition text
        #---------------------------------------------------------------------#
        str_found = False
        for i, line in enumerate(file_txt):
            if line.find(str1) > -1:
                str_found   = True
                file_txt[i] = re.sub(str1r, str2, line)
        
        # Write definition file
        #---------------------------------------------------------------------#
        if str_found:
            print('   - in "/D/' + file + '"')
            file_new = open(rep_dir + '/D/' + file, 'w')
            for line in file_txt:
                file_new.write(line)
            file_new.close()
            file_found = True
 
# Finalize replacement
#-----------------------------------------------------------------------------#
if not file_found:
    print('   - not found in files.')