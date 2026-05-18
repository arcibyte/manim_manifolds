from manim import *
import numpy as np
from palette import *

class GeodesicFlow(Scene):

    def construct(self):
        self.camera.background_color = BG
        grid = NumberPlane(
            x_range=[-7, 7],
            y_range=[-4, 4],
            background_line_style={
                "stroke_color": DIM,
                "stroke_opacity": 0.35,
                "stroke_width": 1,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=2,
        )
        self.add(grid)

        # campo de curvatura (densidad)
        def metric_factor(x, y):
            return np.exp(-0.45 * (x ** 2 + y ** 2))

        density_cells = VGroup()
        for xi in np.arange(-5.5, 5.6, 0.42):
            for yi in np.arange(-3.2, 3.3, 0.42):
                intensity = metric_factor(xi, yi)
                if intensity < 0.04:
                    continue
                cell = Square(side_length=0.40)
                cell.move_to([xi, yi, 0])
                color = interpolate_color(
                    ManimColor(DIM),
                    ManimColor(MANIFOLD_C),
                    intensity,
                )
                cell.set_fill(color, opacity=intensity * 0.55)
                cell.set_stroke(width=0)
                density_cells.add(cell)

        # anillo central
        dense_ring = Ellipse(
            width=3.8, height=2.8,
            color=MANIFOLD_C,
            stroke_width=1.2,
            stroke_opacity=0.6,
        )
        dense_ring.set_fill(MANIFOLD_C, opacity=0.08)

        dense_label = Text(
            "zona de alta curvatura",
            font_size=13,
            color=MUTED,
            slant=ITALIC,
        ).move_to([0, 0.15, 0])

        self.play(
            FadeIn(density_cells, lag_ratio=0.002, run_time=1.6),
            FadeIn(dense_ring, run_time=1.2),
            FadeIn(dense_label, run_time=1.0),
        )

        title = Text(
            "FLUJO DE LA GEODÉSICA",
            font_size=32,
            weight=BOLD,
            color=REAL_PATH,
            font="monospace",
        ).to_edge(UP, buff=0.28)

        subtitle = Text(
            "minimizando la energía en el espacio curvo",
            font_size=16,
            color=MUTED,
            slant=ITALIC,
        ).next_to(title, DOWN, buff=0.08)

        title_line = Line(
            LEFT * 3.8, RIGHT * 3.8,
            stroke_color=REAL_PATH,
            stroke_width=1,
            stroke_opacity=0.4,
        ).next_to(subtitle, DOWN, buff=0.1)

        self.play(
            Write(title, run_time=1.2),
            FadeIn(subtitle, shift=UP * 0.1),
            Create(title_line),
        )
        self.wait(0.3)

        #puntos a y b
        start_pt = np.array([-4.2, -2.2, 0])
        end_pt   = np.array([ 4.2,  2.2, 0])

        dot_a = Dot(start_pt, color=REAL_C, radius=0.14)
        dot_b = Dot(end_pt,   color=REAL_C, radius=0.14)

        ring_a = Circle(radius=0.22, color=REAL_C, stroke_width=1.5, stroke_opacity=0.5).move_to(start_pt)
        ring_b = Circle(radius=0.22, color=REAL_C, stroke_width=1.5, stroke_opacity=0.5).move_to(end_pt)

        label_a = MathTex("A", color=REAL_C, font_size=28).next_to(dot_a, DL, buff=0.15)
        label_b = MathTex("B", color=REAL_C, font_size=28).next_to(dot_b, UR, buff=0.15)

        self.play(
            FadeIn(dot_a, dot_b, scale=1.4),
            Create(ring_a), Create(ring_b),
            Write(label_a), Write(label_b),
            run_time=0.9,
        )
        self.wait(0.2)

        euclidean_line = Line(
            start_pt, end_pt,
            color=WRONG_PATH,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )
        euclidean_line.set_stroke(opacity=0.7)

        straight_label = Text(
            "camino recto  ·  cruza la zona densa",
            font_size=15,
            color=WRONG_PATH,
        ).move_to([-0.3, -1.5, 0])

        self.play(Create(euclidean_line, run_time=1.2))
        self.play(FadeIn(straight_label, shift=UP * 0.1))

        cost_pulses = VGroup()
        for frac in [0.28, 0.50, 0.72]:
            pt = start_pt + frac * (end_pt - start_pt)
            pulse = Circle(radius=0.20, color=WRONG_PATH, stroke_width=1.8).move_to(pt)
            cost_pulses.add(pulse)

        self.play(
            LaggedStartMap(GrowFromCenter, cost_pulses, lag_ratio=0.3),
            run_time=0.9,
        )
        self.wait(0.5)
        self.play(FadeOut(cost_pulses), FadeOut(straight_label))

        # geodesica
        geodesic_curve = CubicBezier(
            start_pt,
            np.array([-2.2, 3.6, 0]),
            np.array([ 2.2, 3.6, 0]),
            end_pt,
            color=REAL_PATH,
            stroke_width=4.5,
        )

        geo_label = Text(
            "geodésica  ·  rodea la zona densa",
            font_size=15,
            color=REAL_PATH,
        ).move_to([0, 3.78, 0])

        self.play(Create(geodesic_curve, run_time=2.2))
        self.play(FadeIn(geo_label, shift=DOWN * 0.1))
        self.wait(0.2)

        particle = Dot(color=REAL_PATH, radius=0.16).move_to(start_pt)
        glow = Circle(radius=0.30, color=REAL_PATH, stroke_width=1.2, stroke_opacity=0.35).move_to(start_pt)
        glow.add_updater(lambda m: m.move_to(particle.get_center()))

        trail = TracedPath(
            particle.get_center,
            stroke_color=REAL_PATH,
            stroke_width=2.5,
            stroke_opacity=0.4,
        )
        self.add(trail, glow, particle)

        self.play(
            MoveAlongPath(particle, geodesic_curve),
            run_time=3.2,
            rate_func=rate_functions.ease_in_out_sine,
        )

        self.play(
            Flash(
                dot_b,
                color=REAL_PATH,
                flash_radius=0.55,
                line_length=0.28,
                num_lines=12,
            ),
            run_time=0.7,
        )
        self.wait(0.3)

        comp_items = VGroup(
            VGroup(
                Text("Camino recto", font_size=16, color=WRONG_PATH, weight=BOLD),
                MathTex(
                    r"E_{\text{rect}} \gg 0",
                    font_size=17,
                    color=WRONG_PATH,
                ),
            ).arrange(RIGHT, buff=0.25),
            VGroup(
                Text("Geodésica", font_size=16, color=REAL_PATH, weight=BOLD),
                MathTex(
                    r"E_{\text{geo}} \to \min",
                    font_size=17,
                    color=REAL_PATH,
                ),
            ).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        comp_items.to_corner(DL, buff=0.5)

        comp_bg = RoundedRectangle(
            corner_radius=0.12,
            width=comp_items.width + 0.55,
            height=comp_items.height + 0.45,
            fill_color=BG,
            fill_opacity=0.92,
            stroke_color=DIM,
            stroke_width=1,
        ).move_to(comp_items)

        self.play(FadeIn(comp_bg), FadeIn(comp_items))
        self.wait(1.6)

        formula = MathTex(
            r"L(\gamma) = \int_a^b \sqrt{g_{ij}\,\dot{\gamma}^{\,i}\dot{\gamma}^{\,j}}\;dt"
            r"\;\longrightarrow\;\min",
            font_size=30,
            color=REAL_PATH,
        ).to_edge(DOWN, buff=0.55)

        formula_bg = RoundedRectangle(
            corner_radius=0.12,
            width=formula.width + 0.6,
            height=formula.height + 0.45,
            fill_color=BG,
            fill_opacity=0.92,
            stroke_color=REAL_PATH,
            stroke_width=0.8,
            stroke_opacity=0.6,
        ).move_to(formula)

        self.play(
            FadeOut(comp_bg, comp_items),
            FadeIn(formula_bg),
            Write(formula, run_time=2),
        )
        self.wait(3)

        self.play(
            FadeOut(
                grid, density_cells, dense_ring, dense_label,
                title, subtitle, title_line,
                dot_a, dot_b, ring_a, ring_b, label_a, label_b,
                euclidean_line,
                geodesic_curve, geo_label,
                trail, particle, glow,
                formula_bg, formula,
            ),
            run_time=1.8,
        )