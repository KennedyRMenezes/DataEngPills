import pandas as pd

# Carrega o arquivo CSV
df = pd.read_csv('./movies_stats.csv', delimiter=";")

# Converte a coluna 'date' para datetime
df['date'] = pd.to_datetime(df['date'])

# Extrai a parte da data (ano, mês, dia) em uma nova coluna
df['day'] = df['date'].dt.date

# Agrupa por 'movie' e 'day' e seleciona a entrada mais recente de cada grupo
most_recent_entries = df.sort_values('date').groupby(['movie', 'day']).tail(1)

# Exibe o resultado
print(most_recent_entries)