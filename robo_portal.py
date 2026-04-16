import datetime
import random
import os

# --- CONFIGURAÇÕES ---
ARQUIVO_HTML = "/var/www/meusite/palpite-do-dia.html"
CHAVE = "<!--MARCA_AQUI-->"

TABELA_BICHOS = {
    1: {"n": "AVESTRUZ", "e": "🦩", "d": ["01", "02", "03", "04"]},
    2: {"n": "ÁGUIA", "e": "🦅", "d": ["05", "06", "07", "08"]},
    3: {"n": "BURRO", "e": "🫏", "d": ["09", "10", "11", "12"]},
    4: {"n": "BORBOLETA", "e": "🦋", "d": ["13", "14", "15", "16"]},
    5: {"n": "CACHORRO", "e": "🐕", "d": ["17", "18", "19", "20"]},
    6: {"n": "CABRA", "e": "🐐", "d": ["21", "22", "23", "24"]},
    7: {"n": "CARNEIRO", "e": "🐑", "d": ["25", "26", "27", "28"]},
    8: {"n": "CAMELO", "e": "🐪", "d": ["29", "30", "31", "32"]},
    9: {"n": "COBRA", "e": "🐍", "d": ["33", "34", "35", "36"]},
    10: {"n": "COELHO", "e": "🐰", "d": ["37", "38", "39", "40"]},
    11: {"n": "CAVALO", "e": "🐎", "d": ["41", "42", "43", "44"]},
    12: {"n": "ELEFANTE", "e": "🐘", "d": ["45", "46", "47", "48"]},
    13: {"n": "GALO", "e": "🐓", "d": ["49", "50", "51", "52"]},
    14: {"n": "GATO", "e": "🐈", "d": ["53", "54", "55", "56"]},
    15: {"n": "JACARÉ", "e": "🐊", "d": ["57", "58", "59", "60"]},
    16: {"n": "LEÃO", "e": "🦁", "d": ["61", "62", "63", "64"]},
    17: {"n": "MACACO", "e": "🐒", "d": ["65", "66", "67", "68"]},
    18: {"n": "PORCO", "e": "🐷", "d": ["69", "70", "71", "72"]},
    19: {"n": "PAVÃO", "e": "🦚", "d": ["73", "74", "75", "76"]},
    20: {"n": "PERU", "e": "🦃", "d": ["77", "78", "79", "80"]},
    21: {"n": "TOURO", "e": "🐂", "d": ["81", "82", "83", "84"]},
    22: {"n": "TIGRE", "e": "🐅", "d": ["85", "86", "87", "88"]},
    23: {"n": "URSO", "e": "🐻", "d": ["89", "90", "91", "92"]},
    24: {"n": "VEADO", "e": "🦌", "d": ["93", "94", "95", "96"]},
    25: {"n": "VACA", "e": "🐄", "d": ["97", "98", "99", "00"]}
}

agora = datetime.datetime.now()
data_str = agora.strftime("%d/%m/%Y")

# --- CONTEÚDO DINÂMICO ---
def gerar_milhar(dezenas):
    return f"{random.randint(0, 99):02d}{random.choice(dezenas)}"

# Gerando os 4 cards
cards_html = ""
sorteados = random.sample(list(TABELA_BICHOS.keys()), 4)
for b in sorteados:
    info = TABELA_BICHOS[b]
    m = gerar_milhar(info['d'])
    cards_html += f'''
    <div class="palpite-card">
        <span class="bicho-icon">{info['e']}</span>
        <h3>{info['n']}</h3>
        <p>Milhar: <strong>{m}</strong></p>
        <p>Centena: <strong>{m[1:]}</strong></p>
    </div>'''

# Estrutura do Portal inspirado na Galaxy MKT
portal_html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Portal Palpites do Bicho | Elite Paulo Peres</title>
    <style>
        :root {{ --p: #0f141e; --s: #f6c945; --f: #f4f7f6; }}
        body {{ background: var(--f); font-family: sans-serif; margin: 0; color: #333; }}
        header {{ background: var(--p); color: #fff; padding: 20px; border-bottom: 5px solid var(--s); text-align: center; }}
        nav a {{ color: #fff; margin: 0 15px; text-decoration: none; font-weight: bold; font-size: 0.9rem; }}
        .hero {{ background: #fff; max-width: 1000px; margin: 30px auto; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .hero-banner {{ background: var(--p); color: #fff; padding: 40px; text-align: center; }}
        .hero-banner h1 {{ color: var(--s); margin: 0; }}
        .grid-palpites {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; }}
        .palpite-card {{ background: #f9f9f9; padding: 20px; border-radius: 15px; border: 1px solid #eee; text-align: center; }}
        .palpite-card strong {{ color: var(--p); font-size: 1.2rem; }}
        .bicho-icon {{ font-size: 3rem; display: block; }}
        .btn {{ display: block; background: var(--s); color: var(--p); text-align: center; padding: 20px; text-decoration: none; font-weight: bold; margin: 20px; border-radius: 10px; }}
        footer {{ background: var(--p); color: #ccc; padding: 40px; text-align: center; font-size: 0.8rem; margin-top: 50px; }}
    </style>
</head>
<body>
<header>
    <nav>
        <a href="index.html">INÍCIO</a>
        <a href="puxadas-do-bicho.html">PUXADAS</a>
        <a href="milhares-viciadas.html">MILHARES</a>
    </nav>
</header>
<main class="hero">
    <div class="hero-banner">
        <span>ATUALIZADO: {data_str}</span>
        <h1>Palpites de Elite Paulo Peres</h1>
        <p>O seu portal vertical de inteligência em loterias.</p>
    </div>
    <div class="grid-palpites">
        {cards_html}
    </div>
    <a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" class="btn">APOSTAR NA ÁGUIA PRIME (BÔNUS ATIVO)</a>
</main>
<footer>
    <p>Portal Palpites do Bicho - Gerenciamento Paulo Peres</p>
    <p>Inspirado em tecnologias de Portais Verticais Corporativos.</p>
</footer>
</body>
</html>'''

# Salvando o arquivo completo
with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
    f.write(portal_html)

os.system(f"cd /var/www/meusite && git add {ARQUIVO_HTML}")
os.system(f'cd /var/www/meusite && git commit -m "Upgrade para Portal Vertical {data_str}"')
os.system("cd /var/www/meusite && git push origin main -f")
print("✅ PORTAL VERTICAL ATUALIZADO COM SUCESSO!")
