# -*- coding: utf-8 -*-
"""
Created on Sun May 11 09:27:23 2025

@author: ismtu
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

def choose_sheet(file_path):
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    sheet_names = xls.sheet_names
    print("Available sheets:")
    for i, sheet in enumerate(sheet_names):
        print(f"{i+1}. {sheet}")
    choice = int(input("Enter the number of the sheet you want to analyze: ")) - 1
    return sheet_names[choice]

file_path = r'C:\Users\ismtu\OneDrive\Desktop\Air Sampling Analysis\Excel/İsos Data Analysis of Concentrations.xlsx'
sheet_name = choose_sheet(file_path)
df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

samples = df["Samples"]
summer = df["Summer"]
winter = df["Winter"]

x = np.arange(len(samples))
width = 0.35

color_pool = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
              '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff']

hatch_pool = ['/', '\\', '////', '-', '+', 'x', 'o', 'O', '.', '**', '//', '...']

summer_color, winter_color = random.sample(color_pool, 2)
summer_hatch, winter_hatch = random.sample(hatch_pool, 2)

fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(x - width/2, summer, width, label='Summer', color=summer_color, hatch=summer_hatch,
               edgecolor='darkred', linewidth=1.2)
bars2 = ax.bar(x + width/2, winter, width, label='Winter', color=winter_color, hatch=winter_hatch,
               edgecolor='black', linewidth=1.2)

for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

ax.set_xlabel('Samples', fontsize=12, fontweight='bold')
ax.set_ylabel(f'{sheet_name} Concentration (pg/m³)', fontsize=12, fontweight='bold')
ax.set_title(f'{sheet_name} Concentration of Samples - Summer vs Winter', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(samples, rotation=45, fontsize=10, fontweight='bold')
ax.legend(fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
