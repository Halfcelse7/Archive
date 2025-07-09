# -*- coding: utf-8 -*-
"""
Created on Sat May 10 18:03:16 2025

@author: ismtu
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def choose_sheet(file_path):
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    sheet_names = xls.sheet_names
    print("Available sheets:")
    for i, sheet in enumerate(sheet_names):
        print(f"{i+1}. {sheet}")
    choice = int(input("Enter the number of the sheet you want to analyze: ")) - 1
    return sheet_names[choice]

file_path = r'C:\Users\ismtu\OneDrive\Desktop\Air Sampling Analysis\Excel/İsos Summer and Winter.xlsx'
sheet_name = choose_sheet(file_path)
df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

samples = df["Samples"]
temperature = df["Temperature"]

concentrations = [df["Di methyl Phthalate"], df["Di ethyl phthalate"], df["Di isobuthyl phtlate"],
    df["Di n butyl phthalate"], df["Benzyl butyl phtlate"], df["Di 2ethyhexyl phtlate"]]

labels = ["Di methyl Phthalate", "Di ethyl phthalate", "Di isobuthyl phtlate", "Di n butyl phthalate",
    "Benzyl butyl phtlate", "Di 2ethyhexyl phtlate"]

colors = ["#e6194B", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4"]

x = np.arange(len(samples))
width = 0.12

fig, ax = plt.subplots(figsize=(13, 6))
ax2 = ax.twinx()

for i in range(6):
    offset = (i - 2.5) * width
    bars = ax.bar(x + offset, concentrations[i], width, label=labels[i],
                  color=colors[i], edgecolor='black', linewidth=1.2)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, rotation=90)

ax2.plot(x, temperature, color='orangered', marker='o', linewidth=2,
         label='Temperature (°C)', linestyle='-', zorder=10)

ax.set_ylabel('Concentration (ng/g)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold', color='orangered')
ax2.tick_params(axis='y', labelcolor='orangered')

ax.set_xlabel('Samples', fontsize=12, fontweight='bold')
ax.set_title(f'{sheet_name} - Concentration and Temperature by Samples',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(samples, rotation=45, fontsize=10, fontweight='bold')

handles1, labels1 = ax.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax.legend(handles1 + handles2, labels1 + labels2,
          fontsize=9, loc='upper left', bbox_to_anchor=(1.1, 1))

ax.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
