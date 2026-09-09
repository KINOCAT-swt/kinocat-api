import sqlite3
from config import config_by_name

def get_db():
    """Veritabanina baglanir; satirlara sutun adiyla erisim saglar"""
    # config_by_name sözlüğünden local/development ayarlarını çekip DATABASE_URL değerini alıyoruz
    db_path = config_by_name['development'].DATABASE_URL
    
    # SQLite URL biçimi olan 'sqlite:///' kısmını temizleyip sadece dosya adını alıyoruz
    if db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
        
    conn = sqlite3.connect(db_path)
    
    # Yönerge Şartı: Satırlara sütun adıyla erişim sağlamak için Row fabrikasını aktif ediyoruz
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    """'leads' tablosunu olusturur (yoksa)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Yönergedeki Tablo Şeması şartlarına birebir uygun SQL sorgusu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                       isim TEXT NOT NULL,

                        telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, mesaj):
    """Yeni kayit ekler (SQL Injection korumali)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Güvenlik Zorunluluğu: Doğrudan metin birleştirmek yerine ? yer tutucuları kullanıyoruz
    cursor.execute('''
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
    ''', (isim, telefon, mesaj))
    
    conn.commit()
    conn.close()

def tum_leadler():
    """Tum kayitlari en yeniden eskiye getirir"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Yönerge Şartı: En yeniden eskiye getirmek için tarih sütununa göre azalan (DESC) sıralama yapıyoruz
    cursor.execute('SELECT * FROM leads ORDER BY tarih DESC')
    leads = cursor.fetchall()
    
    conn.close()
    return leads