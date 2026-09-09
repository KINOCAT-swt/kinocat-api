import os
from dotenv import load_dotenv
from app import create_app

# .env dosyasındaki ortam değişkenlerini yüklüyoruz
load_dotenv()

# Ortam değişkeninden FLASK_ENV değerini alıyoruz (Yoksa varsayılan development)
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Sunucuyu config'den gelen DEBUG ayarıyla ayağa kaldırıyoruz
    is_debug = app.config.get('DEBUG', True)
    app.run(host='0.0.0.0', port=5000, debug=is_debug)
