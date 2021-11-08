#!/usr/bin/env python
"""
Display content in the StatProofBook
_
This script loads all content via the table of contents and visualizes
(i) Content by Type, (ii) Development over Time as well as
(iii) Proof and Definition by Topic.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-04-15 18:15:00
 Last edit: 2021-11-08 22:59:00
"""


# Import modules
#-----------------------------------------------------------------------------#
# import os
import BookTools as spbt
import matplotlib.pyplot as plt
from datetime import datetime

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')
plt.close('all')

# Prepare date information
#-----------------------------------------------------------------------------#
P_ids   = []
D_ids   = []
P_dates = []
D_dates = []

# Prepare ToC information
#-----------------------------------------------------------------------------#
P_chs  = []
D_chs  = []
P_secs = []
D_secs = []

# Load "Table of Contents"
#-----------------------------------------------------------------------------#
toc_md  = '/I/ToC.md'
toc_obj = open(rep_dir + toc_md, 'r')
toc_txt = toc_obj.readlines()
toc_obj.close()

# Browse through files
#-----------------------------------------------------------------------------#
files_checked     = []
nums, tocs, files = spbt.get_all_items(toc_txt)
for file in files:
    if '.md' in file and file not in files_checked:
        
        # Read proof/definition
        #---------------------------------------------------------------------#
        file_obj = open(rep_dir + file, 'r')
        file_txt = file_obj.readlines()
        file_obj.close()
        
        # Get date and info
        #---------------------------------------------------------------------#
        file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
        chapter, section, topic, item            = spbt.get_toc_info(file_txt)
        if file.find('/P/') > -1:
            P_ids.append(file_id)
            P_dates.append(date)
            P_chs.append(chapter)
            P_secs.append(section)
        if file.find('/D/') > -1:
            D_ids.append(file_id)
            D_dates.append(date)
            D_chs.append(chapter)
            D_secs.append(section)
        files_checked.append(file)

# Calculate date differences
#-----------------------------------------------------------------------------#
d0     = datetime(2019,8,26,0,0,0)          # day of inception of StatProofBook
dt     = datetime.today()                   # day and time today and now
T      = (dt-d0).days
t      = range(0,T+1)
P_days = [(d-d0).days for d in P_dates]
D_days = [(d-d0).days for d in D_dates]
P_no   = [sum(i <= x for i in P_days) for x in t]
D_no   = [sum(i <= x for i in D_days) for x in t]

# Generate x and y for plot
#-----------------------------------------------------------------------------#
x1 = [0]
x2 = [0]
y1 = [0]
y2 = [0]
for i,x in enumerate(t):
    if i > 0:
        if P_no[i] != P_no[i-1]:
            x1.append(x)
            y1.append(max(y1))
            x1.append(x)
            y1.append(P_no[i])
        if D_no[i] != D_no[i-1]:
            x2.append(x)
            y2.append(max(y2))
            x2.append(x)
            y2.append(D_no[i])
x1.append(T)
y1.append(max(y1))
x2.append(T)
y2.append(max(y2))

# Calculate ToC proportions
#-----------------------------------------------------------------------------#
ch_labels = ['General Theorems', 'Probability Distributions', 'Statistical Models', 'Model Selection']
D_labels  = [None] * len(ch_labels)
P_labels  = [None] * len(ch_labels)
D_ch_num  = [0] * len(ch_labels)
P_ch_num  = [0] * len(ch_labels)
D_sec_num = [None] * len(ch_labels)
P_sec_num = [None] * len(ch_labels)
for i,li in enumerate(ch_labels):
    D_ch_num[i]  = D_chs.count(li)
    P_ch_num[i]  = P_chs.count(li)
    D_secs_i     = [b for a,b in zip(D_chs,D_secs) if a==li]
    P_secs_i     = [b for a,b in zip(P_chs,P_secs) if a==li]
    D_seen_i     = set()
    P_seen_i     = set()
    D_labels[i]  = [x for x in D_secs_i if not (x in D_seen_i or D_seen_i.add(x))]
    P_labels[i]  = [x for x in P_secs_i if not (x in P_seen_i or P_seen_i.add(x))]
    D_sec_num[i] = [0] * len(D_labels[i])
    P_sec_num[i] = [0] * len(P_labels[i])
    for j,lj in enumerate(D_labels[i]):
        D_sec_num[i][j] = D_secs_i.count(lj)
    for j,lj in enumerate(P_labels[i]):
        P_sec_num[i][j] = P_secs_i.count(lj)

