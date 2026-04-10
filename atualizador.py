import os
from datetime import datetime
import random
import subprocess

# O TOKEN FOI REMOVIDO DAQUI PARA O GITHUB NÃO CANCELAR MAIS
bichos_oficiais = {
    "Avestruz": {"gr": "01", "dz": ["01", "02", "03", "04"], "e": "🦩", "puxa": "Vaca, Águia, Galo, Pavão, Peru"},
    "Águia": {"gr": "02", "dz": ["05", "06", "07", "08"], "e": "🦅", "puxa": "Coelho, Avestruz, Galo, Pavão, Peru"},
    "Burro": {"gr": "03", "dz": ["09", "10", "11", "12"], "e": "🫏", "puxa": "Cavalo, Elefante, Touro, Veado, Coelho, Cobra"},
    "Borboleta": {"gr": "04", "dz": ["13", "14", "15", "16"], "e": "🦋", "puxa": "Cabra, Elefante, Gato, Leão, Cachorro, Galo"},
    "Cachorro": {"gr": "05", "dz": ["17", "18", "19", "20"], "e": "🐕", "puxa": "Galo, Gato, Camelo, Macaco, Porco, Pavão"},
    "Cabra": {"gr": "06", "dz": ["21", "22", "23", "24"], "e": "🐐", "puxa": "Carneiro, Macaco, Elefante, Touro, Tigre, Urso"},
    "Carneiro": {"gr": "07", "dz": ["25", "26", "27", "28"], "e": "🐏", "puxa": "Cabra, Coelho, Vaca"},
    "Camelo": {"gr": "08", "dz": ["29", "30", "31", "32"], "e": "🐪", "puxa": "Cachorro, Elefante, Urso"},
    "Cobra": {"gr": "09", "dz": ["33", "34", "35", "36"], "e": "🐍", "puxa": "Jacaré, Porco, Burro, Gato"},
    "Coelho": {"gr": "10", "dz": ["37", "38", "39", "40"], "e": "🐰", "puxa": "Carneiro, Águia, Burro"},
    "Cavalo": {"gr": "11", "dz": ["41", "42", "43", "44"], "e": "🐎", "puxa": "Burro, Cabra, Touro"},
    "Elefante": {"gr": "12", "dz": ["45", "46", "47", "48"], "e": "🐘", "puxa": "Cabra, Urso, Tigre, Leão, Burro"},
    "Galo": {"gr": "13", "dz": ["49", "50", "51", "52"], "e": "🐓", "puxa": "Cachorro, Avestruz, Águia, Pavão, Peru"},
    "Gato": {"gr": "14", "dz": ["53", "54", "55", "56"], "e": "🐈", "puxa": "Cachorro, Leão, Tigre, Cobra"},
    "Jacaré": {"gr": "15", "dz": ["57", "58", "59", "60"], "e": "🐊", "puxa": "Cobra, Porco, Borboleta, Macaco"},
    "Leão": {"gr": "16", "dz": ["61", "62", "63", "64"], "e": "🦁", "puxa": "Elefante, Gato, Tigre, Urso"},
    "Macaco": {"gr": "17", "dz": ["65", "66", "67", "68"], "e": "🐒", "puxa": "Cachorro, Cabra, Peru, Jacaré"},
    "Porco": {"gr": "18", "dz": ["69", "70", "71", "72"], "e": "🐷", "puxa": "Cobra, Peru, Jacaré, Cachorro"},
    "Pavão": {"gr": "19", "dz": ["73", "74", "75", "76"], "e": "🦚", "puxa": "Avestruz, Águia, Galo, Peru"},
    "Peru": {"gr": "20", "dz": ["77", "78", "79", "80"], "e": "🦃", "puxa": "Avestruz, Águia, Galo, Pavão, Veado"},
    "Touro": {"gr": "21", "dz": ["81", "82", "83", "84"], "e": "🐂", "puxa": "Vaca, Burro, Cabra"},
    "Tigre": {"gr": "22", "dz": ["85", "86", "87", "88"], "e": "🐅", "puxa": "Gato, Leão, Cabra"},
    "Urso": {"gr": "23", "dz": ["89", "90", "91", "92"], "e": "🐻", "puxa": "Leão, Elefante, Camelo, Cabra"},
    "Veado": {"gr": "24", "dz": ["93", "94", "95", "96"], "e": "🦌", "puxa": "Peru, Burro, Cabra"},
    "Vaca": {"gr": "25", "dz": ["97", "98", "99", "00"], "e": "🐄", "puxa": "Touro, Avestruz, Carneiro"}
}

