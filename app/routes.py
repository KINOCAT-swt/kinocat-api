from flask import Blueprint, render_template, request, jsonify
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

# Kurallar Şartı: Sayfalar için yönlendirme Blueprint'i
pages_bp = Blueprint('pages', __name__)

# Kurallar Şartı: API uç noktaları için '/api' önekli Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# GET / -> Karşılama sayfasını gösterir
@pages_bp.route('/')
def index():
    return render_template('index.html')

# GET /dashboard -> Yönetim panelini gösterir
@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
# POST /api/sohbet -> AI'a mesaj iletir
@api_bp.route('/sohbet', methods=['POST'])
def sohbet_ilet():
    data = request.get_json() or {}
    mesaj = data.get('mesaj')
    gecmis = data.get('gecmis', [])

    # Kurallar Şartı: Eksik veri gelirse 400 durum kodu kullanın
    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alani zorunludur."}), 400

    # Kurallar Şartı: AI çağrısını try-except ile sarın; AIServiceError yakalayıp kibar JSON hata dönün
    try:
        yanit = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "yanit": yanit})
        
    except AIServiceError as e:
        # Kurallar Şartı: AI hatası olursa 503 durum kodu kullanın
        return jsonify({"basari": False, "hata": f"Yapay zeka asistanina su an ulasilamiyor: {str(e)}"}), 503
# POST /api/leads -> Yeni lead kaydeder
@api_bp.route('/leads', methods=['POST'])
def lead_kaydet():
    data = request.get_json() or {}
    isim = data.get('isim')
    telefon = data.get('telefon')
    mesaj = data.get('mesaj') # Opsiyonel alan

    # Kurallar Şartı: Eksik veri gelirse 400 durum kodu kullanın
    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "Isim ve telefon alanlari zorunludur."}), 400

    # SQL kodu yazmadan doğrudan veritabanı katmanını çağırıyoruz
    lead_ekle(isim, telefon, mesaj)
    
    # Kurallar Şartı: Yeni kayıtta 201 durum kodu kullanın
    return jsonify({"basari": True, "mesaj": "Kayit basariyla olusturuldu."}), 201

# GET /api/leads -> Tüm lead'leri getirir
@api_bp.route('/leads', methods=['GET'])
def leads_listele():
    # SQL kodu yazmadan doğrudan veritabanı katmanından kayıtları çekiyoruz
    kayitlar = tum_leadler()
    
    # SQLite Row nesnelerini JSON formatına dönüştürebilmek için sözlüğe çeviriyoruz
    liste = []
    for k in kayitlar:
        liste.append({
            "id": k["id"],
            "isim": k["isim"],
            "telefon": k["telefon"],
            "mesaj": k["mesaj"],
            "tarih": k["tarih"]
        })
        
    # Kurallar Şartı: basari alanı içeren bir JSON döndürmeli
    return jsonify({"basari": True, "data": liste})
