import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Popup, Icon

load_dotenv()  # lê o arquivo .env
TOKEN = os.getenv("SPTRANS_TOKEN")
LINHA = "8000"
URL = "http://api.olhovivo.sptrans.com.br/v2.1"

s = requests.Session()
login = s.post(f"{URL}/Login/Autenticar?token={TOKEN}")
print("Login:", login.text)

linhas = s.get(f"{URL}/Linha/Buscar?termosBusca={LINHA}").json()

paradas = []
for l in linhas:
    paradas += s.get(f"{URL}/Parada/BuscarParadasPorLinha?codigoLinha={l['cl']}").json()

m = Map(location=[paradas[3]["py"], paradas[3]["px"]], zoom_start=14)


for i in paradas:
    Marker(location=[i["py"], i["px"]], popup=i["np"], icon=Icon(color="blue")).add_to(m)

for l in linhas:
    posicao = s.get(f"{URL}/Posicao/Linha?codigoLinha={l['cl']}").json()
    for o in posicao["vs"]:
        Marker(
            location=[o["py"], o["px"]],
            popup=Popup(f"Ônibus {o['p']}", max_width="100"),
            icon=Icon(color="red", icon="bus", prefix="fa"),
        ).add_to(m)

m.save("index.html")
print("Mapa criado: index.html")