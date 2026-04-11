from manim import *
import numpy as np

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