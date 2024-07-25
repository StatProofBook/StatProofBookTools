#!/usr/bin/env python
"""
Transfer Proof from LaTeX File to Markdown Document
_
This script takes a proof written in LaTeX and transfers it into a Markdown
file (almost) ready for submission to the StatProofBook.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2023-09-01 13:40:00
 Last edit: 2023-10-20 11:39:00
"""


# Specify proofs
#-----------------------------------------------------------------------------#
temp_proof = 'mlr-mll'
# This is the Markdown (.md) document in the StatProofBook which should be used
# as a template for your proof. It should be in repository sub-folder "/P/".
src_proof  = 'mlr-llr'
# This is the LaTeX (.tex) document in src_dir which contains your proof.
# LaTeX should be between "\begin{document}" and "\end{document}".
src_dir    =r'C:\Users\sochj\ownCloud\StatProofBook\Submissions\JoramSoch\Proofs'
# This is the folder in which src_proof is located and the result will be saved.

# Import modules
#-----------------------------------------------------------------------------#
import re
import webbrowser
import BookTools as spbt
from datetime import datetime

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')

# Load source proof
#-----------------------------------------------------------------------------#
file_tex = src_dir+'/'+src_proof+'.tex'
file_obj = open(file_tex, 'r')
file_txt = file_obj.readlines()
file_obj.close()

# Analyze source proof
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

# Load template proof
#-----------------------------------------------------------------------------#
file_md  = rep_dir+'/P/'+temp_proof+'.md'
file_obj = open(file_md, 'r')
file_txt = file_obj.readlines()
file_obj.close()

# Analyze template proof
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

# Write new proof header
#-----------------------------------------------------------------------------#
proof_md = ['---\n',
            'layout: proof\n',
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
            'theorem: "___"\n',
            '\n',
            'sources:\n',
            '\n',
            'proof_id: "___"\n',
            'shortcut: "'+src_proof+'"\n',
            'username: "'+username+'"\n',
            '---\n',
            '\n',
            '\n']

# Write new proof body
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
    # append current line to proof body
    proof_md.append(line)

# Save and open new proof
#-----------------------------------------------------------------------------#
file_md  = src_dir+'/'+src_proof+'.md'
file_obj = open(file_md, 'w')
for line in proof_md:
    file_obj.write(line)
file_obj.close()
webbrowser.open(file_md)