def get_bicho_pela_dezena(dezena):
    d = int(dezena)
    if d == 0: d = 100
    for nome, dados in bichos_oficiais.items():
        gr = int(dados["gr"])
        if ((gr * 4) - 3) <= d <= (gr * 4) or (gr == 25 and (d >= 97 or d == 0)): return nome
    return "Avestruz"

def salvar_e_push():
    agora = datetime.now()
    hoje = agora.strftime("%d/%m/%Y")
    dia = agora.day
    kw_rio = f"Palpite do dia do Jogo do Bicho de hoje Rio {hoje}"
    kw_look = f"Palpite da Look Loterias de hoje Goiás {hoje}"
    
    dz1 = str(dia).zfill(2)
    b1 = get_bicho_pela_dezena(dz1)
    dz2 = str(dia) + "0" if dia < 10 else str(dia)[::-1].zfill(2)
    b2 = get_bicho_pela_dezena(dz2)
    px1 = random.sample(bichos_oficiais[b1]["puxa"].split(", "), 2)
    px2 = random.sample(bichos_oficiais[b2]["puxa"].split(", "), 2)
    final = [(b1, dz1), (b2, dz2)]
    for p in px1 + px2: final.append((p, random.choice(bichos_oficiais[p]["dz"])))

    palpites_html = ""
    for n, d in final:
        info = bichos_oficiais[n]
        palpites_html += f'<div class="palpite-box"><div class="bicho-title"><h3>{info["gr"]} - {n.upper()} {info["e"]}</h3></div><div class="numbers-grid"><div class="num-card"><label>Milhares</label><span>{random.randint(1,9)}{random.randint(1,9)}{d}</span></div><div class="num-card"><label>Centenas</label><span>{random.randint(1,9)}{d}</span></div><div class="num-card"><label>Dezenas</label><span>{d}</span></div></div></div>'

    grid_bichos = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; margin-top: 20px;">'
    for nome, dados in bichos_oficiais.items():
        grid_bichos += f'<div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; text-align: center; background: #fff;"><div style="font-weight: bold; font-size: 0.9rem; color: #121722; margin-bottom: 5px;">{dados["gr"]}</div><div style="font-size: 2rem;">{dados["e"]}</div><div style="font-weight: bold; font-size: 0.8rem; margin: 5px 0;">{nome.upper()}</div><div style="font-size: 0.75rem; color: #d4a017; font-weight: bold;">{" ".join(dados["dz"])}</div></div>'
    grid_bichos += '</div>'

    federal_html = f'<hr><h2>Palpite Federal de Hoje</h2><p>O sorteio da Federal ocorre quartas e sábados às 20h. Nossos palpites para o dia {hoje} também são válidos para essa extração. Confira o <a href="https://resultadosdojogo.com/" class="links-seo" target="_blank">resultado da federal</a> logo após o sorteio.</p>'

    css = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"><style>
        body { font-family: Arial, sans-serif; background: #fff; color: #333; margin: 0; padding: 0; line-height: 1.8; }
        .container { width: 90%; max-width: 850px; margin: 0 auto; position: relative; }
        header { background: #121722; padding: 20px 0; border-bottom: 3px solid #f6c945; position: relative; }
        .logo img { height: 120px; width: auto; display: block; margin: 0 auto; }
        .menu-toggle { display: block; color: #f6c945; font-size: 25px; cursor: pointer; position: absolute; left: 20px; top: 50%; transform: translateY(-50%); }
        nav { background: #121722; padding: 12px 0; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
        nav a { color: #d8dcec; text-decoration: none; margin: 0 15px; font-weight: 600; font-size: 15px; text-transform: uppercase; }
        .section { padding: 40px 0; }
        h1 { font-size: 1.8rem; text-align: center; font-weight: 700; color: #121212; }
        h2 { font-size: 1.6rem; border-left: 6px solid #f6c945; padding-left: 15px; margin: 35px 0 20px 0; font-weight: 700; }
        .links-seo { color: #d4a017; font-weight: bold; text-decoration: underline; }
        .palpite-box { background: #f9f9f9; border: 1px solid #eee; border-radius: 12px; padding: 20px; margin: 25px 0; }
        .numbers-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; text-align: center; }
        .num-card { border: 1px solid #ddd; padding: 10px; border-radius: 8px; background: #fff; }
        .num-card span { display: block; font-weight: bold; font-size: 1.1rem; color: #d4a017; }
        .btn-apostar { display: inline-block; background: #b8860b; color: white; padding: 18px 40px; border-radius: 10px; text-decoration: none; font-weight: bold; text-transform: uppercase; margin-top: 20px; }
        .btn-whats { display: block; width: fit-content; margin: 30px auto; background: #25d366; color: white; padding: 15px 30px; border-radius: 50px; text-decoration: none; font-weight: bold; }
        .site-footer { background-color: #0d1016; padding: 50px 0; text-align: center; color: #fff; }
        @media (max-width: 768px) { nav { display: none; } .logo img { height: 80px; } }
    </style>'''

    def build_page(title, keyword, btn_link, btn_text):
        return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title>{css}</head><body>
<header><div class="container"><i class="fas fa-bars menu-toggle"></i><a href="index.html" class="logo"><img src="images/logo-palpites.png"></a></div></header>
<nav><div class="container"><a href="index.html">Início</a><a href="palpite-do-dia.html">Palpite do Dia</a><a href="puxadas-do-bicho.html">Puxadas</a><a href="milhares-viciadas.html">Milhares</a><a href="https://resultadosdojogo.com/" target="_blank" style="color:#f6c945">Resultados</a></div></nav>
<section class="section"><div class="container">
    <div style="text-align:center; margin-bottom:25px;"><img src="images/aguia-posts.webp" style="width:300px; border-radius:8px;"></div>
    <h1>{keyword}</h1>
    <div style="text-align:center;"><a href="{btn_link}" class="btn-apostar">{btn_text}</a></div>
    {palpites_html}
    <a href="https://chat.whatsapp.com/HyYz0zMD1ovAaWeY99Jfpi" class="btn-whats">RECEBER NO WHATSAPP</a>
    {grid_bichos}
    {federal_html}
</div></section>
<footer class="site-footer">© 2026 Portal de Palpites.</footer></body></html>'''

    with open("/var/www/meusite/palpite-do-bicho-rj.html", 'w', encoding='utf-8') as f:
        f.write(build_page(f"{kw_rio} | RIO", kw_rio, "https://app.aguiaprime119000.com/pr/y8X6LEBU", "🎰 APOSTAR NO RIO"))
    with open("/var/www/meusite/palpite-do-bicho-look.html", 'w', encoding='utf-8') as f:
        f.write(build_page(f"{kw_look} | LOOK", kw_look, "https://app.valedasorteloterias.club/pr/g5P71dlw", "🎰 APOSTAR NA LOOK"))

    os.chdir("/var/www/meusite")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Clean Auth Fix {hoje}"])
    subprocess.run(["git", "push", "origin", "main", "--force"])

if __name__ == "__main__":
    salvar_e_push()
