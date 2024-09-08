import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cProfile
import pstats


def wczytaj_dane(folder, nazwa_pliku, pliki):
    '''
    Dostaje na wstepie nazwe folderu oraz nazwe plikow .tsv, z ktorego ma zczytac dane
    Następnie dodaje do tablicy pliki[] nazwę pliku z zamienionymi kropkami
    na podłogi i zapisuje przy pomocy pandas.read_csv
    '''
    pelna_nazwa = folder + '/' + nazwa_pliku
    tmp = pd.read_csv(pelna_nazwa, sep='\t')
    nazwa_bez_tsv = nazwa_pliku[:-4]  # Usunięcie '.tsv'
    A, B = nazwa_bez_tsv.split('.')
    nazwa = f"{A}_{B}"
    pliki[nazwa] = tmp

def pobierz_nazwy_plikow(folder):
    '''
    Z danego folderu zczytuje wszystkie nazwy plików w nim zawartych
    '''
    pliki = os.listdir(folder)
    pliki = [element for element in pliki if element != '.DS_Store']
    pliki_tsv = [plik for plik in pliki]
    return pliki_tsv

def quadratic_average(values):
    '''
    Wylicza średnią kwadratową z danych wartości
    '''
    return np.sqrt(np.mean(np.square(values)))

def harmonic_average(values):
    '''
    Wylicza średnią harmoniczną z danych wartości
    '''
    return len(values) / np.sum(1.0 / values)

# Function to calculate top n quality quadratic averages per region
def top_n_quality_per_region(df, n):
    df['quality'] = df['averageRating'] * np.log(df['numVotes'])
    
    # Tworzenie pustej DataFrame do przechowywania n najlepszych wierszy dla każdego regionu na podstawie jakości
    top_n_quality_per_region = pd.DataFrame()
    
    # Grupowanie według 'region' i zastosowanie operacji
    grouped = df.groupby('region')
    
    for region, group in grouped:
        # Sortowanie według 'quality' malejąco i wybieranie n najlepszych
        top_n_quality = group.sort_values('quality', ascending=False).head(n)
        top_n_quality_per_region = pd.concat([top_n_quality_per_region, top_n_quality])
    
    # Teraz oblicz średnią harmoniczną z n najlepszych wartości jakości dla każdego regionu
    region_quad_quality = top_n_quality_per_region.groupby('region')['quality'].apply(harmonic_average)
    
    # Sortowanie według obliczonej średniej kwadratowej i wybieranie 10 najlepszych regionów
    top_10_quality_regions = region_quad_quality.sort_values(ascending=False).head(10)
    
    return top_10_quality_regions

def categorize_region(regions):
    '''
    Dla tablicy regions[] jezeli znajduje sie tam GB oraz USA
    to cięzko jest stwierdzić jakiego kraju jest pochodzenia dany
    film, wiec po prostu uznajmy, ze jest anglojezyczny
    Jezeli z kolei oryginalny tytul jest taki sam jak w GB, ale nie US, mozemy
    zalozyc, ze ten film pochodzi z Wielkiej Brytanii i analogicznie dla US
    Pozostale regiony traktujemy w "normalny" sposob
    '''
    if 'GB' in regions and 'US' in regions:
        return 'English'
    elif 'US' in regions and 'GB' not in regions:
        return 'US'
    elif 'GB' in regions and 'US' not in regions:
        return 'GB'
    else:
        # Jeśli ani 'GB', ani 'US' nie są obecne, zwróć listę regionów jako połączony ciąg
        return ','.join(sorted(regions))

# Function to calculate top n quality averages per region using harmonic mean
def top_n_quality_per_region_harmonic(df, n):
    '''
    Oblicza średnią harmoniczną z n najlepszych filmów dla kazdego danego regionu
    '''
    
    # Tworzenie pustej DataFrame do przechowywania n najlepszych wierszy dla każdego regionu na podstawie jakości
    top_n_quality_per_region = pd.DataFrame()
    
    # Grupowanie według 'region' i zastosowanie operacji
    grouped = df.groupby('region')
    
    for region, group in grouped:
        # Sortowanie według 'quality' malejąco i wybieranie n najlepszych
        top_n_quality = group.sort_values('quality', ascending=False).head(n)
        top_n_quality_per_region = pd.concat([top_n_quality_per_region, top_n_quality])
    
    # Teraz oblicz średnią harmoniczną z n najlepszych wartości jakości dla każdego regionu
    region_harmonic_quality = top_n_quality_per_region.groupby('region')['quality'].apply(harmonic_average)
    
    # Sortowanie według obliczonej średniej harmonicznej i wybieranie 10 najlepszych regionów
    top_10_quality_regions = region_harmonic_quality.sort_values(ascending=False).head(10)
    
    return top_10_quality_regions

