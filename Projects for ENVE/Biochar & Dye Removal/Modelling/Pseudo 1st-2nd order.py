# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 15:29:30 2025

@author: ismtu
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

t = np.array([0, 15, 30, 45, 60, 90, 120, 150, 180])
GAC_Ct = np.array([50, 27.49, 21.12, 17.81, 14.00, 10.60, 5.40, 5.12, 4.19])
BC_Ct = np.array([50, 38.47, 35.58, 30.14, 27.95, 27.49, 21.30, 20.79, 20.19])

C0 = 50
V = 0.5
m = 0.4

GAC_qt = (C0 - GAC_Ct) * V / m
BC_qt = (C0 - BC_Ct) * V / m

def pseudo_first_order(t, k1, qe):
    return qe * (1 - np.exp(-k1 * t))

def pseudo_second_order(t, k2, qe):
    return (k2 * qe**2 * t) / (1 + k2 * qe * t)

popt_gac_pfo, _ = curve_fit(pseudo_first_order, t, GAC_qt, p0=[0.01, max(GAC_qt)])
popt_gac_pso, _ = curve_fit(pseudo_second_order, t, GAC_qt, p0=[0.01, max(GAC_qt)])

popt_bc_pfo, _ = curve_fit(pseudo_first_order, t, BC_qt, p0=[0.01, max(BC_qt)])
popt_bc_pso, _ = curve_fit(pseudo_second_order, t, BC_qt, p0=[0.01, max(BC_qt)])

t_pred = np.linspace(0, 200, 100)
GAC_pfo_pred = pseudo_first_order(t_pred, *popt_gac_pfo)
GAC_pso_pred = pseudo_second_order(t_pred, *popt_gac_pso)
BC_pfo_pred = pseudo_first_order(t_pred, *popt_bc_pfo)
BC_pso_pred = pseudo_second_order(t_pred, *popt_bc_pso)

def calc_r2(y_true, y_pred):
    return r2_score(y_true, y_pred)

GAC_pfo_r2 = calc_r2(GAC_qt, pseudo_first_order(t, *popt_gac_pfo))
GAC_pso_r2 = calc_r2(GAC_qt, pseudo_second_order(t, *popt_gac_pso))
BC_pfo_r2 = calc_r2(BC_qt, pseudo_first_order(t, *popt_bc_pfo))
BC_pso_r2 = calc_r2(BC_qt, pseudo_second_order(t, *popt_bc_pso))

plt.figure(figsize=(12,6))

plt.subplot(1, 2, 1)
plt.scatter(t, GAC_qt, color='black', label='GAC Data')
plt.plot(t_pred, GAC_pfo_pred, 'r--', label=f'Pseudo-1st Order (R²={GAC_pfo_r2:.4f})')
plt.plot(t_pred, GAC_pso_pred, 'b:', label=f'Pseudo-2nd Order (R²={GAC_pso_r2:.4f})')
plt.title("GAC Adsorption Kinetics")
plt.xlabel("Time (min)")
plt.ylabel("Adsorbed amount, q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.scatter(t, BC_qt, color='black', label='BC Data')
plt.plot(t_pred, BC_pfo_pred, 'r--', label=f'Pseudo-1st Order (R²={BC_pfo_r2:.4f})')
plt.plot(t_pred, BC_pso_pred, 'b:', label=f'Pseudo-2nd Order (R²={BC_pso_r2:.4f})')
plt.title("BC Adsorption Kinetics")
plt.xlabel("Time (min)")
plt.ylabel("Adsorbed amount, q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print("GAC Pseudo-First-Order: k1 = {:.4f}  qe = {:.4f} mg/g".format(*popt_gac_pfo))
print("GAC Pseudo-Second-Order: k2 = {:.4f}  qe = {:.4f} mg/g".format(*popt_gac_pso))
print("BC Pseudo-First-Order: k1 = {:.4f}  qe = {:.4f} mg/g".format(*popt_bc_pfo))
print("BC Pseudo-Second-Order: k2 = {:.4f}  qe = {:.4f} mg/g".format(*popt_bc_pso))