# Pie chart (Content by Type)
#-----------------------------------------------------------------------------#
plt.figure(figsize=(12,10))
plt.pie([len(D_ids), len(P_ids)], labels=['Definitions', 'Proofs'], colors=['#0044FF', '#FF4400'],
         autopct=lambda p: '{:.0f}'.format(p * sum([len(D_ids), len(P_ids)]) / 100),
         startangle=90, shadow=False, textprops=dict(fontsize=24))
plt.axis('equal')
plt.title('Content by Type', fontsize=32)
plt.savefig('display_content/Content.png')
plt.show()

# Pie charts (Proofs by Topic)
#-----------------------------------------------------------------------------#
ch_sp  = [1,4,6,3]
ch_col = ['#0000FF', '#FF0000', '#00FF00', '#FFFF00']
plt.figure(figsize=(16,9))
plt.subplot(1,3,2)
plt.pie(P_ch_num, labels=ch_labels, colors=ch_col,
        autopct=lambda p: '{:.0f}'.format(p * sum(P_ch_num) / 100),
        startangle=90, shadow=False, textprops=dict(fontsize=12))
plt.axis('equal')
plt.title('Proofs by Topic', fontsize=32)
for i,li in enumerate(ch_labels):
    plt.subplot(2,3,ch_sp[i])
    plt.pie(P_sec_num[i], labels=P_labels[i], colors=[ch_col[i]],
            wedgeprops={'edgecolor': 'k', 'linewidth': 1},
            autopct=lambda p: '{:.0f}'.format(p * sum(P_sec_num[i]) / 100),
            startangle=90, shadow=False, textprops=dict(fontsize=8))
    plt.axis('equal')
    plt.title(ch_labels[i], fontsize=12)
plt.savefig('display_content/Topic_Proofs.png')
plt.show()

# Pie charts (Definitions by Topic)
#-----------------------------------------------------------------------------#
plt.figure(figsize=(16,9))
plt.subplot(1,3,2)
plt.pie(D_ch_num, labels=ch_labels, colors=ch_col,
        autopct=lambda p: '{:.0f}'.format(p * sum(D_ch_num) / 100),
        startangle=90, shadow=False, textprops=dict(fontsize=12))
plt.axis('equal')
plt.title('Definitions by Topic', fontsize=32)
for i,li in enumerate(ch_labels):
    plt.subplot(2,3,ch_sp[i])
    plt.pie(D_sec_num[i], labels=D_labels[i], colors=[ch_col[i]],
            wedgeprops={'edgecolor': 'k', 'linewidth': 1},
            autopct=lambda p: '{:.0f}'.format(p * sum(D_sec_num[i]) / 100),
            startangle=90, shadow=False, textprops=dict(fontsize=8))
    plt.axis('equal')
    plt.title(ch_labels[i], fontsize=12)
plt.savefig('display_content/Topic_Definitions.png')
plt.show()

# Line plot (Development over Time)
#-----------------------------------------------------------------------------#
plt.figure(figsize=(16,9))
h1 = plt.plot(x2, y2, 'b-', linewidth=2, color='#0044FF')
h2 = plt.plot(x1, y1, 'r-', linewidth=2, color='#FF4400')
plt.axis([0, T, -0.1, +(11/10)*max([max(P_no), max(D_no)])])
plt.grid(True)
plt.xlabel('days since inception of the StatProofBook (August 26, 2019)', fontsize=16)
plt.ylabel('number of proofs and definitions available', fontsize=16)
plt.title('Development over Time', fontsize=32)
plt.legend((h1[0], h2[0]), ('Definitions', 'Proofs'), loc='upper left')
plt.savefig('display_content/Development.png')
plt.show()