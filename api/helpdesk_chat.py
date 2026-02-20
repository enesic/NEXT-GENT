"""
Helpdesk Chat API - Rule-based AI chatbot for landing page
Provides intelligent responses based on keyword matching
"""
import json
import re
from datetime import datetime
from http.server import BaseHTTPRequestHandler


# Knowledge base for rule-based responses
RESPONSES = {
    "greeting": {
        "keywords": ["merhaba", "selam", "hey", "meraba", "merba", "hi", "hello", "günaydın", "iyi akşamlar", "nasılsınız"],
        "response": "Merhaba! 👋 Ben NextGent AI Yardım Asistanı. Size nasıl yardımcı olabilirim?\n\n🔹 **Ürün Bilgisi** — NextGent hakkında detaylı bilgi\n🔹 **Demo Talebi** — Canlı demo planlamak\n🔹 **Fiyatlandırma** — Paket ve fiyat bilgileri\n🔹 **Teknik Destek** — Teknik sorular\n🔹 **İletişim** — Ekibimize ulaşmak\n\nHerhangi bir konuda sormak istediğiniz bir şey var mı?"
    },
    "demo": {
        "keywords": ["demo", "deneme", "test", "görmek", "denemek", "gösterim", "sunum", "canlı", "tanıtım"],
        "response": "🎯 **Canlı Demo Hakkında**\n\nNextGent'in tüm özelliklerini canlı ortamda deneyimleyebilirsiniz!\n\n**Demo sürecimiz:**\n1. 📧 **info@nextgent.co** adresine demo talebi gönderin\n2. 📅 Ekibimiz size uygun bir zaman ayarlar\n3. 🖥️ 30 dakikalık canlı demo oturumu\n4. ❓ Sorularınız yanıtlanır\n\n**Demo'da göreceğiniz:**\n• AI telefon operatörü canlı arama\n• WhatsApp AI diyalog örnekleri\n• Otomatik randevu motoru\n• Anlık raporlama paneli\n\nDemo planlamak için **info@nextgent.co** adresine mail atabilirsiniz!"
    },
    "pricing": {
        "keywords": ["fiyat", "ücret", "maliyet", "paket", "plan", "fiyatlandırma", "kaç para", "ne kadar", "abonelik", "lisans"],
        "response": "💰 **Fiyatlandırma Bilgisi**\n\nNextGent, işletmenizin büyüklüğüne ve ihtiyaçlarına göre özelleştirilmiş fiyatlandırma sunar.\n\n**Paketlerimiz:**\n• 🥉 **Başlangıç** — Küçük işletmeler için\n• 🥈 **Profesyonel** — Orta ölçekli işletmeler için\n• 🥇 **Kurumsal** — Büyük işletmeler için özel çözümler\n\nDetaylı fiyat bilgisi ve size özel teklif için:\n📧 **info@nextgent.co** adresine mail atabilirsiniz\n\nEkibimiz 24 saat içinde dönüş yapacaktır."
    },
    "features": {
        "keywords": ["özellik", "neler yapabilir", "ne yapıyor", "fonksiyon", "yetenek", "modül", "sistem", "platform", "hizmet"],
        "response": "🚀 **NextGent Özellikleri**\n\n**📞 AI Telefon Operatörü**\n• 7/24 otomatik çağrı karşılama\n• Doğal dil işleme ile akıllı yanıt\n• Randevu alma ve yönetimi\n\n**💬 WhatsApp AI Asistan**\n• Otomatik müşteri yanıtı\n• Ürün/hizmet bilgilendirme\n• Lead toplama\n\n**📊 Analitik Dashboard**\n• Gerçek zamanlı raporlama\n• KPI takibi\n• Müşteri memnuniyet analizi\n\n**🔒 Güvenlik**\n• KVKK uyumlu\n• Şifreli veri iletimi\n• ISO standartları\n\nDaha fazla bilgi için sormak istediğiniz bir şey var mı?"
    },
    "sector": {
        "keywords": ["sektör", "sağlık", "hukuk", "gayrimenkul", "e-ticaret", "eticaret", "finans", "güzellik", "beauty", "otomotiv", "eğitim", "konaklama", "üretim"],
        "response": "🏥 **Sektörel Çözümlerimiz**\n\nNextGent, **11 farklı sektör** için özelleştirilmiş AI asistanları sunar:\n\n• 🏥 **Sağlık & Klinik** — Randevu, hasta takibi\n• ⚖️ **Hukuk** — Müvekkil bilgilendirme, dosya takibi\n• 🏠 **Gayrimenkul** — Portföy sunumu, müşteri profilleme\n• 💅 **Güzellik** — Randevu, ürün danışmanlığı\n• 🛒 **E-Ticaret** — Sipariş takibi, müşteri destek\n• 💰 **Finans** — Hesap yönetimi, yatırım danışmanlığı\n• 🚗 **Otomotiv** — Servis, yedek parça\n• 🎓 **Eğitim** — Kayıt, ders programı\n• 🏭 **Üretim** — Tedarik, kalite kontrol\n• ☕ **Konaklama** — Rezervasyon, misafir hizmetleri\n• 🛍️ **Perakende** — Stok, satış takibi\n\nHangi sektörde faaliyet gösteriyorsunuz?"
    },
    "security": {
        "keywords": ["güvenlik", "kvkk", "gdpr", "gizlilik", "veri", "şifre", "koruma", "sertifika", "güvenli"],
        "response": "🔒 **Güvenlik ve Gizlilik**\n\nNextGent, en üst düzey güvenlik standartlarını sağlar:\n\n**Veri Güvenliği:**\n• ✅ Uçtan uca şifreli veri aktarımı\n• ✅ AES-256 şifreleme\n• ✅ IP koruması ve güvenlik duvarı\n\n**KVKK Uyumu:**\n• ✅ Veriler geçici hafızada işlenir\n• ✅ Gereksiz veriler otomatik silinir\n• ✅ Veri talep/silme hakkı\n\n**Mesaj Güvenliği:**\n• ✅ Model hiçbir konuşmayı kalıcı olarak kaydetmez\n• ✅ İzole token oturumları\n• ✅ Yetkisiz erişim engeli\n\nGüvenlik konusunda başka sorularınız var mı?"
    },
    "contact": {
        "keywords": ["iletişim", "ulaşmak", "mail", "telefon", "numara", "adres", "bize ulaş", "konuşmak", "destek", "yardım"],
        "response": "📞 **İletişim Bilgilerimiz**\n\n📧 **E-posta:** info@nextgent.co\n🌐 **Web:** www.nextgent.co\n\n**Çalışma Saatleri:**\nPazartesi - Cuma: 09:00 - 18:00\n\n**Hızlı İletişim Seçenekleri:**\n• Demo talebi → info@nextgent.co\n• Teknik destek → support@nextgent.co\n• İş birliği → partners@nextgent.co\n\nSize nasıl yardımcı olabiliriz?"
    },
    "thanks": {
        "keywords": ["teşekkür", "sağol", "sağ ol", "eywallah", "çok teşekkürler", "memnun", "harika"],
        "response": "Rica ederim! 😊 NextGent olarak size yardımcı olmaktan mutluluk duyarız.\n\nBaşka bir sorunuz olursa her zaman buradayım. İyi günler dilerim! 🙌"
    },
    "how_it_works": {
        "keywords": ["nasıl çalışıyor", "nasıl çalışır", "süreç", "adım", "akış", "işleyiş"],
        "response": "⚙️ **NextGent Nasıl Çalışır?**\n\n**4 Adımda Tam Otomasyon:**\n\n1️⃣ **Müşteri → AI**\nMüşteri talebi herhangi bir kanaldan (telefon, WhatsApp, web) gelir. AI anında karşılar.\n\n2️⃣ **AI → Sekreter Onayı**\nAI taslak oluşturur (randevu, bilgi notu vb.) ve sekreter onayına iletir.\n\n3️⃣ **Onay → CRM İşleme**\nOnaylanan kayıt otomatik olarak CRM ve randevu sistemine işlenir.\n\n4️⃣ **Bildirim → Müşteri**\nSonuç müşteriye bildirilir, geri bildirim kaydedilir.\n\n**Tüm süreç saniyeler içinde tamamlanır!** ⚡\n\nDaha detaylı bilgi ister misiniz?"
    }
}

