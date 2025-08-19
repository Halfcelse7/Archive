# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 23:46:43 2025

@author: ismtu
"""

import random
from datetime import date

burclar = {
    "Koç": {"element":"Ateş","nitelik":"Öncü","ana_konus":"Girişim, cesaret, liderlik"},
    "Boğa": {"element":"Toprak","nitelik":"Sabit","ana_konus":"Kararlılık, güven, maddi konular"},
    "İkizler": {"element":"Hava","nitelik":"Değişken","ana_konus":"İletişim, esneklik, öğrenme"},
    "Yengeç": {"element":"Su","nitelik":"Öncü","ana_konus":"Duygular, aile, koruma"},
    "Aslan": {"element":"Ateş","nitelik":"Sabit","ana_konus":"Özgüven, yaratıcılık, sahne"},
    "Başak": {"element":"Toprak","nitelik":"Değişken","ana_konus":"Analiz, düzen, hizmet"},
    "Terazi": {"element":"Hava","nitelik":"Öncü","ana_konus":"İlişkiler, denge, estetik"},
    "Akrep": {"element":"Su","nitelik":"Sabit","ana_konus":"Derinlik, dönüşüm, tutku"},
    "Yay": {"element":"Ateş","nitelik":"Değişken","ana_konus":"Özgürlük, keşif, felsefe"},
    "Oğlak": {"element":"Toprak","nitelik":"Öncü","ana_konus":"Sorumluluk, hedef, disiplin"},
    "Kova": {"element":"Hava","nitelik":"Sabit","ana_konus":"Yenilik, topluluk, fikir"},
    "Balık": {"element":"Su","nitelik":"Değişken","ana_konus":"Sezgi, hayal, empati"}
}

uyumluluk = {
    "Koç":{"en_uyumlu":"Aslan","en_uyumsuz":"Boğa"},
    "Boğa":{"en_uyumlu":"Başak","en_uyumsuz":"Koç"},
    "İkizler":{"en_uyumlu":"Terazi","en_uyumsuz":"Balık"},
    "Yengeç":{"en_uyumlu":"Balık","en_uyumsuz":"Aslan"},
    "Aslan":{"en_uyumlu":"Koç","en_uyumsuz":"Akrep"},
    "Başak":{"en_uyumlu":"Boğa","en_uyumsuz":"Yay"},
    "Terazi":{"en_uyumlu":"İkizler","en_uyumsuz":"Oğlak"},
    "Akrep":{"en_uyumlu":"Yengeç","en_uyumsuz":"Aslan"},
    "Yay":{"en_uyumlu":"Koç","en_uyumsuz":"Başak"},
    "Oğlak":{"en_uyumlu":"Boğa","en_uyumsuz":"Terazi"},
    "Kova":{"en_uyumlu":"Terazi","en_uyumsuz":"Boğa"},
    "Balık":{"en_uyumlu":"Yengeç","en_uyumsuz":"İkizler"}
}

def yorum_sec(burc, kategori, yorum_listesi):
    today = date.today().strftime("%Y%m%d")
    seed_value = hash(f"{today}-{burc}-{kategori}") % (10**8)
    random.seed(seed_value)
    return random.choice(yorum_listesi)

duygu_opts = [
    "Duygusal olarak yoğun bir gün geçirebilirsiniz.",
    "İçsel huzur ve dengeyi hissetmek mümkün.",
    "Yakın ilişkilerde iletişim biraz hassas olabilir."
]
is_opts = [
    "İş ve projelerde kararlarınızı mantık çerçevesinde alın.",
    "Yeni fırsatlar kapınızı çalabilir; strateji önem kazanıyor.",
    "Günlük görevleri ertelememek sizi rahatlatacak."
]
finans_opts = [
    "Maddi konularda temkinli olun, küçük yatırımlar ön planda.",
    "Harcamalarınızı planlamak, ilerleyen günlerde rahatlık sağlayacak.",
    "Beklenmedik bir fırsat maddi kazanç sağlayabilir."
]
strateji_opts = [
    "Gününüzü planlarken hem mantığı hem sezgiyi kullanın.",
    "Hedeflerinize odaklanın, küçük adımlar büyük fark yaratır.",
    "İlişkilerde açık iletişim sizi güçlü kılacak."
]

kritik_gunler = [
    "Dikkat: Bugün sabırsızlık ve acele karar riskini göz önünde bulundurun.",
    "Fırsat: Yaratıcılık ve risk alma günü, yeni başlangıçlar için uygun.",
    "Uyarı: İlişkilerde yanlış anlaşılmalar olabilir, net iletişim şart."
]

def skor_hesapla(burc, kategori):
    today = date.today().strftime("%Y%m%d")
    seed_value = hash(f"{today}-{burc}-{kategori}") % (10**8)
    random.seed(seed_value)
    return random.randint(0, 10)

def gunluk_burc_yorumu(burc):
    if burc not in burclar:
        return "Geçersiz burç. Lütfen geçerli bir burç girin."
    
    ozellik = burclar[burc]
    
    duygu = yorum_sec(burc, "duygu", duygu_opts)
    is_action = yorum_sec(burc, "is", is_opts)
    finans = yorum_sec(burc, "finans", finans_opts)
    strateji = yorum_sec(burc, "strateji", strateji_opts)
    kritik = yorum_sec(burc, "kritik", kritik_gunler)
    
    skor_gunluk = skor_hesapla(burc, "gunluk")
    skor_is = skor_hesapla(burc, "is")
    skor_finans = skor_hesapla(burc, "finans")
    skor_ask = skor_hesapla(burc, "ask")
    
    en_uyumlu = uyumluluk[burc]["en_uyumlu"]
    en_uyumsuz = uyumluluk[burc]["en_uyumsuz"]
    
    mesaj = f"""
{burc} Burcu - Element: {ozellik['element']}, Nitelik: {ozellik['nitelik']}
Ana Konu: {ozellik['ana_konus']}

Günlük Duygu Durumu: {duygu}
İş / Aksiyon: {is_action}
Finans / Fırsatlar: {finans}
Stratejik Tavsiye: {strateji}
Kritik Gün Uyarısı: {kritik}

Burç Uyumluluğu:
En uyumlu: {en_uyumlu}
En uyumsuz: {en_uyumsuz}

Skor Sistemi (0-10):
Günlük: {skor_gunluk} | İş: {skor_is} | Finans: {skor_finans} | Aşk: {skor_ask}
"""
    return mesaj

print("Günlük burç yorumunu almak için burcunuzu girin (örn: Koç, Boğa, ...):")
secim = input("Burç: ").capitalize()
print("\n=== Günlük Burç Yorumu ===")
print(gunluk_burc_yorumu(secim))
