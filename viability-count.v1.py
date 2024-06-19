import numpy as np
import pandas as pd
import streamlit as st

## Functions
def flat_df(**kwargs):
  '''
  Flattens multiple 96-well plate data into lists (well A1-H12 by row) and assembles them into a dataframe.
  Parameters:  Title = data
    "Title" will be column header
    "data" is 96-well plate data in the form of a matrix that will be transformed to column
  Returns df
  '''

  #initialize dictionary
  data= {}

  #flatten input tables to lists and compile in dictionary
  for column_name, column_data in kwargs.items():
    column_data= column_data.flatten()
    data[column_name]= column_data

  #convert dictionary to df
  df= pd.DataFrame(data)

  return df

# initializing a 12 column dataframe to use as data_editor template
columns = [f'Column {i+1}' for i in range(12)]
df_template = pd.DataFrame(columns=columns)


## Streamlit app

st.title("Celigo Cell Viability and Cell Count Analysis")
st.divider()
# st.write("Paste cell line information along with the number of vials being added to inventory.")

st.write("Paste plate layout below for experimental conditions:")
edited_df_input_layout = st.data_editor(df_template, num_rows="dynamic", key= layout_editor)

st.write("Paste table below for dead cells:")
edited_df_input_dead = st.data_editor(df_template, num_rows="dynamic", key= dead_editor)

st.write("Paste table below for live cells:")
edited_df_input_live = st.data_editor(df_template, num_rows="dynamic", key= live_editor)

# Ensure numerical values for calculations
df_results["Dead"] = pd.to_numeric(df_results["Dead"], errors='coerce').fillna(0)
df_results["Live"] = pd.to_numeric(df_results["Live"], errors='coerce').fillna(0)

df_results= flat_df(Condition = edited_df_input_layout, Dead = edited_df_input_dead, Live = edited_df_input_live)  # flatten and combine tables
df_results["Viability (%)"] = (df_results["Live"]/(df_results["Live"] + df_results["Dead"])) * 100  # Add viability column

# Group by Condition and calculate mean viability
viability_summary = df_results.groupby("Condition")["Viability (%)"].mean().reset_index()

# Display results
st.write("Viability Summary:")
st.write(viability_summary)
