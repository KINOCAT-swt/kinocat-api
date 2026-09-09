import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from app.database import init_db
from app.routes import pages_bp, api_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # 1. Yapılandırma ayarlarını yüklüyoruz
    app.config.from_object(config_by_name[config_name])
    
    # 2. CORS ayarlarını açıyoruz
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))
    
    # 3. Veritabanı tablosunu uygulama bağlamında otomatik oluşturuyoruz
    with app.app_context():
        init_db(app)
        
    # 4. Sunucu canlılık kontrolü (/health) uç noktası
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200
        
    # 5. Rotaları (Blueprint) uygulamaya kaydediyoruz
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
