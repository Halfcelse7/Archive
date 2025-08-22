# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 10:18:59 2025

@author: ismtu
"""

import random
import json
import time
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY_HERE")

json_file_path = "FILE_DIRECTORY_HERE"

with open(json_file_path, "r", encoding="utf-8") as f:
    tarot_cards = json.load(f)

def draw_cards(num=3):
    return random.sample(tarot_cards, num)

def get_ai_short_interpretation(card):
    prompt = f"""
    Sen bir tarot falcısısın. Kullanıcıya seçilen tek kart için kısa yorum yap.
    Kart: {card['name']}
    Anlamı: {card['description']}
    Temalar: {', '.join(card['themes'])}
    
    Yorum:
    - 1-2 cümle ile kısa ve samimi bir açıklama yap.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def get_ai_general_interpretation(name, cards):
    prompt = f"""
    Sen bir tarot falcısısın. Kullanıcıya seçilen kartlara göre genel yorum yap.
    Kullanıcı ismi: {name}
    Kartlar: {', '.join([c['name'] for c in cards])}.
    Kartların anlamları ve temaları: {', '.join([f"{c['name']}: {c['description']}, temalar: {', '.join(c['themes'])}" for c in cards])}.
    
    Yorumun:
    - Kartların genel mesajını anlat.
    - Kullanıcının hayatına nasıl uygulanabileceğini açıkla.
    - Kısa ve samimi bir dille yaz.
    - Kullanıcıya hitap et.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    user_name = input("Lütfen bir kullanıcı ism girin: ")
    chosen = draw_cards()
    
    print("Kartlar çekiliyor...\n")
    
    for card in chosen:
        print("Kart çekiliyor", end="", flush=True)
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print(f" {card['name']} geldi!")
        short_comment = get_ai_short_interpretation(card)
        print(f"Kısa Yorum: {short_comment}\n")
    
    print("\n--- Genel Yapay Zeka Yorumu ---\n")
    general_comment = get_ai_general_interpretation(user_name, chosen)
    print(general_comment)

    
