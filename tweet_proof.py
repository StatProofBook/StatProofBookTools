#!/usr/bin/env python
"""
Tweet New Proof from the StatProofBook
_
This script generates and ouputs a tweet text for posting a new proof,
given only the proof shortcut (e.g. "mvn-ltt").

It can be called from the command line as
    tweet_proof [shortcut]
or, e.g. within Spyder, as
    runfile('tweet_proof.py', args='glm-mi')

Author: Joram Soch, OvGU Magdeburg
E-Mail: joram.soch@ovgu.de

First edit: 2024-06-21 12:19:00
 Last edit: 2024-06-21 12:19:00
"""


# Import modules
#-----------------------------------------------------------------------------#
from sys import argv
import BookTools as spbt

# Get function argument
#-----------------------------------------------------------------------------#
try:
    script, shortcut = argv
except ValueError:
    shortcut = '-temp-'

# Load requested proof
#-----------------------------------------------------------------------------#
rep_dir  = spbt.get_rep_dir('offline')
filename = rep_dir + '/P/' + shortcut + '.md'
file_obj = open(filename, 'r')
file_txt = file_obj.readlines()
file_obj.close()

# Extract and print
#-----------------------------------------------------------------------------#
proof_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
tweet_txt = 'Proof #{}: "{}" ({}) #NewProof\nhttps://statproofbook.github.io/P/{}'
tweet_txt = tweet_txt.format(proof_id[1:], title, shortcut, shortcut)
print('\n'+tweet_txt)