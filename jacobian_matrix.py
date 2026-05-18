from manim import *
import numpy as np

class JacobianMatrix(Scene):
    def construct(self):
        BG     = "#0d0d1a"
        ACCENT = "#7b61ff"
        GOLD   = "#f5c542"
        TEAL   = "#00d4aa"
        SOFT   = "#c9c9e3"
        RED    = "#ff6b6b"
        self.camera.background_color = BG

        title = Text("La Matriz Jacobiana", font_size=52, color=ACCENT, weight=BOLD)
        sub   = Text("Cómo cada componente latente afecta la imagen generada",
                     font_size=26, color=SOFT)
        sub.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP*0.3))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(sub))

        partial_title = Text("Derivada parcial  →  cambio infinitesimal",
                             font_size=30, color=GOLD).to_edge(UP)
        self.play(Write(partial_title))

        partial_eq = MathTex(
            r"\frac{\partial G_j}{\partial w_i}",
            r"= \lim_{\varepsilon \to 0}",
            r"\frac{G_j(w + \varepsilon\, e_i) - G_j(w)}{\varepsilon}",
            font_size=46
        )
        partial_eq.set_color_by_tex(r"\partial G_j", TEAL)
        partial_eq.set_color_by_tex(r"\partial w_i", RED)
        partial_eq[1].set_color(SOFT)
        partial_eq[2].set_color(SOFT)

        meaning = Text(
            "Cuánto cambia el píxel  j  de la imagen\n"
            "cuando se perturba la componente  i  del vector latente",
            font_size=24, color=SOFT, line_spacing=1.3
        ).next_to(partial_eq, DOWN, buff=0.5)

        self.play(Write(partial_eq), run_time=2)
        self.play(FadeIn(meaning, shift=UP*0.2))
        self.wait(2)
        self.play(FadeOut(partial_eq), FadeOut(meaning), FadeOut(partial_title))

        #construccion de la jacobiana
        jac_title = Text("Construcción de  JG(w)", font_size=34, color=ACCENT).to_edge(UP)
        self.play(Write(jac_title))

        col_labels = VGroup(*[
            MathTex(rf"w_{i}", font_size=30, color=RED)
            for i in range(1, 5)
        ]).arrange(RIGHT, buff=1.05).move_to([1.5, 1.5, 0])

        row_labels = VGroup(*[
            MathTex(rf"G_{j}", font_size=30, color=TEAL)
            for j in range(1, 5)
        ]).arrange(DOWN, buff=0.68).move_to([-1.0, 0.1, 0])

        self.play(LaggedStartMap(FadeIn, col_labels, lag_ratio=0.15),
                  LaggedStartMap(FadeIn, row_labels, lag_ratio=0.15))

        # Celdas de la matriz
        cells = VGroup()
        cell_mobs = []
        for j in range(4):
            for i in range(4):
                cell = MathTex(
                    rf"\frac{{\partial G_{j+1}}}{{\partial w_{i+1}}}",
                    font_size=22, color=SOFT
                )
                cell.move_to([0.4 + i*1.1, 0.7 - j*0.72, 0])
                cells.add(cell)
                cell_mobs.append(cell)

        self.play(LaggedStartMap(FadeIn, cells, lag_ratio=0.04), run_time=2.5)
        self.wait(0.5)

        bracket_left  = MathTex(r"\Bigl[", font_size=90, color=ACCENT).move_to([-0.55, 0.1, 0])
        bracket_right = MathTex(r"\Bigr]", font_size=90, color=ACCENT).move_to([ 4.7,  0.1, 0])
        jg_label      = MathTex(r"J_G(w) =", font_size=38, color=ACCENT).next_to(bracket_left, LEFT, buff=0.3)

        self.play(FadeIn(bracket_left), FadeIn(bracket_right), Write(jg_label))
        self.wait(1.5)

        #resaltado de columna
        col_highlight = SurroundingRectangle(
            VGroup(*[cell_mobs[j*4 + 1] for j in range(4)]),
            color=GOLD, stroke_width=3, buff=0.12
        )
        col_meaning = Text(
            "Esta columna describe\ncómo w₂ afecta TODOS los píxeles",
            font_size=22, color=GOLD
        ).to_corner(DR)

        self.play(Create(col_highlight), Write(col_meaning))
        self.wait(2)
        self.play(FadeOut(col_highlight), FadeOut(col_meaning))

        # M(w) = JᵀJ
        self.play(
            FadeOut(cells), FadeOut(col_labels), FadeOut(row_labels),
            FadeOut(bracket_left), FadeOut(bracket_right), FadeOut(jg_label),
            FadeOut(jac_title)
        )

        metric_title = Text("Métrica Riemanniana", font_size=40, color=ACCENT).to_edge(UP)
        self.play(Write(metric_title))

        metric_eq = MathTex(
            r"M(w) = J_G^\top(w)\, J_G(w)",
            font_size=56, color=GOLD
        )
        metric_desc = Text(
            "Captura la geometría intrínseca del manifold\n"
            "en cada punto  w  del espacio latente",
            font_size=26, color=SOFT, line_spacing=1.4
        ).next_to(metric_eq, DOWN, buff=0.6)

        self.play(Write(metric_eq), run_time=1.8)
        self.play(FadeIn(metric_desc, shift=UP*0.2))
        self.wait(2)

        # descomposición  JᵀJ
        jtj_visual = VGroup(
            MathTex(r"J_G^\top", font_size=46, color=TEAL),
            MathTex(r"\times", font_size=36, color=SOFT),
            MathTex(r"J_G", font_size=46, color=RED),
            MathTex(r"=", font_size=36, color=SOFT),
            MathTex(r"M(w)", font_size=46, color=GOLD),
        ).arrange(RIGHT, buff=0.4).next_to(metric_desc, DOWN, buff=0.7)

        self.play(LaggedStartMap(FadeIn, jtj_visual, lag_ratio=0.2), run_time=1.5)
        self.wait(1)

        note = Text(
            "M(w) mide distancias y ángulos REALES sobre el manifold\n"
            "→ base del descenso de gradiente geodésico",
            font_size=22, color=TEAL, line_spacing=1.3
        ).next_to(jtj_visual, DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP*0.2))
        self.wait(2.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        closing = Text(
            "La Jacobiana conecta el espacio latente\ncon la geometría real de las imágenes",
            font_size=34, color=ACCENT, line_spacing=1.5
        )
        self.play(Write(closing), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(closing))