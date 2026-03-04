import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Eq.(S5): heterobilayer hexagonal flake (AA-centered, p != 1)
# Area-normalized energy S(θ,r,p)
# ============================================================

def nanoscale_S_S5_hexagon_AA_mismatch(theta_rad, r, p):
    theta = np.asarray(theta_rad, dtype=float)
    r = np.asarray(r, dtype=float)

    c = np.cos(theta)
    delta = 1.0 + p**2 - 2.0 * p * c
    sqrt_delta = np.sqrt(delta)

    arg = (-p + c) / sqrt_delta
    arg = np.clip(arg, -1.0, 1.0)
    A_minus = theta - np.arccos(arg)

    C = 2.0 * np.sqrt(3.0) * r * sqrt_delta

    denom = 8.0 * np.pi**2 * r**2 * delta * (-1.0 + 2.0 * np.cos(2.0 * A_minus))
    denom = np.where(np.abs(denom) < 1e-14, np.nan, denom)

    cosA = np.cos(A_minus)
    sinA = np.sin(A_minus)
    tanA = np.tan(A_minus)

    F = (
        2*np.sqrt(3)*np.cos((np.pi/3)*(1+2*C*cosA))
        - np.sqrt(3)*np.cos((np.pi/3)*(1+C*cosA+np.sqrt(3)*C*sinA))
        + 2*np.sqrt(3)*np.sin((np.pi/6)*(1+4*C*cosA))
        - np.sqrt(3)*np.sin((np.pi/6)*(1+2*C*cosA-2*np.sqrt(3)*C*sinA))
        - np.sqrt(3)*np.sin((np.pi/6)*(1+2*C*cosA+2*np.sqrt(3)*C*sinA))
        - np.cos((np.pi/3)*(1+C*cosA+np.sqrt(3)*C*sinA))*tanA
        - 4*np.cos((np.pi/6)+(np.pi*C/np.sqrt(3))*sinA)
          *np.sin((np.pi*C*cosA)/3)*tanA
        + np.sin((np.pi/6)*(1+2*C*cosA-2*np.sqrt(3)*C*sinA))*tanA
        + 4*np.sin((np.pi*C*cosA)/3)
          *np.sin((np.pi/3)*(1+np.sqrt(3)*C*sinA))*tanA
        - np.sin((np.pi/6)*(1+2*C*cosA+2*np.sqrt(3)*C*sinA))*tanA
        + np.cos((np.pi/3)*(1+C*cosA-np.sqrt(3)*C*sinA))
          *(-np.sqrt(3)+tanA)
    )

    return -np.sqrt(3) * F / denom


# ============================================================
# Geometry
# ============================================================

def area_hexagon(R):
    return (3.0 * np.sqrt(3.0) / 2.0) * R**2


# ============================================================
# Barrier extraction
# ============================================================

def extract_alignment_barriers(
    a_graphene=2.46,
    a_hbn=2.505,
    theta_align_deg=0.61,
    theta_window_deg=0.15,
    n_theta=30000,
    r_values=(100, 300, 500, 1000, 10000, 100000, 1000000),
):
    p = a_graphene / a_hbn
    theta_align = np.deg2rad(theta_align_deg)

    barriers = []
    r_out = []

    for r in r_values:
        R = r * a_graphene

        theta = np.linspace(
            theta_align - np.deg2rad(theta_window_deg),
            theta_align + np.deg2rad(theta_window_deg),
            n_theta
        )

        S = nanoscale_S_S5_hexagon_AA_mismatch(theta, r, p)
        E = S * area_hexagon(R)

        E = E[np.isfinite(E)]
        barriers.append(np.max(E) - np.min(E) if E.size else np.nan)
        r_out.append(r)

    return np.asarray(r_out), np.asarray(barriers)


# ============================================================
# Log–log slope
# ============================================================

def loglog_slope(x, y):
    mask = (x > 0) & (y > 0)
    lx = np.log(x[mask])
    ly = np.log(y[mask])
    A = np.vstack([lx, np.ones_like(lx)]).T
    return np.linalg.lstsq(A, ly, rcond=None)[0]


# ============================================================
# Publication-quality plot
# ============================================================

def make_publication_plot(
    save_dir="/Users/jharaplaprathap/Desktop",
    filename="heterobilayer_alignment_envelope_R_over_a"
):
    import os
    os.makedirs(save_dir, exist_ok=True)

    # ---- Times Roman font (publication standard)
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times"],
        "mathtext.fontset": "stix",
        "font.size": 12,
        "axes.labelsize": 13,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 11,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    r, barriers = extract_alignment_barriers()
    alpha, intercept = loglog_slope(r, barriers)

    fig, ax = plt.subplots(figsize=(7.2, 4.8))

    ax.loglog(r[:4], barriers[:4], "o", ms=7, label="simulated system sizes")
    ax.loglog(r[4:], barriers[4:], "o", ms=7, label="extended range")

    rfit = np.logspace(np.log10(r.min()), np.log10(r.max()), 300)
    ax.loglog(rfit, np.exp(intercept)*rfit**alpha, "--",
              label=rf"$\Delta E \propto (R/a)^{{{alpha:.2f}}}$")

    # ---- labels (UNCHANGED)
#     ax.set_xlabel(r"$R/a$")
#     ax.set_ylabel(r"$\Delta E$ (a.u.)")

    # ---- ticks & spines (publication quality, same locations)
    ax.tick_params(axis="both", which="major",
                   direction="in", length=7, width=1.5,
                   top=True, right=True)
    ax.tick_params(axis="both", which="minor",
                   direction="in", length=4, width=1.2,
                   top=True, right=True)

    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    
    ax.grid(True, which="major", alpha=0.3)
#     ax.grid(True, which="minor", alpha=0.5)
    ax.legend(frameon=False)
#     ax.set_xticklabels([]) 
#     ax.set_yticklabels([])

    fig.tight_layout()
    fig.savefig(f"{save_dir}/{filename}.pdf")
    fig.savefig(f"{save_dir}/{filename}.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    make_publication_plot()

