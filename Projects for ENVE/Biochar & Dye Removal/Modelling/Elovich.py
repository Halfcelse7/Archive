# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 15:34:11 2025

@author: ismtu
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

t = np.array([0, 15, 30, 45, 60, 90, 120, 150, 180])
GAC_Ct = np.array([50, 27.49, 21.12, 17.81, 14.00, 10.60, 5.40, 5.12, 4.19])
BC_Ct = np.array([50, 38.47, 35.58, 30.14, 27.95, 27.49, 21.30, 20.79, 20.19])

C0 = 50
V = 0.5
m = 0.4

GAC_qt = (C0 - GAC_Ct) * V / m
BC_qt = (C0 - BC_Ct) * V / m

t_nonzero = t[1:]
GAC_qt_nonzero = GAC_qt[1:]
BC_qt_nonzero = BC_qt[1:]
ln_t = np.log(t_nonzero).reshape(-1, 1)

model_gac = LinearRegression().fit(ln_t, GAC_qt_nonzero)
model_bc = LinearRegression().fit(ln_t, BC_qt_nonzero)

GAC_pred = model_gac.predict(ln_t)
BC_pred = model_bc.predict(ln_t)

a_gac = model_gac.intercept_
b_gac = model_gac.coef_[0]

a_bc = model_bc.intercept_
b_bc = model_bc.coef_[0]

beta_gac = 1 / b_gac
alpha_gac = np.exp(a_gac * beta_gac) / beta_gac

beta_bc = 1 / b_bc
alpha_bc = np.exp(a_bc * beta_bc) / beta_bc

from sklearn.metrics import r2_score
r2_gac = r2_score(GAC_qt_nonzero, GAC_pred)
r2_bc = r2_score(BC_qt_nonzero, BC_pred)

plt.figure(figsize=(10,5))

plt.subplot(1, 2, 1)
plt.scatter(ln_t, GAC_qt_nonzero, color='black', label='GAC Data')
plt.plot(ln_t, GAC_pred, color='red', linestyle='--', label=f'Fit: q_t = {a_gac:.3f} + {b_gac:.3f} ln(t)\nR²={r2_gac:.4f}')
plt.title("GAC Elovich Model")
plt.xlabel("ln(Time (min))")
plt.ylabel("Adsorbed Amount q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.scatter(ln_t, BC_qt_nonzero, color='black', label='BC Data')
plt.plot(ln_t, BC_pred, color='blue', linestyle='--', label=f'Fit: q_t = {a_bc:.3f} + {b_bc:.3f} ln(t)\nR²={r2_bc:.4f}')
plt.title("BC Elovich Model")
plt.xlabel("ln(Time (min))")
plt.ylabel("Adsorbed Amount q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"GAC Elovich parameters: alpha = {alpha_gac:.4f}, beta = {beta_gac:.4f}")
print(f"BC Elovich parameters: alpha = {alpha_bc:.4f}, beta = {beta_bc:.4f}")
