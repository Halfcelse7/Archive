# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 15:35:16 2025

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

def avrami(t, qe, k, n):
    return qe * (1 - np.exp(-k * t**n))

popt_gac, _ = curve_fit(avrami, t, GAC_qt, p0=[max(GAC_qt), 0.01, 1])

popt_bc, _ = curve_fit(avrami, t, BC_qt, p0=[max(BC_qt), 0.01, 1])

def format_avrami_eq(qe, k, n, r2):
    return f"qₜ = {qe:.2f}(1 - exp(-{k:.4f}·t^{n:.2f}))\nR² = {r2:.4f}"


t_pred = np.linspace(0, 200, 100)
GAC_pred = avrami(t_pred, *popt_gac)
BC_pred = avrami(t_pred, *popt_bc)

GAC_r2 = r2_score(GAC_qt, avrami(t, *popt_gac))
BC_r2 = r2_score(BC_qt, avrami(t, *popt_bc))

plt.figure(figsize=(12,6))

plt.subplot(1, 2, 1)
plt.scatter(t, GAC_qt, color='black', label='GAC Data')
plt.plot(t_pred, GAC_pred, 'r--', label='Avrami Fit')
plt.text(
    0.05, 0.95,
    format_avrami_eq(*popt_gac, GAC_r2),
    transform=plt.gca().transAxes,
    fontsize=10,
    va='top', ha='left',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.6)
)
plt.title("GAC Avrami Model")
plt.xlabel("Time (min)")
plt.ylabel("Adsorbed amount q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.scatter(t, BC_qt, color='black', label='BC Data')
plt.plot(t_pred, BC_pred, 'b--', label='Avrami Fit')
plt.text(
    0.05, 0.95,
    format_avrami_eq(*popt_bc, BC_r2),
    transform=plt.gca().transAxes,
    fontsize=10,
    va='top', ha='left',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan", alpha=0.6)
)
plt.title("BC Avrami Model")
plt.xlabel("Time (min)")
plt.ylabel("Adsorbed amount q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"GAC Avrami parameters: q_e = {popt_gac[0]:.4f}, k = {popt_gac[1]:.5f}, n = {popt_gac[2]:.4f}")
print(f"BC Avrami parameters: q_e = {popt_bc[0]:.4f}, k = {popt_bc[1]:.5f}, n = {popt_bc[2]:.4f}")
