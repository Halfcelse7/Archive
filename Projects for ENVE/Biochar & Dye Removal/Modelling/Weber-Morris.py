# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 15:33:05 2025

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

sqrt_t = np.sqrt(t).reshape(-1, 1)

model_gac = LinearRegression().fit(sqrt_t, GAC_qt)
model_bc = LinearRegression().fit(sqrt_t, BC_qt)

GAC_pred = model_gac.predict(sqrt_t)
BC_pred = model_bc.predict(sqrt_t)

k_id_gac = model_gac.coef_[0]
C_gac = model_gac.intercept_
k_id_bc = model_bc.coef_[0]
C_bc = model_bc.intercept_

from sklearn.metrics import r2_score
r2_gac = r2_score(GAC_qt, GAC_pred)
r2_bc = r2_score(BC_qt, BC_pred)

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.scatter(sqrt_t, GAC_qt, color='black', label='GAC Data')
plt.plot(sqrt_t, GAC_pred, color='red', linestyle='--', label=f'Fit: q_t = {k_id_gac:.3f}√t + {C_gac:.3f}\nR²={r2_gac:.4f}')
plt.title("GAC Intraparticle Diffusion")
plt.xlabel("Square Root of Time (min^0.5)")
plt.ylabel("Adsorbed Amount q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.subplot(1,2,2)
plt.scatter(sqrt_t, BC_qt, color='black', label='BC Data')
plt.plot(sqrt_t, BC_pred, color='blue', linestyle='--', label=f'Fit: q_t = {k_id_bc:.3f}√t + {C_bc:.3f}\nR²={r2_bc:.4f}')
plt.title("BC Intraparticle Diffusion")
plt.xlabel("Square Root of Time (min^0.5)")
plt.ylabel("Adsorbed Amount q_t (mg/g)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"GAC intraparticle diffusion rate constant (k_id): {k_id_gac:.4f}")
print(f"GAC intercept (C): {C_gac:.4f}")
print(f"BC intraparticle diffusion rate constant (k_id): {k_id_bc:.4f}")
print(f"BC intercept (C): {C_bc:.4f}")
