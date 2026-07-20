"""
Kurzgesagt-style explainer animation made with Manim Community v0.19.

Render (fast preview 480p):
    manim -pql kurzgesagt.py KurzgesagtIntro

Render (final 1080p 60fps):
    manim -qh --fps 60 kurzgesagt.py KurzgesagtIntro

The video walks through a tiny "How big is the Sun?" style explainer,
using the flat-vector, deep-space, glowing look Kurzgesagt is known for.
"""

from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# 1. THE KURZGESAGT PALETTE
# ---------------------------------------------------------------------------
BG_TOP = "#0B1E3F"       # deep navy
BG_BOTTOM = "#123B63"    # lighter ocean blue
SUN_CORE = "#FFD35C"     # warm yellow
SUN_GLOW = "#FF9F1C"     # orange glow
EARTH_BLUE = "#3AAED8"   # bright cyan-blue
EARTH_LAND = "#5FD68B"   # mint green
CREAM = "#F7F3E3"        # off-white text
POP_RED = "#FF5D5D"
POP_PURPLE = "#9B5DE5"
STAR_YELLOW = "#FDE74C"


def gradient_background():
    """A vertical gradient fills the whole frame (Kurzgesagt deep-space look)."""
    bg = Rectangle(
        width=config.frame_width,
        height=config.frame_height,
        stroke_width=0,
    )
    bg.set_fill(color=[BG_BOTTOM, BG_TOP], opacity=1)
    bg.set_sheen_direction(UP)
    return bg


def starfield(n=60, seed=7):
    """Scatter tiny twinkling stars behind everything."""
    rng = np.random.default_rng(seed)
    stars = VGroup()
    for _ in range(n):
        x = rng.uniform(-config.frame_width / 2, config.frame_width / 2)
        y = rng.uniform(-config.frame_height / 2, config.frame_height / 2)
        r = rng.uniform(0.008, 0.03)
        s = Dot(point=[x, y, 0], radius=r, color=CREAM)
        s.set_opacity(rng.uniform(0.3, 0.9))
        stars.add(s)
    return stars


def glowing_body(radius, core_color, glow_color, glow_layers=6):
    """A flat disc surrounded by soft concentric glow rings."""
    group = VGroup()
    for i in range(glow_layers, 0, -1):
        ring = Circle(radius=radius * (1 + i * 0.18), stroke_width=0)
        ring.set_fill(glow_color, opacity=0.06)
        group.add(ring)
    core = Circle(radius=radius, stroke_width=0)
    core.set_fill(core_color, opacity=1)
    group.add(core)
    return group


def little_planet(radius, base, land):
    """A cute planet with a couple of flat 'continents'."""
    planet = VGroup()
    body = Circle(radius=radius, stroke_width=0).set_fill(base, opacity=1)
    planet.add(body)
    # a few blobby continents clipped visually inside
    for angle, scale in [(30, 0.5), (150, 0.4), (250, 0.55)]:
        blob = Circle(radius=radius * scale, stroke_width=0).set_fill(land, opacity=1)
        blob.move_to(body.get_center() + 0.55 * radius * np.array(
            [np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0]))
        planet.add(blob)
    return planet


class KurzgesagtIntro(Scene):
    def construct(self):
        # --- Background & stars ---
        bg = gradient_background()
        stars = starfield()
        self.add(bg, stars)

        # gentle twinkle
        self.play(
            LaggedStart(
                *[Succession(
                    s.animate.set_opacity(1.0),
                    s.animate.set_opacity(0.4),
                ) for s in stars[:20]],
                lag_ratio=0.05, run_time=2,
            ),
            run_time=2,
        )

        # --- Title ---
        title = Text("How big is the Sun?", font="sans-serif",
                     weight=BOLD, color=CREAM).scale(1.1)
        subtitle = Text("a tiny cosmic explainer", font="sans-serif",
                        slant=ITALIC, color=STAR_YELLOW).scale(0.5)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(title, shift=UP * 0.4), run_time=1.2)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # --- The Sun appears ---
        sun = glowing_body(2.2, SUN_CORE, SUN_GLOW)
        sun.move_to(ORIGIN)
        self.play(GrowFromCenter(sun), run_time=1.2)

        # slow breathing pulse of the glow
        self.play(sun.animate.scale(1.06), rate_func=there_and_back,
                  run_time=1.5)

        sun_label = Text("The Sun", font="sans-serif", color=CREAM).scale(0.7)
        sun_label.next_to(sun, DOWN, buff=0.5)
        self.play(Write(sun_label), run_time=0.8)
        self.wait(0.6)

        # --- Shrink sun aside, bring in Earth for comparison ---
        self.play(
            sun.animate.scale(0.55).to_edge(LEFT, buff=1.2),
            FadeOut(sun_label),
            run_time=1.2,
        )

        earth = little_planet(0.28, EARTH_BLUE, EARTH_LAND)
        earth.next_to(sun, RIGHT, buff=3.0)
        earth_label = Text("Earth", font="sans-serif", color=CREAM).scale(0.5)
        earth_label.next_to(earth, DOWN, buff=0.35)

        self.play(GrowFromCenter(earth), FadeIn(earth_label, shift=UP*0.2),
                  run_time=1.0)

        # arrow / scale note
        note = Text("You'd fit ~1,300,000 Earths inside!",
                    font="sans-serif", color=STAR_YELLOW).scale(0.5)
        note.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(note, shift=UP*0.3), run_time=0.9)

        # earth orbits a little
        self.play(
            Rotating(earth, angle=TAU, about_point=sun.get_center(),
                     run_time=3, rate_func=linear),
            earth_label.animate.set_opacity(0),
        )
        self.wait(0.4)

        # --- Closing card ---
        self.play(
            FadeOut(earth), FadeOut(note),
            sun.animate.scale(1.6).move_to(ORIGIN),
            run_time=1.2,
        )

        outro = Text("Stay curious.", font="sans-serif", weight=BOLD,
                     color=CREAM).scale(0.9)
        outro.move_to(ORIGIN)
        # sun tucks behind text
        self.play(sun.animate.scale(0.5).to_edge(UP, buff=0.6), run_time=1.0)
        self.play(Write(outro), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(outro), FadeOut(sun), FadeOut(stars),
                  FadeOut(bg), run_time=1.2)
