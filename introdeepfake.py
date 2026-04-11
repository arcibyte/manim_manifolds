from manim import *
import numpy as np
from palette import *

class IntroDeepfake(Scene):

    def setup(self):
        self.camera.background_color = BG

    def _axes(self):
        ax = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            x_length=10, y_length=6,
            axis_config={
                "stroke_color": DIM,
                "stroke_width": 1.0,
                "include_tip": True,
                "tip_length": 0.16,
                "include_numbers": False,
            },
        )
        lx = MathTex(r"z_1", font_size=20, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.12)
        ly = MathTex(r"z_2", font_size=20, color=DIM).next_to(ax.y_axis, UP,    buff=0.12)
        return ax, VGroup(lx, ly)

    def _dot(self, ax, px, py, color, radius=0.09, glow=False):
        pos = ax.c2p(px, py)
        d = Dot(pos, radius=radius, color=color)
        if glow:
            halo = Circle(radius=radius * 2.2, color=color, stroke_width=1.5)
            halo.set_fill(color, opacity=0.12).move_to(pos)
            return VGroup(halo, d)
        return d

    def _boundary_curve(self, ax, color=BOUNDARY_C):
        return ParametricFunction(
            lambda t: ax.c2p(t, 0.55 * np.sin(0.9 * t) + 0.22 * np.cos(1.9 * t)),
            t_range=[-4.8, 4.8, 0.02],
            color=color,
            stroke_width=2.2,
        ).set_stroke(opacity=0.9)

    def _region_fill(self, ax, side="left", color=REAL_C):
        xs = -5.0 if side == "left" else 0.0
        xe = 0.0  if side == "left" else 5.0
        rect = Rectangle(
            width=abs(xe - xs) * ax.x_length / 10,
            height=ax.y_length,
            fill_color=color,
            fill_opacity=0.06,
            stroke_width=0,
        )
        rect.move_to(ax.c2p((xs + xe) / 2, 0))
        return rect

    def _mono_text(self, s, size=18, color=MUTED):
        return Text(s, font="Courier New", font_size=size, color=color)

    def construct(self):
        self._block1_latent_space()
        self._block2_detector()
        self._block3_attack()
        self._block4_question()
    
    def _block1_latent_space(self):
        ax, ax_labels = self._axes()
        r_fill = self._region_fill(ax, "left",  REAL_C)
        f_fill = self._region_fill(ax, "right", FAKE_C)

        space_tag = self._mono_text("espacio latente  ℝⁿ", 14, DIM)
        space_tag.to_corner(UL, buff=0.45)

        self.play(
            Create(ax), Write(ax_labels),
            FadeIn(r_fill), FadeIn(f_fill),
            FadeIn(space_tag, shift=RIGHT * 0.15),
            run_time=1.3,
        )

        tag_r = Text("REAL",     font="Courier New", font_size=13, color=REAL_C, weight=BOLD)
        tag_f = Text("DEEPFAKE", font="Courier New", font_size=13, color=FAKE_C, weight=BOLD)
        tag_r.move_to(ax.c2p(-3.6, -2.6))
        tag_f.move_to(ax.c2p( 3.4, -2.6))
        self.play(FadeIn(tag_r), FadeIn(tag_f), run_time=0.5)

        real_coords = [
            (-2.5, 1.1), (-1.8, 0.4), (-2.2, -0.9),
            (-3.1, -0.1), (-1.2, 1.8), (-2.7, 0.8),
            (-1.6, -1.6), (-3.3, 1.2),
        ]
        z_star_coord = real_coords[1] 

        fake_coords = [
            (2.0, 0.9), (2.9, 0.2), (1.7, -1.1),
            (3.0, -0.6), (2.4, 1.9), (1.3, 0.4),
            (3.0, 1.4), (2.2, -0.3),
        ]

        real_dots = VGroup(*[
            self._dot(ax, px, py, REAL_C)
            for i, (px, py) in enumerate(real_coords) if i != 1
        ])
        fake_dots = VGroup(*[self._dot(ax, px, py, FAKE_C) for px, py in fake_coords])

        z_star = self._dot(ax, *z_star_coord, REAL_C, radius=0.10, glow=True)
        z_label = MathTex(r"z^*", font_size=22, color=REAL_C)
        z_label.next_to(z_star, UP + RIGHT * 0.3, buff=0.10)

        self.play(
            LaggedStartMap(GrowFromCenter, real_dots, lag_ratio=0.12),
            LaggedStartMap(GrowFromCenter, fake_dots, lag_ratio=0.12),
            run_time=1.6,
        )
        self.play(GrowFromCenter(z_star), Write(z_label), run_time=0.7)
        self.wait(0.6)

        self._ax        = ax
        self._ax_lbl    = ax_labels
        self._r_fill    = r_fill
        self._f_fill    = f_fill
        self._real_dots = real_dots
        self._fake_dots = fake_dots
        self._z_star    = z_star
        self._z_label   = z_label
        self._z_coord   = z_star_coord
        self._space_tag = space_tag
        self._tag_r     = tag_r
        self._tag_f     = tag_f


    def _block2_detector(self):
        ax = self._ax
        boundary = self._boundary_curve(ax)

        boundary_label = self._mono_text("D(z) = 0.5  ←  frontera del detector", 13, BOUNDARY_C)
        boundary_label.to_corner(UR, buff=0.40)

        self.play(Create(boundary), run_time=2.0)
        self.play(FadeIn(boundary_label, shift=LEFT * 0.15), run_time=0.6)
        self.wait(0.3)

        check = self._mono_text("✓  D(z*) > 0.5  →  clasificado como REAL", 14, REAL_C)
        check_bg = SurroundingRectangle(
            check, color=REAL_C, buff=0.18,
            fill_color=BG, fill_opacity=0.92,
            stroke_width=0.8, corner_radius=0.12,
        ).set_stroke(opacity=0.5)
        check_group = VGroup(check_bg, check).to_corner(DL, buff=0.45)

        self.play(FadeIn(check_group, shift=UP * 0.12), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(check_group), run_time=0.4)

        self._boundary  = boundary
        self._bound_lbl = boundary_label

    def _block3_attack(self):
        ax = self._ax
        z_src = self._z_coord
        z_dst = (0.85, 0.78)

        arrow = Arrow(
            ax.c2p(*z_src), ax.c2p(*z_dst),
            buff=0.10,
            color=GRAD_C,
            stroke_width=3.5,
            max_tip_length_to_length_ratio=0.22,
        )

        attack_lbl = Text(
            "Ataque adversarial",
            font="Courier New", font_size=14, color=GRAD_C, weight=BOLD,
        ).to_corner(UL, buff=0.45)

        self.play(
            FadeOut(self._space_tag),
            FadeIn(attack_lbl, shift=RIGHT * 0.15),
            GrowArrow(arrow),
            run_time=1.0,
        )

        formula = MathTex(
            r"\mathbf{z}_{t+1} = \mathbf{z}_t"
            r"- \alpha\,\nabla_{\!\mathcal{M}}\,D(\mathbf{z}_t)",
            font_size=24, color=GRAD_C,
        )
        formula_bg = SurroundingRectangle(
            formula, color=GRAD_C, buff=0.22,
            fill_color=BG, fill_opacity=0.95,
            stroke_width=0.8, corner_radius=0.12,
        ).set_stroke(opacity=0.5)
        formula_group = VGroup(formula_bg, formula)
        formula_group.next_to(arrow, DOWN + RIGHT * 0.5, buff=0.25)

        self.play(FadeIn(formula_group, shift=UP * 0.1), run_time=0.9)
        self.wait(0.5)

        z_star_old = self._z_star
        z_adv = self._dot(ax, *z_dst, FAKE_C, radius=0.10, glow=True)
        z_adv_label = MathTex(r"z_{\mathrm{adv}}", font_size=20, color=FAKE_C)
        z_adv_label.next_to(z_adv, UP + RIGHT * 0.3, buff=0.10)

        self.play(
            Transform(z_star_old, z_adv),
            Transform(self._z_label, z_adv_label),
            run_time=1.8,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.4)

        cross = self._mono_text(
            "✗  D(z_adv) < 0.5  →  clasificado como REAL  [error]",
            13, FAKE_C,
        )
        cross_bg = SurroundingRectangle(
            cross, color=FAKE_C, buff=0.18,
            fill_color=BG, fill_opacity=0.92,
            stroke_width=0.8, corner_radius=0.12,
        ).set_stroke(opacity=0.5)
        cross_group = VGroup(cross_bg, cross).to_corner(DL, buff=0.45)

        self.play(FadeIn(cross_group, shift=UP * 0.12), run_time=0.7)
        self.wait(0.8)

        paradox = Text(
            "La imagen sigue siendo visualmente idéntica\n"
            "— sólo cambió su posición en el espacio latente —",
            font="Courier New", font_size=16, color=WHITE,
            line_spacing=1.4, t2c={"espacio latente": MANIFOLD_C},
        )
        paradox_bg = SurroundingRectangle(
            paradox, color=GRAY_A, buff=0.8,
            fill_color="#0d0d20", fill_opacity=0.96,
            stroke_width=0.7, corner_radius=0.15,
        ).set_stroke(opacity=0.6)
        paradox_group = VGroup(paradox_bg, paradox).to_edge(DOWN, buff=0.40)

        self.play(FadeOut(self._bound_lbl), run_time=0.3)
        self.play(FadeIn(paradox_group, shift=UP * 0.12), run_time=1.0)
        self.wait(1.8)

        self.play(
            FadeOut(
                self._ax, self._ax_lbl,
                self._r_fill, self._f_fill,
                self._tag_r, self._tag_f,
                self._real_dots, self._fake_dots,
                self._boundary,
                z_star_old, self._z_label,
                arrow, formula_group,
                cross_group, paradox_group,
                attack_lbl,
            ),
            run_time=1.3,
        )

    def _block4_question(self):
        question = Text(
            "¿Cómo guía el cálculo vectorial\nese camino sobre el manifold?",
            font_size=36, weight=BOLD, color=WHITE,
            line_spacing=1.35,
            t2c={
                "cálculo vectorial": GRAD_C,
                "manifold":          MANIFOLD_C,
            },
        ).shift(UP * 0.9)

        self.play(Write(question), run_time=1.6)
        self.wait(0.4)

        pillar_data = [
            (GRAD_C,      "·  Gradiente proyectado sobre superficies curvas"),
            (BOUNDARY_C,  "·  Tensor métrico y distancias en el espacio latente"),
            (REAL_C,      "·  Geodésicas como caminos de energía mínima"),
        ]

        pillars = VGroup()
        for color, txt in pillar_data:
            line_accent = Line(ORIGIN, DOWN * 0.42, stroke_width=2.5, color=color)
            label = Text(txt, font="Courier New", font_size=15, color=MUTED)
            group = VGroup(line_accent, label).arrange(RIGHT, buff=0.22, aligned_edge=UP)
            pillars.add(group)

        pillars.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        pillars.next_to(question, DOWN, buff=0.55)

        self.play(
            LaggedStartMap(FadeIn, pillars, shift=RIGHT * 0.25, lag_ratio=0.4),
            run_time=1.8,
        )
        self.wait(2.8)

        self.play(
            FadeOut(question, shift=UP * 0.3),
            FadeOut(pillars,  shift=UP * 0.3),
            run_time=1.1,
        )
        self.wait(0.4)