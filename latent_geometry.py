from manim import *
import numpy as np
class LinearVsGeodesic(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=0.85)

        title = Text("Interpolación Lineal vs Geodésica", font_size=38, weight=BOLD)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        #Superficie (manifold)
        def surface_func(u, v):
            return np.array([
                u,
                v,
                0.4 * np.sin(2 * u) * np.cos(2 * v),
            ])

        surface = Surface(
            surface_func,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(40, 40),
            fill_opacity=0.55,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )
        surface.set_style(stroke_width=0.4, stroke_color=WHITE, stroke_opacity=0.2)

        self.play(Create(surface), run_time=2)
        self.wait(0.5)

        p1 = surface_func(-1.5, -1.5)
        p2 = surface_func(1.5, 1.5)

        dot1 = Dot3D(point=p1, color=GREEN, radius=0.12)
        dot2 = Dot3D(point=p2, color=GREEN, radius=0.12)

        label_start = Text("z₁", font_size=28, color=GREEN)
        label_end = Text("z₂", font_size=28, color=GREEN)
        self.add_fixed_in_frame_mobjects(label_start, label_end)
        label_start.to_corner(UL, buff=0.8)
        label_end.to_corner(UR, buff=0.8)

        self.play(FadeIn(dot1), FadeIn(dot2), Write(label_start), Write(label_end))
        self.wait(0.5)

        def linear_func(t):
            return p1 + t * (p2 - p1)

        linear_path = ParametricFunction(
            linear_func,
            t_range=[0, 1, 0.01],
            color=RED,
        ).set_stroke(width=4)

        linear_label = Text("Interpolación Lineal", font_size=26, color=RED)
        linear_label.next_to(title, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(linear_label)

        self.play(Create(linear_path), Write(linear_label), run_time=1.8)
        self.wait(0.5)

        def geodesic_func(t):
            u = -1.5 + 3 * t
            v = -1.5 + 3 * t
            return surface_func(u, v)

        geodesic_path = ParametricFunction(
            geodesic_func,
            t_range=[0, 1, 0.01],
            color=YELLOW,
        ).set_stroke(width=5)

        geodesic_label = Text("Geodésica (sobre el manifold)", font_size=26, color=YELLOW)
        geodesic_label.next_to(linear_label, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(geodesic_label)

        self.play(Create(geodesic_path), Write(geodesic_label), run_time=2)
        self.wait(0.5)

        sphere_linear = Sphere(radius=0.08).set_color(RED).move_to(p1)
        sphere_geodesic = Sphere(radius=0.08).set_color(YELLOW).move_to(p1)
        self.add(sphere_linear, sphere_geodesic)

        def update_linear(mob, alpha):
            mob.move_to(linear_func(alpha))

        def update_geodesic(mob, alpha):
            mob.move_to(geodesic_func(alpha))

        self.play(
            UpdateFromAlphaFunc(sphere_linear, update_linear),
            UpdateFromAlphaFunc(sphere_geodesic, update_geodesic),
            run_time=4,
            rate_func=linear,
        )
        self.wait(0.5)

        deviation_text = Text(
            "La línea recta atraviesa el espacio ambiente\n"
            "La geodésica permanece sobre el manifold",
            font_size=22,
            color=WHITE,
            line_spacing=1.4,
        ).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(deviation_text)
        self.play(Write(deviation_text))

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(1)



class MetricTensorEvolution(Scene):

    def construct(self):

        title = Text("Geometría del Tensor Métrico", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.5)

        def metric_field(point):
            x, y = point[0], point[1]
            dist = np.sqrt(x ** 2 + y ** 2)
            return 1.0 / (1.0 + 0.5 * dist ** 2)

        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.25,
            },
        )

        heatmap = VGroup()
        res = 0.3
        for x in np.arange(-5, 5 + res, res):
            for y in np.arange(-3, 3 + res, res):
                m_val = metric_field(np.array([x, y, 0]))
                color = interpolate_color(DARK_BLUE, YELLOW, m_val)
                rect = Rectangle(
                    width=res, height=res,
                    fill_color=color,
                    fill_opacity=0.35,
                    stroke_width=0,
                ).move_to([x, y, 0])
                heatmap.add(rect)

        self.play(Write(title), Create(grid))
        self.play(FadeIn(heatmap), run_time=2)

        tensors = VGroup()
        for x in np.linspace(-4.5, 4.5, 10):
            for y in np.linspace(-2.5, 2.5, 6):
                pos = np.array([x, y, 0])
                m_val = metric_field(pos)
                w = max(0.08, 0.9 * (1 - m_val + 0.15))
                h = max(0.05, 0.55 * (1 - m_val + 0.15))
                ellipse = Ellipse(
                    width=w,
                    height=h,
                    stroke_width=1.8,
                    color=RED_A if m_val < 0.5 else YELLOW_A,
                ).move_to(pos)
                if np.linalg.norm([x, y]) > 0.1:
                    ellipse.rotate(np.arctan2(y, x))
                tensors.add(ellipse)

        self.play(LaggedStartMap(Create, tensors, lag_ratio=0.04), run_time=3)
        self.wait(0.5)

        scanner_dot = Dot(color=WHITE, radius=0.1).move_to([-4, 2, 0])

        def make_local_tensor():
            m = metric_field(scanner_dot.get_center())
            w = max(0.12, 1.4 * (1 - m + 0.1))
            h = max(0.08, 0.8 * (1 - m + 0.1))
            return Ellipse(
                width=w, height=h,
                color=PURE_RED,
                stroke_width=4,
            ).move_to(scanner_dot.get_center())

        local_tensor = always_redraw(make_local_tensor)

        label_g = always_redraw(
            lambda: MathTex(r"g(z)_{\text{local}}", color=PURE_RED, font_size=22)
            .next_to(local_tensor, UP, buff=0.15)
        )

        self.play(FadeIn(scanner_dot), Create(local_tensor), Write(label_g))

        path = ArcBetweenPoints(
            np.array([-4, 2, 0]), np.array([4, -2, 0]), angle=-TAU / 4
        )
        self.play(MoveAlongPath(scanner_dot, path), run_time=4.5, rate_func=linear)
        self.wait(0.5)

        formula = MathTex(
            r"ds^2 = \sum_{i,j} g_{ij}\, dz^i\, dz^j",
            font_size=40,
            color=WHITE,
        ).to_edge(DOWN, buff=0.55)

        bg_rect = SurroundingRectangle(
            formula, color=BLUE_A, buff=0.25,
            fill_color=BLACK, fill_opacity=0.85,
        )

        self.play(Create(bg_rect), Write(formula))
        self.wait(2.5)

        self.play(
            FadeOut(
                title, grid, heatmap, tensors,
                scanner_dot, local_tensor, label_g,
                bg_rect, formula,
            ),
            run_time=1.5,
        )

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
