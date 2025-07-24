import pandas as pd
import requests
from bs4 import BeautifulSoup
import unicodedata
import re

def slugify(nome):
    # Remove acentos
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('utf-8')
    # Minúsculas, tira espaços extras, troca por hífen e remove pontuação
    nome = re.sub(r'[^\w\s-]', '', nome.lower())
    nome = re.sub(r'\s+', '-', nome.strip())
    return nome

def get_populacao_ibge_site(uf, cidade_slug):
    url = f"https://www.ibge.gov.br/cidades-e-estados/{uf}/{cidade_slug}.html"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Erro {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    paragrafos = soup.find_all('p', class_='ind-value')

    for p in paragrafos:
        texto_completo = p.get_text(strip=True)
        pessoas_encontradas = 0
        for p in paragrafos:
            texto_completo = p.get_text(strip=True)
            if 'pessoas' in texto_completo:
                pessoas_encontradas += 1
                if pessoas_encontradas == 2:  # Pega a segunda ocorrência
                    numero = texto_completo.split('pessoas')[0].strip()
                    return numero

    return "População não encontrada"

df_cidades = pd.DataFrame({
    'Cidade': [
        'São Luís', 'Imperatriz', 'Caxias', 'Timon', 'Balsas',
        'Codó', 'Barra do Corda', 'Açailândia', 'Bacabal', 'Santa Inês'
    ],
    'Estado': ['ma'] * 10
})

dados = []
for _, row in df_cidades.iterrows():
    nome_cidade = row['Cidade']
    estado = row['Estado']

    if pd.notna(nome_cidade):
        slug = slugify(str(nome_cidade))
        pop = get_populacao_ibge_site(estado, slug)
    else:
        slug = ''
        pop = 'Cidade ausente na planilha'

    dados.append({
        'Cidade': nome_cidade,
        'Slug': slug,
        'População': pop
    })
# Converte em DataFrame e exibe
df_resultado = pd.DataFrame(dados)
print(df_resultado)
