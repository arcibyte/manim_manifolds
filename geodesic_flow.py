from manim import *
import numpy as np

class GeodesicFlow(Scene):

    def construct(self):

        title = Text("Flujo de la Geodésica", font_size=40, weight=BOLD).to_edge(UP)
        subtitle = Text(
            "Minimizando la energía en el espacio curvo",
            font_size=22,
            color=GRAY,
        ).next_to(title, DOWN, buff=0.1)

        grid = NumberPlane(
            x_range=[-7, 7],
            y_range=[-4, 4],
            background_line_style={"stroke_opacity": 0.25},
        )

        def metric_factor(x, y):
            return np.exp(-0.4 * (x ** 2 + y ** 2))

        density_cells = VGroup()
        for xi in np.arange(-5, 5.1, 0.45):
            for yi in np.arange(-3, 3.1, 0.45):
                intensity = metric_factor(xi, yi)
                cell = Square(side_length=0.43)
                cell.move_to([xi, yi, 0])
                cell.set_fill(BLUE, opacity=intensity * 0.5)
                cell.set_stroke(width=0)
                density_cells.add(cell)

        dense_ring = Ellipse(width=3.6, height=2.6, color=BLUE_B, stroke_width=1.5)
        dense_ring.set_fill(BLUE_E, opacity=0.12)
        dense_label = Text("Zona de alta\ncurvatura", font_size=15, color=BLUE_B)
        dense_label.move_to([0, 0.2, 0])

        self.add(grid)
        self.play(FadeIn(density_cells), FadeIn(dense_ring, dense_label))
        self.play(Write(title), Write(subtitle))
        self.wait(0.4)

        start_pt = np.array([-4.0, -2.0, 0])
        end_pt = np.array([4.0, 2.0, 0])

        dot_a = Dot(start_pt, color=GREEN, radius=0.13)
        dot_b = Dot(end_pt, color=GREEN, radius=0.13)
        label_a = MathTex("A", color=GREEN).next_to(dot_a, DL, buff=0.12)
        label_b = MathTex("B", color=GREEN).next_to(dot_b, UR, buff=0.12)

        self.play(FadeIn(dot_a, dot_b, scale=1.5), Write(label_a), Write(label_b))
        self.wait(0.3)

        euclidean_line = Line(start_pt, end_pt, color=RED, stroke_width=3)
        euclidean_line.set_stroke(opacity=0.75)

        euclidean_label = Text(
            "Camino recto — atraviesa la zona densa",
            font_size=17, color=RED,
        ).move_to([-0.4, -1.3, 0])

        self.play(Create(euclidean_line))
        self.play(FadeIn(euclidean_label, shift=UP * 0.15))

        cost_pulses = VGroup()
        for frac in [0.3, 0.5, 0.7]:
            pt = start_pt + frac * (end_pt - start_pt)
            pulse = Circle(radius=0.18, color=RED, stroke_width=2).move_to(pt)
            cost_pulses.add(pulse)
        self.play(LaggedStartMap(GrowFromCenter, cost_pulses, lag_ratio=0.3), run_time=1)
        self.wait(0.8)
        self.play(FadeOut(cost_pulses))

        geodesic_curve = CubicBezier(
            start_pt,
            np.array([-2.5, 3.3, 0]),
            np.array([2.5, 3.3, 0]),
            end_pt,
            color=YELLOW,
            stroke_width=5,
        )
        geodesic_label = Text(
            "Geodésica — rodea la zona densa",
            font_size=17, color=YELLOW,
        ).move_to([0, 3.85, 0])

        self.play(FadeOut(euclidean_label))
        self.play(Create(geodesic_curve), run_time=2.5)
        self.play(FadeIn(geodesic_label, shift=DOWN * 0.15))
        self.wait(0.3)

        particle = Dot(color=YELLOW, radius=0.15).move_to(start_pt)
        self.add(particle)
        trail = TracedPath(
            particle.get_center,
            stroke_color=YELLOW,
            stroke_width=2.5,
            stroke_opacity=0.45,
        )
        self.add(trail)

        self.play(
            MoveAlongPath(particle, geodesic_curve),
            run_time=3.5,
            rate_func=rate_functions.ease_in_out_sine,
        )

        self.play(Flash(dot_b, color=YELLOW, flash_radius=0.5, line_length=0.25, num_lines=10), run_time=0.6)
        self.wait(0.4)

        comparison = VGroup(
            Text("Camino recto:", font_size=17, color=RED),
            MathTex(r"E_{\text{rect}} \gg 0 \quad \text{(cruza zona densa)}", font_size=18, color=RED),
            Text("Geodésica:", font_size=17, color=YELLOW),
            MathTex(r"E_{\text{geo}} \to \min \quad \text{(evita zona densa)}", font_size=18, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        comparison.to_corner(DL, buff=0.45)

        comp_box = SurroundingRectangle(
            comparison, color=WHITE, buff=0.22,
            fill_color=BLACK, fill_opacity=0.8,
        )
        self.play(FadeIn(comp_box), FadeIn(comparison))
        self.wait(1.8)

        formula = MathTex(
            r"L(\gamma) = \int_a^b \sqrt{g_{ij}\,\dot{\gamma}^{\,i}\dot{\gamma}^{\,j}}\;dt"
            r"\;\longrightarrow\;\min",
            font_size=34,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.55)

        formula_box = SurroundingRectangle(
            formula, color=YELLOW, buff=0.22,
            fill_color=BLACK, fill_opacity=0.88,
        )

        self.play(
            FadeOut(comp_box, comparison),
            Create(formula_box),
            Write(formula),
            run_time=2,
        )
        self.wait(3)

        self.play(
            FadeOut(
                grid, density_cells, dense_ring, dense_label,
                title, subtitle,
                dot_a, dot_b, label_a, label_b,
                euclidean_line,
                geodesic_curve, geodesic_label,
                trail, particle,
                formula_box, formula,
            ),
            run_time=1.8,
        )
