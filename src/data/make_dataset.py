# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import os
from urllib.request import urlretrieve

filename = 'Building_and_Safety_Permit_Information.csv'
URL = 'https://data.lacity.org/api/views/yv23-pmwf/rows.csv'
LOCAL_PATH = './data/raw/'

def get_data(url, filename):
    # Check if dataset is presemt
    if filename not in os.listdir(LOCAL_PATH):
        # Download CSV to dataframe
        df = pd.read_csv(URL, parse_dates=["Issue Date", "Status Date"])
    # Read from local file
    df = pd.read_csv(URL, parse_dates=["Issue Date", "Status Date"])
    # Give index name
    df.index.names = ['Index']

    return df

replace_dict = [' ':'_', '-':'_', '\#':'No', '/':'_', '.':'', '(':'', ')':'']

def format_labels(df, replace_with=None):
    for key, value in replace_with.iteritems():
        df.columns = df.columns.str.replace(key, value)

    return df

permits_list = ['Issue_Date', 'Status_Date','Status',
                            'Permit_Type',
                             'Permit_Sub_Type',
                             'Permit_Category','Initiating_Office',
                             'Address_Start',
                             'Address_Fraction_Start',
                             'Address_End',
                             'Address_Fraction_End',
                             'Street_Direction',
                             'Street_Name',
                             'Street_Suffix',
                             'Suffix_Direction',
                             'Unit_Range_Start',
                             'Unit_Range_End',
                             'Zip_Code',
                             'Work_Description',
                             'Valuation', 'No_of_Residential_Dwelling_Units',
                             'No_of_Stories',
                             "Contractors_Business_Name",
                             'Contractor_City',
                             'Contractor_State',
                             'License_Type',
                             'License_No','Zone',
                             'Occupancy','Council_District',
                             'Latitude_Longitude']

permits_mask = (permits.Status == "Issued") |
                  (permits.Status == "Permit Finaled") |
                  (permits.Status == "Re-Activate Permit")


def subset_data(df):
    permits = df[permits_list]
    # Only specific permit types included in analysis
    permits = permits[permits_mask]
    # Exclude family dwellings from analysis
    permits = permits[(permits.Permit_Sub_Type != "1 or 2 Family Dwelling")]

# Create new columns Year and Month
permits["Year"] = pd.DatetimeIndex(permits["Issue_Date"]).year
permits["Month"] = pd.DatetimeIndex(permits["Issue_Date"]).month



# Convert datatype of addresses to int
permits[["Address_Start", "Address_End"]] = permits[["Address_Start",
                                                     "Address_End"]].fillna(0.0).astype(int)

# Create dictionary to correct suffixes
correct_suffix = {"EAST":"EAST", "WEST":"WEST", "NORTH":"NORTH", "SOUTH":"SOUTH",
                  "EAS":"EAST", "WES":"WEST", "NORT":"NORTH", "NOR":"NORTH",
                  "W":"WEST", "SOU":"SOUTH", "SOUT":"SOUTH", "SO":"SOUTH"}

# Apply dictionary to column
permits['Suffix_Direction'] = permits.Suffix_Direction.map(correct_suffix)

# Select street columns
street = ['Street_Direction',
 'Street_Name',
 'Street_Suffix',
 'Suffix_Direction']

# Use hyphen string as place holder for NaN values so that strings can be easily added together
permits[street] = permits[street].fillna("-")

# Add together strings Street_Direction, Street_Name and Street_Suffix
Full_Street_Name = permits.Street_Direction + " " + permits.Street_Name + " " + permits.Street_Suffix + " " + permits.Suffix_Direction

# Remove inserted hyphens and replace with no space
Full_Street_Name = Full_Street_Name.str.replace("-", "")

# Remove whitespace at end
Full_Street_Name = Full_Street_Name.str.rstrip()

# Add Full_Street_Name feature to dataset
permits["Full_Street_Name"] = Full_Street_Name

# Add Address_Start to Full_Street_Name to create new column of Full_Street_Address
permits['Full_Street_Address'] = permits['Address_Start'].astype(str) + " " + permits['Full_Street_Name']

# Add Zip Code
permits['Full_Street_Address_Zip_State'] = permits['Full_Street_Address'] + ", " + permits['Zip_Code'].fillna(0.0).astype(int).astype(str) + ", CA, USA"

# Fix whitespace
permits['Full_Street_Address_Zip_State'] = permits['Full_Street_Address_Zip_State'].str.replace(" ,", ",")

# Convert datatypes to integer
to_int = ['Zip_Code', 'No_of_Residential_Dwelling_Units', 'No_of_Stories',
          'License_No', 'Council_District']
permits[to_int] = permits[to_int].fillna(0.0).astype(int)

# Write out to disk
permits.to_csv('./data/interim/los-angeles-building-permits.csv')
