from manim import *
import numpy as np

class LatentGeometry(Scene):
    def construct(self):
        BG       = "#0d0d1a"
        ACCENT   = "#7b61ff"
        GOLD     = "#f5c542"
        TEAL     = "#00d4aa"
        SOFT     = "#c9c9e3"
        self.camera.background_color = BG

        title = Text("El Espacio Latente", font_size=52, color=ACCENT, weight=BOLD)
        subtitle = Text("Un mapa abstracto de rostros posibles", font_size=28, color=SOFT)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP*0.3))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        #nube de puntos
        axes_label = Text("Espacio latente  ℝⁿ", font_size=32, color=SOFT).to_edge(UP)
        self.play(Write(axes_label))

        np.random.seed(42)
        n_dots = 120
        positions = np.random.randn(n_dots, 2) * 2.8
        color_choices = [ACCENT, TEAL]
        dots = VGroup(*[
            Dot(point=[x, y, 0], radius=0.045,
                color=color_choices[np.random.randint(0, 2)])
            for x, y in positions
        ])
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.03), run_time=2)
        self.wait(0.5)

        region_label = Text("Región estructurada\n(variedad diferenciable)",
                            font_size=24, color=GOLD).to_corner(DR)
        ellipse = Ellipse(width=5.5, height=2.8, color=GOLD, stroke_width=2.5)
        ellipse.set_fill(GOLD, opacity=0.07)

        self.play(Create(ellipse), Write(region_label), run_time=1.5)
        self.wait(0.5)

        inside = VGroup(*[
            Dot(point=[x, y, 0], radius=0.07, color=GOLD)
            for x, y in positions
            if (x/2.75)**2 + (y/1.4)**2 < 1
        ])
        self.play(inside.animate.set_color(GOLD).scale(1.4), run_time=1)
        self.wait(0.8)

        #punto w → IMAGEN (analogía)
        chosen = Dot(point=[0.6, 0.3, 0], radius=0.15, color="#ff6b6b")
        w_label = MathTex(r"\mathbf{w}", color="#ff6b6b", font_size=38)
        w_label.next_to(chosen, UR, buff=0.15)

        arrow_img = Arrow(start=[0.6, 0.3, 0], end=[3.5, 1.8, 0],
                          color=TEAL, stroke_width=3, buff=0.15)
        face_box = RoundedRectangle(corner_radius=0.2, width=1.6, height=1.6,
                                    color=TEAL, stroke_width=2)
        face_box.move_to([4.1, 1.8, 0])
        face_box.set_fill(TEAL, opacity=0.12)
        face_text = Text("G(w)\nrostro", font_size=20, color=TEAL).move_to(face_box)

        self.play(FadeIn(chosen), Write(w_label))
        self.play(GrowArrow(arrow_img), FadeIn(face_box), Write(face_text))
        self.wait(1)

        directions = [
            ([-1.0, 0, 0], "← envejecer"),
            ([ 0, 0.8, 0], "↑ cambiar expresión"),
            ([ 0.7,-0.4, 0], "→ color de cabello"),
        ]
        move_label = Text("Moverse en el espacio latente\ncambia atributos del rostro",
                          font_size=24, color=SOFT).to_corner(DL)
        self.play(Write(move_label))

        dot_copy = chosen.copy().set_color(ACCENT)
        self.add(dot_copy)
        for shift, desc in directions:
            desc_mob = Text(desc, font_size=22, color=GOLD).next_to(move_label, DOWN, buff=0.15)
            self.play(
                dot_copy.animate.shift(shift),
                FadeIn(desc_mob, shift=UP*0.2),
                run_time=1.2
            )
            self.wait(0.4)
            self.play(FadeOut(desc_mob))

        self.wait(1)

        # funcion generadora  G : ℝⁿ → ℝ^(H×W×3)
        self.play(
            FadeOut(dots), FadeOut(inside), FadeOut(ellipse),
            FadeOut(chosen), FadeOut(dot_copy), FadeOut(w_label),
            FadeOut(arrow_img), FadeOut(face_box), FadeOut(face_text),
            FadeOut(move_label), FadeOut(region_label), FadeOut(axes_label),
        )

        func_eq = MathTex(
            r"G : \mathbb{R}^n \;\longrightarrow\; \mathbb{R}^{H \times W \times 3}",
            font_size=54, color=ACCENT
        )
        desc_eq = Text(
            "Cada vector latente  w  se mapea a una imagen RGB completa",
            font_size=26, color=SOFT
        ).next_to(func_eq, DOWN, buff=0.5)

        self.play(Write(func_eq), run_time=1.8)
        self.play(FadeIn(desc_eq, shift=UP*0.3))
        self.wait(2)

        closing = Text(
            "Comprender la geometría de este espacio\nes clave para detectar deepfakes",
            font_size=30, color=GOLD, line_spacing=1.4
        )
        self.play(
            func_eq.animate.shift(UP*1.2).scale(0.75),
            desc_eq.animate.shift(UP*0.8).scale(0.75),
        )
        closing.next_to(desc_eq, DOWN, buff=0.6)
        self.play(Write(closing), run_time=2)
        self.wait(2.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])