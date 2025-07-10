# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 09:23:16 2025

@author: ismtu
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore")

t = np.array([0, 15, 30, 45, 60, 90, 120, 150, 180], dtype=float)
GAC = np.array([50, 27.49, 21.12, 17.81, 14.00, 10.60, 5.40, 5.12, 4.19])
BC = np.array([50, 38.47, 35.58, 30.14, 27.95, 27.49, 21.30, 20.79, 20.19])
C0 = 50
V = 0.5
m = 0.4

GAC_qt = (C0 - GAC) * V / m
BC_qt = (C0 - BC) * V / m
GAC_qe = GAC_qt[-1]
BC_qe = BC_qt[-1]
t_nz = t[1:]
GAC_qt_nz = GAC_qt[1:]
BC_qt_nz = BC_qt[1:]

def first_order(t, k, C0):
    return C0 * np.exp(-k * t)

def second_order(t, k2, C0):
    return 1 / (1/C0 + k2 * t)

def pseudo_first_order(t, k, qe):
    return qe * (1 - np.exp(-k * t))

def pseudo_second_order(t, k2, qe):
    return (k2 * qe**2 * t) / (1 + k2 * qe * t)

def calc_r2(y_true, y_pred):
    return r2_score(y_true, y_pred)

def avrami(t, qe, k, n):
    return qe * (1 - np.exp(-k * t**n))

def format_avrami_eq(qe, k, n, r2):
    return f"qₜ = {qe:.2f}(1 - exp(-{k:.4f}·t^{n:.2f}))\nR² = {r2:.4f}"

def elovich_eq(t, alpha, beta):
    return (1/beta) * np.log(alpha * beta) + (1/beta) * np.log(t)

def boyd_func(F):
    return -0.4977 - np.log(1 - F)

def format_eq(model, r2):
    a = model.coef_[0]
    b = model.intercept_
    return f'y = {a:.4f}x + {b:.4f}\nR² = {r2:.4f}'

def bangham(qt, C0, m, V):
    return np.log10(np.log10(C0 / (C0 - qt * m / V)))

def format_poly_eq(coefs, intercept):
    a, b = coefs[2], coefs[1]
    c = intercept
    return f"y = {a:.4f}x² + {b:.4f}x + {c:.2f}"

print("Select a model to visualize:")
print("1: First-order & Second-order (Concentration based)")
print("2: Pseudo First-order & Second-order (qₜ based)")
print("3: Avrami")
print("4: Elovich")
print("5: Intraparticle Diffusion (Weber)")
print("6: Boyd")
print("7: Bangham")

choice = int(input("Enter model number (1-7): "))
plt.figure(figsize=(12,6))

if choice == 1:
    t_pred = np.linspace(0, 200, 100)
    popt_gac_1st, _ = curve_fit(first_order, t, GAC, p0=(0.01, C0))
    popt_gac_2nd, _ = curve_fit(second_order, t, GAC, p0=(0.001, C0))
    popt_bc_1st, _ = curve_fit(first_order, t, BC, p0=(0.01, C0))
    popt_bc_2nd, _ = curve_fit(second_order, t, BC, p0=(0.001, C0))

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
    GAC_r2 = r2_score(GAC, model_gac.predict(t_poly))
    BC_r2 = r2_score(BC, model_bc.predict(t_poly))

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

elif choice == 2:
    
    popt_gac_pfo, _ = curve_fit(pseudo_first_order, t, GAC_qt, p0=[0.01, max(GAC_qt)])
    popt_gac_pso, _ = curve_fit(pseudo_second_order, t, GAC_qt, p0=[0.01, max(GAC_qt)])

    popt_bc_pfo, _ = curve_fit(pseudo_first_order, t, BC_qt, p0=[0.01, max(BC_qt)])
    popt_bc_pso, _ = curve_fit(pseudo_second_order, t, BC_qt, p0=[0.01, max(BC_qt)])

    t_pred = np.linspace(0, 200, 100)
    GAC_pfo_pred = pseudo_first_order(t_pred, *popt_gac_pfo)
    GAC_pso_pred = pseudo_second_order(t_pred, *popt_gac_pso)
    BC_pfo_pred = pseudo_first_order(t_pred, *popt_bc_pfo)
    BC_pso_pred = pseudo_second_order(t_pred, *popt_bc_pso)

    GAC_pfo_r2 = calc_r2(GAC_qt, pseudo_first_order(t, *popt_gac_pfo))
    GAC_pso_r2 = calc_r2(GAC_qt, pseudo_second_order(t, *popt_gac_pso))
    BC_pfo_r2 = calc_r2(BC_qt, pseudo_first_order(t, *popt_bc_pfo))
    BC_pso_r2 = calc_r2(BC_qt, pseudo_second_order(t, *popt_bc_pso))
    
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

    print("GAC Pseudo-First-Order: k1 = {:.4f}  qe = {:.4f} mg/g".format(*popt_gac_pfo))
    print("GAC Pseudo-Second-Order: k2 = {:.4f}  qe = {:.4f} mg/g".format(*popt_gac_pso))
    print("BC Pseudo-First-Order: k1 = {:.4f}  qe = {:.4f} mg/g".format(*popt_bc_pfo))
    print("BC Pseudo-Second-Order: k2 = {:.4f}  qe = {:.4f} mg/g".format(*popt_bc_pso))
       