# Funkcja do obliczania średniej harmonicznej z n najlepszych wartości jakości na region
def calculate_harmonic_average_top_n(grouped_df, n=10):
    '''
    Dla kadego kraju wylicza średnią harmoniczną naszej metryki
    dla n (domyślnie 10) filmów z tego regionu (grupy regionów)
    '''
    # Tworzenie pustego słownika do przechowywania średnich harmonicznych
    region_harmonic_averages = {}

    # Grupowanie według 'region' i zastosowanie obliczania średniej harmonicznej
    grouped = grouped_df.groupby('region')

    for region, group in grouped:
        # Sortowanie według 'quality' malejąco i wybieranie n najlepszych
        top_n_quality = group.sort_values('quality', ascending=False).head(n)['quality']
        # Jeśli jest mniej niż n filmów, pomiń ten region
        if len(top_n_quality) < n:
            continue
        # Obliczanie średniej harmonicznej
        harmonic_average_value = harmonic_average(top_n_quality)
        region_harmonic_averages[region] = harmonic_average_value

    # Konwersja do DataFrame dla łatwiejszego sortowania
    region_harmonic_averages_df = pd.DataFrame.from_dict(region_harmonic_averages, orient='index', columns=['harmonic_average'])
    region_harmonic_averages_df = region_harmonic_averages_df.sort_values(by='harmonic_average', ascending=False)

    return region_harmonic_averages_df

def calculate_harmonic_average_for_all_movies(grouped_df):
    '''
    Dla kadego kraju wylicza średnią harmoniczną naszej metryki
    dla wszystkich filmów z tego regionu (grupy regionów)
    '''
    # Grupowanie według 'region' i zastosowanie obliczania średniej harmonicznej dla 'quality'
    region_harmonic_averages = grouped_df.groupby('region')['quality'].agg(harmonic_average)
    
    # Konwersja do DataFrame dla łatwiejszego sortowania
    region_harmonic_averages_df.columns = ['region', 'harmonic_average']
    
    # Sortowanie według średniej harmonicznej malejąco
    region_harmonic_averages_df = region_harmonic_averages_df.sort_values(by='harmonic_average', ascending=False)
    region_harmonic_averages_df = region_harmonic_averages.reset_index()
    
    return region_harmonic_averages_df

def get_best_and_worst_movies(group):
    '''
    Z pośród wybranych filmów wybieramy dwa najlepsze
    przy zalozeniu, ze są one posortowane od najlepszego
    do najgorszego
    '''
    best = group.iloc[0]['tconst']
    second_best = group.iloc[1]['tconst']
    return pd.Series([best, second_best])

def convert_gdp_format(txt: str):
    """
    Converts format of gdp column.
    """

    txt = txt.strip()

    if txt == "-":
        ret = np.nan
    else:
        ret = float(txt.replace(",", ""))
        
    return ret

def profile_function(func, file_name='profiling_results.txt'):
    '''
    Funckja do zapisywania informacji o profilowaniu
    poszczególnej funkcji
    '''
    #Tworzenie obiekt Profile
    prof = cProfile.Profile()
    
    # Wywołujemy funkcje
    prof.enable()  # Start profilowanie
    func()         # Wywołanie funkcji
    prof.disable() # Stop profilowania
    
    # Zapis profilowania do pliku
    with open(file_name, 'a') as f:  # Uzywamy 'a', zeby dodac do pliku (append)
        stats = pstats.Stats(prof, stream=f)
        stats.sort_stats('cumulative')  # Sortowania po czasie trwania
        stats.print_stats()
    
    print(f"Profiling results saved to {file_name}")
