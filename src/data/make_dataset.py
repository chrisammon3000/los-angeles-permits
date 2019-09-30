# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')

import os
print(os.listdir('..'))
import sys

from urllib.request import urlretrieve

filename = 'Building_and_Safety_Permit_Information.csv'
url = 'https://data.lacity.org/api/views/yv23-pmwf/rows.csv'

# Check if dataset is presemt
if filename not in os.listdir('../data/raw/'):
    url = 'https://data.lacity.org/api/views/yv23-pmwf/rows.csv'
    #urlretrieve(url, filename)
    print(os.listdir('../data/raw/'))
