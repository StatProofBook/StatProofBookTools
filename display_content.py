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
 Last edit: 2025-12-19 17:46:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import numpy as np
import BookTools as spbt
import matplotlib.pyplot as plt
from datetime import datetime

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')

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
        if file.startswith('/P/'):
            P_ids.append(file_id)
            P_dates.append(date)
            P_chs.append(chapter)
            P_secs.append(section)
        if file.startswith('/D/'):
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
t      = np.arange(0,T+1)
P_days = np.array([(d-d0).days for d in P_dates])
D_days = np.array([(d-d0).days for d in D_dates])
P_no   = np.array([np.sum(P_days <= x) for x in t])
D_no   = np.array([np.sum(D_days <= x) for x in t])

# Generate x and y for plot
#-----------------------------------------------------------------------------#
x1 = [0]
x2 = [0]
y1 = [0]
y2 = [0]
for i in t:
    if i > 0:
        if P_no[i] != P_no[i-1]:
            x1.extend([i, i])
            y1.extend([np.max(y1), P_no[i]])            
        if D_no[i] != D_no[i-1]:
            x2.extend([i, i])
            y2.extend([np.max(y2), D_no[i]])
    if i == T:
        x1.append(i)
        y1.append(np.max(y1))
        x2.append(i)
        y2.append(np.max(y2))
x1 = np.array(x1)
x2 = np.array(x2)
y1 = np.array(y1)
y2 = np.array(y2)

# Calculate ToC proportions
#-----------------------------------------------------------------------------#
ch_labels = ['General Theorems', 'Probability Distributions', 'Statistical Models', 'Model Selection']
D_ch_num  = np.zeros(len(ch_labels))
P_ch_num  = np.zeros(len(ch_labels))
D_sec_num = [None] * len(ch_labels)
P_sec_num = [None] * len(ch_labels)
for i,li in enumerate(ch_labels):
    D_ch_num[i]  = D_chs.count(li)
    P_ch_num[i]  = P_chs.count(li)
    D_secs_i     = [b for a,b in zip(D_chs,D_secs) if a==li]
    P_secs_i     = [b for a,b in zip(P_chs,P_secs) if a==li]
    D_seen_i     = set()
    P_seen_i     = set()
    D_labels_i   = [x for x in D_secs_i if not (x in D_seen_i or D_seen_i.add(x))]
    P_labels_i   = [x for x in P_secs_i if not (x in P_seen_i or P_seen_i.add(x))]
    D_counts_i   = np.zeros(len(D_labels_i))
    P_counts_i   = np.zeros(len(P_labels_i))
    for j,lj in enumerate(D_labels_i):
        D_counts_i[j] = D_secs_i.count(lj)
    for j,lj in enumerate(P_labels_i):
        P_counts_i[j] = P_secs_i.count(lj)
    D_sec_num[i] = {'labels': D_labels_i, 'counts': D_counts_i}
    P_sec_num[i] = {'labels': P_labels_i, 'counts': P_counts_i}
del D_secs_i, P_secs_i, D_labels_i, P_labels_i, D_counts_i, P_counts_i

# Label function for pie charts
#-----------------------------------------------------------------------------#
def pie_counts(N):
    def my_autopct(p):
        return '{:.0f}'.format(p * sum(N) / 100)
    return my_autopct
ch_sp  = [1,4,6,3]
ch_col = ['#0000FF', '#FF0000', '#00FF00', '#FFFF00']

# Date labels for line plot
#-----------------------------------------------------------------------------#
years = np.arange(2020, dt.year+1)
days  = np.zeros(years.size)
dates = [None] * years.size
for i,year in enumerate(years):
    dy       = datetime(year,1,1,0,0,0)
    days[i]  = (dy-d0).days
    dates[i] = '01.01.'+str(year)

# Pie chart (Content by Type)
#-----------------------------------------------------------------------------#
fig = plt.figure(figsize=(16,9))
ax  = fig.add_subplot(111)
ax.pie([len(D_ids), len(P_ids)], labels=['Definitions', 'Proofs'],
       colors=['#0044FF', '#FF4400'], autopct=pie_counts([len(D_ids), len(P_ids)]),
       startangle=90, shadow=False, textprops=dict(fontsize=24))
