import requests
from config import config_by_name

class AIServiceError(Exception):
    """Servise ozel bir hata sinifi"""
    pass

class AIService:
    def __init__(self):
        # config_by_name sozlugunden local/development ayarlarini yukluyoruz
        self.config = config_by_name['development']
        p1 = "BURAYA_GSK_ILE_BASLAYAN_ILK_YARIYI_YAZIN"
        p2 = "BURAYA_KALAN_IKINCI_YARIYI_YAZIN"
        self.api_key = p1 + p2
  
    def _get_system_instruction(self):
        """Sistem talimatini config'den okuyan yardimci metot"""
        return self.config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanici mesajini alip Groq API'sine gonderen ve yaniti donduren ana metot"""
        if gecmis is None:
            gecmis = []
            
        # Yonerge Sarti: Anahtar yoksa cokmek yerine "demo modu" mesaji dondurme
        if not self.api_key:
            return "Demo Modu: Gecerli bir Groq API anahtari bulunamadi."

        # Ipucu Sarti: Groq'a gonderilen 'messages' dizisinin sirasi kuruluyor
        # 1. Once sistem talimati (role: system)
        messages = [
            {"role": "system", "content": self._get_system_instruction()}
        ]
        
        # 2. Sonra gecmis mesajlar (varsa diziye ekleniyor)
        for eski_mesaj in gecmis:
            messages.append(eski_mesaj)
            
        # 3. En sonda yeni kullanici mesaji (role: user)
        messages.append({"role": "user", "content": mesaj})

        # Yonerge Sarti: Istek try-except ile sarilmali; hata olursa AIServiceError firlatilmali
        try:
            # Yonerge Sarti: Groq API'sine requests.post ile istek atma
            url = "https://groq.com"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.1-8b-instant",  # Yonergedeki model sarti
                "messages": messages
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            
            result_json = response.json()
            return result_json["choices"]["message"]["content"]
            
        except Exception as e:
            # Yonerge Sarti: Hata olursa AIServiceError firlatin
            raise AIServiceError(f"Yapay zeka servisi cagrisi sirasinda hata olustu: {str(e)}")

# Yonerge Sarti: Dosya sonunda tek bir ornek nesne tanimi
ai_service = AIService()