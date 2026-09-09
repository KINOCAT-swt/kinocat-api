# KINOCAT AI Assistant & Management Dashboard

Bu proje, sinema ve dijital yayıncılık odaklı bir yapay zeka asistanı ve müşteri adaylarını filtreleyen bulut tabanlı bir yönetim panelidir.

## Projenin Yaptığı İş (Özet)
- **Frontend (Wix Studio):** Kullanıcıların KINOCAT yapay zeka asistanı ile etkileşime girdiği ve kurumsal müşteri yönetim paneline (Dashboard) eriştiği iki ana arayüzü barındırır.
- **Backend (Flask & Render):** Wix'ten gelen kullanıcı taleplerini yakalar, veritabanına güvenli bir şekilde kaydeder ve yönetim paneline anlık olarak besler.

## Sistemi Çalıştırma Adımları
1. Projenin yerel bilgisayarda çalıştırılması için terminalde `python run.py` komutu verilir. Sunucu `http://127.0.0.1:5000` adresinde ayağa kalkar.
2. Canlı dağıtım için kodlar GitHub aracılığıyla Render bulut sunucusuna (Web Service) bağlanmıştır. Her yeni push işleminde Render otomatik olarak canlı sürümü günceller.
