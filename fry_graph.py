"""
Creates a clean Fry Readability Graph - NO data points, only grade boundaries.
Matches the standard Fry Graph format (Edward Fry, 1968).
See FRY_FORMULAE.md for X and Y axis computation formulae.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Fry Graph: X = syllables per 100 words (108-172), Y = sentences per 100 words (2-25)
x_min, x_max = 108, 172
y_min, y_max = 2.0, 25.0

def fry_grade(syllables, sentences):
    """Approximate Fry grade level from syllables and sentences per 100 words."""
    s_norm = (syllables - 108) / 64
    p_norm = (sentences - 2) / 23
    difficulty = (1 - p_norm) * 0.6 + s_norm * 0.4 + 0.08 * (1 - p_norm) * s_norm
    return np.clip(1 + difficulty * 14, 1, 15)

# Build grid for contour
xx = np.linspace(x_min, x_max, 300)
yy = np.linspace(y_min, y_max, 300)
XG, YG = np.meshgrid(xx, yy)
ZG = np.vectorize(fry_grade)(XG, YG)

fig, ax = plt.subplots(figsize=(14, 11))

# Gradient background (light blue top-left to darker blue bottom-right)
gradient = np.zeros((*ZG.shape, 4))
for i in range(ZG.shape[0]):
    for j in range(ZG.shape[1]):
        t = (i / ZG.shape[0] + j / ZG.shape[1]) / 2
        gradient[i, j] = (0.88 - t*0.25, 0.94 - t*0.15, 1.0, 0.5)
ax.imshow(gradient, extent=[x_min, x_max, y_min, y_max], origin='lower', aspect='auto', zorder=0)

# Grade regions (filled, subtle)
levels = np.arange(1, 17, 1)
ax.contourf(XG, YG, ZG, levels=levels, alpha=0.2, cmap='Blues', zorder=1)

# Curved boundary lines (main feature - clear and bold)
ax.contour(XG, YG, ZG, levels=levels, colors='#1e3a5f', linewidths=1.5, alpha=0.9, zorder=2)

# Grade numbers in white circles
for g in range(1, 16):
    s_frac = (g - 1) / 15
    p_frac = 1 - s_frac * 0.9
    sx = x_min + (x_max - x_min) * (s_frac * 0.7 + 0.15)
    sy = y_min + (y_max - y_min) * (p_frac * 0.85 + 0.08)
    circle = mpatches.Circle((sx, sy), 0.9, color='white', ec='#1a365d', linewidth=2, zorder=3)
    ax.add_patch(circle)
    ax.text(sx, sy, str(g), ha='center', va='center', fontsize=11, fontweight='bold', color='#1a365d', zorder=4)

# "long words" region (upper-right)
ax.add_patch(mpatches.Rectangle((x_max-10, y_max-3), 10, 3, facecolor='#1a365d', edgecolor='#2c5282', alpha=0.8, zorder=1))
ax.text(x_max-5, y_max-1.5, 'long words', fontsize=9, ha='center', va='center', color='white', fontweight='bold', zorder=5)

# "long sentences" region (bottom-left)
ax.add_patch(mpatches.Rectangle((x_min, y_min), 8, 2.5, facecolor='#1a365d', edgecolor='#2c5282', alpha=0.8, zorder=1))
ax.text(x_min+4, y_min+1.25, 'long sentences', fontsize=9, ha='center', va='center', color='white', fontweight='bold', zorder=5)

# NO data points - clean graph only

# Axes with Fry-style tick marks
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xticks(np.arange(108, 173, 4))
ax.set_yticks([2.0, 2.5, 3.0, 3.3, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.7, 7.1, 8.3, 10.0, 12.5, 16.7, 20, 25])
ax.set_xlabel("Average number of syllables per 100 words", fontsize=13, fontweight='bold')
ax.set_ylabel("Average number of sentences per 100 words", fontsize=13, fontweight='bold')
ax.set_title("Fry Graph\nFOR ESTIMATING READING AGES (GRADE LEVEL)", fontsize=15, fontweight='bold')
ax.grid(True, alpha=0.5, linestyle='-', color='#94a3b8')

# "Grade Levels" diagonal watermark
ax.text(0.5, 0.5, 'Grade Levels', transform=ax.transAxes, fontsize=12, alpha=0.2,
        rotation=-35, ha='center', va='center', style='italic')

plt.tight_layout()
plt.savefig("fry_readability_diagram.png", dpi=200, bbox_inches="tight")
plt.close()
print("Fry diagram saved to: fry_readability_diagram.png")