elif choice == 3:
    popt_gac, _ = curve_fit(avrami, t, GAC_qt, p0=(GAC_qe, 0.01, 1))
    popt_bc, _ = curve_fit(avrami, t, BC_qt, p0=(BC_qe, 0.01, 1))
    
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
    
elif choice == 4:
    ln_t = np.log(t_nz).reshape(-1, 1)
    model_gac = LinearRegression().fit(ln_t, GAC_qt_nz)
    model_bc = LinearRegression().fit(ln_t, BC_qt_nz)
    pred_gac = model_gac.predict(ln_t)
    pred_bc = model_bc.predict(ln_t)
    a_gac = model_gac.intercept_
    b_gac = model_gac.coef_[0]
    a_bc = model_bc.intercept_
    b_bc = model_bc.coef_[0]
    beta_gac = 1 / b_gac
    alpha_gac = np.exp(a_gac * beta_gac) / beta_gac
    beta_bc = 1 / b_bc
    alpha_bc = np.exp(a_bc * beta_bc) / beta_bc
    r2_gac = r2_score(GAC_qt_nz, pred_gac)
    r2_bc = r2_score(BC_qt_nz, pred_bc)
    
    plt.subplot(1, 2, 1)
    plt.scatter(ln_t, GAC_qt_nz, color='black', label='GAC Data')
    plt.plot(ln_t, pred_gac, color='red', linestyle='--', label=f'Fit: q_t = {a_gac:.3f} + {b_gac:.3f} ln(t)\nR²={r2_gac:.4f}')
    plt.title("GAC Elovich Model")
    plt.xlabel("ln(Time (min))")
    plt.ylabel("Adsorbed Amount q_t (mg/g)")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.scatter(ln_t, BC_qt_nz, color='black', label='BC Data')
    plt.plot(ln_t, pred_bc, color='blue', linestyle='--', label=f'Fit: q_t = {a_bc:.3f} + {b_bc:.3f} ln(t)\nR²={r2_bc:.4f}')
    plt.title("BC Elovich Model")
    plt.xlabel("ln(Time (min))")
    plt.ylabel("Adsorbed Amount q_t (mg/g)")
    plt.legend()
    plt.grid(True)

    print(f"GAC Elovich parameters: alpha = {alpha_gac:.4f}, beta = {beta_gac:.4f}")
    print(f"BC Elovich parameters: alpha = {alpha_bc:.4f}, beta = {beta_bc:.4f}")
    
