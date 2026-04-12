import os
import random
from datetime import datetime

# LISTA DE BICHOS DO SEU ROBO
bichos_oficiais = {
    "Avestruz": {"gr": "01", "dz": ["01", "02", "03", "04"], "e": "🦩"},
    "Águia": {"gr": "02", "dz": ["05", "06", "07", "08"], "e": "🦅"},
    "Burro": {"gr": "03", "dz": ["09", "10", "11", "12"], "e": "🫏"},
    "Cachorro": {"gr": "05", "dz": ["17", "18", "19", "20"], "e": "🐕"},
    "Cobra": {"gr": "09", "dz": ["33", "34", "35", "36"], "e": "🐍"},
    "Leão": {"gr": "16", "dz": ["61", "62", "63", "64"], "e": "🦁"}
}

def teste_manual():
    hoje = "11/04/2026"
    print(f"--- INICIANDO TESTE PARA DATA: {hoje} ---")
    
    html_palpites = ""
    # Gera 6 palpites aleatórios para o teste
    sorteados = random.sample(list(bichos_oficiais.items()), 6)
    
    for nome, dados in sorteados:
        dz = random.choice(dados["dz"])
        m = f"{random.randint(1,9)}{random.randint(0,9)}{dz}"
        c = f"{random.randint(1,9)}{dz}"
        
        html_palpites += f'''
        <div class="palpite-box">
            <div class="bicho-title"><h3>{dados["gr"]} - {nome.upper()} {dados["e"]}</h3></div>
            <div class="numbers-grid">
                <div class="num-card"><label>Milhar</label><span>{m}</span></div>
                <div class="num-card"><label>Centena</label><span>{c}</span></div>
                <div class="num-card"><label>Dezena</label><span>{dz}</span></div>
            </div>
        </div>'''

    # Criando o arquivo de resultado do teste
    conteudo_final = f"<h1>Teste de Palpites - {hoje}</h1>" + html_palpites
    
    with open("/var/www/meusite/resultado_do_teste.html", 'w', encoding='utf-8') as f:
        f.write(conteudo_final)
    
    print("SUCESSO: O arquivo 'resultado_do_teste.html' foi criado na pasta /var/www/meusite/")
    print("Abra esse arquivo para conferir se os bichos e números mudaram!")

if __name__ == "__main__":
    teste_manual()
