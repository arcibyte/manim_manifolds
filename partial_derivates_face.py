from manim import *
import numpy as np
from palette import (
    BG, REAL_C, FAKE_C, BOUNDARY_C, GRAD_C,
    MUTED, DIM, MANIFOLD_C, REAL_PATH, WRONG_PATH,
)

class PartialDerivativesFace(Scene):

    def construct(self):
        self.camera.background_color = BG

        # grid
        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": DIM, "stroke_width": 0.8, "stroke_opacity": 0.25},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=3,
        )
        self.add(grid)

        # titulo
        title = Text("DERIVADAS PARCIALES", font_size=30, weight=BOLD, color=BOUNDARY_C, font="monospace").to_edge(UP, buff=0.26)
        subtitle = Text("cambio local en el espacio latente", font_size=15, color=MUTED, slant=ITALIC).next_to(title, DOWN, buff=0.07)
        title_line = Line(LEFT * 2.8, RIGHT * 2.8, stroke_color=BOUNDARY_C, stroke_width=0.8, stroke_opacity=0.35).next_to(subtitle, DOWN, buff=0.08)
        self.play(Write(title, run_time=0.9), FadeIn(subtitle, shift=UP * 0.08), Create(title_line))

        # superficie de apariencia G(z1, z2) 
        def G(x, y):
            return 0.4 * np.sin(0.9 * x) * np.cos(0.7 * y) + 0.3 * np.cos(0.5 * x + 0.3 * y)

        heatmap = VGroup()
        res = 0.30
        for x in np.arange(-5.5, 5.5 + res, res):
            for y in np.arange(-3.2, 3.2 + res, res):
                v = (G(x, y) + 0.8) / 1.6
                v = np.clip(v, 0, 1)
                color = interpolate_color(ManimColor(DIM), ManimColor(MANIFOLD_C), v)
                rect = Rectangle(width=res, height=res, fill_color=color,
                                  fill_opacity=v * 0.55, stroke_width=0).move_to([x, y, 0])
                heatmap.add(rect)

        self.play(FadeIn(heatmap, lag_ratio=0.001, run_time=1.5))

        # punto base z0 
        z0 = np.array([0.0, 0.0, 0])
        dot_z0 = Dot(z0, color=REAL_C, radius=0.14)
        ring_z0 = Circle(radius=0.24, color=REAL_C, stroke_width=1.5, stroke_opacity=0.45).move_to(z0)
        label_z0 = MathTex(r"z_0", color=REAL_C, font_size=22).next_to(dot_z0, DL, buff=0.12)

        self.play(FadeIn(dot_z0, scale=1.4), Create(ring_z0), Write(label_z0))
        self.wait(0.3)

        #flecha ∂G/∂z₁ (dirección x) 
        dz1 = 0.9 * np.cos(0.9 * 0) * np.cos(0.7 * 0) - 0.15 * np.sin(0.5 * 0 + 0)
        arrow_z1 = Arrow(
            z0, z0 + np.array([1.6, 0, 0]),
            buff=0, color=GRAD_C, stroke_width=2.8,
            max_tip_length_to_length_ratio=0.22,
        )
        label_dz1 = MathTex(r"\frac{\partial G}{\partial z_1}", color=GRAD_C, font_size=22).next_to(arrow_z1, RIGHT, buff=0.12)

        # flecha ∂G/∂z₂ (dirección y)
        arrow_z2 = Arrow(
            z0, z0 + np.array([0, 1.3, 0]),
            buff=0, color=BOUNDARY_C, stroke_width=2.8,
            max_tip_length_to_length_ratio=0.22,
        )
        label_dz2 = MathTex(r"\frac{\partial G}{\partial z_2}", color=BOUNDARY_C, font_size=22).next_to(arrow_z2, UP, buff=0.12)

        self.play(GrowArrow(arrow_z1), Write(label_dz1))
        self.wait(0.3)
        self.play(GrowArrow(arrow_z2), Write(label_dz2))
        self.wait(0.3)

        grad_dir = np.array([1.6, 1.3, 0])
        grad_dir_n = grad_dir / np.linalg.norm(grad_dir) * 2.1
        arrow_grad = Arrow(
            z0, z0 + grad_dir_n,
            buff=0, color=WRONG_PATH, stroke_width=3.2,
            max_tip_length_to_length_ratio=0.20,
        )
        label_grad = MathTex(r"\nabla_z G", color=WRONG_PATH, font_size=24).next_to(z0 + grad_dir_n, UR, buff=0.12)

        self.play(GrowArrow(arrow_grad), Write(label_grad))
        self.wait(0.3)

        level_curves = VGroup()
        for r, a in [(0.5, 0.55), (1.1, 0.38), (1.8, 0.22)]:
            level_curves.add(Circle(radius=r, color=MANIFOLD_C, stroke_width=0.9, stroke_opacity=a).move_to(z0))
        self.play(FadeIn(level_curves, lag_ratio=0.3))

        # perturbacion Δz
        delta_pt = z0 + np.array([0.9, 0.65, 0])
        dot_delta = Dot(delta_pt, color=FAKE_C, radius=0.11)
        ring_delta = Circle(radius=0.18, color=FAKE_C, stroke_width=1.2, stroke_opacity=0.45).move_to(delta_pt)
        label_delta = MathTex(r"z_0 + \Delta z", color=FAKE_C, font_size=18).next_to(dot_delta, UR, buff=0.10)

        dashed = DashedLine(z0, delta_pt, color=MUTED, stroke_width=1.2, stroke_opacity=0.6, dash_length=0.12)

        self.play(Create(dashed), FadeIn(dot_delta, scale=1.3), Create(ring_delta), Write(label_delta))
        self.wait(0.5)

        formula = MathTex(
            r"\Delta G \approx \frac{\partial G}{\partial z_1}\Delta z_1 + \frac{\partial G}{\partial z_2}\Delta z_2",
            font_size=30, color=REAL_PATH,
        ).to_edge(DOWN, buff=0.52)

        formula_bg = RoundedRectangle(
            corner_radius=0.12, width=formula.width + 0.65, height=formula.height + 0.46,
            fill_color=BG, fill_opacity=0.93, stroke_color=REAL_PATH, stroke_width=0.9, stroke_opacity=0.55,
        ).move_to(formula)

        self.play(FadeIn(formula_bg), Write(formula, run_time=1.8))
        self.wait(2.8)

        self.play(FadeOut(*self.mobjects), run_time=1.6)