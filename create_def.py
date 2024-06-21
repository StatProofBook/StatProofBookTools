#!/usr/bin/env python
"""
Transfer Definition from LaTeX File to Markdown Document
_
This script takes a definition written in LaTeX and transfers it into a
Markdown file (almost) ready for submission to the StatProofBook.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2023-09-22 10:55:00
 Last edit: 2024-03-15 11:31:00
"""


# Specify definitions
#-----------------------------------------------------------------------------#
temp_def = 'llf'
# This is the Markdown (.md) document in the StatProofBook which should be used
# as a template for your definition. It should be in repository sub-folder "/D/".
src_def  = 'llr'
# This is the LaTeX (.tex) document in src_dir which contains your definition.
# LaTeX should be between "\begin{document}" and "\end{document}".
src_dir  =r'C:\Users\sochj\ownCloud\StatProofBook\Submissions\JoramSoch\Definitions'

# Import modules
#-----------------------------------------------------------------------------#
import re
import webbrowser
import BookTools as spbt
from datetime import datetime

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')

# Load source definition
#-----------------------------------------------------------------------------#
file_tex = src_dir+'/'+src_def+'.tex'
file_obj = open(file_tex, 'r')
file_txt = file_obj.readlines()
file_obj.close()

# Analyze source definition
#-----------------------------------------------------------------------------#
begin = False
i1 = 0; i2 = 0;
for (i, line) in enumerate(file_txt):
    if len(line) > 1:
        if begin == True and i1 == 0:
            i1 = i
        if i1 > 0 and line.find('\\end{document}') < 0:
            i2 = i
    if line.find('\\begin{document}') > -1:
        begin = True
body_txt = file_txt[i1:i2+1]

# Load template definition
#-----------------------------------------------------------------------------#
file_md  = rep_dir+'/D/'+temp_def+'.md'
file_obj = open(file_md, 'r')
file_txt = file_obj.readlines()
file_obj.close()

# Analyze template definition
#-----------------------------------------------------------------------------#
file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
chapter, section, topic, item            = spbt.get_toc_info(file_txt)
i1 = 0; i2 = 0; i3 = 0;
for (i, line) in enumerate(file_txt):
    if line.find('author:') > -1:
        i1 = i
    if line.find('affiliation:') > -1:
        i2 = i
    if line.find('e_mail:') > -1:
        i3 = i

# Write new definition header
#-----------------------------------------------------------------------------#
def_md = ['---\n',
          'layout: definition\n',
          'mathjax: true\n',
          '\n',
          file_txt[i1],
          file_txt[i2],
          file_txt[i3],
          'date: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n',
          '\n',
          'title: "___"\n',
          'chapter: "'+chapter+'"\n',
          'section: "'+section+'"\n',
          'topic: "'+topic+'"\n',
          'definition: "___"\n',
          '\n',
          'sources:\n',
          '\n',
          'def_id: "___"\n',
          'shortcut: "'+src_def+'"\n',
          'username: "'+username+'"\n',
          '---\n',
          '\n',
          '\n']

# Write new definition body
#-----------------------------------------------------------------------------#
in_equation = False
for line in body_txt:
    # correct equation enviroment (\begin/end{equation} -> $$...$$)
    if not in_equation and line.find('\\begin{equation}') == 0:
        line = re.sub('\\\\begin{equation}', '$$', line)
        in_equation = True
    if in_equation and line.find('\\end{equation}') == 0:
        line = re.sub('\\\\end{equation}', '$$', line)
        in_equation = False
    # append current line to definition body
    def_md.append(line)

# Save and open new definition
#-----------------------------------------------------------------------------#
file_md  = src_dir+'/'+src_def+'.md'
file_obj = open(file_md, 'w')
for line in def_md:
    file_obj.write(line)
file_obj.close()
webbrowser.open(file_md)