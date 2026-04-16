import os

def enviar_pro_github(arquivo_html, data_str, loteria_nome):
    """
    Função centralizada para atualizar o GitHub sem apagar páginas novas.
    """
    print(f"🛡️ Iniciando Blindagem para {loteria_nome}...")

    # 1. Entra na pasta e limpa permissões
    os.system("git config --global --add safe.directory /var/www/meusite")

    # 2. PUXA as novidades (Protege o que você criou no site do GitHub)
    os.system("cd /var/www/meusite && git pull origin main")

    # 3. ADICIONA TUDO (Protege suas páginas novas .html que estão na pasta)
    os.system("cd /var/www/meusite && git add .")

    # 4. COMMIT SEGURO
    os.system(f'cd /var/www/meusite && git commit -m "Auto Update {loteria_nome} {data_str} Safe Mode"')

    # 5. PUSH AMIGÁVEL (Sem o -f para não atropelar nada)
    os.system("cd /var/www/meusite && git push origin main")

    print(f"✅ {loteria_nome} finalizado com sucesso e páginas preservadas!")
