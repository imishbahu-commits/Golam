"""
memory.py  -  Studio-level explainer showcase:
"How Are Memories Stored Inside Your Brain?"

Recreates the reference video's style:
  * dark navy->purple palette + neon accents
  * kinetic MOVING CAMERA (constant drift + zoom-through)
  * MORPHING transforms instead of hard cuts
  * SNAPPY whip transitions on beats
  * glowing neuron / synapse motifs with travelling pulses

Render preview :  manim -pql memory.py MemoryFilm
Render final   :  manim -qh --fps 60 memory.py MemoryFilm
"""

from manim import *
import numpy as np
from studio_style import (
    deep_space_bg, particle_field, glow_dot, glow_line, neuron,
    travelling_pulse, title_text, kicker,
    BG_DEEP, NEON_VIOLET, NEON_MAGENTA, NEON_CYAN, NEON_BLUE,
    POP_YELLOW, POP_ORANGE, INK_WHITE, ACCENTS,
)


class MemoryFilm(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG_DEEP
        cam = self.camera.frame

        bg = deep_space_bg()
        dust = particle_field()
        self.add(bg, dust)

        # slow perpetual dust drift running "under" everything
        dust.add_updater(lambda m, dt: m.rotate(0.02 * dt, about_point=ORIGIN))

        # ============================================================
        # SCENE 1 - TITLE  (calm intro, gentle camera breath)
        # ============================================================
        spark = glow_dot(ORIGIN, radius=0.05, color=NEON_CYAN, layers=6)
        self.play(GrowFromCenter(spark), run_time=0.8)

        title = title_text("How Are Memories", 0.95).shift(UP * 0.45)
        title2 = title_text("Stored in Your Brain?", 0.95,
                            color=NEON_CYAN).next_to(title, DOWN, buff=0.25)
        kick = kicker("a neural journey", NEON_MAGENTA).next_to(
            title2, DOWN, buff=0.4)

        self.play(
            spark.animate.scale(3).set_opacity(0.0),
            FadeIn(title, shift=UP * 0.3),
            run_time=0.9,
        )
        self.remove(spark)
        self.play(FadeIn(title2, shift=UP * 0.3), run_time=0.7)
        self.play(Write(kick), run_time=0.6)
        # gentle camera breath in
        self.play(cam.animate.scale(0.94), run_time=1.6, rate_func=smooth)
        self.wait(0.3)

        # SNAPPY whip transition out (quick pan + scale)
        self.play(
            VGroup(title, title2, kick).animate.shift(LEFT * 12).set_opacity(0),
            cam.animate.shift(RIGHT * 2).scale(1.2),
            run_time=0.45, rate_func=rush_into,
        )
        self.remove(title, title2, kick)
        self.play(cam.animate.move_to(ORIGIN).scale(1/1.2 * 1/0.94),
                  run_time=0.01)

        # ============================================================
        # SCENE 2 - A SINGLE NEURON (zoom-through reveal + morph)
        # ============================================================
        n1 = neuron(ORIGIN, n_dendrites=7, size=0.95,
                    color=NEON_VIOLET, soma_color=NEON_MAGENTA, seed=3)
        # camera pushes IN from far -> the "zoom-through" signature move
        cam.scale(2.4)
        self.play(
            LaggedStart(*[FadeIn(m, scale=0.6) for m in n1],
                        lag_ratio=0.04),
            cam.animate.scale(1/2.4),
            run_time=1.4, rate_func=smooth,
        )

        lbl = title_text("This is a neuron.", 0.6).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(lbl, shift=UP * 0.25), run_time=0.5)

        # a signal fires down one dendrite (travelling pulse)
        travelling_pulse(self, n1.soma_center, n1.tips[0],
                         color=POP_YELLOW, run_time=0.55)
        self.play(FadeOut(lbl, shift=DOWN * 0.2), run_time=0.4)

        # ============================================================
        # SCENE 3 - NETWORK GROWS (morph one -> many, camera orbit/pan)
        # ============================================================
        rng = np.random.default_rng(9)
        positions = [
            np.array([3.2, 1.6, 0]), np.array([-3.4, 1.2, 0]),
            np.array([2.8, -1.8, 0]), np.array([-2.9, -1.7, 0]),
            np.array([0.2, 2.6, 0]),
        ]
        neurons = [n1]
        anims = []
        for i, p in enumerate(positions):
            nn = neuron(p, n_dendrites=int(rng.integers(5, 8)),
                        size=float(rng.uniform(0.55, 0.8)),
                        color=ACCENTS[i % len(ACCENTS)],
                        soma_color=NEON_MAGENTA, seed=10 + i)
            neurons.append(nn)
            anims.append(FadeIn(nn, scale=0.5))

        # camera pulls back to reveal the growing network
        self.play(
            LaggedStart(*anims, lag_ratio=0.12),
            cam.animate.scale(1.5).shift(UP * 0.2),
            run_time=1.8, rate_func=smooth,
        )

        # draw glowing synaptic connections between nearby neurons
        connections = VGroup()
        centers = [n.soma_center for n in neurons]
        pairs = [(0, 1), (0, 2), (0, 4), (1, 4), (2, 3), (0, 3), (3, 4)]
        for a, b in pairs:
            connections.add(glow_line(centers[a], centers[b],
                                      color=NEON_BLUE, width=2))
        self.play(
            LaggedStart(*[Create(m) for m in connections], lag_ratio=0.08),
            run_time=1.2,
        )

        net_lbl = title_text("Memories live in the connections.", 0.52,
                             color=NEON_CYAN).to_edge(UP, buff=0.7)
        self.play(FadeIn(net_lbl, shift=DOWN * 0.2), run_time=0.5)

        # fire a cascade of pulses across the network (snappy, rhythmic)
        for a, b in [(0, 1), (1, 4), (4, 0), (0, 2), (2, 3), (3, 4)]:
            travelling_pulse(self, centers[a], centers[b],
                             color=POP_YELLOW, run_time=0.32, radius=0.07)
        self.wait(0.2)

        # SNAPPY whip transition (rotate + zoom through the network)
        self.play(
            cam.animate.scale(0.28).move_to(centers[0]),
            net_lbl.animate.set_opacity(0),
            rate_func=rush_into, run_time=0.6,
        )

        # ============================================================
        # SCENE 4 - THE SYNAPSE (macro zoom-in, strengthening morph)
        # ============================================================
        self.clear()
        self.camera.background_color = BG_DEEP
        bg2 = deep_space_bg()
        dust2 = particle_field(seed=21)
        self.add(bg2, dust2)
        cam.move_to(ORIGIN).scale(3.57)  # reset zoom cleanly

        left_end = np.array([-1.4, 0, 0])
        right_end = np.array([1.4, 0, 0])
        pre = glow_dot(left_end, radius=0.35, color=NEON_VIOLET, layers=8)
        post = glow_dot(right_end, radius=0.35, color=NEON_CYAN, layers=8)
        gap = glow_line(left_end + RIGHT * 0.4, right_end + LEFT * 0.4,
                        color=NEON_BLUE, width=2)
        self.play(FadeIn(pre, scale=0.5), FadeIn(post, scale=0.5),
                  cam.animate.scale(1/3.57), run_time=1.0)
        self.play(Create(gap), run_time=0.5)

        syn_lbl = title_text("A synapse.", 0.6).to_edge(UP, buff=0.9)
        self.play(FadeIn(syn_lbl), run_time=0.4)

        # neurotransmitters crossing the gap
        for i in range(5):
            travelling_pulse(self, left_end + RIGHT * 0.4,
                             right_end + LEFT * 0.4,
                             color=POP_ORANGE, run_time=0.28, radius=0.06)

        # "strengthening" = the connection grows brighter & thicker (morph)
        strong = glow_line(left_end + RIGHT * 0.4, right_end + LEFT * 0.4,
                           color=POP_YELLOW, width=6)
        self.play(
            Transform(gap, strong),
            pre.animate.scale(1.25), post.animate.scale(1.25),
            FadeOut(syn_lbl, shift=UP * 0.2),
            run_time=0.8,
        )
        strengthen = title_text("Repetition strengthens it.", 0.52,
                                color=POP_YELLOW).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(strengthen, shift=UP * 0.2), run_time=0.5)
        self.wait(0.4)

        # ============================================================
        # SCENE 5 - OUTRO (pull WAY back: synapse -> network -> spark)
        # ============================================================
        self.play(
            FadeOut(strengthen), FadeOut(gap), FadeOut(pre), FadeOut(post),
            cam.animate.scale(0.35),
            run_time=0.7, rate_func=rush_into,
        )
        self.clear()
        self.camera.background_color = BG_DEEP
        self.add(deep_space_bg(), particle_field(seed=33))
        cam.move_to(ORIGIN).scale(1/0.35)

        outro = title_text("That is a memory.", 0.9)
        outro2 = kicker("built from a billion glowing connections",
                        NEON_CYAN, 0.45).next_to(outro, DOWN, buff=0.35)
        end_spark = glow_dot(ORIGIN, 0.05, NEON_MAGENTA, layers=6)
        self.play(GrowFromCenter(end_spark), run_time=0.5)
        self.play(end_spark.animate.scale(4).set_opacity(0),
                  FadeIn(outro, shift=UP * 0.25), run_time=0.9)
        self.remove(end_spark)
        self.play(FadeIn(outro2), cam.animate.scale(0.95),
                  run_time=0.9)
        self.wait(1.2)
        self.play(FadeOut(VGroup(outro, outro2)), run_time=0.8)
        self.wait(0.3)
