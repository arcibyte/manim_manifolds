from manim import *
import numpy as np

class StyleGAN(Scene):
    def construct(self):
        BG     = "#0d0d1a"
        ACCENT = "#7b61ff"
        GOLD   = "#f5c542"
        TEAL   = "#00d4aa"
        SOFT   = "#c9c9e3"
        RED    = "#ff6b6b"
        PINK   = "#ff79c6"
        self.camera.background_color = BG

        title  = Text("StyleGAN", font_size=60, color=ACCENT, weight=BOLD)
        sub    = Text("Modelos Generativos Avanzados", font_size=30, color=SOFT)
        sub.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP*0.3))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(sub))

        gan_title = Text("Base: GAN (Goodfellow et al., 2014)",
                         font_size=30, color=GOLD).to_edge(UP)
        self.play(Write(gan_title))

        gen_box  = RoundedRectangle(corner_radius=0.3, width=3, height=1.4,
                                    color=TEAL, stroke_width=2.5)
        gen_box.set_fill(TEAL, opacity=0.12).move_to([-3.5, 0, 0])
        gen_text = Text("Generador\nG", font_size=26, color=TEAL).move_to(gen_box)

        disc_box  = RoundedRectangle(corner_radius=0.3, width=3, height=1.4,
                                     color=RED, stroke_width=2.5)
        disc_box.set_fill(RED, opacity=0.12).move_to([3.5, 0, 0])
        disc_text = Text("Discriminador\nD", font_size=26, color=RED).move_to(disc_box)

        arrow_gd = Arrow(start=gen_box.get_right(), end=disc_box.get_left(),
                         color=SOFT, stroke_width=2.5, buff=0.15)
        img_label = Text("imagen\nfake", font_size=20, color=SOFT).next_to(arrow_gd, UP, buff=0.15)

        arrow_fb = CurvedArrow(disc_box.get_bottom(), gen_box.get_bottom(),
                               angle=-TAU/6, color=GOLD, stroke_width=2)
        fb_label = Text("retroalimentación\n(error)", font_size=18, color=GOLD)
        fb_label.next_to(arrow_fb, DOWN, buff=0.15)

        self.play(FadeIn(gen_box), Write(gen_text))
        self.play(FadeIn(disc_box), Write(disc_text))
        self.play(FadeIn(arrow_gd), FadeIn(img_label))
        self.play(FadeIn(arrow_fb), FadeIn(fb_label))
        self.wait(1.5)
        self.play(FadeOut(VGroup(gen_box, gen_text, disc_box, disc_text,
                                  arrow_gd, img_label, arrow_fb, fb_label, gan_title)))

        sg_title = Text("StyleGAN: espacio  W  y control de estilo",
                        font_size=30, color=ACCENT).to_edge(UP)
        self.play(Write(sg_title))

        # bloques del pipeline
        blocks = [
            ("z ∈ ℝⁿ",          "Ruido\nlatente",   SOFT,   [-5.2, 0, 0]),
            ("Mapping\nNetwork", "8 capas FC",        TEAL,   [-2.6, 0, 0]),
            ("w ∈ W",            "Espacio\nestilo",   GOLD,   [ 0.0, 0, 0]),
            ("Síntesis\nG",      "Control\npor capa", ACCENT, [ 2.8, 0, 0]),
            ("Imagen\nfinal",    "H×W×3",             PINK,   [ 5.4, 0, 0]),
        ]

        boxes, labels = VGroup(), VGroup()
        for i, (main, sub_t, col, pos) in enumerate(blocks):
            box = RoundedRectangle(corner_radius=0.25, width=2.3, height=1.3,
                                   color=col, stroke_width=2)
            box.set_fill(col, opacity=0.10).move_to(pos)
            txt = Text(main, font_size=20, color=col).move_to(box)
            boxes.add(box)
            labels.add(txt)

        self.play(LaggedStartMap(FadeIn, boxes, lag_ratio=0.15), run_time=2)
        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.15), run_time=1.5)

        arrows = VGroup(*[
            Arrow(boxes[i].get_right(), boxes[i+1].get_left(),
                  color=SOFT, stroke_width=2, buff=0.1)
            for i in range(len(blocks)-1)
        ])
        self.play(LaggedStartMap(FadeIn, arrows, lag_ratio=0.15))
        self.wait(1)

        self.play(FadeOut(VGroup(boxes, labels, arrows, sg_title)))

        attr_title = Text("Control fino de atributos visuales",
                          font_size=34, color=GOLD).to_edge(UP)
        self.play(Write(attr_title))

        w_center = Dot(point=ORIGIN, radius=0.18, color=GOLD)
        w_lbl    = MathTex(r"\mathbf{w}", font_size=42, color=GOLD).next_to(w_center, UP, buff=0.2)
        self.play(FadeIn(w_center), Write(w_lbl))

        attributes = [
            ("Edad",         UP    * 2.2,               TEAL),
            ("Iluminación",  UP    * 1.5 + RIGHT * 2.5, ACCENT),
            ("Expresión",    RIGHT * 2.8,                PINK),
            ("Color cabello",DOWN  * 1.5 + RIGHT * 2.5, RED),
            ("Estructura\nfacial", DOWN * 2.2,           SOFT),
            ("Género",       DOWN  * 1.5 + LEFT * 2.5,  GOLD),
            ("Pose",         LEFT  * 2.8,                TEAL),
        ]

        for attr, direction, col in attributes:
            end_pt = direction
            arr = Arrow(ORIGIN, end_pt, color=col, stroke_width=2.5, buff=0.18)
            lbl = Text(attr, font_size=20, color=col).next_to(end_pt, direction/np.linalg.norm(direction)*0.5)
            self.play(FadeIn(arr), FadeIn(lbl), run_time=0.6)

        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])

        compare_title = Text("¿Por qué el espacio W?", font_size=38, color=ACCENT).to_edge(UP)
        self.play(Write(compare_title))

        z_box = RoundedRectangle(corner_radius=0.3, width=4.5, height=3.5,
                                 color=RED, stroke_width=2)
        z_box.set_fill(RED, opacity=0.07).move_to([-3.2, -0.3, 0])
        z_head = Text("Espacio Z", font_size=26, color=RED, weight=BOLD).next_to(z_box, UP, buff=0.1)
        z_pts = VGroup(*[
            Dot(point=[np.random.uniform(-2.0,-0.5),
                       np.random.uniform(-1.5, 1.5), 0],
                radius=0.06, color=RED)
            for _ in range(30)
        ])
        z_note = Text("Entrelazado\n(atributos mezclados)", font_size=20, color=RED)
        z_note.move_to(z_box)

        w_box = RoundedRectangle(corner_radius=0.3, width=4.5, height=3.5,
                                 color=GOLD, stroke_width=2)
        w_box.set_fill(GOLD, opacity=0.07).move_to([3.2, -0.3, 0])
        w_head = Text("Espacio W", font_size=26, color=GOLD, weight=BOLD).next_to(w_box, UP, buff=0.1)

        # W: puntos mas ordenados en clusters
        w_clusters = [
            ([2.0, 0.8, 0], TEAL,   "jóvenes"),
            ([3.2, 0.8, 0], ACCENT, "adultos"),
            ([4.4, 0.8, 0], PINK,   "mayores"),
            ([2.6,-0.5, 0], GOLD,   "sonrientes"),
            ([3.8,-0.5, 0], SOFT,   "serios"),
        ]
        w_pts_group = VGroup()
        for center, col, _ in w_clusters:
            for _ in range(6):
                w_pts_group.add(Dot(
                    point=[center[0]+np.random.randn()*0.18,
                           center[1]+np.random.randn()*0.18, 0],
                    radius=0.06, color=col
                ))
        w_note = Text("Desacoplado\n(atributos independientes)", font_size=20, color=GOLD)
        w_note.move_to(w_box)

        self.play(FadeIn(z_box), Write(z_head), FadeIn(z_pts))
        self.play(FadeIn(z_note))
        self.play(FadeIn(w_box), Write(w_head), FadeIn(w_pts_group))
        self.play(FadeIn(w_note))
        self.wait(2)

        # seccion de deepfakes comparacion
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        manifold_title = Text("StyleGAN y el manifold de rostros",
                              font_size=34, color=ACCENT).to_edge(UP)
        self.play(Write(manifold_title))

        conclusion_lines = [
            ("Cada imagen StyleGAN proviene de un punto  w ∈ W", SOFT),
            ("Los rostros plausibles forman un manifold en W",    GOLD),
            ("La geometría de ese manifold determina\nla calidad y detectabilidad del deepfake", TEAL),
            ("Explotar esa geometría → ataque adversarial exitoso", RED),
        ]
        prev = manifold_title
        for line, col in conclusion_lines:
            mob = Text(line, font_size=25, color=col, line_spacing=1.3)
            mob.next_to(prev, DOWN, buff=0.5)
            self.play(FadeIn(mob, shift=UP*0.2), run_time=1)
            self.wait(0.8)
            prev = mob

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])