ax.axis('equal')
ax.set_title('Content by Type', fontsize=32)
fig.savefig('display_content/Content.png', dpi=150, transparent=True)

# Pie charts (Proofs by Topic)
#-----------------------------------------------------------------------------#
fig    = plt.figure(figsize=(16,9))
axs    = fig.subplots(1,3)
axs[1].pie(P_ch_num, labels=ch_labels,
           colors=ch_col, autopct=pie_counts(P_ch_num), 
           startangle=90, shadow=False, textprops=dict(fontsize=12))
axs[1].axis('equal')
axs[0].axis('off'); axs[2].axis('off');
axs[1].set_title('Proofs by Topic', fontsize=32)
axs    = fig.subplots(2,3)
for i,li in enumerate(ch_labels):
    j = int(np.ceil(ch_sp[i]/3))-1
    k = (ch_sp[i] % 3)-1
    if k == -1: k = 2
    axs[j,k].pie(P_sec_num[i]['counts'], labels=P_sec_num[i]['labels'],
                 colors=[ch_col[i]], wedgeprops={'edgecolor': 'k', 'linewidth': 1},
                 autopct=pie_counts(P_sec_num[i]['counts']), 
                 startangle=90, shadow=False, textprops=dict(fontsize=8))
    axs[j,k].axis('equal')
    axs[j,k].set_title(ch_labels[i], fontsize=12)
axs[0,1].axis('off'); axs[1,1].axis('off')
fig.savefig('display_content/Topic_Proofs.png', dpi=150, transparent=True)

# Pie charts (Definitions by Topic)
#-----------------------------------------------------------------------------#
fig    = plt.figure(figsize=(16,9))
axs    = fig.subplots(1,3)
axs[1].pie(D_ch_num, labels=ch_labels,
           colors=ch_col, autopct=pie_counts(D_ch_num), 
           startangle=90, shadow=False, textprops=dict(fontsize=12))
axs[1].axis('equal')
axs[0].axis('off'); axs[2].axis('off');
axs[1].set_title('Definitions by Topic', fontsize=32)

axs    = fig.subplots(2,3)
for i,li in enumerate(ch_labels):
    j = int(np.ceil(ch_sp[i]/3))-1
    k = (ch_sp[i] % 3)-1
    if k == -1: k = 2
    axs[j,k].pie(D_sec_num[i]['counts'], labels=D_sec_num[i]['labels'],
                 colors=[ch_col[i]], wedgeprops={'edgecolor': 'k', 'linewidth': 1},
                 autopct=pie_counts(D_sec_num[i]['counts']), 
                 startangle=90, shadow=False, textprops=dict(fontsize=8))
    axs[j,k].axis('equal')
    axs[j,k].set_title(ch_labels[i], fontsize=12)
axs[0,1].axis('off'); axs[1,1].axis('off')
fig.savefig('display_content/Topic_Definitions.png', dpi=150, transparent=True)

# Line plot (Development over Time)
#-----------------------------------------------------------------------------#
fig = plt.figure(figsize=(16,9))
ax  = fig.add_subplot(111)
ax.plot(x2, y2, 'b-', linewidth=2, color='#0044FF', label='Definitions')
ax.plot(x1, y1, 'r-', linewidth=2, color='#FF4400', label='Proofs')
ax.axis([0, T, -1, +(21/20)*np.max([np.max(P_no), np.max(D_no)])])
ax.grid(True)
ax.set_xticks(days, labels=dates)
ax.set_xlabel('date [dd.mm.yyyy]', fontsize=20)
ax.set_ylabel('number of proofs and definitions available', fontsize=20)
ax.set_title('Development over Time', fontsize=32)
ax.tick_params(axis='both', labelsize=16)
ax.legend(loc='upper left', fontsize=16)
fig.savefig('display_content/Development.png', dpi=150, transparent=True)