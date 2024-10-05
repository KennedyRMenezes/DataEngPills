import sys
import os

# Adiciona o caminho absoluto do MovieStats ao sys.path
sys.path.append('/home/kennedy/KR/Programação/01.Exercícios/DE/Movies/MovieStats')

# Tente importar a classe MovieData
try:
    from scrap import MovieData
    print("Import successful!")
except ModuleNotFoundError as e:
    print(f"Import failed: {e}")
