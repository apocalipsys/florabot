from bs4 import BeautifulSoup

import requests
url = 'https://www.tutiempo.net/ushuaia.html'

contenido_pagina = requests.get(url).content

soup = BeautifulSoup(contenido_pagina,'html.parser')
#/html/body/div[4]/div[5]/div[1]/div/div[5]/div[2]/span[1]
lat = soup.find('span',{'itemprop':'latitude'})
lon = soup.find('span',{'itemprop':'longitude'})

[print(lat) for lat in lat]
[print(lon) for lon in lon]

ciudad = 'Ushuaia'
ciudad = ciudad.lower().replace(' ','-')
print(ciudad)


