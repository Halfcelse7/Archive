# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 15:18:27 2025

@author: ismtu
"""

import random

tarot_cards = {

    "The Fool": {"upright": "Yeni başlangıç, özgürlük", "reversed": "Dikkatsizlik, sorumsuzluk"},
    "The Magician": {"upright": "Yaratıcılık, beceri", "reversed": "Hile, yetersizlik"},
    "The High Priestess": {"upright": "Sezgi, gizem", "reversed": "Gizli planlar, bilinmezlik"},
    "The Empress": {"upright": "Bereket, şefkat", "reversed": "Aşırı kontrol, ihmal"},
    "The Emperor": {"upright": "Otorite, düzen", "reversed": "Tuzak, kontrolsüzlük"},
    "The Hierophant": {"upright": "Öğreti, rehberlik", "reversed": "Kural dışılık, başkaldırı"},
    "The Lovers": {"upright": "Aşk, uyum", "reversed": "Uyumsuzluk, çatışma"},
    "The Chariot": {"upright": "Zafer, irade", "reversed": "Engeller, kayıtsızlık"},
    "Strength": {"upright": "Cesaret, sabır", "reversed": "Güçsüzlük, öfke"},
    "The Hermit": {"upright": "İçsel arayış, bilgelik", "reversed": "Yalnızlık, geri çekilme"},
    "Wheel of Fortune": {"upright": "Şans, döngü", "reversed": "Talihsizlik, durgunluk"},
    "Justice": {"upright": "Adalet, denge", "reversed": "Haksızlık, dengesizlik"},
    "The Hanged Man": {"upright": "Teslimiyet, perspektif", "reversed": "İnat, kayıtsızlık"},
    "Death": {"upright": "Dönüşüm, son", "reversed": "Değişime direnç, kayıp"},
    "Temperance": {"upright": "Denge, uyum", "reversed": "Aşırılık, uyumsuzluk"},
    "The Devil": {"upright": "Bağımlılık, sınırlar", "reversed": "Kurtulma, özgürlük"},
    "The Tower": {"upright": "Ani değişim, şok", "reversed": "Direnç, gecikme"},
    "The Star": {"upright": "Umut, iyileşme", "reversed": "Umutsuzluk, hayal kırıklığı"},
    "The Moon": {"upright": "Sezgi, bilinçaltı", "reversed": "Yanılsama, korku"},
    "The Sun": {"upright": "Mutluluk, başarı", "reversed": "Hüzün, gecikme"},
    "Judgement": {"upright": "Uyanış, karar", "reversed": "Kendini sorgulama, ertelenme"},
    "The World": {"upright": "Tamamlama, başarı", "reversed": "Erteleme, eksiklik"},


    "Ace of Cups": {"upright": "Duygusal başlangıç", "reversed": "Duygusal tıkanıklık"},
    "Two of Cups": {"upright": "İkili uyum", "reversed": "Uyumsuzluk, çatışma"},
    "Three of Cups": {"upright": "Kutlama, arkadaşlık", "reversed": "Gurur, ihanet"},
    "Four of Cups": {"upright": "Düşünce, içe dönüş", "reversed": "Kıskançlık, fırsat kaybı"},
    "Five of Cups": {"upright": "Kayıp, pişmanlık", "reversed": "Kabul, iyileşme"},
    "Six of Cups": {"upright": "Anılar, geçmiş", "reversed": "Takıntı, saplantı"},
    "Seven of Cups": {"upright": "Hayaller, seçenekler", "reversed": "Yanılsama, kararsızlık"},
    "Eight of Cups": {"upright": "Vazgeçiş, yolculuk", "reversed": "Kaçış, inat"},
    "Nine of Cups": {"upright": "Dileklerin gerçekleşmesi", "reversed": "Tatminsizlik, aşırı güven"},
    "Ten of Cups": {"upright": "Aile mutluluğu", "reversed": "Çatışma, hayal kırıklığı"},
    "Page of Cups": {"upright": "Yeni fikirler, duygusal haber", "reversed": "Küçük hayal kırıklıkları"},
    "Knight of Cups": {"upright": "Romantik girişim", "reversed": "Hayal kırıklığı, erteleme"},
    "Queen of Cups": {"upright": "Şefkat, sezgi", "reversed": "Duygusal karışıklık"},
    "King of Cups": {"upright": "Dengeli duygular", "reversed": "Manipülasyon, duygusal karmaşa"},


    "Ace of Swords": {"upright": "Zihin açıklığı", "reversed": "Yanılsama, kafa karışıklığı"},
    "Two of Swords": {"upright": "Kararsızlık, denge", "reversed": "Karar erteleme, çatışma"},
    "Three of Swords": {"upright": "Kalp kırıklığı", "reversed": "Kabul, iyileşme"},
    "Four of Swords": {"upright": "Dinlenme, içsel farkındalık", "reversed": "Aşırı stres, erteleme"},
    "Five of Swords": {"upright": "Çatışma, galibiyet", "reversed": "Haksızlık, pişmanlık"},
    "Six of Swords": {"upright": "Taşınma, iyileşme", "reversed": "Kaçış, belirsizlik"},
    "Seven of Swords": {"upright": "Kurnazlık, strateji", "reversed": "Açığa çıkma, ihanet"},
    "Eight of Swords": {"upright": "Kısıtlanma, engel", "reversed": "Kurtulma, özgürlük"},
    "Nine of Swords": {"upright": "Kaygı, uykusuzluk", "reversed": "Açığa çıkma, rahatlama"},
    "Ten of Swords": {"upright": "Son, bitiş", "reversed": "Kurtuluş, toparlanma"},
    "Page of Swords": {"upright": "Yeni fikir, araştırma", "reversed": "Dedikodu, kafa karışıklığı"},
    "Knight of Swords": {"upright": "Hızlı hareket, mücadele", "reversed": "Sabırsızlık, çarpışma"},
    "Queen of Swords": {"upright": "Zeka, objektiflik", "reversed": "Soğukluk, mesafe"},
    "King of Swords": {"upright": "Otorite, mantık", "reversed": "Tiranlık, yargılama"},


    "Ace of Wands": {"upright": "Yeni fikir, enerji", "reversed": "Erteleme, blokaj"},
    "Two of Wands": {"upright": "Planlama, seçim", "reversed": "Kararsızlık, gecikme"},
    "Three of Wands": {"upright": "Gelişme, ilerleme", "reversed": "Engel, hayal kırıklığı"},
    "Four of Wands": {"upright": "Kutlama, başarı", "reversed": "Erteleme, hayal kırıklığı"},
    "Five of Wands": {"upright": "Rekabet, mücadele", "reversed": "Anlaşmazlık, çatışma"},
    "Six of Wands": {"upright": "Zafer, tanınma", "reversed": "Gurur, ihmal"},
    "Seven of Wands": {"upright": "Savunma, cesaret", "reversed": "Çekilme, teslimiyet"},
    "Eight of Wands": {"upright": "Hızlı gelişme, haber", "reversed": "Gecikme, engel"},
    "Nine of Wands": {"upright": "Direnç, azim", "reversed": "Yorgunluk, teslimiyet"},
    "Ten of Wands": {"upright": "Sorumluluk, yük", "reversed": "Baskı, tükenmişlik"},
    "Page of Wands": {"upright": "Keşif, ilham", "reversed": "Hareketsizlik, erteleme"},
    "Knight of Wands": {"upright": "Tutku, macera", "reversed": "Dikkatsizlik, acelecilik"},
    "Queen of Wands": {"upright": "Karizma, özgüven", "reversed": "Kıskançlık, kontrol"},
    "King of Wands": {"upright": "Liderlik, vizyon", "reversed": "Tiryanlık, kibir"},


    "Ace of Pentacles": {"upright": "Yeni fırsat, maddi kazanç", "reversed": "Kaynak kaybı, erteleme"},
    "Two of Pentacles": {"upright": "Denge, çoklu görev", "reversed": "Dengesizlik, aşırı yük"},
    "Three of Pentacles": {"upright": "İş birliği, beceri", "reversed": "Uyumsuzluk, başarısızlık"},
    "Four of Pentacles": {"upright": "Güvenlik, tasarruf", "reversed": "Kıskançlık, tutuculuk"},
    "Five of Pentacles": {"upright": "Maddi kayıp, zorluk", "reversed": "Kurtuluş, toparlanma"},
    "Six of Pentacles": {"upright": "Cömertlik, denge", "reversed": "Adaletsizlik, dengesizlik"},
    "Seven of Pentacles": {"upright": "Sabır, değerlendirme", "reversed": "Acelecillik, hayal kırıklığı"},
    "Eight of Pentacles": {"upright": "Çalışma, ustalık", "reversed": "Tembellik, yetersizlik"},
    "Nine of Pentacles": {"upright": "Başarı, bağımsızlık", "reversed": "Gurur, kayıp"},
    "Ten of Pentacles": {"upright": "Maddi güven, aile", "reversed": "Kaynak kaybı, miras problemi"},
    "Page of Pentacles": {"upright": "Yeni öğrenim, fırsat", "reversed": "Erteleme, dikkatsizlik"},
    "Knight of Pentacles": {"upright": "Sorumluluk, sabır", "reversed": "Tembellik, sıkıcılık"},
    "Queen of Pentacles": {"upright": "Bereket, pratiklik", "reversed": "Aşırı kontrol, ihmal"},
    "King of Pentacles": {"upright": "Maddi başarı, liderlik", "reversed": "Hırs, kayıp"}
}

card_themes = {
    "The Fool": ["Yeni başlangıç", "Hayat dersi"],
    "The Magician": ["Yaratıcılık", "Beceri"],
    "The High Priestess": ["Sezgi", "Gizem"],
    "The Empress": ["Bereket", "Sevgi", "Yaratıcılık"],
    "The Emperor": ["Otorite", "Kontrol", "Sorumluluk"],
    "The Hierophant": ["Öğreti", "Gelenek", "Bilgelik"],
    "The Lovers": ["Aşk", "İlişki", "Sevgi"],
    "The Chariot": ["Zafer", "Motivasyon", "Hareket"],
    "Strength": ["Cesaret", "İrade", "Sabır"],
    "The Hermit": ["Yalnızlık", "İçsel rehberlik", "Bilgelik"],
    "Wheel of Fortune": ["Değişim", "Kısmet", "Dönüşüm"],
    "Justice": ["Adalet", "Denge", "Doğruluk"],
    "The Hanged Man": ["Bekleme", "Fedakarlık", "Farklı bakış"],
    "Death": ["Son", "Dönüşüm", "Yenilenme"],
    "Temperance": ["Denge", "Uyum", "Ölçülülük"],
    "The Devil": ["Bağımlılık", "Kısıtlama", "Korku"],
    "The Tower": ["Çöküş", "Şok", "Ani değişim"],
    "The Star": ["Umut", "İlham", "Rehberlik"],
    "The Moon": ["Sezgiler", "Yanılsama", "Gizlilik"],
    "The Sun": ["Başarı", "Mutluluk", "Pozitif enerji"],
    "Judgement": ["Uyanış", "Farkındalık", "Karar"],
    "The World": ["Tamamlama", "Başarı", "Bütünlük"],

    "Ace of Cups": ["Aşk", "Duygusal başlangıç"],
    "Two of Cups": ["İlişki", "Uyum", "Sevgi"],
    "Three of Cups": ["Kutlama", "Arkadaşlık", "Mutluluk"],
    "Four of Cups": ["Memnuniyetsizlik", "Düşünce", "Kayıtsızlık"],
    "Five of Cups": ["Kayip", "Üzüntü", "Hayal kırıklığı"],
    "Six of Cups": ["Geçmiş", "Nostalji", "Hatıra"],
    "Seven of Cups": ["Hayaller", "Kararsızlık", "Seçenekler"],
    "Eight of Cups": ["Terketme", "Arayış", "Değişim"],
    "Nine of Cups": ["Dileklerin gerçekleşmesi", "Tatmin", "Başarı"],
    "Ten of Cups": ["Mutluluk", "Aile", "Duygusal tatmin"],
    "Page of Cups": ["Yeni başlangıç", "Duygusal mesaj", "Sezgi"],
    "Knight of Cups": ["Romantizm", "Hareketli duygular", "Takip"],
    "Queen of Cups": ["Duygusal denge", "Şefkat", "Sezgi"],
    "King of Cups": ["Olgun duygusallık", "Kontrol", "Empati"],

    "Ace of Swords": ["Yeni fikir", "Karar", "Zihinsel netlik"],
    "Two of Swords": ["Kararsızlık", "Seçim", "Denge"],
    "Three of Swords": ["Kalp kırıklığı", "Üzüntü", "Ayrılık"],
    "Four of Swords": ["Dinlenme", "Düşünce", "İyileşme"],
    "Five of Swords": ["Çatışma", "Yenilgi", "Hile"],
    "Six of Swords": ["Geçiş", "Taşınma", "Yolculuk"],
    "Seven of Swords": ["Aldatma", "Kaçış", "Hilekarlık"],
    "Eight of Swords": ["Kısıtlama", "Engel", "Korku"],
    "Nine of Swords": ["Endişe", "Korku", "Kabuslar"],
    "Ten of Swords": ["Bitiş", "Ağrı", "Ayrılık"],
    "Page of Swords": ["Haber", "Merak", "Araştırma"],
    "Knight of Swords": ["Hızlı hareket", "Mücadele", "Kararlılık"],
    "Queen of Swords": ["Zeka", "Objektiflik", "Netlik"],
    "King of Swords": ["Mantık", "Adalet", "Strateji"],

    "Ace of Wands": ["Yeni başlangıç", "Enerji", "Tutku"],
    "Two of Wands": ["Planlama", "Gelişim", "Karar"],
    "Three of Wands": ["İlerleme", "Fırsatlar", "Bekleyiş"],
    "Four of Wands": ["Kutlama", "Başarı", "Topluluk"],
    "Five of Wands": ["Rekabet", "Mücadele", "Anlaşmazlık"],
    "Six of Wands": ["Zafer", "Tanınırlık", "Başarı"],
    "Seven of Wands": ["Savunma", "Kararlılık", "Mücadele"],
    "Eight of Wands": ["Hız", "İlerleme", "Hareket"],
    "Nine of Wands": ["Direnç", "Sabır", "Hazırlık"],
    "Ten of Wands": ["Ağırlık", "Sorumluluk", "Yorgunluk"],
    "Page of Wands": ["Yeni fikir", "Keşif", "Enerji"],
    "Knight of Wands": ["Hareketlilik", "Cesaret", "Tutku"],
    "Queen of Wands": ["Karizma", "Güç", "Yaratıcılık"],
    "King of Wands": ["Liderlik", "Vizyon", "Kararlılık"],

    "Ace of Pentacles": ["Yeni maddi başlangıç", "Fırsat", "Para"],
    "Two of Pentacles": ["Denge", "Çoklu işler", "Esneklik"],
    "Three of Pentacles": ["İş birliği", "Ustalık", "Başarı"],
    "Four of Pentacles": ["Kontrol", "Tutuculuk", "Maddi güvenlik"],
    "Five of Pentacles": ["Maddi kayıp", "Zorluk", "Yoksulluk"],
    "Six of Pentacles": ["Cömertlik", "Denge", "Yardım"],
    "Seven of Pentacles": ["Sabır", "Değerlendirme", "Bekleme"],
    "Eight of Pentacles": ["Çalışma", "Ustalık", "Gelişim"],
    "Nine of Pentacles": ["Bağımsızlık", "Başarı", "Tatmin"],
    "Ten of Pentacles": ["Maddi güven", "Aile", "Başarı"],
    "Page of Pentacles": ["Yeni öğrenim", "Fırsat", "Araştırma"],
    "Knight of Pentacles": ["Sorumluluk", "Sabır", "İstikrar"],
    "Queen of Pentacles": ["Bereket", "Pratiklik", "Denge"],
    "King of Pentacles": ["Maddi başarı", "Liderlik", "Kontrol"]
}

theme_texts = {
    "Aşk": [
        "Kalbin bugün biraz daha açık olabilir.",
        "İlişkilerde iletişime dikkat et.",
        "Yeni tanışmalar veya yakın ilişkiler öne çıkabilir."
    ],
    "Maddi": [
        "Finansal konularda planlı olman faydalı.",
        "Bugün gelir-gider dengesine dikkat et.",
        "Yatırım veya harcama kararlarını iyi düşün."
    ],
    "Hayat dersi": [
        "Hayatın sana önemli bir ders vermesi olası.",
        "Geçmiş deneyimlerinden öğrenmek için fırsatlar var.",
        "Kararlarınız, gelecekte etkili olacak."
    ],
    "Yeni başlangıç": [
        "Bugün yeni fırsatlar karşına çıkabilir.",
        "Eski alışkanlıkları bırakıp ilerlemek için uygun bir gün.",
        "Hayatına taze bir yön vermen mümkün."
    ],
    "Kariyer": [
        "İş hayatında önemli gelişmeler olabilir.",
        "Bugün mesleki hedeflerine odaklanman faydalı.",
        "Yeni projeler veya sorumluluklar gündeme gelebilir."
    ],
    "Sağlık": [
        "Kendi sağlığına özen göstermek için uygun bir gün.",
        "Dinlenmeye ve enerji toplamak için fırsatlar var.",
        "Sağlık rutinlerini aksatmamak önemli."
    ],
    "Aile": [
        "Aile ilişkilerine zaman ayırmak faydalı.",
        "Yakınlarınla iletişimde dikkatli ol.",
        "Ev içi sorumluluklarda dengeyi korumaya çalış."
    ],
    "İlişki": [
        "Arkadaşlık ve sosyal ilişkilerde uyum ön planda.",
        "Çevrendeki insanlarla iletişim önem kazanıyor.",
        "İlişkilerde dengeyi gözetmek gerekli."
    ],
    "Kayıp/Üzüntü": [
        "Duygusal bir yükten kurtulmak için fırsatlar var.",
        "Geçmiş üzüntüler üzerinde düşünmek faydalı olabilir.",
        "Olumsuzlukları bırakmak için adım atabilirsin."
    ],
    "Fırsat": [
        "Beklenmedik olumlu gelişmeler olabilir.",
        "Yeni şanslar karşına çıkabilir.",
        "Fırsatları değerlendirmek için açık ol."
    ],
    "Uyarı": [
        "Bugün dikkatli olman gereken durumlar var.",
        "Ani kararlar yerine planlı adımlar öne çıkmalı.",
        "Çevrendeki insanlara karşı temkinli ol."
    ],
    "Kişisel gelişim": [
        "Kendini geliştirmek için fırsatlar var.",
        "Bugün öğrenmeye ve deneyim kazanmaya açık ol.",
        "Kendi sınırlarını keşfetmek için uygun bir gün."
    ],
    "Değişim": [
        "Hayatında beklenmedik değişiklikler olabilir.",
        "Değişime açık olmak sana avantaj sağlayabilir.",
        "Eski alışkanlıklardan sıyrılmak için fırsatlar var."
    ]
}


major_arcana = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World"
]

draw = random.sample(list(tarot_cards.keys()), 3)
positions = ["Geçmiş", "Şimdi", "Gelecek"]
draw_results = []

print("🎴 Bugünkü Tarot Falın 🎴\n")

for idx, card in enumerate(draw):
    input(f"{positions[idx]} kartını çekmek için Enter'a bas...")
    orientation = random.choice(["upright", "reversed"])
    meaning = tarot_cards[card][orientation]
    themes = card_themes.get(card, [])
    theme_comments = []
    for theme in themes:
        if theme in theme_texts:
            theme_comments.append(random.choice(theme_texts[theme]))
    print(f"{positions[idx]} → {card} ({orientation}): {meaning}")
    if theme_comments:
        for comment in theme_comments:
            print(f"  - {comment}")
    print()
    
    draw_results.append((positions[idx], card, orientation, meaning, themes, theme_comments))

print("\n📜 Bugünkü Tarot Falı Özeti 📜")
for pos, card, orientation, meaning, themes, comments in draw_results:
    print(f"{pos} → {card} ({orientation}): {meaning}")
    for c in comments:
        print(f"  - {c}")

theme_scores = {}
for _, _, _, _, themes, _ in draw_results:
    for theme in themes:
        theme_scores[theme] = theme_scores.get(theme, 0) + 1

print("\n🔮 Genel Yorum 🔮")

if any(card in major_arcana for _, card, _, _, _, _ in draw_results):
    print("🌟 Major Arcana kartları var, bu falda önemli değişimler veya hayat dersleri öne çıkıyor.")

for theme, score in theme_scores.items():
    if score >= 1:
        print(f"💡 {theme} teması öne çıkıyor; bu konuya dikkat etmen faydalı.")

if not theme_scores:
    print("Her kart farklı temalara sahip, genel yorum daha geniş ve esnek düşünülmeli.")