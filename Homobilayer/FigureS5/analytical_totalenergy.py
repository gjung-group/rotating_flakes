import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

# ============================================================
# Publication-quality matplotlib style
# ============================================================

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "STIXGeneral"],
    "mathtext.fontset": "stix",
    "figure.dpi": 900,
    "savefig.dpi": 600,
    "axes.linewidth": 1.2,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "lines.linewidth": 1.8,
    "grid.linewidth": 0.6,
})

# ============================================================
# Eq.(S5): hexagon, AA-centered, lattice mismatch p ≠ 1
# ============================================================

def nanoscale_S_S5_hexagon_AA_mismatch(theta_rad, r, p):
    c = np.cos(theta_rad)
    delta = 1 + p**2 - 2*p*c
    sqrt_delta = np.sqrt(delta)

    arg = (-p + c) / sqrt_delta
    arg = np.clip(arg, -1.0, 1.0)

    A = theta_rad - np.arccos(arg)
    C = 2*np.sqrt(3)*r*sqrt_delta

    denom = 8*np.pi**2*r**2*delta*(-1 + 2*np.cos(2*A))
    denom = np.where(np.abs(denom) < 1e-14, np.nan, denom)

    tA = np.tan(A)
    cA, sA = np.cos(A), np.sin(A)

    brace = (
        2*np.sqrt(3)*np.cos((np.pi/3)*(1+2*C*cA))
        -np.sqrt(3)*np.cos((np.pi/3)*(1+C*cA+np.sqrt(3)*C*sA))
        +2*np.sqrt(3)*np.sin((np.pi/6)*(1+4*C*cA))
        -np.sqrt(3)*np.sin((np.pi/6)*(1+2*C*cA-2*np.sqrt(3)*C*sA))
        -np.sqrt(3)*np.sin((np.pi/6)*(1+2*C*cA+2*np.sqrt(3)*C*sA))
        -np.cos((np.pi/3)*(1+C*cA+np.sqrt(3)*C*sA))*tA
        -4*np.cos((np.pi/6)+(np.pi*C/np.sqrt(3))*sA)
         *np.sin((np.pi*C*cA)/3)*tA
        +np.sin((np.pi/6)*(1+2*C*cA-2*np.sqrt(3)*C*sA))*tA
        +4*np.sin((np.pi*C*cA)/3)
         *np.sin((np.pi/3)*(1+np.sqrt(3)*C*sA))*tA
        -np.sin((np.pi/6)*(1+2*C*cA+2*np.sqrt(3)*C*sA))*tA
        +np.cos((np.pi/3)*(1+C*cA-np.sqrt(3)*C*sA))*(-np.sqrt(3)+tA)
    )

    return -np.sqrt(3)*brace / denom

# ============================================================
# Geometry
# ============================================================

def area_hexagon_circumradius(R):
    return (3*np.sqrt(3)/2)*R**2

# ============================================================
# Plot with MANUAL y-limits per panel
# ============================================================

def plot_small_angle_manual_ylims(r_values, a, p, save_path):

    # ===== YOU CONTROL THESE NUMBERS =====
    y_limits = {
        100: (-10000, 12000),
        300: (-15000, 40000),
        500: (-51000, 50000),
        1000: (-90000, 110000),
    }
    # ====================================

    fig, axes = plt.subplots(
        nrows=len(r_values),
        ncols=1,
        figsize=(6.2, 2.4*len(r_values)),
        sharex=True,
        gridspec_kw={"hspace": 0.0},  # no gaps
    )

    axes = np.atleast_1d(axes)

    theta_deg = np.linspace(1e-3, 3.0, 8000)
    theta_rad = np.deg2rad(theta_deg)

    for i, r in enumerate(r_values):
        ax = axes[i]

        A = area_hexagon_circumradius(r*a)
        E = nanoscale_S_S5_hexagon_AA_mismatch(theta_rad, r, p) * A
        E -= np.nanmean(E)

        ax.plot(theta_deg, E, color="black")
        ax.set_xlim(0.0, 3.0)
#         ax.set_xticklabels([]) 
#         ax.set_yticklabels([])
#         plt.tick_params(axis='both', which='major', width=2, length=12, labelsize=20)
#         plt.tick_params(axis='both', which='minor', width=2, length=12, labelsize=20)
#         ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
#         ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
#         for spine in ax.spines.values():
#             spine.set_linewidth(2.5)
            
            
        ax.plot(theta_deg, E, color="black")
        ax.set_xlim(0.0, 3.0)

        # ---- Ticks: control per axis (CORRECT way) ----
        ax.tick_params(
            axis='both',
            which='major',
            width=2.5,
            length=12,
            labelsize=20,
        )

        ax.tick_params(
            axis='both',
            which='minor',
            width=2.0,
            length=6,
        )

        # Remove tick labels (keep ticks)
        ax.tick_params(labelbottom=False, labelleft=False)

        # Tick density
        ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

        # Thicker frame (journal style)
        for spine in ax.spines.values():
            spine.set_linewidth(2.5)


        ymin, ymax = y_limits[r]
        ax.set_ylim(ymin, ymax)

#         ax.grid(True, alpha=0.25)

#         ax.text(
#             0.02, 0.85,
#             rf"$R/a = {r}$",
#             transform=ax.transAxes,
#             fontsize=13,
#         )

        if i != len(r_values)-1:
            ax.set_xticklabels([])

#     axes[-1].set_xlabel(r"Twist angle $\theta$ (degrees)")
#     fig.supylabel(r"$E(\theta)-\langle E\rangle$ (arb. units)", x=0.04)
    

    fig.tight_layout(rect=(0.06, 0.02, 1, 1))
    fig.savefig(save_path, bbox_inches="tight")
    print(f"Saved figure: {save_path}")
    plt.show()

# ============================================================
# Run
# ============================================================

def run():
    desktop = "/Users/jharaplaprathap/Desktop"

    r_values = (100, 300, 500, 1000)
    a_graphene = 2.505
    a_hbn = 2.46
    p = a_graphene / a_hbn

    plot_small_angle_manual_ylims(
        r_values,
        a_graphene,
        p,
        os.path.join(desktop, "Fig_S5_manual_ylims.png"),
    )

if __name__ == "__main__":
    run()

