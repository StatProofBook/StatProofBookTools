#!/usr/bin/env python
"""
Tweet Random Proofs from the StatProofBook
_
This script generates a list of random proofs from the StatProofBook,
one proof per day, without repetition within a year, and then saves
this list into an MS Office Excel sheet.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2024-01-01 17:13:00
 Last edit: 2024-01-01 17:13:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import random
import webbrowser
import pandas as pd
import BookTools as spbt
from datetime import datetime, timedelta

# Set year to generate for
#-----------------------------------------------------------------------------#
year = 2023                     # enter 0 for current year

# List files in proof directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')
files   = os.listdir(rep_dir + '/P/')
files   = [file for file in files if not file.startswith('-temp-')]
proofs  = []

# Browse through list of files
#-----------------------------------------------------------------------------#
for file in files:
    
    # Read proof text
    #-------------------------------------------------------------------------#
    file_obj = open(rep_dir + '/P/' + file, 'r')
    file_txt = file_obj.readlines()
    file_obj.close()
    
    # Get proof info
    #-------------------------------------------------------------------------#
    proof_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
    proofs.append({'proof_id': proof_id, 'shortcut': shortcut, 'title': title, \
                   'username': username, 'date': date})
    del file_obj, file_txt, proof_id, shortcut, title, username, date

# Collect eligible proofs and randomize
#-----------------------------------------------------------------------------#
if year == 0:
    dt = datetime.today()
    ys = dt.year
    year = ys
else:
    ys = year
d0 = datetime(ys, 1, 1)
proofs = [proof for proof in proofs if proof['date']<d0]
random.seed(ys)
random.shuffle(proofs)

# Prepare for generating schedule
#-----------------------------------------------------------------------------#
days       = []
dates1     = []
dates2     = []
proof_ids  = []
shortcuts  = []
tweet_txts = []

# Create schedule for selected year
#-----------------------------------------------------------------------------#
date = d0
while date.year == ys:
    
    # get day index and current date
    #-------------------------------------------------------------------------#
    i   = (date-d0).days
    day = i + 1
    days.append(day)
    dates1.append(date.strftime('%Y-%m-%d'))
    dates2.append(date.strftime('%A, %B %d, %Y'))
    
    # get proof details and tweet text
    #-------------------------------------------------------------------------#
    proof = proofs[i]
    proof_ids.append(proof['proof_id'])
    shortcuts.append(proof['shortcut'])
    tweet_txt = 'Proof #{}: "{}" ({}) #RandomProof\nhttps://statproofbook.github.io/P/{}'
    tweet_txt = tweet_txt.format(proof['proof_id'][1:], proof['title'], proof['shortcut'], proof['shortcut'])
    tweet_txts.append(tweet_txt)
    
    # continue to next day
    #-------------------------------------------------------------------------#
    date = date + timedelta(days=1)

# Clean up after scheduling
#-----------------------------------------------------------------------------#
proofs = proofs[:day]
del i, day, date, proof, tweet_txt

# Save schedule to file
#-----------------------------------------------------------------------------#
data = zip(days, dates1, dates2, proof_ids, shortcuts, tweet_txts)
cols = ['Day', 'Short Date', 'Long Date', 'Proof ID', 'Shortcut', 'Tweet Text']
df   = pd.DataFrame(data, columns=cols)
filename = 'tweet_proofs/Random_Proofs_'+str(year)+'.xlsx'
df.to_excel(filename, index=False)

# Open proof schedule
#-----------------------------------------------------------------------------#
filename = os.path.abspath(filename)
webbrowser.open(filename)