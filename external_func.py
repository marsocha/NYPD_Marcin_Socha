import numpy as np
import pandas as pd
import os

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

def add(x,y):
    return x+y
def multiply(x,y,z):
    return x*y*z
