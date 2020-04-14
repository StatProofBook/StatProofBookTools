#!/usr/bin/env python
"""
The StatProofBookTools Unit
_
This module collects several functions that are used by different scripts
within the StatProofBookTools repository.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-04-14 16:35:00
 Last edit: 2020-04-14 16:35:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import re
from datetime import datetime

# Get repository directory
#-----------------------------------------------------------------------------#
def get_rep_dir(rep_type):
    """
    Return respository directory read from "init_tools.txt"
    """
    ini_obj = open('init_tools.txt')
    ini_txt = ini_obj.readlines()
    ini_obj.close()
    rep_dir = ini_txt[0][0:-1]
    www_dir = ini_txt[1][0:]
    if rep_type == 'online':
        return www_dir
    else:
        return rep_dir

# Get meta data
#-----------------------------------------------------------------------------#
def get_meta_data(file_txt):
    """
    Return meta data of proof or definition
    """
    for line in file_txt:
        if line.find('proof_id:') == 0:
            file_id = re.sub('"', '', line[10:-1])
        if line.find('def_id:') == 0:
            file_id = re.sub('"', '', line[8:-1])
        if line.find('shortcut:') == 0:
            shortcut = re.sub('"', '', line[10:-1])
        if line.find('title:') == 0:
            title = re.sub('"', '', line[7:-1])
        if line.find('author:') == 0:
            author = re.sub('"', '', line[8:-1])
        if line.find('username:') == 0:
            username = re.sub('"', '', line[10:-1])
            if not username:
                if not author:
                    username = 'unknown'
                else:
                    username = author
        if line.find('date:') == 0:
            date = datetime.strptime(line[6:-1], '%Y-%m-%d %H:%M:%S')
    return file_id, shortcut, title, username, date

# Get ToC info
#-----------------------------------------------------------------------------#
def get_toc_info(file_txt):
    """
    Return table of contents location of proof or definition
    """
    for line in file_txt:
        if line.find('chapter:') == 0:
            chapter = re.sub('"', '', line[9:-1])
        if line.find('section:') == 0:
            section = re.sub('"', '', line[9:-1])
        if line.find('topic:') == 0:
            topic = re.sub('"', '', line[7:-1])
        if line.find('theorem:') == 0:
            item = re.sub('"', '', line[9:-1])
        if line.find('definition:') == 0:
            item = re.sub('"', '', line[12:-1])
    return chapter, section, topic, item

# Get sources
#-----------------------------------------------------------------------------#
def get_sources(file_txt):
    """
    Return sources of proof or definition
    """
    new_src = False
    sources = []
    for line in file_txt:
        if line.find('  - authors:') == 0:
            if new_src: sources.append(source)
            new_src = True
            source  = dict()
            source['authors'] = re.sub('"', '', line[13:-1])
            source['authors'] = re.sub('&', '\&', source['authors'])
        if line.find('    year:') == 0:
            source['year'] = re.sub('"', '', line[10:-1])
        if line.find('    title:') == 0:
            source['title'] = re.sub('"', '', line[11:-1])
            source['title'] = re.sub('&', '\&', source['title'])
        if line.find('    in:') == 0:
            source['in'] = re.sub('"', '', line[8:-1])
            source['in'] = re.sub('&', '\&', source['in'])
        if line.find('    pages:') == 0:
            source['pages'] = re.sub('"', '', line[11:-1])
        if line.find('    url:') == 0:
            source['url'] = re.sub('"', '', line[9:-1])
        if line.find('    doi:') == 0:
            source['doi'] = re.sub('"', '', line[9:-1])
    if new_src: sources.append(source)
    return sources

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

# Replace links/URLs
#-----------------------------------------------------------------------------#
def replace_links(line, rep_dir):
    """
    Replace links such as [text](/P/shortcut) or [text](/D/shortcut)
                       by (-> Proof I/1.2.3) or (Definition "shortcut").
    """
    while line.find('](/') > -1:
        # get bracket/parantheses indices
        i2 = line.find('](/')
        i3 = i2 + 1
        i4 = line.find(')', i2)
        i1 = line.rfind('[', 0, i2)
        # extract file information
        file     = line[i3+1:i4]
        file_md  = file + '.md'
        shortcut = file_md[3:-3]
        if file_md.find('/P/') > -1: file_type = 'Proof'
        if file_md.find('/D/') > -1: file_type = 'Definition'
        # create new reference
        if os.path.isfile(rep_dir + file_md):
            file_obj = open(rep_dir + file_md, 'r')
            file_txt = file_obj.readlines()
            file_obj.close()
            chapter, section, topic, item = get_toc_info(file_txt)
            new_ref = ' ($\\rightarrow$ ' + file_type + ' \\ref{sec:' + chapter + '}/\\ref{sec:' + shortcut + '})'
        else:
            new_ref = ' ($\\rightarrow$ ' + file_type + ' "' + shortcut + '")'
        # adapt to new reference
        line = line[0:i1] + line[i1+1:i2] + new_ref + line[i4+1:]
    return line