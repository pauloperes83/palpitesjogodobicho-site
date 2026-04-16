# config_portal.py
COOKIES_HTML = """
<div id="cookie-banner" style="display: none; position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 600px; background: #121722; color: #fff; padding: 20px; border-radius: 15px; border: 2px solid #f6c945; box-shadow: 0 10px 30px rgba(0,0,0,0.5); z-index: 10000; text-align: center;">
    <p style="margin-bottom: 15px; font-size: 14px; line-height: 1.5;">
        🍪 Utilizamos cookies para melhorar sua experiência. Ao continuar navegando, você concorda com nossa Política de Privacidade.
    </p>
    <button onclick="acceptCookies()" style="background: #f6c945; color: #121722; border: none; padding: 10px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; text-transform: uppercase;">
        Aceitar e Fechar
    </button>
</div>
<script>
    function acceptCookies() {
        localStorage.setItem('cookiesAceitos', 'true');
        document.getElementById('cookie-banner').style.display = 'none';
    }
    window.onload = function() {
        if (!localStorage.getItem('cookiesAceitos')) {
            document.getElementById('cookie-banner').style.display = 'block';
        }
    };
</script>
"""
