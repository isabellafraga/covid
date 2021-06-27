
# # Casos Confirmados COVID-19




import pandas as pd
from urllib.request import urlretrieve
import matplotlib.pyplot as plt



url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlretrieve(url, 'D:\HD Isabella\Área de Trabalho\casos_covid\casos_brasil_Covid19.csv')

df_covid = pd.read_csv('D:\HD Isabella\Área de Trabalho\casos_covid\casos_brasil_Covid19.csv')

type(df_covid)

df_covid.drop(['Lat','Long'], axis=1, inplace=True)
df_country = df_covid.groupby('Country/Region').sum()

date = df_country.loc['Brazil'].index
cases = df_country.loc['Brazil'].values

plt.figure(figsize=(14,8))
plt.bar(date, cases)


df_country.head()
s_brazil = df_country.loc['Brazil']
s_brasil = s_brazil[s_brazil>0]
s_brasil.index
s_brasil.values

tam = len(s_brasil)

plt.figure(figsize=(14,8))
plt.xticks(rotation=60)
plt.bar(s_brasil.index[tam-30:tam], s_brasil.values[tam-30:tam])
plt.title('T')
plt.show()

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlretrieve(url, 'D:\HD Isabella\Área de Trabalho\casos_covid\casos_brasil_Covid19.csv')
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlretrieve(url, 'D:\HD Isabella\Área de Trabalho\casos_covid\casos_brasil_Covid19.csv')



