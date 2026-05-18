from manim import *
import numpy as np
from palette import (
    BG, REAL_C, FAKE_C, BOUNDARY_C, GRAD_C,
    MUTED, DIM, MANIFOLD_C, REAL_PATH, WRONG_PATH,
)


class GradientDescentManifold(Scene):

    def construct(self):
        self.camera.background_color = BG
        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": DIM, "stroke_width": 0.8, "stroke_opacity": 0.28},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=3,
        )
        self.add(grid)

        # ── Título ─────────────────────────────────────────────────────
        title = Text("DESCENSO DE GRADIENTE", font_size=30, weight=BOLD, color=GRAD_C, font="monospace").to_edge(UP, buff=0.26)
        subtitle = Text("sobre el manifold latente", font_size=15, color=MUTED, slant=ITALIC).next_to(title, DOWN, buff=0.07)
        title_line = Line(LEFT * 2.8, RIGHT * 2.8, stroke_color=GRAD_C, stroke_width=0.8, stroke_opacity=0.35).next_to(subtitle, DOWN, buff=0.08)
        self.play(Write(title, run_time=0.9), FadeIn(subtitle, shift=UP * 0.08), Create(title_line))

        # campo de perdida
        def loss_fn(x, y):
            return np.exp(-0.18 * ((x - 1.5)**2 + (y - 0.8)**2)) + \
                   0.5 * np.exp(-0.25 * ((x + 2)**2 + (y + 1)**2))

        heatmap = VGroup()
        res = 0.32
        for x in np.arange(-6, 6 + res, res):
            for y in np.arange(-3.5, 3.5 + res, res):
                v = loss_fn(x, y)
                color = interpolate_color(ManimColor(DIM), ManimColor(GRAD_C), np.clip(v, 0, 1))
                rect = Rectangle(width=res, height=res, fill_color=color,
                                  fill_opacity=min(0.65, v * 0.8), stroke_width=0).move_to([x, y, 0])
                heatmap.add(rect)

        # isolineas
        contours = VGroup()
        for r, a in [(0.6, 0.6), (1.2, 0.4), (2.0, 0.25), (2.9, 0.13)]:
            contours.add(Ellipse(width=r * 2.2, height=r * 1.5, color=GRAD_C,
                                  stroke_width=0.9, stroke_opacity=a).move_to([1.5, 0.8, 0]))

        self.play(FadeIn(heatmap, lag_ratio=0.001, run_time=1.5), FadeIn(contours, lag_ratio=0.3))

        manifold_curve = FunctionGraph(
            lambda x: 0.18 * x**2 - 0.6,
            x_range=[-5.5, 5.5],
            color=MANIFOLD_C,
            stroke_width=2.8,
            stroke_opacity=0.85,
        )
        manifold_label = Text("manifold M", font_size=14, color=MANIFOLD_C, slant=ITALIC).move_to([4.8, 3.2, 0])
        self.play(Create(manifold_curve, run_time=1.4), FadeIn(manifold_label))

        #punto inicial
        def on_manifold(x):
            return np.array([x, 0.18 * x**2 - 0.6, 0])

        start_x = -4.5
        start = on_manifold(start_x)

        dot = Dot(start, color=REAL_C, radius=0.13)
        ring = Circle(radius=0.22, color=REAL_C, stroke_width=1.5, stroke_opacity=0.5).move_to(start)
        ring.add_updater(lambda m: m.move_to(dot.get_center()))

        label_z = MathTex(r"z_0", color=REAL_C, font_size=22).next_to(dot, UL, buff=0.12)
        self.play(FadeIn(dot, scale=1.4), Create(ring), Write(label_z))
        self.wait(0.3)

        steps_x = np.linspace(start_x, 1.5, 9)
        step_dots = VGroup()
        step_arrows = VGroup()

        prev = start
        for i, sx in enumerate(steps_x[1:], 1):
            curr = on_manifold(sx)
            arrow = Arrow(
                prev, curr,
                buff=0.05,
                color=GRAD_C,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.25,
            )
            d = Dot(curr, color=GRAD_C, radius=0.07)
            step_dots.add(d)
            step_arrows.add(arrow)
            prev = curr

            self.play(
            AnimationGroup(
                *[Create(arrow) for arrow in step_arrows],
                lag_ratio=0.18
            ),
            run_time=2.8
        )
        self.play(
            AnimationGroup(
                *[FadeIn(dot_obj) for dot_obj in step_dots], # he cambiaod el nombre a dot_obj para evitar conflictos
                lag_ratio=0.18
            ),
            run_time=1.0
        )

        # mover dot al mínimo
        minimum = on_manifold(1.5)
        self.play(dot.animate.move_to(minimum), FadeOut(label_z), run_time=1.0)

        flash_dot = Dot(minimum, color=WRONG_PATH, radius=0.16)
        min_ring = Circle(radius=0.28, color=WRONG_PATH, stroke_width=1.5, stroke_opacity=0.5).move_to(minimum)
        label_min = MathTex(r"z^*", color=WRONG_PATH, font_size=24).next_to(flash_dot, UR, buff=0.13)
        label_adv = Text("imagen adversarial", font_size=13, color=WRONG_PATH, slant=ITALIC).next_to(label_min, DOWN, buff=0.06)

        self.play(
            FadeIn(flash_dot, scale=1.5),
            Create(min_ring),
            Write(label_min),
            FadeIn(label_adv),
        )
        self.play(Flash(flash_dot, color=WRONG_PATH, flash_radius=0.45, line_length=0.22, num_lines=10), run_time=0.7)
        self.wait(0.4)

        formula = MathTex(
            r"z_{t+1} = \Pi_M\!\left(z_t - \eta\,\nabla_z \mathcal{L}(z_t)\right)",
            font_size=32, color=GRAD_C,
        ).to_edge(DOWN, buff=0.52)

        formula_bg = RoundedRectangle(
            corner_radius=0.12, width=formula.width + 0.65, height=formula.height + 0.46,
            fill_color=BG, fill_opacity=0.93, stroke_color=GRAD_C, stroke_width=0.9, stroke_opacity=0.55,
        ).move_to(formula)

        self.play(FadeIn(formula_bg), Write(formula, run_time=1.8))
        self.wait(2.8)

        self.play(FadeOut(*self.mobjects), run_time=1.6)