elif choice == 5:
    sqrt_t = np.sqrt(t_nz).reshape(-1, 1)
    model_gac = LinearRegression().fit(sqrt_t, GAC_qt_nz)
    model_bc = LinearRegression().fit(sqrt_t, BC_qt_nz)
    pred_gac = model_gac.predict(sqrt_t)
    pred_bc = model_bc.predict(sqrt_t)
    k_id_gac = model_gac.coef_[0]
    C_gac = model_gac.intercept_
    k_id_bc = model_bc.coef_[0]
    C_bc = model_bc.intercept_
    r2_gac = r2_score(GAC_qt_nz, pred_gac)
    r2_bc = r2_score(BC_qt_nz, pred_bc)
    
    plt.subplot(1,2,1)
    plt.scatter(np.sqrt(t_nz), GAC_qt_nz, color='black', label="GAC Data")
    plt.plot(np.sqrt(t_nz), pred_gac, color='red', linestyle='--', label=f'Fit: q_t = {k_id_gac:.3f}√t + {C_gac:.3f}\nR²={r2_gac:.4f}')
    plt.title("GAC Intraparticle Diffusion")
    plt.xlabel("Square Root of Time (min^0.5)")
    plt.ylabel("Adsorbed Amount q_t (mg/g)")
    plt.legend()
    plt.grid(True)

    plt.subplot(1,2,2)
    plt.scatter(np.sqrt(t_nz), BC_qt_nz, color='black', label="BC Data")
    plt.plot(np.sqrt(t_nz), pred_bc, color='blue', linestyle='--', label=f'Fit: q_t = {k_id_bc:.3f}√t + {C_bc:.3f}\nR²={r2_bc:.4f}')
    plt.title("BC Intraparticle Diffusion")
    plt.xlabel("Square Root of Time (min^0.5)")
    plt.ylabel("Adsorbed Amount q_t (mg/g)")
    plt.legend()
    plt.grid(True)

    print(f"GAC intraparticle diffusion rate constant (k_id): {k_id_gac:.4f}")
    print(f"GAC intercept (C): {C_gac:.4f}")
    print(f"BC intraparticle diffusion rate constant (k_id): {k_id_bc:.4f}")
    print(f"BC intercept (C): {C_bc:.4f}")
    

elif choice == 6:
    F_gac = np.clip(GAC_qt / GAC_qe, 0, 1 - 1e-10)
    F_bc = np.clip(BC_qt / BC_qe, 0, 1 - 1e-10)
    Bt_gac = boyd_func(F_gac)[1:]
    Bt_bc = boyd_func(F_bc)[1:]
    t_fit = t[1:].reshape(-1, 1)
    model_gac = LinearRegression().fit(t_fit, Bt_gac)
    pred_gac = model_gac.predict(t_fit)
    r2_gac = r2_score(Bt_gac, pred_gac)
    model_bc = LinearRegression().fit(t_fit, Bt_bc)
    pred_bc = model_bc.predict(t_fit)
    r2_bc = r2_score(Bt_bc, pred_bc)
    pred_gac = model_gac.predict(t_nz.reshape(-1,1))
    pred_bc = model_bc.predict(t_nz.reshape(-1,1))
    
    plt.subplot(1,2,1)
    plt.scatter(t[1:], Bt_gac, color='black', label='Data')
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
    plt.scatter(t[1:], Bt_bc, color='black', label='Data')
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

elif choice == 7:
    Y_gac = bangham(GAC_qt_nz, C0, m, V)
    Y_bc = bangham(BC_qt_nz, C0, m, V)
    log_t = np.log10(t_nz).reshape(-1, 1)
    model_gac = LinearRegression().fit(log_t, Y_gac)
    model_bc = LinearRegression().fit(log_t, Y_bc)
    pred_gac = model_gac.predict(log_t)
    pred_bc = model_bc.predict(log_t)
    slope_gac = model_gac.coef_[0]
    intercept_gac = model_gac.intercept_
    slope_bc = model_bc.coef_[0]
    intercept_bc = model_bc.intercept_

    r2_gac = r2_score(Y_gac, pred_gac)
    r2_bc = r2_score(Y_bc, pred_bc)

    plt.subplot(1,2,1)
    plt.scatter(log_t, Y_gac, color='black', label='GAC Data')
    plt.plot(log_t, pred_gac, color='red', linestyle='--',
             label=f'Fit: y = {slope_gac:.3f}x + {intercept_gac:.3f}\nR² = {r2_gac:.4f}')
    plt.title("Bangham Plot - GAC")
    plt.xlabel("log(t)")
    plt.ylabel("log(log(C0 / (C0 - qt·m/V)))")
    plt.legend()
    plt.grid(True)

    plt.subplot(1,2,2)
    plt.scatter(log_t, Y_bc, color='black', label='BC Data')
    plt.plot(log_t, pred_bc, color='blue', linestyle='--',
             label=f'Fit: y = {slope_bc:.3f}x + {intercept_bc:.3f}\nR² = {r2_bc:.4f}')
    plt.title("Bangham Plot - BC")
    plt.xlabel("log(t)")
    plt.ylabel("log(log(C0 / (C0 - qt·m/V)))")
    plt.legend()
    plt.grid(True)

    print(f"GAC Bangham parameters: α = {slope_gac:.4f}, log(k) = {intercept_gac:.4f}")
    print(f"BC Bangham parameters: α = {slope_bc:.4f}, log(k) = {intercept_bc:.4f}")

else:
    print("Invalid selection.")
    exit()

plt.tight_layout()
plt.show()
