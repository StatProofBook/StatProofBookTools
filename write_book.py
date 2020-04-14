#!/usr/bin/env python
"""
Write "The Book of Statistical Proofs"
_
This script loads all content from the proof/definition/index directories and
compiles it into a LaTeX source file that results in a PDF of the book.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-02-06 05:47:00
 Last edit: 2020-04-14 07:41:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import re
import numpy as np
from datetime import datetime

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
        file_md  = file + '.md' # re.sub('.html', '.md', file_html)
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

# Set repository directory
#-----------------------------------------------------------------------------#
ini_obj = open('init_tools.txt')
ini_txt = ini_obj.readlines()
ini_obj.close()
rep_dir = ini_txt[0][0:-1]
www_dir = ini_txt[1][0:]
toc_md  = '/I/Table_of_Contents.md'

# Read "Table of Contents"
#-----------------------------------------------------------------------------#
toc_obj = open(rep_dir + toc_md, 'r')
toc_txt = toc_obj.readlines()
toc_obj.close()
# import urllib2 as ul2
# toc_txt = ul2.urlopen(www_dir)

# Read the LaTeX header
#-----------------------------------------------------------------------------#
hdr_obj = open('write_book/StatProofBook.txt', 'r')
hdr_txt = hdr_obj.readlines()
hdr_obj.close()

# Open "The Book of Statistical Proofs"
#-----------------------------------------------------------------------------#
print('\n-> LaTeX source code producing the StatProofBook PDF:')
book = open('write_book/StatProofBook.tex', 'w')
for line in hdr_txt:
    if line.find('\date{') == 0:
        today_now = datetime.now().strftime('%Y-%m-%d, %H:%M')
        book.write('\\date{' + today_now + '}')
    else:
        book.write(line)

# Set chapter and section names
#-----------------------------------------------------------------------------#
num_chap  = 0;
num_sect  = 0;
num_ssec  = 0;
num_ssse  = 0;
curr_chap = '';
curr_sect = '';
curr_ssec = '';
curr_ssse = '';

# Parse "Table of Contents"
# Write "The Book of Statistical Proofs"
#-----------------------------------------------------------------------------#
for entry in toc_txt:
    
    # If there is a new chapter
    #-------------------------------------------------------------------------#
    if entry.count('.') == 0 and entry.find('<h3>') > -1:
        
        num_sect  = 0
        num_chap  = num_chap + 1
        curr_chap = entry[entry.find('<h3>')+4:entry.find('</h3>')]
        curr_chap = curr_chap[curr_chap.find(': ')+2:]
        book.write('\n\n% Chapter ' + str(num_chap) + ' %\n')
        book.write('\chapter{' + curr_chap + '} \label{sec:' + curr_chap + '} \\newpage\n\n')
    
    # If there is a new section
    #-------------------------------------------------------------------------#
    if entry.count('.') == 1 and entry.find(str(num_sect+1) + '. ') > -1:
  # if entry[0].isdigit() and entry.find('. ') == 1:
                
        num_ssec  = 0
        num_sect  = num_sect + 1        
        curr_sect = entry[entry.find('. ')+2:entry.find('\n')]
        book.write('\pagebreak\n')
        book.write('\section{' + curr_sect + '}\n\n')
        
    # If there is a new subsection
    #-------------------------------------------------------------------------#
    if entry.count('.') == 2 and entry.find(str(num_sect) + '.' + str(num_ssec+1) + '. ') > -1:  
  # if curr_sect != '' and entry.count('.') == 2:
        
        num_ssse  = 0
        num_ssec  = num_ssec + 1
        curr_ssec = entry[entry.find('. ')+2:entry.find('<br>')]
        if curr_ssec[-1] == ' ': curr_ssec = curr_ssec[0:-1]
        book.write('\subsection{' + curr_ssec + '}\n\n')
        
    # If there is a new subsubsection
    #-------------------------------------------------------------------------#
    if entry.count('.') >= 3 and entry.find(str(num_sect) + '.' + str(num_ssec) + '.' + str(num_ssse+1) + '. ') > -1:
  # if entry.find('&emsp;&ensp;') > -1:
        
        num_ssse  = num_ssse + 1
        curr_ssse = entry[entry.find('[')+1:entry.find(']')]
        file      = entry[entry.find('(', entry.find(']'))+1:entry.find(')', entry.find(']'))]
        file_md   = file + '.md' # re.sub('.html', '.md', file_html)
        
        # Read proof or definition
        if file_md.find('/P/') > -1:
            is_proof = True
        if file_md.find('/D/') > -1:
            is_proof = False
        file_obj = open(rep_dir + file_md, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Extract file information
        file_id, shortcut, title, username, date = get_meta_data(file_txt)
        chapter, section, topic, item            = get_toc_info(file_txt)
        sources  = get_sources(file_txt)
        body_txt = extract_body(file_txt)
        
        # Write title
        if is_proof:
            book.write(r'\subsubsection[\textbf{' + curr_ssse + '}]{' + curr_ssse + '} \label{sec:' + shortcut + '}\n')
            book.write(r'\setcounter{equation}{0}')
            book.write('\n\n')
        else:
            book.write(r'\subsubsection[\textit{' + curr_ssse + '}]{' + curr_ssse + '} \label{sec:' + shortcut + '}\n')
            book.write(r'\setcounter{equation}{0}')
            book.write('\n\n')
        
        # Write body
        in_equation = False
        in_itemize  = False
        for line in body_txt:
            
            # write bold text
            line = re.sub('\*\*Definition:\*\*', '\\\\textbf{Definition:}', line)
            line = re.sub('\*\*Theorem:\*\*', '\\\\textbf{Theorem:}', line)
            line = re.sub('\*\*Proof:\*\*', '\\\\vspace{1em}\n\\\\textbf{Proof:}', line)
            
            # use equation environment
            if not in_equation and line.find('$$') == 0:
                line = re.sub('\$\$', '\\\\begin{equation}', line)
                in_equation = True
            if in_equation and line.find('$$') == 0:
                line = re.sub('\$\$', '\\\\end{equation}', line)
                in_equation = False
            
            # replace equation labels
            line = re.sub('\\\\label{eq:', '\\\\label{eq:'+shortcut+'-', line)
            line = re.sub('\\\\eqref{eq:', '\\\\eqref{eq:'+shortcut+'-', line)
            
            # replace hyperlinks
            line = replace_links(line, rep_dir)
            
            # eliminate linebreaks
            line = re.sub('<br>', '\\\\vspace{1em}', line)
            
            # configure itemize
            if not in_itemize and line.find('* ') == 0:
                book.write('\\begin{itemize}\n\n')
                in_itemize = True
            if in_itemize and len(line) > 1 and line.find('* ') != 0:
                book.write('\\end{itemize}\n\n')
                in_itemize = False
            if in_itemize and line.find('* ') == 0:
                line = re.sub('\* ', '\\\\item ', line)
            
            # write code line
            book.write(line)
            
        # Write sources
        book.write('\n\n\n')
        book.write('\\vspace{1em}\n')
        book.write('\\textbf{Sources:}\n')
        book.write('\\begin{itemize}\n')
        if not sources:
            book.write('\\item original work')
        else:
            for source in sources:
                book.write('\\item ' + source['authors'] + ' (' + source['year'] + '): "' + source['title'] + '"')
                if 'in'    in source: book.write('; in: \\textit{' + source['in'] + '}')
                if 'pages' in source: book.write(', ' + source['pages'])
                if 'url'   in source: book.write('; URL: \\url{' + source['url'] + '}')
                if 'doi'   in source: book.write('; DOI: ' + source['doi'])
                book.write('.\n')
        book.write('\\end{itemize}')
        
        # Write metadata
        book.write('\n\n\n')
        book.write('\\vspace{1em}\n')
        book.write('\\textbf{Metadata:} ID: ' + file_id + ' | shortcut: ' + shortcut + ' | author: ' + username + ' | date: ' + date.strftime('%Y-%m-%d, %H:%M') + '.\n')
        book.write('\\vspace{1em}\n')
        book.write('\n\n\n')
        
# Close "The Book of Statistical Proofs"
#-----------------------------------------------------------------------------#        
book.write('\end{document}')
book.close()
print('   - written into "' + book.name + '"')