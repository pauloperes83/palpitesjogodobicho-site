import os
import sys
from datetime import datetime
import random
import subprocess

bichos_oficiais = {
    "Avestruz": {"gr": "01", "dz": ["01", "02", "03", "04"], "e": "🦩", "puxa": "Vaca, Águia, Galo, Pavão, Peru"},
    "Águia": {"gr": "02", "dz": ["05", "06", "07", "08"], "e": "🦅", "puxa": "Coelho, Avestruz, Galo, Pavão, Peru"},
    "Burro": {"gr": "03", "dz": ["09", "10", "11", "12"], "e": "🫏", "puxa": "Cavalo, Elefante, Touro, Veado, Coelho, Cobra"},
    "Borboleta": {"gr": "04", "dz": ["13", "14", "15", "16"], "e": "🦋", "puxa": "Cabra, Elefante, Gato, Leão, Cachorro, Galo"},
    "Cachorro": {"gr": "05", "dz": ["17", "18", "19", "20"], "e": "🐕", "puxa": "Galo, Gato, Camelo, Macaco, Porco, Pavão"},
    "Cabra": {"gr": "06", "dz": ["21", "22", "23", "24"], "e": "🐐", "puxa": "Carneiro, Macaco, Elefante, Touro, Tigre, Urso"},
    "Carneiro": {"gr": "07", "dz": ["25", "26", "27", "28"], "e": "RAM", "puxa": "Cabra, Coelho, Vaca"},
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
        html += f'<div class="palpite-box"><div class="bicho-title"><h3>{info["gr"]} - {n.upper()} {info["e"]}</h3></div><div class="numbers-grid"><div class="num-card"><label>Milhares</label><span>{random.randint(1,9)}{random.randint(1,9)}{d}</span></div><div class="num-card"><label>Centenas</label><span>{random.randint(1,9)}{d}</span></div><div class="num-card"><label>Dezenas</label><span>{d}</span></div></div></div>'
    return html

def build_full_page(kw, btn_link, btn_text, artigo_content, palpites_txt, grid_bichos):
    css = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"><style>
        .dropdown-content { display: none; position: absolute; background-color: #121722; min-width: 160px; box-shadow: 0px 8px 16px rgba(0,0,0,0.5); z-index: 99; border: 1px solid rgba(255,255,255,0.1); text-align: left; }
        .dropdown-content a { margin: 0 !important; padding: 12px 16px !important; display: block !important; font-size: 14px !important; }
        .dropdown:hover .dropdown-content { display: block; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #ffffff; color: #333; margin: 0; padding: 0; line-height: 1.8; }
        .container { width: 95%; max-width: 1000px; margin: 0 auto; }
        header { background: #121722; padding: 20px 0; border-bottom: 3px solid #f6c945; text-align: center; }
        .logo img { height: 150px; width: auto; }
        nav { background: #121722; padding: 12px 0; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
        nav a { color: #d8dcec; text-decoration: none; margin: 0 15px; font-weight: 600; font-size: 15px; text-transform: uppercase; }
        .section { padding: 40px 0; }
        h1 { font-size: 2.2rem; color: #222; text-align: center; margin-bottom: 25px; }
        h2 { font-size: 1.6rem; color: #b8860b; border-left: 6px solid #f6c945; padding-left: 15px; margin: 35px 0 20px 0; }
        p { margin-bottom: 15px; font-size: 1.1rem; color: #444; text-align: justify; }
        .link-seo { color: #d4a017; font-weight: bold; text-decoration: underline; }
        .palpite-box { background: #f9f9f9; border: 1px solid #eee; border-radius: 12px; padding: 20px; margin: 25px 0; }
        .numbers-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; text-align: center; }
        .num-card { border: 1px solid #ddd; padding: 10px; border-radius: 8px; background: #fff; }
        .num-card span { display: block; font-weight: bold; font-size: 1.1rem; color: #d4a017; }
        .btn-apostar { display: inline-block; background: #b8860b; color: white; padding: 18px 40px; border-radius: 10px; text-decoration: none; font-weight: bold; text-transform: uppercase; margin-top: 20px; }
        .btn-whats { display: block; width: fit-content; margin: 30px auto; background: #25d366; color: white; padding: 15px 35px; border-radius: 50px; text-decoration: none; font-weight: bold; text-align: center; }
        .site-footer { background-color: #0d1016; border-top: 1px solid rgba(255,255,255,0.08); padding: 50px 0 30px 0; text-align: center; margin-top: 50px; width: 100%; }
        .footer-wrap { display: flex; flex-direction: column; align-items: center; }
        .footer-title { font-size: 1.8rem; color: #f6c945; margin-bottom: 15px; font-weight: bold; }
        .footer-warning { font-size: 0.85rem; color: #888ea1; max-width: 700px; margin: 0 auto 30px auto; line-height: 1.6; text-align: center; }
        .footer-social { display: flex; gap: 20px; margin-bottom: 30px; justify-content: center; }
        .footer-social svg { width: 30px; height: 30px; fill: #ffffff; transition: fill 0.3s; }
        .footer-social a:hover svg { fill: #f6c945; }
        .footer-links { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; margin-bottom: 30px; }
        .footer-links a { color: #d8dcec; font-size: 0.95rem; font-weight: 500; text-decoration: none; transition: color 0.3s; }
        .footer-copy { font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px; width: 90%; margin: 0 auto; color: #6c757d; }
        @media (max-width: 768px) { .logo img { height: 100px; } nav a { margin: 0 5px; font-size: 12px; } }
    </style>'''
    
    return f'''<!DOCTYPE html><html lang="pt-BR"><head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9Y3FW10LC2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9Y3FW10LC2');</script>
<link rel="icon" type="image/png" href="images/favicon.png"><link rel="shortcut icon" href="images/favicon.png">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{kw}</title>{css}</head><body>
<header><div class="container"><a href="index.html" class="logo"><img src="images/logo-palpites.png"></a></div></header>
<nav><div class="container">
    <a href="index.html">Início</a><a href="palpite-do-dia.html">Palpite do Dia</a>
    <div class="dropdown" style="display: inline-block; position: relative;"><a href="#" style="cursor: default; margin-right: 15px;">Bancas ▾</a>
    <div class="dropdown-content"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" target="_blank">Águia Prime</a><a href="https://app.valedasorteloterias.club/pr/g5P71dlw" target="_blank">Vale da Sorte</a></div></div>
    <a href="puxadas-do-bicho.html">Puxadas</a><a href="milhares-viciadas.html">Milhares</a><a href="https://resultadosdojogo.com/" target="_blank" style="color: #f6c945;">Resultados</a>
</div></nav>
<section class="section"><div class="container">
    <div style="text-align: center; margin-bottom: 25px;"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU"><img src="images/aguia-posts.webp" style="width: 300px; border-radius: 8px;"></a></div>
    <h1>{kw}</h1>
    {artigo_content}
    <p style="text-align: center; font-weight: bold; margin-top: 30px; font-size: 1.2rem; color: #b8860b;">🍀 Desejamos muita sorte em suas apostas e que os palpites de hoje tragam prêmios! 🍀</p>
</div></section>
<footer class="site-footer"><div class="container footer-wrap">
    <div class="footer-title">Palpites do Jogo do Bicho</div>
    <p class="footer-warning">Esclarecemos que não temos vínculo com o serviço ou pessoas que operam o Jogo do Bicho e que os resultados e estatísticas são meramente informativos.</p>
    <div class="footer-social">
        <a href="https://www.instagram.com/palpitess_jb?igsh=MW5uaTVjb3ZramhiNQ%3D%3D&utm_source=qr" target="_blank"><svg viewBox="0 0 24 24"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2.2A2.8 2.8 0 0 0 4.2 7v10A2.8 2.8 0 0 0 7 19.8h10a2.8 2.8 0 0 0 2.8-2.8V7A2.8 2.8 0 0 0 17 4.2H7Zm10.6 1.6a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2.2A2.8 2.8 0 1 0 12 14.8 2.8 2.8 0 0 0 12 9.2Z"/></svg></a>
        <a href="https://www.facebook.com/palpitesdobicho" target="_blank"><svg viewBox="0 0 24 24"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.5 1.6-1.5h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.4v2.2H8v3.2h2.1V22h3.4Z"/></svg></a>
        <a href="https://www.youtube.com/@Palpitesdo_JogodoBicho" target="_blank"><svg viewBox="0 0 24 24"><path d="M23 12s0-3.1-.4-4.6a3 3 0 0 0-2.1-2.1C19 5 12 5 12 5s-7 0-8.5.4A3 3 0 0 0 1.4 7.4C1 8.9 1 12 1 12s0 3.1.4 4.6a3 3 0 0 0 2.1 2.1C5 19 12 19 12 19s7 0 8.5-.4a3 3 0 0 0 2.1-2.1c.4-1.5.4-4.5.4-4.5ZM9.8 15.5v-7L16 12l-6.2 3.5Z"/></svg></a>
    </div>
    <div class="footer-links">
        <a href="sobre.html">Sobre nós</a><a href="contato.html">Contato</a>
        <a href="politica-de-privacidade.html">Privacidade</a><a href="termos-de-uso.html">Termos de Uso</a>
    </div>
    <p class="footer-copy" style="text-align: center;">© 2026 Palpites do Jogo. Todos os direitos reservados.</p>
</div></footer></body></html>'''

def executar():
    tipo = sys.argv[1] if len(sys.argv) > 1 else "todos"
    agora = datetime.now()
    hoje = agora.strftime("%d/%m/%Y")
    dia = agora.day
    palpites_txt = gerar_palpites_html(dia)

    grid_bichos = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; margin-top: 20px;">'
    for nome, dados in bichos_oficiais.items():
        grid_bichos += f'<div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; text-align: center; background: #fff;"><div style="font-weight: bold; font-size: 0.9rem; color: #121722; margin-bottom: 5px;">{dados["gr"]}</div><div style="font-size: 2rem;">{dados["e"]}</div><div style="font-weight: bold; font-size: 0.8rem; margin: 5px 0;">{nome.upper()}</div><div style="font-size: 0.75rem; color: #d4a017; font-weight: bold;">{" ".join(dados["dz"])}</div></div>'
    grid_bichos += '</div>'

    l_pal = '<a href="https://palpitesjogodobicho.com.br/palpite-do-dia.html" class="link-seo">Palpite do dia</a>'
    l_pux = '<a href="https://palpitesjogodobicho.com.br/puxadas-do-bicho.html" class="link-seo">Puxadas do Bicho</a>'
    l_mil = '<a href="https://palpitesjogodobicho.com.br/milhares-viciadas.html" class="link-seo">Milhares Viciadas</a>'

    if tipo in ["rio", "todos"]:
        kw = f"Palpite do dia do Jogo do Bicho de hoje Rio {hoje}"
        art = f'''<p>Se você busca <strong>{kw}</strong>, aqui vai encontrar um conteúdo focado apenas na banca do Rio.</p>
        <p>Reunimos análises, grupos que chamam atenção e combinações muito procuradas por quem acompanha os sorteios do dia. O objetivo é trazer um texto direto, organizado e fácil de ler. Tudo com foco em <strong>{kw}</strong>, sem misturar outras loterias.</p>
        
        <div style="text-align: center;"><a href="https://app.aguiaprime119000.com/pr/y8X6LEBU" class="btn-apostar">🎰 APOSTAR AGORA</a></div>
        
        {palpites_txt}
        
        <a href="https://chat.whatsapp.com/HyYz0zMD1ovAaWeY99Jfpi" class="btn-whats" target="_blank">RECEBER PALPITES NO WHATSAPP</a>
        
        <h2>{kw} com foco na banca Rio</h2>
        <p>Quem pesquisa palpite do dia quer encontrar uma base para analisar melhor os jogos do dia. Por isso, o foco aqui está nas combinações mais observadas dentro da rotina da banca Rio. O Jogo do Bicho do Rio movimenta buscas diárias por grupos, dezenas, centenas e milhares.</p>
        <p>Muitos jogadores acompanham os resultados anteriores para tentar identificar repetições, atrasos e padrões. Esse comportamento faz crescer ainda mais a procura por <strong>{kw}</strong>. Principalmente entre quem gosta de montar jogos com mais atenção aos detalhes.</p>

        <h2>Por que o termo {kw} é tão buscado</h2>
        <p>A expressão <strong>{kw}</strong> é muito forte porque une data, local e intenção de busca. Quem digita isso normalmente quer um conteúdo exato, atualizado e voltado só para o Rio.</p>
        <p>Além disso, muitas pessoas também procuram por termos relacionados como palpite do Rio, resultado do Rio, grupo do dia e milhar do dia. Essas variações ajudam a reforçar o tema principal da página. Outro ponto importante é que o público costuma buscar conteúdos rápidos e objetivos. Por isso, textos com boa escaneabilidade tendem a funcionar melhor para esse tipo de palavra-chave.</p>

        <h2>{kw} e análise dos grupos mais observados</h2>
        <p>Dentro da rotina do Jogo do Bicho do Rio, alguns grupos sempre despertam mais atenção. Isso acontece porque certos bichos se tornam populares entre os apostadores em diferentes períodos. Ao montar um conteúdo sobre <strong>{kw}</strong>, vale destacar os grupos mais lembrados.</p>

        <h3>Grupos populares no Jogo do Bicho do Rio</h3>
        <p>Os grupos populares costumam receber mais atenção de quem acompanha palpites diariamente. Muita gente observa o histórico recente para decidir em qual grupo apostar. Também é comum relacionar grupos com sonhos, datas especiais e repetições de resultados passados. Esses fatores aumentam ainda mais o interesse por determinados bichos ao longo do dia.</p>

        <h3>Dezenas, centenas e milhares mais procuradas</h3>
        <p>Não é só o grupo que chama atenção no Jogo do Bicho do Rio. As buscas por dezena, centena e milhar também são muito fortes. Quem procura <strong>{kw}</strong> geralmente quer sugestões completas. Ou seja, não apenas o bicho, mas também números que possam ser aproveitados no jogo.</p>

        <h2>Como usar o {kw} de forma estratégica</h2>
        <p>O ideal é usar o <strong>{kw}</strong> como apoio na sua análise. Muitos jogadores observam tendências antes de definir se vão no grupo, dezena, centena ou milhar. Outra prática comum é comparar o palpite com o histórico recente da banca Rio.</p>
        <p>Isso ajuda a perceber quais combinações estão mais comentadas no momento. Também vale acompanhar os horários tradicionais do Rio, como PTM, PT, PTV, PTN e Corujinha. Esses horários fazem parte da rotina de quem acompanha os resultados diariamente.</p>
        <p>Aprenda usar as {l_mil} e {l_pux} para jogar, pois com elas suas chances de ganhar no jogo do bicho aumentam.</p>

        <h2>Resultado do Rio e histórico recente no Jogo do Bicho</h2>
        <p>As buscas por resultado do Rio costumam caminhar junto com a procura por palpites. Afinal, muita gente usa os últimos resultados como base para montar os jogos do dia. Por isso, conteúdos sobre <strong>{kw}</strong> ficam mais fortes quando conversam com esse interesse. O leitor quer palpite, mas também quer contexto.</p>

        <h3>A importância de observar o histórico</h3>
        <p>Observar o histórico é uma forma de tentar enxergar padrões dentro da banca Rio. Embora não exista garantia de resultado, essa análise faz parte da rotina de muitos jogadores. Há quem prefira observar grupos atrasados. Outros gostam mais de seguir bichos que vêm aparecendo com frequência recente.</p>

        <h2>Palpite do Bicho Loteria Federal de Hoje</h2>
        <p>Se você procura <strong>Palpite do Bicho Loteria Federal de Hoje</strong>, aqui encontra um conteúdo direto e fácil de acompanhar. A proposta é trazer um texto curto, objetivo e pensado para quem busca essa palavra-chave no Google. A busca por Palpite do Bicho Loteria Federal de Hoje cresce entre quem gosta de acompanhar a Federal e consultar referências antes do sorteio.</p>

        <h2>Tabela dos bichos e significado dos sonhos no Rio</h2>
        {grid_bichos}
        <p>Outro ponto muito buscado por quem procura <strong>{kw}</strong> é a tabela dos bichos. Ela ajuda a relacionar grupo, animal e numeração dentro do jogo. O significado dos sonhos também aparece bastante nesse universo. Muitos jogadores gostam de transformar sonhos em palpites para o dia. Isso aumenta a relevância de conteúdos que trabalham o tema de forma completa. Especialmente quando o foco está totalmente na banca do Rio.</p>'''
        with open("/var/www/meusite/palpite-do-bicho-rj.html", 'w', encoding='utf-8') as f:
            f.write(build_full_page(kw, "https://app.aguiaprime119000.com/pr/y8X6LEBU", "🎰 APOSTAR NO RIO", art, palpites_txt, grid_bichos))

    if tipo in ["look", "todos"]:
        kw = f"Palpite da Look Loterias de hoje Goiás {hoje}"
        art = f'''<p>Procurando pelo melhor <strong>{kw}</strong>? Nossa equipe foca nas tendências exclusivas das loterias de Goiás e Goiânia.</p>
        <p>O <strong>resultado look loterias de hoje</strong> influencia as milhares sugeridas para os horários das <strong>07h, 09h, 11h, 14h, 16h, 18h, 21h e 23h</strong>.</p>
        <div style="text-align: center;"><a href="https://app.valedasorteloterias.club/pr/g5P71dlw" class="btn-apostar">🎰 APOSTAR NA LOOK</a></div>
        {palpites_txt}
        <a href="https://chat.whatsapp.com/HyYz0zMD1ovAaWeY99Jfpi" class="btn-whats" target="_blank">GRUPO LOOK GOIÁS WHATSAPP</a>
        <h2>Estratégia Look: {kw}</h2><p>Observe os atrasos da banca Look. Nosso <strong>palpite da look de hoje</strong> é gerado com dados técnicos e o <strong>resultado da look de ontem</strong>.</p>
        <h2>Como Jogar e Ganhar na Look</h2><p>Consulte o {l_pal} e utilize técnicas de {l_pux} focadas na banca Look e Goiás. As {l_mil} seguem padrões regionais separados do Rio.</p>
        {grid_bichos}'''
        with open("/var/www/meusite/palpite-do-bicho-look.html", 'w', encoding='utf-8') as f:
            f.write(build_full_page(kw, "https://app.valedasorteloterias.club/pr/g5P71dlw", "🎰 APOSTAR NA LOOK", art, palpites_txt, grid_bichos))

    os.chdir("/var/www/meusite")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Timed Update {tipo} {hoje}"])
    subprocess.run(["git", "push", "origin", "main", "--force"])

if __name__ == "__main__":
    executar()
