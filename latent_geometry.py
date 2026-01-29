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
            "La línea recta sale del manifold,\nla geodésica permanece en él",
            font_size=26,
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
        
