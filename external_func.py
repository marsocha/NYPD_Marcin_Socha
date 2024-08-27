import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def wczytaj_dane(folder, nazwa_pliku, pliki):
    pelna_nazwa = folder + '/' + nazwa_pliku
    tmp = pd.read_csv(pelna_nazwa, sep='\t')
    nazwa_bez_tsv = nazwa_pliku[:-4]  # Usunięcie '.tsv'
    A, B = nazwa_bez_tsv.split('.')
    nazwa = f"{A}_{B}"
    pliki[nazwa] = tmp

def pobierz_nazwy_plikow(folder):
    pliki = os.listdir(folder)
    pliki_tsv = [plik for plik in pliki]
    return pliki_tsv

def top_n_quality_per_regions(df, n):

    # Add a new column 'quality' calculated as averageRating * log(numVotes)
    max_votes_per_region = df.groupby('region')['numVotes'].max()

    # Step 2: Map these maximum votes back to the original DataFrame
    df['maxVotesFromThatRegion'] = df['region'].map(max_votes_per_region)

    # Step 3: Calculate the new column
    df['quality'] = df['averageRating'] * np.log(df['numVotes'] / df['maxVotesFromThatRegion'] * 100)
    
    # Create an empty DataFrame to store top n rows for each region based on quality
    top_n_quality_per_region = pd.DataFrame()
    
    # Group by 'region' and apply the operations
    grouped = df.groupby('region')
    
    for region, group in grouped:
        # Sort by 'quality' in descending order and take the top n
        top_n_quality = group.sort_values('quality', ascending=False).head(n)
        top_n_quality_per_region = pd.concat([top_n_quality_per_region, top_n_quality])
    
    # Now calculate the average of the top n quality values for each region
    region_avg_quality = top_n_quality_per_region.groupby('region')['quality'].mean()
    
    # Sort by the calculated average and take the top 10 regions
    top_10_quality_regions = region_avg_quality.sort_values(ascending=False).head(10)
    
    return top_10_quality_regions

def top_n_quality_per_regions_var(df, n):

    # Add a new column 'quality' calculated as averageRating * log(numVotes)
    max_votes_per_region = df.groupby('region')['numVotes'].max()

    # Step 2: Map these maximum votes back to the original DataFrame
    df['maxVotesFromThatRegion'] = df['region'].map(max_votes_per_region)

    # Step 3: Calculate the new column
    df['quality'] = df['averageRating'] * np.log(df['numVotes'] / df['maxVotesFromThatRegion'] * 100)
    
    # Create an empty DataFrame to store top n rows for each region based on quality
    top_n_quality_per_region = pd.DataFrame()
    
    # Group by 'region' and apply the operations
    grouped = df.groupby('region')
    
    for region, group in grouped:
        # Sort by 'quality' in descending order and take the top n
        top_n_quality = group.sort_values('quality', ascending=False).head(n)
        top_n_quality_per_region = pd.concat([top_n_quality_per_region, top_n_quality])
    
    # Now calculate the average of the top n quality values for each region
    region_avg_quality = top_n_quality_per_region.groupby('region')['quality'].mean()
    
    # Sort by the calculated average and take the top 10 regions
    top_10_quality_regions = region_avg_quality.sort_values(ascending=False).head(10)
    #print("new")
    
    return top_10_quality_regions

# Function to calculate quadratic average (Root Mean Square)
def quadratic_average(values):
    return np.sqrt(np.mean(np.square(values)))

def harmonic_average(values):
    return len(values) / np.sum(1.0 / values)

# Function to calculate top n quality quadratic averages per region
def top_n_quadratic_quality_per_region(df, n):
    df['quality'] = df['averageRating'] * np.log(df['numVotes'])
    
    # Create an empty DataFrame to store top n rows for each region based on quality
    top_n_quality_per_region = pd.DataFrame()
    
    # Group by 'region' and apply the operations
    grouped = df.groupby('region')
    
    for region, group in grouped:
        # Sort by 'quality' in descending order and take the top n
        top_n_quality = group.sort_values('quality', ascending=False).head(n)
        top_n_quality_per_region = pd.concat([top_n_quality_per_region, top_n_quality])
    
    # Now calculate the quadratic average of the top n quality values for each region
    region_quad_quality = top_n_quality_per_region.groupby('region')['quality'].apply(harmonic_average)
    
    # Sort by the calculated quadratic average and take the top 10 regions
    top_10_quality_regions = region_quad_quality.sort_values(ascending=False).head(10)
    
    return top_10_quality_regions

def categorize_region(regions):
    if 'GB' in regions and 'US' in regions:
        return 'English'
    elif 'US' in regions and 'GB' not in regions:
        return 'US'
    elif 'GB' in regions and 'US' not in regions:
        return 'GB'
    else:
        # If neither 'UK' nor 'US' is present, return the list of regions as a combined string
        return ','.join(sorted(regions))


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate harmonic mean
def harmonic_mean(x):
    return len(x) / np.sum(1.0 / x)

# Function to calculate top n quality averages per region using harmonic mean
def top_n_quality_per_region_harmonic(df, n):
    
    # Create an empty DataFrame to store top n rows for each region based on quality
    top_n_quality_per_region = pd.DataFrame()
    
    # Group by 'region' and apply the operations
    grouped = df.groupby('region')
    
    for region, group in grouped:
        # Sort by 'quality' in descending order and take the top n
        top_n_quality = group.sort_values('quality', ascending=False).head(n)
        top_n_quality_per_region = pd.concat([top_n_quality_per_region, top_n_quality])
    
    # Now calculate the harmonic mean of the top n quality values for each region
    region_harmonic_quality = top_n_quality_per_region.groupby('region')['quality'].apply(harmonic_mean)
    
    # Sort by the calculated harmonic mean and take the top 10 regions
    top_10_quality_regions = region_harmonic_quality.sort_values(ascending=False).head(10)
    
    return top_10_quality_regions

# Function to calculate harmonic mean of top n quality values per region
def calculate_harmonic_mean_top_n(grouped_df, n=10):
    # Create an empty dictionary to store harmonic means
    region_harmonic_means = {}

    # Group by 'region' and apply the harmonic mean calculation
    grouped = grouped_df.groupby('region')

    for region, group in grouped:
        # Sort by 'quality' in descending order and take the top n
        top_n_quality = group.sort_values('quality', ascending=False).head(n)['quality']
        # If there are fewer than n movies, skip this region
        if len(top_n_quality) < n:
            continue
        # Calculate the harmonic mean
        harmonic_mean_value = harmonic_mean(top_n_quality)
        region_harmonic_means[region] = harmonic_mean_value

    # Convert to DataFrame for easier ranking and sorting
    region_harmonic_means_df = pd.DataFrame.from_dict(region_harmonic_means, orient='index', columns=['harmonic_mean'])
    region_harmonic_means_df = region_harmonic_means_df.sort_values(by='harmonic_mean', ascending=False)

    return region_harmonic_means_df

def calculate_harmonic_mean_for_all_movies(grouped_df):
    # Group by 'region' and apply the harmonic mean calculation to 'quality'
    region_harmonic_means = grouped_df.groupby('region')['quality'].agg(harmonic_mean)
    
    # Convert to DataFrame for easier sorting
    region_harmonic_means_df.columns = ['region', 'harmonic_mean']
    
    # Sort by harmonic mean in descending order
    region_harmonic_means_df = region_harmonic_means_df.sort_values(by='harmonic_mean', ascending=False)
    region_harmonic_means_df = region_harmonic_means.reset_index()
    
    return region_harmonic_means_df
