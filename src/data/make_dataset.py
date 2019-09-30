# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')

import os
import sys

from urllib.request import urlretrieve

filename = 'Building_and_Safety_Permit_Information.csv'
url = 'https://data.lacity.org/api/views/yv23-pmwf/rows.csv'

# Check if dataset is presemt
if filename not in os.listdir('./data/raw/'):
    print("downloading...")
    url = 'https://data.lacity.org/api/views/yv23-pmwf/rows.csv'
    #urlretrieve(url, filename)
    print(os.listdir('./data/raw/'))

# Import CSV
df = pd.read_csv('./data/raw/'+filename, parse_dates=["Issue Date", "Status Date"])
df.index.names = ['Index']

# Replace whitespace with underscore
df.columns = df.columns.str.replace(' ', '_')

# Replace hyphen with underscore
df.columns = df.columns.str.replace('-', '_')

# Replace hashtag with No (short for number)
df.columns = df.columns.str.replace('#', 'No')

# Replace forward slash with underscore
df.columns = df.columns.str.replace('/', '_')

# Remove period
df.columns = df.columns.str.replace('.', '')

# Remove open parenthesis
df.columns = df.columns.str.replace('(', '')

# Remove closed parenthesis
df.columns = df.columns.str.replace(')', '')

# Remove apostrophe
df.columns = df.columns.str.replace("'", '')

# Write out to disk
df.to_csv('./data/interim/'+filename)
