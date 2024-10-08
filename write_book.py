#!/usr/bin/env python
"""
Write "The Book of Statistical Proofs"
_
This script loads all content from the proof/definition/index directories and
compiles it into a LaTeX source file that results in a PDF of the book.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-02-06 05:47:00
 Last edit: 2024-10-04 15:42:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import re
import BookTools as spbt
from datetime import datetime

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
# import urllib2 as ul2
# toc_txt = ul2.urlopen(www_dir)

# Read the LaTeX header
#-----------------------------------------------------------------------------#
hdr_obj = open('write_book/StatProofBook.txt', 'r')
hdr_txt = hdr_obj.readlines()
hdr_obj.close()

# Parse "Table of Contents"
#-----------------------------------------------------------------------------#
chapters          = ['I', 'II', 'III', 'IV']
nums, tocs, files = spbt.get_all_items(toc_txt)

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

# Set proof and definition info
#-----------------------------------------------------------------------------#
pr_ids     = []
def_ids    = []
pr_titles  = []
def_titles = []
pr_infos   = []
def_infos  = []

# Initialize chapter/section numbers
#-----------------------------------------------------------------------------#
num_chap = 0
num_sect = 0
num_ssec = 0
num_ssse = 0

# Write "The Book of Statistical Proofs"
#-----------------------------------------------------------------------------#
for num, toc, file_md in zip(nums, tocs, files):
    
    # Start new chapter
    if num[0] != num_chap:
        book.write('\n\n% Chapter ' + str(num[0]) + ' %\n')
        book.write('\\chapter{' + toc[0] + '} \\label{sec:' + toc[0] + '} \\newpage\n\n')
    
    # Start new section
    if num[1] != num_sect:
        book.write('\\pagebreak\n')
        book.write('\\section{' + toc[1] + '}\n\n')
    
    # Start new subsection
    if num[2] != num_ssec:
        book.write('\\subsection{' + toc[2] + '}\n\n')
    
    # Extract ToC information
    num_chap  = num[0]
    num_sect  = num[1]
    num_ssec  = num[2]
    num_ssse  = num[3]
    # curr_chap = toc[0]
    # curr_sect = toc[1]
    # curr_ssec = toc[2]
    # curr_ssse = toc[3]
    
    # Read proof or definition
    if file_md.find('/P/') > -1:
        is_proof = True
    elif file_md.find('/D/') > -1:
        is_proof = False
    else:
        is_proof = None
    file_obj = open(rep_dir + file_md, 'r')
    file_txt = file_obj.readlines()
    file_obj.close()
    
    # Extract file information
    file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
    chapter, section, topic, item            = spbt.get_toc_info(file_txt)
    sources  = spbt.get_sources(file_txt)
    body_txt = spbt.extract_body(file_txt)
    
    # Edit title for sorting
    title_edit = re.sub('[^a-zA-Z- ]', '', title)
    title_sort = title_edit.lower()
    
    # Store file information
    if is_proof:
        pr_ids.append(int(file_id[1:]))
        pr_titles.append(title_sort)
        pr_infos.append({'proof_id': file_id, 'shortcut': shortcut, 'title': title, \
                         'username': username, 'date': date, 'source': sources})
    else:
        def_ids.append(int(file_id[1:]))
        def_titles.append(title_sort)
        def_infos.append({'def_id': file_id, 'shortcut': shortcut, 'title': title, \
                          'username': username, 'date': date, 'source': sources})
    
    # Write title
    if is_proof:
        book.write('\\subsubsection[\\textbf{' + toc[3] + '}]{' + toc[3] + '} \\label{sec:' + shortcut + '}\n')
        book.write('\\setcounter{equation}{0}')
        book.write('\n\n')
    else:
        book.write('\\subsubsection[\\textit{' + toc[3] + '}]{' + toc[3] + '} \\label{sec:' + shortcut + '}\n')
        book.write('\\setcounter{equation}{0}')
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
        line = spbt.replace_links(line, rep_dir)
        
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
    
    # End itemize
    if in_itemize:
        book.write('\n\n\\end{itemize}')
        in_itemize = False
    
    # Add tombstone
    if is_proof:
        book.write('\n\\begin{flushright} $\\blacksquare$ \\end{flushright}\n')
    
    # Write sources
    if bool(sources):
        book.write('\n\n')
        if is_proof:
            book.write('\\vspace{-1em}\n')
        else:
            book.write('\\vspace{1em}\n')
        book.write('\\textbf{Sources:}\n')
        book.write('\\begin{itemize}\n')
        for source in sources:
            book.write('\\item ' + source['authors'] + ' (' + source['year'] + '): "' + source['title'] + '"')
            if 'in'    in source: book.write('; in: \\textit{' + source['in'] + '}')
            if 'pages' in source: book.write(', ' + source['pages'])
            if 'url'   in source: book.write('; URL: \\url{' + source['url'] + '}')
            if 'doi'   in source: book.write('; DOI: ' + source['doi'])
            book.write('.\n')
        book.write('\\end{itemize}\n')
        book.write('\\vspace{1em}\n')
    
    # Write metadata
    # book.write('\n\n')
    # book.write('\\vspace{1em}\n')
    # book.write('\\textbf{Metadata:} ID: ' + file_id + ' | shortcut: ' + shortcut + ' | author: ' + username + ' | date: ' + date.strftime('%Y-%m-%d, %H:%M') + '.\n')
    # book.write('\\vspace{1em}\n')
    book.write('\n\n\n')
        
# Open "Appendix"
#-----------------------------------------------------------------------------#
book.write('% Appendix %\n')
book.write('\\chapter{Appendix} \\label{sec:Appendix} \\newpage\n\n')

# Write "Proof by Number"
#-----------------------------------------------------------------------------#
book.write('\\pagebreak\n')
book.write('\\section{Proof by Number}\n\n')
book.write('\\begin{longtable}{|p{1cm}|p{2cm}|p{6.5cm}|p{3cm}|p{2cm}|c|}\n')
book.write('\\hline\n')
book.write('\\textbf{ID} & \\textbf{Shortcut} & \\textbf{Theorem} & \\textbf{Author} & \\textbf{Date} & \\textbf{Page} \\\\ \\hline\n')
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(pr_ids)])]
for i in sort_ind:
    if pr_ids[i] != 0:
        book.write(pr_infos[i]['proof_id'] + ' & ' + \
                   pr_infos[i]['shortcut'] + ' & ' + \
                   pr_infos[i]['title'] + ' & ' + \
                   pr_infos[i]['username'] + ' & ' + \
                   pr_infos[i]['date'].strftime('%Y-%m-%d') + ' & ' + \
                   '\\pageref{sec:' + pr_infos[i]['shortcut'] + '} \\\\ \\hline\n')
book.write('\\end{longtable}\n')
book.write('\n\n\n')

# Write "Definition by Number"
#-----------------------------------------------------------------------------#
book.write('\\pagebreak\n')
book.write('\\section{Definition by Number}\n\n')
book.write('\\begin{longtable}{|p{1cm}|p{2cm}|p{6.5cm}|p{3cm}|p{2cm}|c|}\n')
book.write('\\hline\n')
book.write('\\textbf{ID} & \\textbf{Shortcut} & \\textbf{Definition} & \\textbf{Author} & \\textbf{Date} & \\textbf{Page} \\\\ \\hline\n')
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(def_ids)])]
for i in sort_ind:
    if def_ids[i] != 0:
        book.write(def_infos[i]['def_id'] + ' & ' + \
                   def_infos[i]['shortcut'] + ' & ' + \
                   def_infos[i]['title'] + ' & ' + \
                   def_infos[i]['username'] + ' & ' + \
                   def_infos[i]['date'].strftime('%Y-%m-%d') + ' & ' + \
                   '\\pageref{sec:' + def_infos[i]['shortcut'] + '} \\\\ \\hline\n')
book.write('\\end{longtable}\n')
book.write('\n\n\n')

# Write "Proof by Topic"
#-----------------------------------------------------------------------------#
book.write('\\pagebreak\n')
book.write('\\section{Proof by Topic}\n\n')
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(pr_titles)])]
lett_one = '0'
for i in sort_ind:
    if pr_ids[i] != 0:
        if pr_titles[i][0] != lett_one:
            if lett_one != '0': book.write('\n\\vspace{1em}\n')
            book.write('\\textbf{' + pr_titles[i][0].upper() + '}\n\n')
        book.write('$\\bullet$ ' + pr_infos[i]['title'] + ', \\pageref{sec:' + pr_infos[i]['shortcut'] + '}\n\n')
        lett_one = pr_titles[i][0]
book.write('\n\n')

# Write "Definition by Topic"
#-----------------------------------------------------------------------------#
book.write('\\pagebreak\n')
book.write('\\section{Definition by Topic}\n\n')
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(def_titles)])]
lett_one = '0'
for i in sort_ind:
    if def_ids[i] != 0:
        if def_titles[i][0] != lett_one:
            if lett_one != '0': book.write('\n\\vspace{1em}\n')
            book.write('\\textbf{' + def_titles[i][0].upper() + '}\n\n')
        book.write('$\\bullet$ ' + def_infos[i]['title'] + ', \\pageref{sec:' + def_infos[i]['shortcut'] + '}\n\n')
        lett_one = def_titles[i][0]
book.write('\n')

# Close "The Book of Statistical Proofs"
#-----------------------------------------------------------------------------#
book.write('\end{document}')
book.close()
print('   - written into "' + book.name + '"')