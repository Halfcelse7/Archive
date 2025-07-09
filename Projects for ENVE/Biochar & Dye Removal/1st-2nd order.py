# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 11:02:56 2025

@author: ismtu
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

t = np.array([0, 15, 30, 45, 60, 90, 120, 150, 180])
GAC = np.array([50, 27.49, 21.12, 17.81, 14.00, 10.60, 5.40, 5.12, 4.19])
BC = np.array([50, 38.47, 35.58, 30.14, 27.95, 27.49, 21.30, 20.79, 20.19])

def first_order(t, k, C0):
    return C0 * np.exp(-k * t)

def second_order(t, k2, C0):
    return 1 / (1/C0 + k2 * t)

popt_gac_1st, _ = curve_fit(first_order, t, GAC, p0=(0.01, GAC[0]))
popt_gac_2nd, _ = curve_fit(second_order, t, GAC, p0=(0.001, GAC[0]))

popt_bc_1st, _ = curve_fit(first_order, t, BC, p0=(0.01, BC[0]))
popt_bc_2nd, _ = curve_fit(second_order, t, BC, p0=(0.001, BC[0]))

t_pred = np.linspace(0, 200, 100)
GAC_1st_pred = first_order(t_pred, *popt_gac_1st)
GAC_2nd_pred = second_order(t_pred, *popt_gac_2nd)
BC_1st_pred = first_order(t_pred, *popt_bc_1st)
BC_2nd_pred = second_order(t_pred, *popt_bc_2nd)

poly = PolynomialFeatures(degree=3)
t_poly = poly.fit_transform(t.reshape(-1, 1))

model_gac = LinearRegression().fit(t_poly, GAC)
model_bc = LinearRegression().fit(t_poly, BC)

t_pred_poly = poly.transform(t_pred.reshape(-1, 1))
GAC_ml_pred = model_gac.predict(t_pred_poly)
BC_ml_pred = model_bc.predict(t_pred_poly)

plt.figure(figsize=(12,6))

GAC_r2 = r2_score(GAC, model_gac.predict(t_poly))
BC_r2 = r2_score(BC, model_bc.predict(t_poly))

def format_poly_eq(coefs, intercept):
    a, b= coefs[2], coefs[1]
    c = intercept
    return f"y = {a:.4f}x² + {b:.4f}x + {c:.2f}"

plt.subplot(1, 2, 1)
plt.scatter(t, GAC, label="GAC Actual", color="black")
plt.plot(t_pred, GAC_1st_pred, label="1st-order", linestyle="--")
plt.plot(t_pred, GAC_2nd_pred, label="2nd-order", linestyle=":")
plt.plot(t_pred, GAC_ml_pred, label="PolyReg", linestyle="-")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.axhline(y=0, color='black', linewidth=0.5)
plt.axvline(x=0, color='black', linewidth=0.5)
plt.title("GAC Dye Removal")
plt.xlabel("Time (min)")
plt.ylabel("Concentration (mg/L)")
plt.text(
    0.02, 0.98,
    f"{format_poly_eq(model_gac.coef_, model_gac.intercept_)}\nR² = {GAC_r2:.4f}",
    transform=plt.gca().transAxes,
    fontsize=11, ha='left', va='top',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.6)
)

plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(t, BC, label="BC Actual", color="black")
plt.plot(t_pred, BC_1st_pred, label="1st-order", linestyle="--")
plt.plot(t_pred, BC_2nd_pred, label="2nd-order", linestyle=":")
plt.plot(t_pred, BC_ml_pred, label="PolyReg", linestyle="-")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.axhline(y=0, color='black', linewidth=0.5)
plt.axvline(x=0, color='black', linewidth=0.5)
plt.title("BC Dye Removal")
plt.xlabel("Time (min)")
plt.ylabel("Concentration (mg/L)")
plt.text(
    0.02, 0.98,
    f"{format_poly_eq(model_bc.coef_, model_bc.intercept_)}\nR² = {BC_r2:.4f}",
    transform=plt.gca().transAxes,
    fontsize=11, ha='left', va='top',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.6)
)

plt.legend()

plt.tight_layout()
plt.show()
