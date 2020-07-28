#!/usr/bin/env python
"""
Display content in the StatProofBook
_
This script loads all content from the proof and definition directories and
visualizes proof and definition numbers over time.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2020-04-15 18:15:00
 Last edit: 2020-07-28 07:36:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import BookTools as spbt
import matplotlib.pyplot as plt
from datetime import date
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
        
        # Get proof date
        #---------------------------------------------------------------------#
        file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
        P_ids.append(file_id)
        P_dates.append(date)

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
        
        # Get proof date
        #---------------------------------------------------------------------#
        file_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
        D_ids.append(file_id)
        D_dates.append(date)

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

# Pie chart
#-----------------------------------------------------------------------------#
plt.figure(figsize=(12,10))
plt.pie([len(D_ids)-1, len(P_ids)-1], labels=['Definitions', 'Proofs'], colors=['b', 'r'],
         autopct=lambda p: '{:.0f}'.format(p * sum([len(D_ids)-1, len(P_ids)-1]) / 100),
         startangle=90, shadow=False, textprops=dict(fontsize=24))
plt.axis('equal')
plt.title('StatProofBook Content', fontsize=32)
plt.savefig('display_content/Content.png')
plt.show()

# Line plot
#-----------------------------------------------------------------------------#
plt.figure(figsize=(16,9))
h1 = plt.plot(x2, y2, 'b-', linewidth=2)
h2 = plt.plot(x1, y1, 'r-', linewidth=2)
plt.axis([0, T, -0.1, +(11/10)*max([max(P_no), max(D_no)])])
plt.grid(True)
plt.xlabel('days since inception of the StatProofBook (August 26, 2019)', fontsize=16)
plt.ylabel('number of proofs and definitions available', fontsize=16)
plt.title('Development over Time', fontsize=32)
plt.legend((h1[0], h2[0]), ('Definitions', 'Proofs'), loc='upper left')
plt.savefig('display_content/Development.png')
plt.show()