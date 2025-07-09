# -*- coding: utf-8 -*-
"""
Created on Mon May 26 20:05:47 2025

@author: ismtu
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = r"C:\Users\ismtu\OneDrive\Desktop\Green Deal and Cross-Border Carbon Trading\EDGARv8.0_FT2022_GHG_booklet_2023_fossilCO2_only.xlsx"

xls = pd.ExcelFile(file_path)
print("Available Sheets:")
for i, name in enumerate(xls.sheet_names):
    print(f"{i + 1}. {name}")

sheet_index = int(input("Select sheet number: ")) - 1
if sheet_index < 0 or sheet_index >= len(xls.sheet_names):
    raise ValueError("❌ Invalid sheet number selected.")

sheet_name = xls.sheet_names[sheet_index]
df = pd.read_excel(file_path, sheet_name=sheet_name)

df.columns = df.columns.map(lambda x: str(x).strip())
year_columns = [col for col in df.columns if col.isdigit()]

n = int(input("How many countries will be compared? "))
selected_countries = [input(f"Enter country #{i+1}: ").strip() for i in range(n)]

sector_choice = input("Do you want to filter by sector? (y/n): ").strip().lower()
if sector_choice == 'y':
    sector = input("Enter sector name: ").strip()
    df = df[df['Sector'].str.lower() == sector.lower()]
    df = df[df['Country'].isin(selected_countries)]
    title_suffix = f"({sector})"
else:
    df = df[df['Country'].isin(selected_countries)]
    df = df.groupby('Country')[year_columns].sum().reset_index()
    title_suffix = "(All Sectors)"

print("Available years: ")
print(", ".join(year_columns))
selected_years = input("Enter years to compare: ").split(',')
selected_years = [y.strip() for y in selected_years if y.strip() in year_columns]

if not selected_years:
    print("⚠️ No valid years selected.")
else:
    plot_data = df[['Country'] + selected_years].copy()
    plot_data[selected_years] = plot_data[selected_years].apply(pd.to_numeric, errors='coerce')

    x = np.arange(len(plot_data['Country']))
    width = 0.8 / len(selected_years)
    colors = ['tomato', 'skyblue', 'limegreen', 'orange', 'violet', 'gold', 'crimson', 'teal']

    plt.figure(figsize=(12, 6))
    for i, year in enumerate(selected_years):
        color = colors[i % len(colors)]
        bar_positions = x + i * width
        heights = plot_data[year].values
        bars = plt.bar(bar_positions, heights, width, label=year, color=color)

        for xpos, height in zip(bar_positions, heights):
            plt.text(
                xpos, height, f'{height:.1f}',
                ha='center', va='bottom',
                fontsize=12, rotation=45
            )

    plt.xticks(x + width * (len(selected_years) - 1) / 2, plot_data['Country'], rotation=45)
    plt.ylabel("CO₂ Emissions (Mt or appropriate unit)")
    plt.xlabel("Country")
    plt.title(f"CO₂ Emissions by Country {title_suffix}")
    plt.legend(title="Year")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
