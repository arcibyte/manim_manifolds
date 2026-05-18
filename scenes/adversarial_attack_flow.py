from manim import *
import numpy as np
from palette import (
    BG, REAL_C, FAKE_C, BOUNDARY_C, GRAD_C,
    MUTED, DIM, MANIFOLD_C, REAL_PATH, WRONG_PATH,
)

class AdversarialAttackFlow(Scene):

    def construct(self):
        self.camera.background_color = BG
        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": DIM, "stroke_width": 0.7, "stroke_opacity": 0.22},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=3,
        )
        self.add(grid)

        # --- Título ---
        title = Text("FLUJO DEL ATAQUE ADVERSARIAL", font_size=26, weight=BOLD, color=FAKE_C, font="monospace").to_edge(UP, buff=0.26)
        subtitle = Text("imagen real → manifold → engañar al detector", font_size=14, color=MUTED, slant=ITALIC).next_to(title, DOWN, buff=0.07)
        title_line = Line(LEFT * 3.0, RIGHT * 3.0, stroke_color=FAKE_C, stroke_width=0.8, stroke_opacity=0.35).next_to(subtitle, DOWN, buff=0.08)
        self.play(Write(title, run_time=0.9), FadeIn(subtitle, shift=UP * 0.08), Create(title_line))

        manifold_region = Ellipse(width=9.5, height=4.2, color=MANIFOLD_C, stroke_width=1.8, stroke_opacity=0.5)
        manifold_region.set_fill(MANIFOLD_C, opacity=0.07)
        manifold_region.move_to([0, -0.3, 0])
        manifold_label = Text("manifold M  (StyleGAN)", font_size=13, color=MANIFOLD_C, slant=ITALIC).move_to([0, 1.9, 0])
        self.play(Create(manifold_region, run_time=1.2), FadeIn(manifold_label))

        z0 = np.array([-3.5, -0.3, 0])
        dot_real = Dot(z0, color=REAL_C, radius=0.15)
        ring_real = Circle(radius=0.26, color=REAL_C, stroke_width=1.5, stroke_opacity=0.45).move_to(z0)
        label_real = VGroup(
            MathTex(r"z_0", color=REAL_C, font_size=22),
            Text("imagen real", font_size=12, color=REAL_C, slant=ITALIC),
        ).arrange(DOWN, buff=0.05).next_to(dot_real, DL, buff=0.13)
        self.play(FadeIn(dot_real, scale=1.5), Create(ring_real), Write(label_real))
        self.wait(0.3)

        n_steps = 8
        xs = np.linspace(-3.5, 1.8, n_steps)
        ys = -0.3 + 0.18 * np.sin(np.linspace(0, np.pi, n_steps))
        step_positions = [np.array([xs[i], ys[i], 0]) for i in range(n_steps)]

        trail_arrows = VGroup()
        trail_dots = VGroup()
        for i in range(1, n_steps - 1):
            a = Arrow(step_positions[i - 1], step_positions[i], buff=0.05,
                      color=GRAD_C, stroke_width=2.0, max_tip_length_to_length_ratio=0.22)
            d = Dot(step_positions[i], color=GRAD_C, radius=0.07)
            trail_arrows.add(a)
            trail_dots.add(d)

        grad_label = Text("descenso de gradiente\n∇ₙL(z)", font_size=13, color=GRAD_C, slant=ITALIC).move_to([-0.8, 1.2, 0])

        # FIX: GrowArrow está diseñado para Arrow; Create falla con ArrowTriangleFilledTip
        self.play(LaggedStart(*[GrowArrow(a) for a in trail_arrows], lag_ratio=0.15), run_time=2.2)
        self.play(LaggedStartMap(FadeIn, trail_dots, lag_ratio=0.12), FadeIn(grad_label))
        self.wait(0.3)

        z_star = step_positions[-1]
        dot_adv = Dot(z_star, color=WRONG_PATH, radius=0.15)
        ring_adv = Circle(radius=0.26, color=WRONG_PATH, stroke_width=1.5, stroke_opacity=0.5).move_to(z_star)
        label_adv = VGroup(
            MathTex(r"z^*", color=WRONG_PATH, font_size=22),
            Text("imagen falsa", font_size=12, color=WRONG_PATH, slant=ITALIC),
        ).arrange(DOWN, buff=0.05).next_to(dot_adv, DR, buff=0.13)
        self.play(FadeIn(dot_adv, scale=1.5), Create(ring_adv), Write(label_adv))
        self.play(Flash(dot_adv, color=WRONG_PATH, flash_radius=0.45, line_length=0.22, num_lines=10), run_time=0.7)
        self.wait(0.3)

        boundary = DashedVMobject(
            Line(np.array([0.8, 2.5, 0]), np.array([1.2, -2.8, 0]),
                 color=BOUNDARY_C, stroke_width=2.0, stroke_opacity=0.7),
            num_dashes=22,
        )
        boundary_label = Text("frontera\ndetector", font_size=13, color=BOUNDARY_C, slant=ITALIC).move_to([2.2, 1.8, 0])
        self.play(Create(boundary, run_time=1.0), FadeIn(boundary_label))

        cross_arrow = Arrow(
            np.array([0.9, -0.3, 0]), np.array([2.5, -0.3, 0]),
            buff=0.05, color=WRONG_PATH, stroke_width=2.2, max_tip_length_to_length_ratio=0.20,
        )
        cross_label = Text("cruza sin\nartefactos", font_size=12, color=WRONG_PATH, slant=ITALIC).next_to(cross_arrow, DOWN, buff=0.10)

        # FIX: GrowArrow en lugar de Create
        self.play(GrowArrow(cross_arrow), FadeIn(cross_label))
        self.wait(0.5)

        result = VGroup(
            Text("Detector:", font_size=15, color=MUTED),
            Text("REAL  ✓", font_size=18, color=REAL_C, weight=BOLD),
            Text("(engañado)", font_size=13, color=FAKE_C, slant=ITALIC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        result.to_corner(DR, buff=0.5)

        result_bg = RoundedRectangle(
            corner_radius=0.10, width=result.width + 0.45, height=result.height + 0.38,
            fill_color=BG, fill_opacity=0.92, stroke_color=BOUNDARY_C, stroke_width=0.8,
        ).move_to(result)
        self.play(FadeIn(result_bg), FadeIn(result, lag_ratio=0.3, run_time=1.0))
        self.wait(0.5)

        formula = MathTex(
            r"z^* = \arg\min_{z \in M}\; \mathcal{L}_{\text{adv}}(G(z),\, D)",
            font_size=30, color=FAKE_C,
        ).to_edge(DOWN, buff=0.52)

        formula_bg = RoundedRectangle(
            corner_radius=0.12, width=formula.width + 0.65, height=formula.height + 0.46,
            fill_color=BG, fill_opacity=0.93, stroke_color=FAKE_C, stroke_width=0.9, stroke_opacity=0.55,
        ).move_to(formula)
        self.play(FadeIn(formula_bg), Write(formula, run_time=1.8))
        self.wait(3.0)

        self.play(FadeOut(*self.mobjects), run_time=1.6)