import os
from datetime import datetime, timedelta
import random
import subprocess

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

def gerar_palpites_html():
    final_bichos = []
    while len(final_bichos) < 6:
        b = random.choice(list(bichos_oficiais.keys()))
        dz = random.choice(bichos_oficiais[b]["dz"])
        if b not in [x[0] for x in final_bichos]:
            final_bichos.append((b, dz))
    palpites_html = ""
    for n, d in final_bichos:
        info = bichos_oficiais[n]
        palpites_html += f'''
    <div class="palpite-box">
        <div class="bicho-title"><h3>{info["gr"]} - {n.upper()} {info["e"]}</h3></div>
        <div class="numbers-grid">
            <div class="num-card"><label>Milhares</label><span>{random.randint(1,9)}{random.randint(1,9)}{d}</span></div>
            <div class="num-card"><label>Centenas</label><span>{random.randint(1,9)}{d}</span></div>
            <div class="num-card"><label>Dezenas</label><span>{d}</span></div>
        </div>
    </div>'''
    return palpites_html

def salvar_e_push():
    agora = datetime.now()
    hoje_str = agora.strftime("%d/%m/%Y")
    p_html = gerar_palpites_html()
    
    css = '''<style>body{font-family:'Segoe UI',Arial,sans-serif;background:#fff;margin:0;padding:0;line-height:1.8}
    header{background:#121722;padding:20px 0;border-bottom:3px solid #f6c945;text-align:center}
    .logo img{height:120px;width:auto}
    nav{background:#121722;padding:12px 0;text-align:center;position:sticky;top:0;z-index:1000}
    nav a{color:#d8dcec;text-decoration:none;margin:0 15px;font-weight:600;text-transform:uppercase}
    .container{width:95%;max-width:1000px;margin:0 auto}
    .section{padding:40px 0}
    h1{font-size:2.2rem;color:#222;text-align:center;margin-bottom:25px;font-weight:700}
    h2{font-size:1.6rem;color:#b8860b;border-left:6px solid #f6c945;padding-left:15px;margin:35px 0 20px}
    .links-seo{color:#d4a017;font-weight:700;text-decoration:underline}
    .palpite-box{background:#f9f9f9;border:1px solid #eee;border-radius:12px;padding:20px;margin:25px 0}
    .numbers-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:15px;text-align:center}
    .num-card{border:1px solid #ddd;padding:10px;border-radius:8px;background:#fff}
    .num-card span{display:block;font-weight:700;font-size:1.1rem;color:#d4a017}
    .btn-apostar{display:inline-block;background:#b8860b;color:#fff;padding:18px 40px;border-radius:10px;text-decoration:none;font-weight:700;text-transform:uppercase;margin-top:20px}
    .site-footer{background:#0d1016;padding:50px 0;text-align:center;margin-top:50px;color:#fff}</style>'''
    
    header = f'<header><div class="container"><a href="index.html" class="logo"><img src="images/logo-palpites.png"></a></div></header><nav><a href="index.html">Início</a><a href="palpite-do-dia.html">Palpite do Dia</a><a href="https://resultadosdojogo.com/" target="_blank">Resultados</a></nav>'
    footer = '<footer class="site-footer"><div class="container"><h3>Palpites do Jogo do Bicho</h3><p>© 2026 Portal de Palpites.</p></div></footer></body></html>'

    # RIO
    kw_rio = f"Palpite do dia do Jogo do Bicho de hoje Rio {hoje_str}"
    html_rio = f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{kw_rio}</title>{css}</head><body>{header}<section class="section"><div class="container"><h1>{kw_rio}</h1><p>Confira o melhor palpite para as extrações do Rio. Veja o <a href="https://resultadosdojogo.com/" class="links-seo" target="_blank">resultado do jogo do bicho de hoje rio</a> para PTM, PT, PTV, PTN e Corujinha.</p><div style="text-align:center"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" class="btn-apostar">🎰 APOSTAR NO RIO</a></div>{p_html}<hr><h2>Palpite Federal</h2><p>Palpites válidos para a Federal de quarta e sábado.</p></div></section>{footer}'
    with open("/var/www/meusite/palpite-do-bicho-rj.html", 'w', encoding='utf-8') as f: f.write(html_rio)

    # LOOK
    kw_look = f"Palpite da Look Loterias de hoje Goiás {hoje_str}"
    html_look = f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{kw_look}</title>{css}</head><body>{header}<section class="section"><div class="container"><h1>{kw_look}</h1><p>Confira o melhor <strong>{kw_look}</strong> para Goiás e Goiânia. Veja também o <a href="https://resultadosdojogo.com/" class="links-seo" target="_blank">resultado look loterias de hoje</a> e Lotece.</p><div style="text-align:center"><a href="https://app.valedasorteloterias.club/pr/g5P71dlw" class="btn-apostar">🎰 APOSTAR NA LOOK</a></div>{p_html}</div></section>{footer}'
    with open("/var/www/meusite/palpite-do-bicho-look.html", 'w', encoding='utf-8') as f: f.write(html_look)

    os.chdir("/var/www/meusite")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Restore SEO Rio e Look {hoje_str}"])
    subprocess.run(["git", "push", "origin", "main", "--force"])

if __name__ == "__main__":
    salvar_e_push()
