from manim import *
import numpy as np
from palette import (
    BG, REAL_C, FAKE_C, BOUNDARY_C, GRAD_C,
    MUTED, DIM, MANIFOLD_C, REAL_PATH, WRONG_PATH,
)


class ConclusionScene(Scene):

    def construct(self):
        self.camera.background_color = BG

        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": DIM, "stroke_width": 0.6, "stroke_opacity": 0.18},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=4,
        )
        self.add(grid)

        # ── Título central ──────────────────────────────────────────────
        title = Text("SÍNTESIS", font_size=44, weight=BOLD, color=REAL_PATH, font="monospace")
        subtitle = Text("gradiente  +  curvatura  +  manifold", font_size=18, color=MUTED, slant=ITALIC)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.18).move_to([0, 2.5, 0])
        title_line = Line(LEFT * 3.5, RIGHT * 3.5, stroke_color=REAL_PATH, stroke_width=0.8, stroke_opacity=0.35).next_to(subtitle, DOWN, buff=0.12)

        self.play(Write(title, run_time=1.1), FadeIn(subtitle, shift=UP * 0.08), Create(title_line))
        self.wait(0.3)

        # ── Tres bloques conceptuales ──────────────────────────────────
        blocks = [
            (r"\nabla G", "Gradiente guía\nel ataque", GRAD_C),
            (r"\kappa(z)", "Curvatura define\nla calidad visual", MANIFOLD_C),
            (r"\mathcal{M}", "Manifold restringe\na imágenes reales", BOUNDARY_C),
        ]

        block_group = VGroup()
        for symbol, desc, color in blocks:
            sym = MathTex(symbol, font_size=36, color=color)
            txt = Text(desc, font_size=14, color=MUTED)
            box_content = VGroup(sym, txt).arrange(DOWN, buff=0.18)
            box = RoundedRectangle(
                corner_radius=0.14,
                width=box_content.width + 0.7,
                height=box_content.height + 0.55,
                fill_color=BG, fill_opacity=0.88,
                stroke_color=color, stroke_width=1.2, stroke_opacity=0.7,
            ).move_to(box_content)
            block_group.add(VGroup(box, box_content))

        block_group.arrange(RIGHT, buff=0.55).move_to([0, 0.4, 0])

        for b in block_group:
            self.play(FadeIn(b, shift=UP * 0.12), run_time=0.7)
        self.wait(0.4)

        # ── Flechas de conexión entre bloques ─────────────────────────
        arrow_list = []
        for i in range(len(block_group) - 1):
            right_edge = block_group[i][0].get_right()
            left_edge  = block_group[i + 1][0].get_left()
            a = Arrow(right_edge, left_edge, buff=0.05,
                      color=MUTED, stroke_width=1.5, max_tip_length_to_length_ratio=0.22)
            a.set_opacity(0.6)
            arrow_list.append(a)
        self.play(AnimationGroup(
            *[FadeIn(a, shift=RIGHT * 0.1) for a in arrow_list],
            lag_ratio=0.4,
        ))
        self.wait(0.3)

        # ── Resultado final ────────────────────────────────────────────
        result_txt = VGroup(
            Text("deepfake indetectable", font_size=20, color=FAKE_C, weight=BOLD),
            Text("precisión del detector: >90%  →  <1%", font_size=15, color=MUTED, slant=ITALIC),
        ).arrange(DOWN, buff=0.12).move_to([0, -1.5, 0])

        result_bg = RoundedRectangle(
            corner_radius=0.14, width=result_txt.width + 0.65, height=result_txt.height + 0.48,
            fill_color=BG, fill_opacity=0.92, stroke_color=FAKE_C, stroke_width=1.2, stroke_opacity=0.65,
        ).move_to(result_txt)

        down_arrow = Arrow(
            block_group.get_bottom() + DOWN * 0.1,
            result_bg.get_top() + UP * 0.1,
            buff=0.05, color=MUTED, stroke_width=1.5, max_tip_length_to_length_ratio=0.22,
        )

        self.play(Create(down_arrow))
        self.play(FadeIn(result_bg), FadeIn(result_txt, lag_ratio=0.3))
        self.play(Flash(result_txt[0], color=FAKE_C, flash_radius=0.8, line_length=0.25, num_lines=12), run_time=0.8)
        self.wait(0.5)

        # ── Fórmula unificadora ────────────────────────────────────────
        formula = MathTex(
            r"z^* = \arg\min_{z \in \mathcal{M}}\;\mathcal{L}_{\text{adv}}(G(z), D)"
            r"\quad\text{s.t.}\quad \kappa(z) \leq \kappa_{\max}",
            font_size=26, color=REAL_PATH,
        ).to_edge(DOWN, buff=0.50)

        formula_bg = RoundedRectangle(
            corner_radius=0.12, width=formula.width + 0.65, height=formula.height + 0.46,
            fill_color=BG, fill_opacity=0.93, stroke_color=REAL_PATH, stroke_width=0.9, stroke_opacity=0.55,
        ).move_to(formula)

        self.play(FadeIn(formula_bg), Write(formula, run_time=2.0))
        self.wait(3.5)

        self.play(FadeOut(*self.mobjects), run_time=2.0)