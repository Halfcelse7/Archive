# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 08:57:31 2025

@author: ismtu
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

t = np.array([0, 15, 30, 45, 60, 90, 120, 150, 180], dtype=float)
GAC_Ct = np.array([50, 27.49, 21.12, 17.81, 14.00, 10.60, 5.40, 5.12, 4.19])
BC_Ct = np.array([50, 38.47, 35.58, 30.14, 27.95, 27.49, 21.30, 20.79, 20.19])

C0 = 50
V = 0.5
m = 0.4

GAC_qt = (C0 - GAC_Ct) * V / m
BC_qt = (C0 - BC_Ct) * V / m

t_nonzero = t[1:]
GAC_qt_nz = GAC_qt[1:]
BC_qt_nz = BC_qt[1:]

def bangham_transform(qt, C0, m, V):
    inside_log = C0 / (C0 - qt * m / V)
    return np.log10(np.log10(inside_log))

GAC_bangham_y = bangham_transform(GAC_qt_nz, C0, m, V)
BC_bangham_y = bangham_transform(BC_qt_nz, C0, m, V)
log_t = np.log10(t_nonzero).reshape(-1, 1)

model_gac = LinearRegression().fit(log_t, GAC_bangham_y)
model_bc = LinearRegression().fit(log_t, BC_bangham_y)

GAC_pred = model_gac.predict(log_t)
BC_pred = model_bc.predict(log_t)

slope_gac = model_gac.coef_[0]
intercept_gac = model_gac.intercept_
slope_bc = model_bc.coef_[0]
intercept_bc = model_bc.intercept_

from sklearn.metrics import r2_score
r2_gac = r2_score(GAC_bangham_y, GAC_pred)
r2_bc = r2_score(BC_bangham_y, BC_pred)

plt.figure(figsize=(12,6))

plt.subplot(1,2,1)
plt.scatter(log_t, GAC_bangham_y, color='black', label='GAC Data')
plt.plot(log_t, GAC_pred, color='red', linestyle='--',
         label=f'Fit: y = {slope_gac:.3f}x + {intercept_gac:.3f}\nR² = {r2_gac:.4f}')
plt.title("Bangham Plot - GAC")
plt.xlabel("log(t)")
plt.ylabel("log(log(C0 / (C0 - qt·m/V)))")
plt.legend()
plt.grid(True)

plt.subplot(1,2,2)
plt.scatter(log_t, BC_bangham_y, color='black', label='BC Data')
plt.plot(log_t, BC_pred, color='blue', linestyle='--',
         label=f'Fit: y = {slope_bc:.3f}x + {intercept_bc:.3f}\nR² = {r2_bc:.4f}')
plt.title("Bangham Plot - BC")
plt.xlabel("log(t)")
plt.ylabel("log(log(C0 / (C0 - qt·m/V)))")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"GAC Bangham parameters: α = {slope_gac:.4f}, log(k) = {intercept_gac:.4f}")
print(f"BC Bangham parameters: α = {slope_bc:.4f}, log(k) = {intercept_bc:.4f}")
