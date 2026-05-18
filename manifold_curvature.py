from manim import *
import numpy as np
from palette import (
    BG, REAL_C, FAKE_C, BOUNDARY_C, GRAD_C,
    MUTED, DIM, MANIFOLD_C, REAL_PATH, WRONG_PATH,
)

class ManifoldCurvature(Scene):

    def construct(self):
        self.camera.background_color = BG

        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": DIM, "stroke_width": 0.8, "stroke_opacity": 0.25},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=3,
        )
        self.add(grid)

        # ── Título ─────────────────────────────────────────────────────
        title = Text("CURVATURA DEL MANIFOLD", font_size=28, weight=BOLD, color=MANIFOLD_C, font="monospace").to_edge(UP, buff=0.26)
        subtitle = Text("por qué la curvatura produce artefactos", font_size=15, color=MUTED, slant=ITALIC).next_to(title, DOWN, buff=0.07)
        title_line = Line(LEFT * 2.8, RIGHT * 2.8, stroke_color=MANIFOLD_C, stroke_width=0.8, stroke_opacity=0.35).next_to(subtitle, DOWN, buff=0.08)
        self.play(Write(title, run_time=0.9), FadeIn(subtitle, shift=UP * 0.08), Create(title_line))

        #  campo de curvatura (κ) 
        def kappa(x, y):
            return np.exp(-0.3 * x**2) * (1 + 0.6 * np.cos(1.1 * y))

        heatmap = VGroup()
        res = 0.30
        for x in np.arange(-6, 6 + res, res):
            for y in np.arange(-3.5, 3.5 + res, res):
                v = np.clip(kappa(x, y) / 1.6, 0, 1)
                color = interpolate_color(ManimColor(DIM), ManimColor(MANIFOLD_C), v)
                rect = Rectangle(width=res, height=res, fill_color=color,
                                  fill_opacity=v * 0.58, stroke_width=0).move_to([x, y, 0])
                heatmap.add(rect)

        self.play(FadeIn(heatmap, lag_ratio=0.001, run_time=1.5))

        manifold = FunctionGraph(
            lambda x: 0.55 * np.sin(0.9 * x) - 0.2,
            x_range=[-5.8, 5.8],
            color=MANIFOLD_C,
            stroke_width=2.8,
            stroke_opacity=0.9,
        )
        manifold_label = Text("manifold M", font_size=13, color=MANIFOLD_C, slant=ITALIC).move_to([5.0, 2.8, 0])
        self.play(Create(manifold, run_time=1.3), FadeIn(manifold_label))

        high_k_zone = Ellipse(width=2.8, height=1.8, color=FAKE_C, stroke_width=1.2, stroke_opacity=0.55)
        high_k_zone.set_fill(FAKE_C, opacity=0.08)
        high_k_zone.move_to([-0.2, -0.2, 0])
        high_k_label = Text("alta κ\nartefactos", font_size=13, color=FAKE_C, slant=ITALIC).move_to([-0.2, 1.2, 0])

        self.play(Create(high_k_zone), FadeIn(high_k_label))

        low_k_zone = Ellipse(width=2.2, height=1.4, color=REAL_C, stroke_width=1.0, stroke_opacity=0.45)
        low_k_zone.set_fill(REAL_C, opacity=0.07)
        low_k_zone.move_to([4.2, 0.3, 0])
        low_k_label = Text("baja κ\nmovimiento suave", font_size=13, color=REAL_C, slant=ITALIC).move_to([4.2, 1.4, 0])

        self.play(Create(low_k_zone), FadeIn(low_k_label))
        self.wait(0.4)

        p_start = np.array([-1.8, 0.55 * np.sin(0.9 * -1.8) - 0.2, 0])
        p_end   = np.array([ 1.8, 0.55 * np.sin(0.9 *  1.8) - 0.2, 0])

        eucl_step = Arrow(p_start, p_end, buff=0.05, color=WRONG_PATH, stroke_width=2.5,
                           max_tip_length_to_length_ratio=0.2)
        eucl_label = Text("paso euclídeo\n(off-manifold)", font_size=13, color=WRONG_PATH).move_to([-0.0, -1.5, 0])

        off_pt = (p_start + p_end) / 2
        off_dot = Dot(off_pt, color=WRONG_PATH, radius=0.12)

        self.play(GrowArrow(eucl_step), FadeIn(eucl_label))
        self.play(FadeIn(off_dot, scale=1.3))
        self.wait(0.3)

        geo_pts = [
            np.array([x, 0.55 * np.sin(0.9 * x) - 0.2, 0])
            for x in np.linspace(-1.8, 1.8, 40)
        ]
        geo_path = VMobject(color=REAL_PATH, stroke_width=3.0)
        geo_path.set_points_as_corners(geo_pts)
        geo_label = Text("geodésica\n(on-manifold)", font_size=13, color=REAL_PATH).move_to([-0.0, -2.6, 0])

        self.play(Create(geo_path, run_time=1.4), FadeIn(geo_label))
        self.wait(0.5)

        def osculating_circle(x0, radius, color, alpha):
            y0 = 0.55 * np.sin(0.9 * x0) - 0.2
            center = np.array([x0, y0 + radius, 0])
            return Circle(radius=radius, color=color, stroke_width=1.2, stroke_opacity=alpha).move_to(center)

        osc_high = osculating_circle(-0.2, 0.55, FAKE_C, 0.65)
        osc_low  = osculating_circle( 4.2, 2.20, REAL_C, 0.50)

        self.play(Create(osc_high), Create(osc_low))
        self.wait(0.3)

        # formula de curvatura gaussiana 
        formula = MathTex(
            r"\kappa(z) = \frac{|f''(z)|}{(1 + f'(z)^2)^{3/2}}",
            font_size=34, color=MANIFOLD_C,
        ).to_edge(DOWN, buff=0.52)

        formula_bg = RoundedRectangle(
            corner_radius=0.12, width=formula.width + 0.65, height=formula.height + 0.46,
            fill_color=BG, fill_opacity=0.93, stroke_color=MANIFOLD_C, stroke_width=0.9, stroke_opacity=0.55,
        ).move_to(formula)

        self.play(FadeIn(formula_bg), Write(formula, run_time=1.8))
        self.wait(2.8)

        self.play(FadeOut(*self.mobjects), run_time=1.6)