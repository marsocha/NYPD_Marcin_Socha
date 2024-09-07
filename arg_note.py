import argparse
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

def main(notebook_filename, gdp_filename, population_filename, pocz, kon):
    # Wczytanie notebooka
    with open(notebook_filename) as f:
        notebook = nbformat.read(f, as_version=4)

    # Przekazanie argumentów do komórek notebooka
    notebook.cells.insert(0, nbformat.v4.new_code_cell(f"""
gdp_filename = '{gdp_filename}'
population_filename = '{population_filename}'
pocz = {pocz}
kon = {kon}
"""))

    # Użycie NotebookClient do wykonania notebooka
    client = NotebookClient(notebook)
    client.execute()

    # Zapisanie zmodyfikowanego notebooka
    wynikowy_notebook_filename = 'wynikowy_' + notebook_filename
    with open(wynikowy_notebook_filename, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)

    # Konwersja notebooka do HTML
    html_exporter = HTMLExporter()
    (body, resources) = html_exporter.from_notebook_node(notebook)

    # Zapisanie HTML do pliku
    html_filename = wynikowy_notebook_filename.replace('.ipynb', '.html')
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(body)

    print(f'Zapisano wynikowy notebook jako {wynikowy_notebook_filename}')
    print(f'Zapisano wynikowy HTML jako {html_filename}')
    

if __name__ == "__main__":
    # Tworzenie parsera argumentów
    parser = argparse.ArgumentParser(description="Przekaż nazwę notebooka oraz pliki GDP i Population.")
    
    # Argument dla notebooka
    parser.add_argument('notebook_file', type=str, help="Ścieżka do pliku notebooka (.ipynb)")
    # Argument dla pliku GDP
    parser.add_argument('gdp_file', type=str, help="Ścieżka do pliku GDP")
    # Argument dla pliku Population
    parser.add_argument('population_file', type=str, help="Ścieżka do pliku Population")
    
    # Parsowanie argumentów
    args = parser.parse_args()

    # Pytanie o dwie liczby w terminalu
    pocz = float(input("Podaj pierwszą liczbę: "))
    kon = float(input("Podaj drugą liczbę: "))
    if pocz > kon:
        print('niepoprawne dane')
    else:
        # Wywołanie głównej funkcji z czterema argumentami
        main(args.notebook_file, args.gdp_file, args.population_file, pocz, kon)
