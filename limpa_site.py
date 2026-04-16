import os
import re
from config_portal import COOKIES_HTML

paginas = [
    "index.html", "contato.html", "sobre.html", 
    "politica-de-privacidade.html", "termos-de-uso.html", 
    "palpite-do-dia.html", "milhares-viciadas.html", "puxadas-do-bicho.html"
]

diretorio = "/var/www/meusite/"

print("🔄 Iniciando Injeção Forçada de Cookies...")

for nome_arquivo in paginas:
    caminho = os.path.join(diretorio, nome_arquivo)

    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Limpa qualquer versão antiga (mesmo que esteja incompleta)
        conteudo = re.sub(r'<div id="cookie-banner".*?</script>', '', conteudo, flags=re.DOTALL)

        # Injeta o banner antes do fechamento do Body (case insensitive para evitar erro)
        if "</body>" in conteudo.lower():
            # Faz a troca preservando a tag original
            padrao = re.compile(r"</body>", re.IGNORECASE)
            novo_conteudo = padrao.sub(COOKIES_HTML + "\n</body>", conteudo)

            with open(caminho, "w", encoding="utf-8") as f:
                f.write(novo_conteudo)
            print(f"✅ Banner aplicado com sucesso: {nome_arquivo}")
        else:
            print(f"⚠️ Erro: Não achei a tag body em {nome_arquivo}")
    else:
        print(f"❌ Arquivo não encontrado: {nome_arquivo}")

print("\n🚀 PROCESSO CONCLUÍDO!")
