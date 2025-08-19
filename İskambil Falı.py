# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 23:12:46 2025

@author: ismtu
"""

# -*- coding: utf-8 -*-
from dataclasses import dataclass

SUIT_MAP = {"Kupa":"♥", "Maça":"♠", "Karo":"♦", "Sinek":"♣"}
RANK_ORDER = ["As"] + [str(i) for i in range(2,11)] + ["Vale","Kız","Papaz"]

PIP_MEANINGS = {
    "As":"başlangıç/potansiyel",
    "2":"ikilik/ortaklık",
    "3":"gelişme",
    "4":"stabilite",
    "5":"değişim/gerilim",
    "6":"akıcılık/uyum",
    "7":"şüphe/değerlendirme",
    "8":"hareket/ustalık",
    "9":"olgunlaşma",
    "10":"bitiriş/eşik"
}
FACE_MEANINGS = {"Vale":"haber/ara kişi","Kız":"sezgi/ilişki kurma","Papaz":"otorite/karar"}
SUIT_MEANINGS = {"♥":"duygular/ilişkiler/aile",
                 "♠":"zorluklar/uyarılar/gerçekçilik",
                 "♦":"maddi konular/fırsatlar",
                 "♣":"iş/aksiyon/çevre/beceri"}
COLOR = {"♥":"kırmızı","♦":"kırmızı","♠":"siyah","♣":"siyah"}

@dataclass(frozen=True)
class Card:
    suit_name_tr: str
    rank_tr: str
    @property
    def suit(self):
        return SUIT_MAP[self.suit_name_tr]
    def display(self):
        return f"{self.suit_name_tr} {self.rank_tr} {self.suit}"

def parse_card(label):
    label = label.strip()
    parts = label.split()
    if len(parts)<2:
        raise ValueError(f"Kart formatı hatalı: '{label}'")
    suit = parts[0].capitalize()
    rank = " ".join(parts[1:]).capitalize()
    # normalize special ranks
    if rank.lower()=="vale": rank="Vale"
    elif rank.lower()=="kız": rank="Kız"
    elif rank.lower()=="papaz": rank="Papaz"
    elif rank.lower()=="as": rank="As"
    elif rank.isdigit(): rank=str(int(rank))
    if suit not in SUIT_MAP: raise ValueError(f"Bilinmeyen suit: {suit}")
    if rank not in RANK_ORDER: raise ValueError(f"Bilinmeyen rank: {rank}")
    return Card(suit, rank)

def base_rank_meaning(rank):
    return PIP_MEANINGS.get(rank, FACE_MEANINGS.get(rank, "?"))
def base_suit_meaning(suit_symbol):
    return SUIT_MEANINGS[suit_symbol]

def pair_score(c1,c2):
    score = 0
    if COLOR[c1.suit]=="kırmızı": score+=1
    else: score-=1
    if COLOR[c2.suit]=="kırmızı": score+=1
    else: score-=1
    if c1.rank_tr=="As" or c2.rank_tr=="As": score+=1
    return max(-2,min(2,score))

def mini_message(c1,c2):
    c1_suit_m = base_suit_meaning(c1.suit)
    c2_suit_m = base_suit_meaning(c2.suit)
    c1_rank_m = base_rank_meaning(c1.rank_tr)
    c2_rank_m = base_rank_meaning(c2.rank_tr)
    if c1.suit==c2.suit:
        role="aynı alanda derinleşme ve netleşme"
    elif COLOR[c1.suit]!=COLOR[c2.suit]:
        role="fırsat–engel karşılaşmasıyla tablo değişiyor"
    else:
        role="yan alandan gelen bir etki resmi tamamlıyor"
    if c2.rank_tr in FACE_MEANINGS:
        role=f"bir kişi/figür ({FACE_MEANINGS[c2.rank_tr]}) etkisini gösteriyor"
    elif c2.rank_tr=="As":
        role="yeni bir kapı açılıyor"
    elif c2.rank_tr=="10":
        role="bir eşik/kapanış beliriyor"
    return f"{c1.display()} → {c1_suit_m} alanında {c1_rank_m}; {c2.display()} → {c2_suit_m}, {c2_rank_m} ve {role}."

def interpret_pair(c1,c2):
    return {"pair":(c1.display(),c2.display()),"score":pair_score(c1,c2),"message":mini_message(c1,c2)}

def overall_summary(pairs):
    suit_counts={"♥":0,"♠":0,"♦":0,"♣":0}
    rank_counts={}
    face_counts={"Vale":0,"Kız":0,"Papaz":0}
    color_counts={"kırmızı":0,"siyah":0}
    total_score=0
    for c1,c2 in pairs:
        for c in (c1,c2):
            suit_counts[c.suit]+=1
            rank_counts[c.rank_tr]=rank_counts.get(c.rank_tr,0)+1
            color_counts[COLOR[c.suit]]+=1
            if c.rank_tr in face_counts: face_counts[c.rank_tr]+=1
        total_score+=pair_score(c1,c2)
    dominant_suit=max(suit_counts.items(),key=lambda x:x[1])[0]
    dominant_suit_meaning=SUIT_MEANINGS[dominant_suit]
    repeating={r:n for r,n in rank_counts.items() if n>=2}
    rep_str=", ".join([f"{r}×{n}" for r,n in repeating.items()]) or "—"
    color_balance="kırmızı ağır basıyor" if color_counts["kırmızı"]>color_counts["siyah"] else ("siyah ağır basıyor" if color_counts["siyah"]>color_counts["kırmızı"] else "denge")
    summary_lines=[]
    summary_lines.append(f"Baskın suit: {dominant_suit} ({dominant_suit_meaning}).")
    summary_lines.append(f"Renk dengesi: {color_balance}.")
    summary_lines.append(f"Tekrarlayan rütbeler: {rep_str}.")
    if face_counts["Papaz"] or face_counts["Kız"] or face_counts["Vale"]:
        summary_lines.append(f"Figür yoğunluğu → Papaz:{face_counts['Papaz']}, Kız:{face_counts['Kız']}, Vale:{face_counts['Vale']}.")
    summary_lines.append(f"Genel skor (−12…+12): {total_score}.")
    guideline=[]
    if rank_counts.get("7",0)>=3: guideline.append("7'lerin vurgusu: acele değil, ölçüp biçme zamanı.")
    if rank_counts.get("As",0)>=1: guideline.append("En az bir As var: yeni bir kapı/başlangıç enerjisi.")
    if face_counts["Papaz"]>=1: guideline.append("Papaz etkisi: otorite/karar mekanizmaları belirgin.")
    if face_counts["Kız"]>=1: guideline.append("Kız etkisi: ilişkisel zekâ ve sezgi öne çıkıyor.")
    if face_counts["Vale"]>=1: guideline.append("Vale etkisi: haberler/mesajlar akışa dahil.")
    if COLOR[dominant_suit]=="kırmızı": guideline.append("Genel akış destekleyici; siyah kartların uyarılarını dikkate al.")
    else: guideline.append("Tedbirli dönem; kırmızı alanlardan gelen destekleri kaçırma.")
    return {"summary_text":" ".join(summary_lines),"guideline":" ".join(guideline)}

# --- Konsol girişi ---
cards=[]
print("12 kartı sırayla giriniz (örn: 'Kupa 10', 'Maça As'):")
for i in range(12):
    while True:
        try:
            entry=input(f"{i+1}. kart: ")
            card=parse_card(entry)
            cards.append(card)
            break
        except Exception as e:
            print("Hata:",e,"Tekrar deneyin.")

# Çiftleri oluştur
pairs=[(cards[i],cards[i+1]) for i in range(0,12,2)]

# Her çifti yorumla
print("\n== Çift Analizleri ==")
for idx,pair in enumerate(pairs,1):
    r=interpret_pair(*pair)
    print(f"{idx}. Çift: {r['pair'][0]} → {r['pair'][1]} | Skor: {r['score']}")
    print("-", r["message"])

# Genel özet
overall=overall_summary(pairs)
print("\n== Genel Özet ==")
print(overall["summary_text"])
print("\n== Yol Haritası ==")
print(overall["guideline"])
