from manim import *
import numpy as np
from palette import (
    BG, REAL_C, FAKE_C, BOUNDARY_C, GRAD_C,
    MUTED, DIM, MANIFOLD_C, REAL_PATH, WRONG_PATH,
)


class DecisionBoundary(Scene):

    def construct(self):
        self.camera.background_color = BG

        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": DIM, "stroke_width": 0.7, "stroke_opacity": 0.22},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=3,
        )
        self.add(grid)

        title = Text("FRONTERA DE DECISIÓN", font_size=30, weight=BOLD, color=BOUNDARY_C, font="monospace").to_edge(UP, buff=0.26)
        subtitle = Text("espacio latente del detector", font_size=15, color=MUTED, slant=ITALIC).next_to(title, DOWN, buff=0.07)
        title_line = Line(LEFT * 2.8, RIGHT * 2.8, stroke_color=BOUNDARY_C, stroke_width=0.8, stroke_opacity=0.35).next_to(subtitle, DOWN, buff=0.08)
        self.play(Write(title, run_time=0.9), FadeIn(subtitle, shift=UP * 0.08), Create(title_line))

        real_region = Rectangle(width=6.0, height=7.5, fill_color=REAL_C, fill_opacity=0.06, stroke_width=0)
        real_region.move_to([-3.2, -0.3, 0])
        real_label = Text("REGIÓN REAL", font_size=14, color=REAL_C, weight=BOLD).move_to([-4.5, 2.8, 0])

        fake_region = Rectangle(width=6.0, height=7.5, fill_color=FAKE_C, fill_opacity=0.06, stroke_width=0)
        fake_region.move_to([3.2, -0.3, 0])
        fake_label = Text("REGIÓN FALSA", font_size=14, color=FAKE_C, weight=BOLD).move_to([4.5, 2.8, 0])

        self.play(FadeIn(real_region), FadeIn(fake_region), FadeIn(real_label), FadeIn(fake_label))

        boundary_curve = FunctionGraph(
            lambda y: 0.4 * np.sin(0.8 * y) + 0.1,
            x_range=[-3.5, 3.5],
            color=BOUNDARY_C,
            stroke_width=2.8,
            stroke_opacity=0.85,
        ).rotate(PI / 2)
        self.play(Create(boundary_curve, run_time=1.3))

        #nube de puntos reales
        np.random.seed(42)
        real_dots = VGroup()
        for _ in range(18):
            x = np.random.uniform(-5.5, -0.8)
            y = np.random.uniform(-2.8, 2.8)
            real_dots.add(Dot(np.array([x, y, 0]), color=REAL_C, radius=0.09,
                              fill_opacity=0.7))

        fake_dots = VGroup()
        for _ in range(18):
            x = np.random.uniform(0.8, 5.5)
            y = np.random.uniform(-2.8, 2.8)
            fake_dots.add(Dot(np.array([x, y, 0]), color=FAKE_C, radius=0.09,
                              fill_opacity=0.7))

        self.play(
            LaggedStartMap(FadeIn, real_dots, lag_ratio=0.06),
            LaggedStartMap(FadeIn, fake_dots, lag_ratio=0.06),
            run_time=1.5,
        )
        self.wait(0.3)
        manifold_arc = ArcBetweenPoints(
            np.array([-5.0, -1.8, 0]),
            np.array([-0.2, 1.5, 0]),
            angle=-TAU / 5,
            color=MANIFOLD_C,
            stroke_width=2.5,
            stroke_opacity=0.85,
        )
        manifold_label = Text("manifold M", font_size=13, color=MANIFOLD_C, slant=ITALIC).move_to([-3.5, -2.5, 0])
        self.play(Create(manifold_arc, run_time=1.2), FadeIn(manifold_label))

        # Punto adversarial que cruza la frontera
        z0 = np.array([-1.2, 0.3, 0])
        z_star = np.array([1.5, 0.6, 0])

        dot_z0 = Dot(z0, color=REAL_C, radius=0.14)
        ring_z0 = Circle(radius=0.23, color=REAL_C, stroke_width=1.4, stroke_opacity=0.45).move_to(z0)
        label_z0 = MathTex(r"z_0", color=REAL_C, font_size=20).next_to(dot_z0, UL, buff=0.10)

        self.play(FadeIn(dot_z0, scale=1.4), Create(ring_z0), Write(label_z0))

        attack_arrow = CurvedArrow(z0, z_star, angle=-TAU / 6,
                                    color=GRAD_C, stroke_width=2.5,
                                    tip_length=0.2)
        self.play(Create(attack_arrow, run_time=1.2))

        dot_zstar = Dot(z_star, color=WRONG_PATH, radius=0.14)
        ring_zstar = Circle(radius=0.23, color=WRONG_PATH, stroke_width=1.4, stroke_opacity=0.5).move_to(z_star)
        label_zstar = MathTex(r"z^*", color=WRONG_PATH, font_size=20).next_to(dot_zstar, UR, buff=0.10)

        self.play(FadeIn(dot_zstar, scale=1.4), Create(ring_zstar), Write(label_zstar))
        self.play(Flash(dot_zstar, color=WRONG_PATH, flash_radius=0.42, line_length=0.20, num_lines=10), run_time=0.6)
        self.wait(0.4)

        panel = VGroup(
            Text("D(G(z₀)) = FAKE", font_size=14, color=REAL_C),
            Text("D(G(z*)) = REAL", font_size=14, color=WRONG_PATH, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        panel.to_corner(DL, buff=0.5)

        panel_bg = RoundedRectangle(
            corner_radius=0.10, width=panel.width + 0.45, height=panel.height + 0.38,
            fill_color=BG, fill_opacity=0.92, stroke_color=DIM, stroke_width=0.8,
        ).move_to(panel)
        self.play(FadeIn(panel_bg), FadeIn(panel, lag_ratio=0.3))
        self.wait(0.5)

        formula = MathTex(
            r"D(G(z^*)) > \tau \implies \text{clasificado como REAL}",
            font_size=28, color=BOUNDARY_C,
        ).to_edge(DOWN, buff=0.52)

        formula_bg = RoundedRectangle(
            corner_radius=0.12, width=formula.width + 0.65, height=formula.height + 0.46,
            fill_color=BG, fill_opacity=0.93, stroke_color=BOUNDARY_C, stroke_width=0.9, stroke_opacity=0.55,
        ).move_to(formula)
        self.play(FadeIn(formula_bg), Write(formula, run_time=1.8))
        self.wait(2.8)

        self.play(FadeOut(*self.mobjects), run_time=1.6)