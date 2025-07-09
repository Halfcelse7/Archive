# -*- coding: utf-8 -*-
"""
Created on Sun May 11 08:17:16 2025

@author: ismtu
"""

import pandas as pd

T0 = 273.15
P0 = 760
duration_min = 24 * 60

def choose_sheet(file_path):
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    sheet_names = xls.sheet_names
    print("Available sheets:")
    for i, sheet in enumerate(sheet_names):
        print(f"{i+1}. {sheet}")
    choice = int(input("Enter the number of the sheet you want to analyze: ")) - 1
    return sheet_names[choice]

file_path = r'C:\Users\ismtu\OneDrive\Desktop\Air Sampling Analysis\Excel/İsos Air Sampling Data.xlsx'
sheet_name = choose_sheet(file_path)
df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

    phthalates = df.iloc[0:6, 1:10].astype(float)
    temperature = df.iloc[6, 1:10].astype(float)
    pressure = df.iloc[7, 1:10].astype(float)
    flow_rate = df.iloc[8, 1:10].astype(float)

    V_corrected = flow_rate * duration_min * (P0 / pressure) * ((temperature + T0) / T0)
    concentration_pg_m3 = phthalates.multiply(1000, axis=0).divide(V_corrected, axis=1)

    concentration_pg_m3.index = ['Dimethyl Phthalate', 'Diethyl Phthalate', 'Diisobutyl Phthalate',
                                 'Di-n-butyl Phthalate', 'Benzyl Butyl Phthalate', 'DEHP']
    concentration_pg_m3.columns = [f'Sample {i+1}' for i in range(9)]

    print("\nConcentration (pg/m³):\n")
    print(concentration_pg_m3.round(2))

    concentration_pg_m3.to_excel(f'corrected_concentrations_{sheet_name.replace(" ", "_")}.xlsx')

except ValueError as ve:
    print(f"Error: {ve}. Please make sure the sheet name is typed correctly.")
except FileNotFoundError:
    print("Error: Excel file not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
