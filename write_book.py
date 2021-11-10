#!/usr/bin/env python
"""
Write "The Book of Statistical Proofs"
_
This script loads all content from the proof/definition/index directories and
compiles it into a LaTeX source file that results in a PDF of the book.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-02-06 05:47:00
 Last edit: 2021-11-10 10:39:00
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

# Set proof and definition info
#-----------------------------------------------------------------------------#
pr_nos   = []
pr_tits  = []
pr_info  = []
def_nos  = []
def_tits = []
def_info = []

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
        file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
        chapter, section, topic, item            = spbt.get_toc_info(file_txt)
        sources  = spbt.get_sources(file_txt)
        body_txt = spbt.extract_body(file_txt)
        
        # Edit title for sorting
        title_edit = re.sub('[^a-zA-Z- ]', '', title)
        title_sort = title_edit.upper()
        
        # Store file information
        if is_proof:
            pr_nos.append(int(file_id[1:]))
            pr_tits.append(title_sort)
            pr_info.append([file_id, shortcut, title, username, date])
        else:
            def_nos.append(int(file_id[1:]))
            def_tits.append(title_sort)
            def_info.append([file_id, shortcut, title, username, date])
        
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
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(pr_nos)])]
for i in sort_ind:
    if pr_nos[i] != 0:
        book.write(pr_info[i][0] + ' & ' + pr_info[i][1] + ' & ' + pr_info[i][2] + ' & ' + pr_info[i][3] + ' & ' + \
                   pr_info[i][4].strftime('%Y-%m-%d') + ' & \\pageref{sec:' + pr_info[i][1] + '} \\\\ \\hline\n')
book.write('\\end{longtable}\n')
book.write('\n\n\n')

# Write "Definition by Number"
#-----------------------------------------------------------------------------#
book.write('\\pagebreak\n')
book.write('\\section{Definition by Number}\n\n')
book.write('\\begin{longtable}{|p{1cm}|p{2cm}|p{6.5cm}|p{3cm}|p{2cm}|c|}\n')
book.write('\\hline\n')
book.write('\\textbf{ID} & \\textbf{Shortcut} & \\textbf{Definition} & \\textbf{Author} & \\textbf{Date} & \\textbf{Page} \\\\ \\hline\n')
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(def_nos)])]
for i in sort_ind:
    if def_nos[i] != 0:
        book.write(def_info[i][0] + ' & ' + def_info[i][1] + ' & ' + def_info[i][2] + ' & ' + def_info[i][3] + ' & ' + \
                   def_info[i][4].strftime('%Y-%m-%d') + ' & \\pageref{sec:' + def_info[i][1] + '} \\\\ \\hline\n')
book.write('\\end{longtable}\n')
book.write('\n\n\n')

# Write "Proof by Topic"
#-----------------------------------------------------------------------------#
book.write('\\pagebreak\n')
book.write('\\section{Proof by Topic}\n\n')
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(pr_tits)])]
lett_one = '0'
for i in sort_ind:
    if pr_nos[i] != 0:
        if pr_tits[i][0] != lett_one:
            if lett_one != '0': book.write('\n\\vspace{1em}\n')
            book.write('\\textbf{' + pr_tits[i][0] + '}\n\n')
        book.write('$\\bullet$ ' + pr_info[i][2] + ', \\pageref{sec:' + pr_info[i][1] + '}\n\n')
        lett_one = pr_tits[i][0]
book.write('\n\n\n')

# Write "Definition by Topic"
#-----------------------------------------------------------------------------#
book.write('\\pagebreak\n')
book.write('\\section{Definition by Topic}\n\n')
sort_ind = [i for (v, i) in sorted([(v, i) for (i, v) in enumerate(def_tits)])]
lett_one = '0'
for i in sort_ind:
    if def_nos[i] != 0:
        if def_tits[i][0] != lett_one:
            if lett_one != '0': book.write('\n\\vspace{1em}\n')
            book.write('\\textbf{' + def_tits[i][0] + '}\n\n')
        book.write('$\\bullet$ ' + def_info[i][2] + ', \\pageref{sec:' + def_info[i][1] + '}\n\n')
        lett_one = def_tits[i][0]
book.write('\n\n\n')

# Close "The Book of Statistical Proofs"
#-----------------------------------------------------------------------------#
book.write('\end{document}')
book.close()
print('   - written into "' + book.name + '"')