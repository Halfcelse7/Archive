# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 11:10:16 2025

@author: ismtu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder

time_points = [0, 15, 30, 45, 60, 90, 120, 150, 180]

data = {
    'Time': time_points * 2,
    'Sorbent': ['GAC'] * 9 + ['BC'] * 9,
    'Fe_added': [1] * 18,
    'H2O2_added': [1] * 18,
    'Stirring': [1] * 9 + [0] * 9,
    'Aeration': [1] * 18,
    'pH': [5.6] * 18,
    'Fe_conc_mol': [0.05] * 18,
    'Fe_type': ['Fe3+'] * 18,
    'Fe_source': ['Fe(NO3)3'] * 18,
    'H2O2_mmol': [5] * 18,
    'Mechanism': ['Fenton'] * 18,
    'Concentration': [
        50, 27.49, 21.12, 17.81, 14.00, 10.60, 5.40, 5.12, 4.19,
        50, 38.47, 35.58, 30.14, 27.95, 27.49, 21.30, 20.79, 20.19
    ]
}

df_raw = pd.DataFrame(data)

simulated = pd.DataFrame({
    'Time': time_points,
    'Sorbent': ['BC'] * 9,
    'Fe_added': [0] * 9,
    'H2O2_added': [1] * 9,
    'Stirring': [0] * 9,
    'Aeration': [1] * 9,
    'pH': [5.6] * 9,
    'Fe_conc_mol': [0.00] * 9,
    'Fe_type': ['Fe3+'] * 9,
    'Fe_source': ['Fe(NO3)3'] * 9,
    'H2O2_mmol': [5] * 9,
    'Mechanism': ['Adsorption'] * 9,
    'Concentration': [50, 45, 43, 41, 39, 38, 36, 35, 34]
})

df_all = pd.concat([df_raw, simulated], ignore_index=True)

le_sorbent = LabelEncoder()
le_fe_type = LabelEncoder()
le_fe_source = LabelEncoder()
le_mechanism = LabelEncoder()

le_sorbent.fit(df_all['Sorbent'])
le_fe_type.fit(df_all['Fe_type'])
le_fe_source.fit(df_all['Fe_source'])
le_mechanism.fit(df_all['Mechanism'])

df_raw['Sorbent'] = le_sorbent.transform(df_raw['Sorbent'])
df_raw['Fe_type'] = le_fe_type.transform(df_raw['Fe_type'])
df_raw['Fe_source'] = le_fe_source.transform(df_raw['Fe_source'])
df_raw['Mechanism'] = le_mechanism.transform(df_raw['Mechanism'])

X = df_raw[['Time', 'Sorbent', 'Fe_added', 'H2O2_added', 'Stirring', 'Aeration',
            'pH', 'Fe_conc_mol', 'H2O2_mmol', 'Fe_type', 'Fe_source', 'Mechanism']]
y = df_raw['Concentration']

model = XGBRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

def H2O2_mmol_to_mL(mmol, solution_volume_L=1.0):
    mapping = {
        1.0: {2: 0.225, 5: 0.45, 10: 0.9, 20: 1.8},
        0.5: {2: 0.09, 5: 0.225, 10: 0.45, 20: 0.9}
    }
    return mapping.get(solution_volume_L, {}).get(mmol, None)

def predict_scenario(sorbent, Fe_added, Fe_conc_mol, Fe_type, Fe_source,
                     H2O2_added, H2O2_mmol, stirrer, aeration, pH,
                     mechanism='Fenton', solution_volume_L=0.5, show_plot=True):

    t_values = np.array([15, 30, 45, 60, 90, 120, 150, 180])

    sorbent_val = le_sorbent.transform([sorbent])[0]
    fe_type_val = le_fe_type.transform([Fe_type])[0]
    fe_source_val = le_fe_source.transform([Fe_source])[0]
    mech_val = le_mechanism.transform([mechanism])[0]

    H2O2_mL = H2O2_mmol_to_mL(H2O2_mmol, solution_volume_L)

    scenario_df = pd.DataFrame({
        'Time': t_values,
        'Sorbent': [sorbent_val]*len(t_values),
        'Fe_added': [Fe_added]*len(t_values),
        'H2O2_added': [H2O2_added]*len(t_values),
        'Stirring': [stirrer]*len(t_values),
        'Aeration': [aeration]*len(t_values),
        'pH': [pH]*len(t_values),
        'Fe_conc_mol': [Fe_conc_mol]*len(t_values),
        'H2O2_mmol': [H2O2_mmol]*len(t_values),
        'Fe_type': [fe_type_val]*len(t_values),
        'Fe_source': [fe_source_val]*len(t_values),
        'Mechanism': [mech_val]*len(t_values)
    })

    y_pred = model.predict(scenario_df)

    t_values = np.insert(t_values, 0, 0)
    y_pred = np.insert(y_pred, 0, 50)

    if show_plot:
        plt.figure(figsize=(8, 5))
        plt.plot(t_values, y_pred, marker='o', label='Predicted')
        offset = max(y_pred) * 0.02
        for x, y in zip(t_values, y_pred):
            plt.text(x, y + offset, f"{y:.1f}", ha='center', fontsize=9, color='black', rotation=45)

        plt.axhline(50, color='gray', linestyle='--', linewidth=1, label='Initial 50 mg/L')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.xlabel("Time (min)")
        plt.ylabel("Dye Concentration (mg/L)")
        plt.title(f"{sorbent} | Fe={Fe_conc_mol}M | {Fe_type} ({Fe_source}) | {mechanism} |\n"
                  f"H2O2={H2O2_mmol} mmol ≈ {H2O2_mL} mL in {solution_volume_L} L")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return pd.DataFrame({'Time (min)': t_values, 'Predicted Conc. (mg/L)': y_pred})

print("\n🧪 Scenario 1: BC without Fe at pH 5.6")
res1 = predict_scenario('BC', Fe_added=0, Fe_conc_mol=0.0,
                        Fe_type='Fe3+', Fe_source='Fe(NO3)3',
                        H2O2_added=1, H2O2_mmol=5, stirrer=0, aeration=1,
                        pH=5.6, mechanism='Adsorption')
print(res1)

print("\n🧪 Scenario 2: GAC with Fe at pH 3.0")
res2 = predict_scenario('GAC', Fe_added=1, Fe_conc_mol=0.05,
                        Fe_type='Fe3+', Fe_source='Fe(NO3)3',
                        H2O2_added=1, H2O2_mmol=5, stirrer=1, aeration=1,
                        pH=3.0, mechanism='Fenton')
print(res2)

print("\n🧪 Scenario 3: BC with Fe at pH 7.5")
res3 = predict_scenario('BC', Fe_added=1, Fe_conc_mol=0.05,
                        Fe_type='Fe3+', Fe_source='Fe(NO3)3',
                        H2O2_added=1, H2O2_mmol=5, stirrer=0, aeration=1,
                        pH=7.5, mechanism='Fenton')
print(res3)