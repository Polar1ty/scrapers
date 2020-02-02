import pandas as pd

df = pd.read_csv('yandex_dzen.csv')
modifiedDF = df.dropna(how='all')
modifiedDF.to_csv('yandex_dzen_rewrited.csv', index=False)