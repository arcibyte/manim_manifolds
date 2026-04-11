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
