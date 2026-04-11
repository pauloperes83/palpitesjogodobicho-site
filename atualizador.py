import os
import sys
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
    "Carneiro": {"gr": "07", "dz": ["25", "26", "27", "28"], "e": "🐑", "puxa": "Cabra, Coelho, Vaca"},
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

def gerar_palpites_html(dia):
    dz1 = str(dia).zfill(2)
    b1 = get_bicho_pela_dezena(dz1)
    dz2 = str(dia) + "0" if dia < 10 else str(dia)[::-1].zfill(2)
    b2 = get_bicho_pela_dezena(dz2)
    px = random.sample(bichos_oficiais[b1]["puxa"].split(", "), 2) + random.sample(bichos_oficiais[b2]["puxa"].split(", "), 2)
    final = list(dict.fromkeys([(b1, dz1), (b2, dz2)] + [(p, random.choice(bichos_oficiais[p]["dz"])) for p in px]))[:6]
    html = ""
    for n, d in final:
        info = bichos_oficiais[n]
        m = f"{random.randint(1,9)}{random.randint(0,9)}{d}"
        c = f"{random.randint(1,9)}{d}"
        html += f'<div class="palpite-box"><div class="bicho-title"><h3>{info["gr"]} - {n.upper()} {info["e"]}</h3></div><div class="numbers-grid"><div class="num-card"><label>Milhar</label><span>{m}</span></div><div class="num-card"><label>Centena</label><span>{c}</span></div><div class="num-card"><label>Dezena</label><span>{d}</span></div></div></div>'
    return html

