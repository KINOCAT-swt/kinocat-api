import os
from dotenv import load_dotenv

# .env dosyasındaki değerleri okumak için yükleme fonksiyonunu çağırıyoruz
load_dotenv()

class Config:
    "Tum ayarlari tek merkezde toplayan ana yapilandirma sinifi"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan_gizli_anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    BUSINESS_CONTEXT = os.environ.get('BUSINESS_CONTEXT', 'sen bir turkce konusan yapay zeka asistanisin.')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

class DevelopmentConfig(Config):
    """Gelistirme (Local) ortami icin ayarlar"""
    DEBUG = True

class ProductionConfig(Config):
   """Canliya alim (Uretim) ortami icin ayarlar"""
DEBUG = False

# Geliştirme ve üretim için iki ayrı sınıfı seçen yapılandırma sözlüğü
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}