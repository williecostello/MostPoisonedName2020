import pandas as pd



print('Loading data...')

# Read in data
df_raw = pd.read_csv('data/babynames.csv', names=['year', 'name', 'sex', 'count'])

# Define year range in dataset
years = df_raw['year'].unique()
year_range = (years[0], years[-1])

# Create a dataframe listing yearly count of all unique names, regardless of birth sex
df_all = df_raw.groupby(['year', 'name'])['count'].sum()
df_all = df_all.reset_index()



# Sort new dataframe so that each year's names are listed in descending order of their counts
print('Sorting data...')

# Initialize empty dataframe
df_count = pd.DataFrame()

# Loop through each year in dataset
for year in years:
    
    # Grab data for the selected year
    df_year = df_all[df_all['year']==year]
    
    # Sort data by count in descending order
    df_year = df_year.sort_values('count', ascending=False)
    
    # Add sorted data to master dataframe
    df_count = df_count.append(df_year, ignore_index=True)



# Perform various calculations on data
print('Crunching data...')

# Create a pivot table listing the count of each name for each year
df_pivot = pd.pivot_table(df_count, values='count', index='year', columns='name')

# Calculate total count of baby names per year
year_totals = df_pivot.sum(axis=1)

# Divide name count by total yearly count
df_pcts = df_pivot.divide(year_totals, axis=0)

# Calculate the percent change in each name's yearly percentage since the preceding year 
df_pctchg = df_pcts.pct_change()

# Unpivot the percent change dataframe
df_pctchg_melt = df_pctchg.reset_index().melt(id_vars='year', value_name='loss')

# Calculate the 2-year percent change in yearly percentage
df_pctchg_2 = df_pcts.pct_change(periods=2)

# Unpivot the 2-year percent change dataframe
df_pctchg_2_melt = df_pctchg_2.reset_index().melt(id_vars='year', value_name='loss_2')



# Create a master dataframe
print('Concatenating data...')

# Make a copy of the original female baby names dataframe
df_a = df_count.copy()

# Unpivot the percentages dataframe
df_b = df_pcts.reset_index().melt(id_vars='year', value_name='percent')

# Add columns for the 1-year, 2-year, and 5-year percent change
df_b['loss'] = df_pctchg_melt['loss']
df_b['loss_2'] = df_pctchg_2_melt['loss_2']

# Change the index of these dataframe to each row's name/year pair
df_a.index = df_a['name'] + '_' + df_a['year'].astype(str)
df_b.index = df_b['name'] + '_' + df_b['year'].astype(str)

# Join the dataframes together
df = df_a.join(df_b[['percent', 'loss', 'loss_2']])



# Add cumulative sum column
print('Crunching more data...')

# Initialize empty series
cumsum_col = pd.Series(name='cumsum', dtype='float64')

# Loop through each year in dataset
for year in years:

    # Grab data for the selected year
    df_year = df[df['year']==year]
    
    # Calculate the cumulative sum of the percentage values for that year
    cumsum_year = df_year['percent'].cumsum()
    
    # Append the series to master list
    cumsum_col = cumsum_col.append(cumsum_year)
    
# Add cumsum column to master dataframe
df['cumsum'] = cumsum_col



# Add columns listing each name's cumulative sum value from two & ten years prior

# Create a pivot table listing the cumulative sum of each name for each year
df_cumsum_pivot = pd.pivot_table(df, values='cumsum', index='year', columns='name')

# Change value to name's cumulative sum value from two / ten years prior
df_cumsum_pivot_lag_2 = df_cumsum_pivot.shift(periods=2)
df_cumsum_pivot_lag_10 = df_cumsum_pivot.shift(periods=10)

# Unpivot the 2- / 10-years-prior cumulative sum dataframes
df_cumsum_lag_2 = df_cumsum_pivot_lag_2.reset_index().melt(id_vars='year', value_name='cumsum_lag_2')
df_cumsum_lag_10 = df_cumsum_pivot_lag_10.reset_index().melt(id_vars='year', value_name='cumsum_lag_10')

# Combine these dataframes into a single dataframe
df_c = df_cumsum_lag_2.copy()
df_c['cumsum_lag_10'] = df_cumsum_lag_10['cumsum_lag_10']

# Change the index of this dataframe to each row's name/year pair
df_c.index = df_c['name'] + '_' + df_c['year'].astype(str)

# Join new columns to master dataframe
df = df.join(df_c[['cumsum_lag_2', 'cumsum_lag_10']])



# Write dataframes to file
print('Saving data...')

df.to_csv('data/babynames_stats.csv')
print('babynames_stats.csv saved!')

df_pcts.to_csv('data/babynames_pcts.csv')
print('babynames_pcts.csv saved!')

df_pcts.dropna(axis=1, thresh=10).to_csv('data/babynames_pcts_abrg.csv')
print('babynames_pcts_abrg.csv saved!')