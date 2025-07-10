# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 15:35:33 2025

@author: ismtu
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

t = np.array([0, 15, 30, 45, 60, 90, 120, 150, 180], dtype=float)
GAC_Ct = np.array([50, 27.49, 21.12, 17.81, 14.00, 10.60, 5.40, 5.12, 4.19])
BC_Ct = np.array([50, 38.47, 35.58, 30.14, 27.95, 27.49, 21.30, 20.79, 20.19])

C0 = 50
V = 0.5
m = 0.4

GAC_qt = (C0 - GAC_Ct) * V / m
BC_qt = (C0 - BC_Ct) * V / m

GAC_qe = GAC_qt[-1]
BC_qe = BC_qt[-1]

GAC_F = GAC_qt / GAC_qe
BC_F = BC_qt / BC_qe

epsilon = 1e-10
GAC_F = np.clip(GAC_F, 0, 1 - epsilon)
BC_F = np.clip(BC_F, 0, 1 - epsilon)



def boyd(F):
    return -0.4977 - np.log(1 - F)

def format_eq(model, r2):
    a = model.coef_[0]
    b = model.intercept_
    return f'y = {a:.4f}x + {b:.4f}\nR² = {r2:.4f}'

GAC_B = boyd(GAC_F)
BC_B = boyd(BC_F)

t_fit = t[1:].reshape(-1, 1)

model_gac = LinearRegression().fit(t_fit, GAC_B[1:])
pred_gac = model_gac.predict(t_fit)
r2_gac = r2_score(GAC_B[1:], pred_gac)

model_bc = LinearRegression().fit(t_fit, BC_B[1:])
pred_bc = model_bc.predict(t_fit)
r2_bc = r2_score(BC_B[1:], pred_bc)

plt.figure(figsize=(12,6))

plt.subplot(1,2,1)
plt.scatter(t[1:], GAC_B[1:], color='black', label='Data')
plt.plot(t[1:], pred_gac, 'r--', label='Linear fit')
plt.text(
    0.05, 0.95,
    format_eq(model_gac, r2_gac),
    transform=plt.gca().transAxes,
    fontsize=11,
    ha='left', va='top',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan", alpha=0.5)
)
plt.title("GAC Boyd Plot")
plt.xlabel("Time (min)")
plt.ylabel("B(t)")
plt.legend()
plt.grid(True)

plt.subplot(1,2,2)
plt.scatter(t[1:], BC_B[1:], color='black', label='Data')
plt.plot(t[1:], pred_bc, 'b--', label='Linear fit')
plt.text(
    0.05, 0.95,
    format_eq(model_bc, r2_bc),
    transform=plt.gca().transAxes,
    fontsize=11,
    ha='left', va='top',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lavender", alpha=0.5)
)
plt.title("BC Boyd Plot")
plt.xlabel("Time (min)")
plt.ylabel("B(t)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
