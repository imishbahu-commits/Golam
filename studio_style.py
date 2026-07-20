"""
studio_style.py
Reusable "studio-grade" style toolkit derived from analysis of the
"How Are Memories Stored Inside Your Brain?" reference video.

PALETTE (measured from the reference):
  - Deep navy -> indigo -> purple background (mean brightness ~47/255)
  - Neon accents: electric violet, magenta, cyan, warm-yellow pop, white
MOTION SIGNATURE:
  - ~62% frames in continuous motion (camera drift + morphs)
  - snappy whip transitions, zoom-through camera moves
"""

from manim import *
import numpy as np

# ----------------------------------------------------------------------
# PALETTE  (hex values measured from the reference video frames)
# ----------------------------------------------------------------------
BG_DEEP     = "#05010F"   # near-black indigo (deepest)
BG_NAVY     = "#0B0A2A"   # dark navy
BG_INDIGO   = "#1A0B3D"   # indigo
BG_PURPLE   = "#2A0B50"   # purple mid

NEON_VIOLET = "#8A4BFF"
NEON_MAGENTA= "#C060FF"
NEON_CYAN   = "#3AE0FF"
NEON_BLUE   = "#4A6BFF"
POP_YELLOW  = "#FFE060"
POP_ORANGE  = "#FF9F1C"
INK_WHITE   = "#F4F1FF"

ACCENTS = [NEON_VIOLET, NEON_MAGENTA, NEON_CYAN, NEON_BLUE, POP_YELLOW]


# ----------------------------------------------------------------------
# BACKGROUND
# ----------------------------------------------------------------------
def deep_space_bg():
    """Vertical dark navy->purple gradient covering a generous area
    (bigger than frame so the camera can drift without showing edges)."""
    bg = Rectangle(width=config.frame_width * 3,
                   height=config.frame_height * 3, stroke_width=0)
    bg.set_fill(color=[BG_PURPLE, BG_INDIGO, BG_NAVY, BG_DEEP], opacity=1)
    bg.set_sheen_direction(UP)
    return bg


def particle_field(n=90, spread_x=22, spread_y=13, seed=11):
    """Faint drifting dust/particles for depth (parallax candy)."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        x = rng.uniform(-spread_x/2, spread_x/2)
        y = rng.uniform(-spread_y/2, spread_y/2)
        r = rng.uniform(0.01, 0.045)
        col = rng.choice([INK_WHITE, NEON_CYAN, NEON_VIOLET])
        d = Dot([x, y, 0], radius=r, color=col)
        d.set_opacity(rng.uniform(0.15, 0.7))
        g.add(d)
    return g


# ----------------------------------------------------------------------
# GLOW PRIMITIVES
# ----------------------------------------------------------------------
def glow_dot(point=ORIGIN, radius=0.16, color=NEON_CYAN, layers=7,
             intensity=0.10):
    """A bright core wrapped in soft additive-looking glow rings."""
    g = VGroup()
    for i in range(layers, 0, -1):
        ring = Circle(radius=radius * (1 + i * 0.55), stroke_width=0)
        ring.set_fill(color, opacity=intensity)
        g.add(ring)
    core = Circle(radius=radius, stroke_width=0).set_fill(INK_WHITE, opacity=1)
    core2 = Circle(radius=radius*1.6, stroke_width=0).set_fill(color, opacity=0.9)
    g.add(core2, core)
    g.move_to(point)
    return g


def glow_line(start, end, color=NEON_VIOLET, width=4):
    """A glowing connection (dendrite/axon) = fat soft line + bright core."""
    g = VGroup()
    for w, op in [(width*4, 0.08), (width*2.3, 0.16), (width, 1.0)]:
        ln = Line(start, end, stroke_width=w, color=color)
        ln.set_opacity(op if op < 1 else 1)
        g.add(ln)
    return g


# ----------------------------------------------------------------------
# NEURON MOTIF
# ----------------------------------------------------------------------
def neuron(center=ORIGIN, n_dendrites=6, size=0.9, color=NEON_VIOLET,
           soma_color=NEON_MAGENTA, seed=1):
    """A stylized neuron: glowing soma + radiating dendrites with tips."""
    rng = np.random.default_rng(seed)
    grp = VGroup()
    tips = []
    for k in range(n_dendrites):
        ang = (TAU * k / n_dendrites) + rng.uniform(-0.25, 0.25)
        length = size * rng.uniform(1.4, 2.3)
        end = center + length * np.array([np.cos(ang), np.sin(ang), 0])
        # a slight bend via a second segment
        mid = center + (length*0.55) * np.array([np.cos(ang), np.sin(ang), 0])
        bend = mid + size*0.25*np.array([np.cos(ang+1.3), np.sin(ang+1.3), 0])
        grp.add(glow_line(center, bend, color=color, width=3))
        grp.add(glow_line(bend, end, color=color, width=2.4))
        grp.add(glow_dot(end, radius=0.05, color=NEON_CYAN, layers=4,
                         intensity=0.13))
        tips.append(end)
    soma = glow_dot(center, radius=size*0.42, color=soma_color, layers=8,
                    intensity=0.11)
    grp.add(soma)
    grp.tips = tips
    grp.soma_center = center
    return grp


def travelling_pulse(scene, path_start, path_end, color=POP_YELLOW,
                     run_time=0.7, radius=0.09):
    """Fire a bright pulse that races along a dendrite (synaptic signal)."""
    p = glow_dot(path_start, radius=radius, color=color, layers=5,
                 intensity=0.18)
    scene.add(p)
    scene.play(p.animate.move_to(path_end),
               rate_func=rush_from, run_time=run_time)
    scene.play(FadeOut(p, scale=2.2), run_time=0.25)


# ----------------------------------------------------------------------
# TEXT
# ----------------------------------------------------------------------
def title_text(txt, scale=1.0, color=INK_WHITE, weight=BOLD):
    return Text(txt, font="sans-serif", weight=weight, color=color).scale(scale)


def kicker(txt, color=NEON_CYAN, scale=0.42):
    return Text(txt, font="sans-serif", slant=ITALIC, color=color).scale(scale)