def build_full_page(kw, artigo_content, palpites_txt, grid_bichos):
    css = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"><style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #ffffff; color: #333; margin: 0; padding: 0; line-height: 1.6; }
        .container { width: 95%; max-width: 1000px; margin: 0 auto; }
        header { background: #121722; padding: 15px 0; border-bottom: 3px solid #f6c945; }
        .header-wrap { display: flex; justify-content: space-between; align-items: center; position: relative; }
        .logo img { height: 80px; width: auto; }
        
        /* Menu Hambúrguer Mobile */
        .menu-toggle { display: none; color: #fff; font-size: 25px; cursor: pointer; background: none; border: none; }
        nav { background: #121722; padding: 0; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
        .nav-links { display: flex; justify-content: center; list-style: none; margin: 0; padding: 12px 0; }
        .nav-links a { color: #d8dcec; text-decoration: none; margin: 0 15px; font-weight: 600; font-size: 14px; text-transform: uppercase; }
        
        .dropdown { position: relative; display: inline-block; }
        .dropdown-content { display: none; position: absolute; background-color: #121722; min-width: 160px; box-shadow: 0px 8px 16px rgba(0,0,0,0.5); z-index: 99; border: 1px solid rgba(255,255,255,0.1); text-align: left; }
        .dropdown-content a { margin: 0 !important; padding: 12px 16px !important; display: block !important; font-size: 14px !important; border: none !important; }
        .dropdown:hover .dropdown-content { display: block; }

        .section { padding: 30px 0; }
        h1 { font-size: 1.8rem; color: #222; text-align: center; margin-bottom: 20px; padding: 0 10px; }
        h2 { font-size: 1.4rem; color: #b8860b; border-left: 6px solid #f6c945; padding-left: 15px; margin: 30px 0 15px 0; }
        p { margin-bottom: 15px; font-size: 1.05rem; color: #444; text-align: justify; }
        .link-seo { color: #d4a017; font-weight: bold; text-decoration: underline; }
        
        .palpite-box { background: #f9f9f9; border: 1px solid #eee; border-radius: 12px; padding: 15px; margin: 20px 0; }
        .numbers-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; text-align: center; }
        .num-card { border: 1px solid #ddd; padding: 8px; border-radius: 8px; background: #fff; }
        .num-card span { display: block; font-weight: bold; font-size: 1rem; color: #d4a017; }
        
        .btn-apostar { display: inline-block; background: #b8860b; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; text-transform: uppercase; margin-top: 15px; }
        .btn-whats { display: block; width: fit-content; margin: 25px auto; background: #25d366; color: white; padding: 12px 30px; border-radius: 50px; text-decoration: none; font-weight: bold; text-align: center; }

        .site-footer { background-color: #0d1016; padding: 40px 0 20px 0; text-align: center; margin-top: 40px; color: #fff; }
        .footer-copy { font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px; color: #6c757d; margin-top: 20px;}

        @media (max-width: 768px) {
            .logo img { height: 60px; }
            .menu-toggle { display: block; margin-right: 15px; }
            .nav-links { display: none; flex-direction: column; padding: 0; }
            .nav-links.active { display: flex; }
            .nav-links a { padding: 12px; margin: 0; border-bottom: 1px solid rgba(255,255,255,0.05); width: 100%; box-sizing: border-box; }
            h1 { font-size: 1.5rem; }
            .dropdown-content { position: static; width: 100%; box-shadow: none; background: #1a202c; }
        }
    </style>'''
    
    return f'''<!DOCTYPE html><html lang="pt-BR"><head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9Y3FW10LC2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9Y3FW10LC2');</script>
<link rel="icon" type="image/png" href="images/favicon.png"><link rel="shortcut icon" href="images/favicon.png">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{kw}</title>{css}</head><body>
<header><div class="container header-wrap">
    <a href="index.html" class="logo"><img src="images/logo-palpites.png"></a>
    <button class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')"><i class="fas fa-bars"></i></button>
</div></header>
<nav><div class="container">
    <div class="nav-links">
        <a href="index.html">Início</a><a href="palpite-do-dia.html">Palpite do Dia</a>
        <div class="dropdown"><a href="#">Bancas ▾</a>
            <div class="dropdown-content">
                <a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" target="_blank">Águia Prime</a>
                <a href="https://app.valedasorteloterias.club/pr/g5P71dlw" target="_blank">Vale da Sorte</a>
            </div>
        </div>
        <a href="puxadas-do-bicho.html">Puxadas</a><a href="milhares-viciadas.html">Milhares</a>
        <a href="https://resultadosdojogo.com/" target="_blank" style="color: #f6c945;">Resultados</a>
    </div>
</div></nav>
<section class="section"><div class="container">
    <div style="text-align: center; margin-bottom: 20px;"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU"><img src="images/aguia-posts.webp" style="max-width: 100%; height: auto; border-radius: 8px;"></a></div>
    <h1>{kw}</h1>
    {artigo_content}
    <p style="text-align: center; font-weight: bold; margin-top: 20px; font-size: 1.1rem; color: #b8860b;">🍀 Desejamos muita sorte em suas apostas! 🍀</p>
</div></section>
<footer class="site-footer"><div class="container">
    <div style="font-size: 1.5rem; color: #f6c945; font-weight: bold; margin-bottom: 15px;">Palpites do Jogo do Bicho</div>
    <p style="font-size: 0.8rem; color: #888ea1; line-height: 1.4;">Informativo sem vínculo com o Jogo do Bicho.</p>
    <p class="footer-copy">© 2026 Palpites do Jogo. Todos os direitos reservados.</p>
</div></footer></body></html>'''

def executar():
    tipo = sys.argv[1] if len(sys.argv) > 1 else "todos"
    agora = datetime.now()
    alvo = agora + timedelta(days=1) if agora.hour >= 21 else agora
    hoje = alvo.strftime("%d/%m/%Y")
    dia_num = alvo.day
    palpites_txt = gerar_palpites_html(dia_num)

    grid_bichos = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(90px, 1fr)); gap: 8px; margin-top: 20px;">'
    for nome, dados in bichos_oficiais.items():
        grid_bichos += f'<div style="border: 1px solid #ddd; border-radius: 8px; padding: 8px; text-align: center; background: #fff;"><div style="font-weight: bold; font-size: 0.8rem;">{dados["gr"]}</div><div style="font-size: 1.8rem;">{dados["e"]}</div><div style="font-weight: bold; font-size: 0.7rem;">{nome.upper()}</div></div>'
    grid_bichos += '</div>'

    l_pal = '<a href="https://palpitesjogodobicho.com.br/palpite-do-dia.html" class="link-seo">Palpite do dia</a>'
    l_pux = '<a href="https://palpitesjogodobicho.com.br/puxadas-do-bicho.html" class="link-seo">Puxadas do Bicho</a>'
    l_mil = '<a href="https://palpitesjogodobicho.com.br/milhares-viciadas.html" class="link-seo">Milhares Viciadas</a>'

    if tipo in ["rio", "todos"]:
        kw = f"Palpite do dia do Jogo do Bicho de hoje Rio {hoje}"
        art = f'''<p>Se você busca <strong>{kw}</strong>, aqui vai encontrar um conteúdo focado apenas na banca do Rio.</p>
        <p>Reunimos análises, grupos que chamam atenção e combinações muito procuradas por quem acompanha os sorteios do dia.</p>
        <p>O objetivo é trazer um texto direto, organizado e fácil de ler. Tudo com foco em <strong>{kw}</strong>, sem misturar outras loterias.</p>
        <div style="text-align: center;"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" class="btn-apostar">🎰 APOSTAR AGORA</a></div>
        {palpites_txt}
        <a href="https://chat.whatsapp.com/HyYz0zMD1ovAaWeY99Jfpi" class="btn-whats" target="_blank">RECEBER PALPITES NO WHATSAPP</a>
        <h2>{kw} com foco na banca Rio</h2>
        <p>Quem pesquisa {l_pal} quer encontrar uma base para analisar melhor os jogos do dia. Por isso, o foco aqui está nas combinações.</p>
        <p>As análises são focadas na rotina da banca Rio. O Jogo do Bicho do Rio movimenta buscas diárias por grupos, dezenas, centenas e milhares.</p>
        <p>Muitos jogadores acompanham os resultados anteriores para tentar identificar repetições, atrasos e padrões. Esse comportamento fortalece a procura por <strong>{kw}</strong>.</p>
        <h2>Por que o termo {kw} é tão buscado</h2>
        <p>A expressão <strong>{kw}</strong> é muito forte porque une data, local e intenção de busca exata.</p>
        <p>Quem digita isso normalmente quer um conteúdo atualizado e voltado só para o Rio. Além disso, as pessoas procuram por termos relacionados.</p>
        <p>Buscamos entregar conteúdos rápidos e objetivos. Por isso, textos curtos tendem a funcionar melhor para esse tipo de palavra-chave.</p>
        <h2>{kw} e análise dos grupos mais observados</h2>
        <p>Dentro da rotina do Jogo do Bicho do Rio, alguns grupos sempre despertam mais atenção dos apostadores.</p>
        <p>Isso acontece porque certos bichos se tornam populares em diferentes períodos. Ao montar um conteúdo sobre <strong>{kw}</strong>, vale destacar os grupos.</p>
        <h3>Grupos populares no Jogo do Bicho do Rio</h3>
        <p>Os grupos populares costumam receber mais atenção de quem acompanha palpites diariamente no Rio.</p>
        <p>Muita gente observa o histórico recente para decidir em qual grupo apostar. Também é comum relacionar grupos com sonhos e datas especiais.</p>
        <h2>Como usar o {kw} de forma estratégica</h2>
        <p>O ideal é usar o <strong>{kw}</strong> como apoio na sua análise pessoal. Muitos jogadores observam tendências antes de definir o jogo.</p>
        <p>Isso ajuda a perceber quais combinações estão mais comentadas. Também vale acompanhar os horários tradicionais como PTM, PT, PTV, PTN e Corujinha.</p>
        <p>Aprenda usar as {l_mil} e {l_pux} para jogar, pois com elas suas chances de ganhar no jogo do bicho aumentam.</p>
        <h2>Palpite do Bicho Loteria Federal de Hoje</h2>
        <p>Se você procura <strong>Palpite do Bicho Loteria Federal de Hoje</strong>, aqui encontra um conteúdo direto.</p>
        <p>A busca por Palpite do Bicho Loteria Federal de Hoje cresce entre quem gosta de acompanhar a Federal antes do sorteio oficial.</p>
        <h2>Tabela dos bichos no Rio</h2>
        {grid_bichos}'''
        with open("/var/www/meusite/palpite-do-bicho-rj.html", 'w', encoding='utf-8') as f:
            f.write(build_full_page(kw, art, palpites_txt, grid_bichos))

    os.chdir("/var/www/meusite")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Auto Update {hoje} {agora.strftime('%H:%M:%S')}"])
    subprocess.run(["git", "push", "origin", "main", "--force"])

if __name__ == "__main__":
    executar()