DEFAULT_RESPONSE = "Anlıyorum! 🤔 Bu konuda size daha iyi yardımcı olabilmem için ekibimizle iletişime geçmenizi öneriyorum.\n\n📧 **info@nextgent.co** adresine mail atabilirsiniz.\n\nSize şu konularda yardımcı olabilirim:\n• Ürün özellikleri\n• Demo talebi\n• Fiyatlandırma\n• Güvenlik bilgileri\n• Sektörel çözümler\n• İletişim bilgileri\n\nBaşka bir konuda sormak istediğiniz bir şey var mı?"


def find_best_response(message):
    """Find the best matching response based on keyword analysis"""
    msg_lower = message.lower().strip()

    best_match = None
    best_score = 0

    for category, data in RESPONSES.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword in msg_lower:
                score += len(keyword)  # Longer keyword matches score higher
        if score > best_score:
            best_score = score
            best_match = category

    if best_match and best_score > 0:
        return RESPONSES[best_match]["response"]

    return DEFAULT_RESPONSE


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}

            user_message = data.get("message", "").strip()

            if not user_message:
                response = RESPONSES["greeting"]["response"]
            else:
                response = find_best_response(user_message)

            result = {
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            error_result = {
                "response": "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.",
                "status": "error"
            }
            self.send_response(200)  # Return 200 even on error for frontend compatibility
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_result, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
