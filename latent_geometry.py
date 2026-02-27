from manim import *
import numpy as np

class LinearVsGeodesic(ThreeDScene):

    def construct(self):
        title = Text("Interpolación Lineal vs Geodésica", font_size=42)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # manifold superficie
        def surface_func(u, v):
            return np.array([
                u,
                v,
                0.3 * np.sin(2*u) * np.cos(2*v)
            ])
        
        surface = Surface(
            surface_func,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            fill_opacity=0.6,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        self.play(Create(surface))
        self.wait()
        
        p1 = surface_func(-1.5, -1.5)
        p2 = surface_func(1.5, 1.5)
        
        dot1 = Dot3D(point=p1, color=GREEN, radius=0.15)
        dot2 = Dot3D(point=p2, color=GREEN, radius=0.15)
        
        label_start = Text("z₁", font_size=30, color=GREEN)
        label_end = Text("z₂", font_size=30, color=GREEN)
        self.add_fixed_in_frame_mobjects(label_start, label_end)
        label_start.move_to([-5, 2, 0])
        label_end.move_to([5, 2, 0])
        
        self.play(
            FadeIn(dot1),
            FadeIn(dot2),
            Write(label_start),
            Write(label_end)
        )
        self.wait()
        
        linear_path = Line(p1, p2, color=RED).set_stroke(width=4)
        
        linear_label = Text("Interpolación Lineal", font_size=28, color=RED)
        linear_label.next_to(title, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(linear_label)
        
        self.play(
            Create(linear_path),
            Write(linear_label),
            run_time=2
        )
        self.wait()
        
        def geodesic_func(t):
            u = -1.5 + 3 * t
            v = -1.5 + 3 * t
            return surface_func(u, v)
        
        geodesic_path = ParametricFunction(
            geodesic_func,
            t_range=[0, 1],
            color=YELLOW
        ).set_stroke(width=6)
        
        geodesic_label = Text("Geodésica", font_size=28, color=YELLOW)
        geodesic_label.next_to(linear_label, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(geodesic_label)
        
        self.play(
            Create(geodesic_path),
            Write(geodesic_label),
            run_time=2
        )
        self.wait()
        
        moving_dot_linear = Dot3D(point=p1, color=RED, radius=0.12)
        moving_dot_geodesic = Dot3D(point=p1, color=YELLOW, radius=0.12)
        
        self.play(
            MoveAlongPath(moving_dot_linear, linear_path),
            MoveAlongPath(moving_dot_geodesic, geodesic_path),
            run_time=4,
            rate_func=linear
        )
        self.wait()
        
        deviation_text = Text(
            "La línea recta sale del manifold, la geodésica permanece en él",
            font_size=22,
            color=WHITE,
            line_spacing=1.5
        )
        deviation_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(deviation_text)
        self.play(Write(deviation_text))
        
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        self.wait(2)
        
from manim import *
import numpy as np

class MetricTensorEvolution(Scene):
    def construct(self):
        title = Text("Geometría del Tensor Métrico", font_size=44, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        def metric_field(point):
            x, y = point[0], point[1]
            dist = np.sqrt(x**2 + y**2)
            return 1 / (1 + 0.5 * dist**2)

        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.2
            }
        )

        heatmap = VGroup()
        res = 0.25 
        for x in np.arange(-5, 5 + res, res):
            for y in np.arange(-3, 3 + res, res):
                m_val = metric_field(np.array([x, y, 0]))
                color = interpolate_color(DARK_BLUE, YELLOW, m_val)
                rect = Rectangle(
                    width=res, height=res, 
                    fill_color=color, fill_opacity=0.3, 
                    stroke_width=0
                ).move_to([x, y, 0])
                heatmap.add(rect)

        self.play(Write(title), Create(grid))
        self.play(FadeIn(heatmap, run_time=2))

        tensors = VGroup()
        for x in np.linspace(-5, 5, 11):
            for y in np.linspace(-3, 3, 7):
                pos = np.array([x, y, 0])
                m_val = metric_field(pos)
                ellipse = Ellipse(
                    width=0.8 * (1 - m_val + 0.2),
                    height=0.5 * (1 - m_val + 0.2),
                    stroke_width=2,
                    color=RED_A if m_val < 0.5 else YELLOW_A
                ).move_to(pos)
                if np.linalg.norm(pos) > 0.1: 
                    ellipse.rotate(np.arctan2(y, x))
                tensors.add(ellipse)

        self.play(LaggedStartMap(Create, tensors, lag_ratio=0.05), run_time=3)
        self.wait()

        scanner_dot = Dot(color=WHITE).move_to([-4, 2, 0])
        local_tensor = always_redraw(lambda: 
            Ellipse(
                width=1.2 * (1 - metric_field(scanner_dot.get_center())),
                height=0.7 * (1 - metric_field(scanner_dot.get_center())),
                color=PURE_RED,
                stroke_width=5
            ).move_to(scanner_dot.get_center())
        )
        
        label_g = always_redraw(lambda:
            MathTex(r"g(z)_{local}", color=PURE_RED, font_size=24)
            .next_to(local_tensor, UP, buff=0.2)
        )

        self.play(FadeIn(scanner_dot), Create(local_tensor), Write(label_g))
        
        path = ArcBetweenPoints(np.array([-4, 2, 0]), np.array([4, -2, 0]), angle=-TAU/4)
        self.play(MoveAlongPath(scanner_dot, path), run_time=4, rate_func=linear)
        self.wait()

        formula = MathTex(
            r"ds^2 = \sum_{i,j} g_{ij} dz^i dz^j",
            font_size=40
        ).to_edge(DOWN, buff=0.5)
        
        bg_rect = SurroundingRectangle(formula, color=BLUE_A, fill_color=BLACK, fill_opacity=0.8)
        
        self.play(Create(bg_rect), Write(formula))
        self.wait(2)