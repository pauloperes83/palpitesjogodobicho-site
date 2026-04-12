import datetime
import random
import re

# Configurações
ARQUIVO_HTML = "palpite-do-bicho-rj.html"

TABELA_BICHOS = {
    1: "AVESTRUZ", 2: "ÁGUIA", 3: "BURRO", 4: "BORBOLETA", 5: "CACHORRO",
    6: "CABRA", 7: "CARNEIRO", 8: "CAMELO", 9: "COBRA", 10: "COELHO",
    11: "CAVALO", 12: "ELEFANTE", 13: "GALO", 14: "GATO", 15: "JACARÉ",
    16: "LEÃO", 17: "MACACO", 18: "PORCO", 19: "PAVÃO", 20: "PERU",
    21: "TOURO", 22: "TIGRE", 23: "URSO", 24: "VEADO", 25: "VACA"
}

# Puxadas padrão para completar os 6 cards
PUXADAS_PADRAO = [11, 7, 17, 1, 19, 25]

def gerar_milhar(grupo):
    dezena = random.choice([(grupo*4)-3, (grupo*4)-2, (grupo*4)-1, (grupo*4)])
    if dezena == 0: dezena = 100
    milhar = f"{random.randint(10, 99)}{dezena:02d}"
    return milhar

# Lógica do Dia
hoje = datetime.date.today()
dia = hoje.day
data_str = hoje.strftime("%d/%m/%Y")

# 1. Bicho do Dia (Data)
bicho_dia = dia if dia <= 25 else (dia - 25)

# 2. Bicho Invertido (Inversa) - Se inverter der mais de 25, usa o bicho da soma
inverso_str = str(dia)[::-1]
inverso_num = int(inverso_str)
if inverso_num > 25:
    inverso_num = sum(int(d) for d in str(dia))

# Lista de bichos (Dia + Inversa)
bichos_finais = [bicho_dia, inverso_num]

# Adiciona as puxadas para completar 6 cards
for p in PUXADAS_PADRAO:
    if p not in bichos_finais and len(bichos_finais) < 6:
        bichos_finais.append(p)

# Gerar o HTML dos 6 cards
html_cards = "    \n"
for num in bichos_finais:
    m = gerar_milhar(num)
    html_cards += f'    <div class="palpite-box"><div class="bicho-title"><h3>{num:02d} - {TABELA_BICHOS[num]}</h3></div><div class="numbers-grid"><div class="num-card"><label>Milhar</label><span>{m}</span></div><div class="num-card"><label>Centena</label><span>{m[1:]}</span></div><div class="num-card"><label>Dezena</label><span>{m[2:]}</span></div></div></div>\n'
html_cards += "    "

# Abrir e atualizar o HTML
with open(ARQUIVO_HTML, "r", encoding="utf-8") as f:
    conteudo = f.read()

# 1. Troca todas as datas encontradas no texto
conteudo = re.sub(r"\d{2}/\d{2}/\d{4}", data_str, conteudo)

# 2. Troca as dezenas do Duque de Dezena no texto SEO (12 e 21)
dez_1 = f"{bicho_dia:02d}"
dez_2 = f"{inverso_num:02d}"
conteudo = re.sub(r"\(12 e 21\)", f"({dez_1} e {dez_2})", conteudo)

# 3. Injeta os cards novos entre as etiquetas
partes = conteudo.split("")
if len(partes) >= 3:
    novo_html = partes[0] + html_cards + partes[2]
    with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
        f.write(novo_html)
    print(f"Site atualizado para {data_str}")
else:
    print("Erro: Etiquetas não encontradas no HTML.")
