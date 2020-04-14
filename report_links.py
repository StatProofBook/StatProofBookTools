#!/usr/bin/env python
"""
Report dead links in the StatProofBook
_
This script loads all content from the proof and definition directories and
lists proof and definition pages which are referenced but non-existing.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-04-14 06:27:00
 Last edit: 2020-04-14 07:32:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import re
import numpy as np
from datetime import datetime

# Extract file body
#-----------------------------------------------------------------------------#
def extract_body(file_txt):
    """
    Return body text of proof or definition
    """
    num_dash   = 0
    start_line = 0
    end_line   = len(file_txt)
    for i in range(0,end_line):
        if file_txt[i].find('---') == 0:
            num_dash = num_dash + 1
        if file_txt[i].find('**') == 0 and num_dash == 2 and start_line == 0:
            start_line = i
    body_txt = file_txt[start_line:end_line]
    return body_txt

# Set repository directory
#-----------------------------------------------------------------------------#
ini_obj = open('init_tools.txt')
ini_txt = ini_obj.readlines()
ini_obj.close()
rep_dir = ini_txt[0][0:-1]
www_dir = ini_txt[1][0:]

# Prepare page references
#-----------------------------------------------------------------------------#
filenames = []                  # list of referenced files
linktexts = []                  # list of reference texts
srcefiles = []                  # list of files referenced from

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
        
        # Search proof body
        #---------------------------------------------------------------------#
        body_txt = extract_body(file_txt)
        for line in body_txt:
            while line.find('](/') > -1:
                # get bracket/parantheses indices
                i2 = line.find('](/')
                i3 = i2 + 1
                i4 = line.find(')', i2)
                i1 = line.rfind('[', 0, i2)
                # get shortcut/filename
                file_md  = line[i3+1:i4] + '.md'
                linktext = line[i1+1:i2]
                # if file does not exist
                if not os.path.isfile(rep_dir + file_md):
                    filenames.append(file_md)
                    linktexts.append(linktext)
                    srcefiles.append('/P/'+file)
                # shorten the file line
                line = line[i4+1:]

# Browse through definitions
#-----------------------------------------------------------------------------#
files = os.listdir(rep_dir + '/D/')
for file in files:
    if '.md' in file:
        
        # Read proof file
        #---------------------------------------------------------------------#
        file_obj = open(rep_dir + '/D/' + file, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Search proof body
        #---------------------------------------------------------------------#
        body_txt = extract_body(file_txt)
        for line in body_txt:
            while line.find('](/') > -1:
                # get bracket/parantheses indices
                i2 = line.find('](/')
                i3 = i2 + 1
                i4 = line.find(')', i2)
                i1 = line.rfind('[', 0, i2)
                # get shortcut/filename
                file_md  = line[i3+1:i4] + '.md'
                linktext = line[i1+1:i2]
                # if file does not exist
                if not os.path.isfile(rep_dir + file_md):
                    filenames.append(file_md)
                    linktexts.append(linktext)
                    srcefiles.append('/D/'+file)
                # shorten the file line
                line = line[i4+1:]

# Prepare unique references
#-----------------------------------------------------------------------------#
unique_filenames = []           # list of unique referenced files
unique_linktexts = []           # list of unique reference texts
unique_srcefiles = []           # list of unique files referenced from

# Browse through references
#-----------------------------------------------------------------------------#
sort_ind  = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(filenames)])]
last_file = 'last_file'
ults = False
for i in range(0,len(filenames)):
    filename = filenames[sort_ind[i]]
    if filename != last_file:
        if ults:
            unique_filenames.append(last_file)
            unique_linktexts.append(sorted(ults))
        ults = []
        ults.append(linktexts[sort_ind[i]])
    else:
        if linktexts[sort_ind[i]] not in ults:
            ults.append(linktexts[sort_ind[i]])
    last_file = filename
unique_filenames.append(last_file)
unique_linktexts.append(sorted(ults))

# Extract source files
#-----------------------------------------------------------------------------#
for i in range(0,len(unique_filenames)):                # filenames
    usfs_i = []
    for j in range(0,len(unique_linktexts[i])):         # link texts
        usfs_j = []
        for k in range(0,len(srcefiles)):               # source files
            if filenames[k] == unique_filenames[i] and linktexts[k] == unique_linktexts[i][j] and srcefiles[k] not in usfs_j:
                usfs_j.append(srcefiles[k])
        usfs_i.append(sorted(usfs_j))
    unique_srcefiles.append(usfs_i)

# Open protocol file
#-----------------------------------------------------------------------------#
today_now = datetime.now().strftime('%Y-%m-%d, %H:%M')
protocol  = open('report_links/Dead_Links.txt', 'w')

# Display non-existing pages
#-----------------------------------------------------------------------------#
print('\n-> Pages which are referenced but non-existing:')
protocol.write('-> Pages which are referenced but non-existing (' + today_now + '):\n')
for i in range(0,len(unique_filenames)):
    filename = unique_filenames[i]
    shortcut = filename[3:-3]
    if filename.find('/P/') > -1:
        protocol.write('   - Proof "' + shortcut + '" ("' + filename + '"), referenced as\n')
    if filename.find('/D/') > -1:
        protocol.write('   - Definition "' + shortcut + '" ("' + filename + '"), referenced as\n')
    for j in range(0,len(unique_linktexts[i])):
        linktext = unique_linktexts[i][j]
        protocol.write('     - "' + linktext + '", referenced in\n')
        for k in range(0,len(unique_srcefiles[i][j])):
            srcefile = unique_srcefiles[i][j][k]
            protocol.write('       - "' + srcefile + '"\n')

# Close protocol file
#-----------------------------------------------------------------------------#        
protocol.close()
print('   - written into "' + protocol.name + '"')