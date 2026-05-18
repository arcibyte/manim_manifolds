from manim import *
import numpy as np
from palette import *

class MetricTensorEvolution(Scene):

    def construct(self):
        self.camera.background_color = BG

        def metric_field(point):
            x, y = point[0], point[1]
            dist = np.sqrt(x ** 2 + y ** 2)
            return 1.0 / (1.0 + 0.5 * dist ** 2)

        # grid de coordenadas 
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": DIM,
                "stroke_width": 0.8,
                "stroke_opacity": 0.28,
            },
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=3,
        )
        self.add(grid)

        # heatmap con 3 colores (DIM → MANIFOLD_C → REAL_PATH)
        heatmap = VGroup()
        res = 0.28
        for x in np.arange(-6, 6 + res, res):
            for y in np.arange(-3.5, 3.5 + res, res):
                m_val = metric_field(np.array([x, y, 0]))
                if m_val < 0.05:
                    continue
                if m_val < 0.5:
                    t = m_val / 0.5
                    color = interpolate_color(ManimColor(DIM), ManimColor(MANIFOLD_C), t)
                else:
                    t = (m_val - 0.5) / 0.5
                    color = interpolate_color(ManimColor(MANIFOLD_C), ManimColor(REAL_PATH), t * 0.6)
                rect = Rectangle(
                    width=res, height=res,
                    fill_color=color,
                    fill_opacity=min(0.7, m_val * 0.75),
                    stroke_width=0,
                ).move_to([x, y, 0])
                heatmap.add(rect)

        # anillos de contorno (isolíneas de curvatura) 
        contours = VGroup()
        for r, alpha in [(0.9, 0.55), (1.8, 0.38), (3.0, 0.22), (4.2, 0.12)]:
            ring = Circle(
                radius=r,
                color=MANIFOLD_C,
                stroke_width=0.8,
                stroke_opacity=alpha,
            )
            contours.add(ring)
        title = Text(
            "TENSOR MÉTRICO",
            font_size=32,
            weight=BOLD,
            color=REAL_PATH,
            font="monospace",
        ).to_edge(UP, buff=0.26)

        subtitle = Text(
            "geometría del espacio latente",
            font_size=15,
            color=MUTED,
            slant=ITALIC,
        ).next_to(title, DOWN, buff=0.07)

        title_line = Line(
            LEFT * 3.0, RIGHT * 3.0,
            stroke_color=REAL_PATH,
            stroke_width=0.8,
            stroke_opacity=0.35,
        ).next_to(subtitle, DOWN, buff=0.08)

        self.play(
            Write(title, run_time=0.9),
            FadeIn(subtitle, shift=UP * 0.08),
            Create(title_line),
        )
        self.play(
            FadeIn(heatmap, lag_ratio=0.001, run_time=1.6),
            FadeIn(contours, lag_ratio=0.3, run_time=1.2),
        )

        # elipses tensores
        tensors = VGroup()
        for x in np.linspace(-5.0, 5.0, 12):
            for y in np.linspace(-3.0, 3.0, 7):
                pos = np.array([x, y, 0])
                m_val = metric_field(pos)
                stretch = 1 - m_val + 0.12
                w = max(0.07, 0.78 * stretch)
                h = max(0.04, 0.42 * stretch)
                t = np.clip(m_val, 0, 1)
                color = interpolate_color(ManimColor(MANIFOLD_C), ManimColor(BOUNDARY_C), t)
                ellipse = Ellipse(
                    width=w,
                    height=h,
                    stroke_width=1.4,
                    color=color,
                    stroke_opacity=0.75,
                ).move_to(pos)
                norm = np.linalg.norm([x, y])
                if norm > 0.1:
                    ellipse.rotate(np.arctan2(y, x))
                tensors.add(ellipse)

        self.play(
            LaggedStartMap(Create, tensors, lag_ratio=0.03),
            run_time=2.5,
        )
        self.wait(0.5)

        scanner_start = np.array([-4.2, 2.2, 0])
        scanner_dot = Dot(color=REAL_C, radius=0.13).move_to(scanner_start)

        scanner_ring_inner = Circle(radius=0.20, color=REAL_C, stroke_width=1.8, stroke_opacity=0.6)
        scanner_ring_outer = Circle(radius=0.34, color=REAL_C, stroke_width=0.8, stroke_opacity=0.25)
        for ring in [scanner_ring_inner, scanner_ring_outer]:
            ring.move_to(scanner_start)
            ring.add_updater(lambda m: m.move_to(scanner_dot.get_center()))

        def make_local_tensor():
            pos = scanner_dot.get_center()
            m = metric_field(pos)
            stretch = 1 - m + 0.12
            w = max(0.14, 1.5 * stretch)
            h = max(0.09, 0.82 * stretch)
            norm = np.linalg.norm(pos[:2])
            angle = np.arctan2(pos[1], pos[0]) if norm > 0.1 else 0
            e = Ellipse(
                width=w, height=h,
                color=BOUNDARY_C,
                stroke_width=3.0,
                stroke_opacity=0.9,
            ).move_to(pos).rotate(angle)
            return e

        local_tensor = always_redraw(make_local_tensor)

        def make_value_label():
            pos = scanner_dot.get_center()
            m = metric_field(pos)
            return VGroup(
                MathTex(r"g(z)_{\text{local}}", color=BOUNDARY_C, font_size=19),
                MathTex(
                    r"= {:.3f}".format(m),
                    color=REAL_PATH,
                    font_size=17,
                ),
            ).arrange(RIGHT, buff=0.08).next_to(
                scanner_dot, UP, buff=0.38
            )

        label_g = always_redraw(make_value_label)

        self.play(
            FadeIn(scanner_dot, scale=1.5),
            Create(scanner_ring_inner),
            Create(scanner_ring_outer),
            Create(local_tensor),
            Write(label_g),
        )

        path = ArcBetweenPoints(
            scanner_start,
            np.array([4.2, -2.2, 0]),
            angle=-TAU / 3.8,
        )

        trail = TracedPath(
            scanner_dot.get_center,
            stroke_color=GRAD_C,
            stroke_width=2.0,
            stroke_opacity=0.5,
        )
        self.add(trail)

        self.play(
            MoveAlongPath(scanner_dot, path),
            run_time=5.0,
            rate_func=rate_functions.ease_in_out_sine,
        )

        self.play(
            Flash(scanner_dot, color=REAL_C, flash_radius=0.45, line_length=0.22, num_lines=10),
            run_time=0.6,
        )
        self.wait(0.3)

        legend_items = VGroup(
            VGroup(
                Square(side_length=0.18, fill_color=DIM, fill_opacity=0.9, stroke_width=0),
                Text("baja curvatura", font_size=13, color=MUTED),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Square(side_length=0.18, fill_color=MANIFOLD_C, fill_opacity=0.9, stroke_width=0),
                Text("curvatura media", font_size=13, color=MUTED),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Square(side_length=0.18, fill_color=REAL_PATH, fill_opacity=0.9, stroke_width=0),
                Text("alta curvatura", font_size=13, color=MUTED),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend_items.to_corner(DR, buff=0.5)

        legend_bg = RoundedRectangle(
            corner_radius=0.10,
            width=legend_items.width + 0.45,
            height=legend_items.height + 0.38,
            fill_color=BG,
            fill_opacity=0.90,
            stroke_color=DIM,
            stroke_width=0.8,
        ).move_to(legend_items)

        self.play(FadeIn(legend_bg), FadeIn(legend_items, lag_ratio=0.25))
        self.wait(0.8)

        formula = MathTex(
            r"ds^2 = \sum_{i,j} g_{ij}(z)\, dz^i\, dz^j",
            font_size=34,
            color=REAL_PATH,
        ).to_edge(DOWN, buff=0.50)

        formula_bg = RoundedRectangle(
            corner_radius=0.12,
            width=formula.width + 0.65,
            height=formula.height + 0.48,
            fill_color=BG,
            fill_opacity=0.93,
            stroke_color=REAL_PATH,
            stroke_width=0.9,
            stroke_opacity=0.55,
        ).move_to(formula)

        self.play(
            FadeOut(legend_bg, legend_items),
            FadeIn(formula_bg),
            Write(formula, run_time=1.8),
        )
        self.wait(2.8)

        self.play(
            FadeOut(
                grid, heatmap, contours, tensors,
                title, subtitle, title_line,
                scanner_dot, scanner_ring_inner, scanner_ring_outer,
                local_tensor, label_g, trail,
                formula_bg, formula,
            ),
            run_time=1.8,
        )