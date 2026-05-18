from manim import *
import numpy as np
from palette import *

#funciones matematicas
def D(x, y):
    val = -0.18 * ((x + 1.2)**2 + (y - 0.4)**2) + 1.1
    return 1.0 / (1.0 + np.exp(-3.5 * val))


def grad_D(x, y, eps=1e-4):
    dx = (D(x + eps, y) - D(x - eps, y)) / (2 * eps)
    dy = (D(x, y + eps) - D(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])


def surface_z(x, y):
    # z = 0.25·sin(1.2x)·cos(1.0y)
    return 0.25 * np.sin(1.2 * x) * np.cos(1.0 * y)


def normal_M(x, y, eps=1e-4):
    fx = (surface_z(x + eps, y) - surface_z(x - eps, y)) / (2 * eps)
    fy = (surface_z(x, y + eps) - surface_z(x, y - eps)) / (2 * eps)
    n = np.array([-fx, -fy, 1.0])
    return n / np.linalg.norm(n)


def proj_tangent(gx, gy, x, y):
    n = normal_M(x, y)
    g3 = np.array([gx, gy, 0.0])
    proj = g3 - np.dot(g3, n) * n
    return proj[0], proj[1]


class GradienteAdversarial(Scene):

    def setup(self):
        self.camera.background_color = BG

    def _make_axes(self):
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=9.5, y_length=5.8,
            axis_config={
                "stroke_color": DIM,
                "stroke_width": 0.9,
                "include_tip": True,
                "tip_length": 0.15,
                "include_numbers": False,
            },
        )
        lx = MathTex(r"z_1", font_size=19, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.1)
        ly = MathTex(r"z_2", font_size=19, color=DIM).next_to(ax.y_axis, UP,    buff=0.1)
        return ax, VGroup(lx, ly)

    def _mono(self, s, size=15, color=MUTED):
        return Text(s, font="Courier New", font_size=size, color=color)

    def _hud_box(self, mob, border_color=GRAD_C):
        bg = SurroundingRectangle(
            mob, color=border_color, buff=0.20,
            fill_color="#0d0d22", fill_opacity=0.95,
            stroke_width=0.8, corner_radius=0.12,
        ).set_stroke(opacity=0.55)
        return VGroup(bg, mob)

    def construct(self):
        self._block0_title()
        ax, ax_lbl = self._make_axes()
        self._block1_heatmap(ax, ax_lbl)
        self._block2_gradient_field(ax)
        self._block3_tangent_projection(ax)
        self._block4_descent(ax)
        self._block5_formula(ax)

    def _block0_title(self):
        tag = self._mono("03 / gradiente adversarial", 13, DIM)
        tag.to_corner(UL, buff=0.4)

        title = Text(
            "Gradiente sobre el Manifold",
            font_size=38, weight=BOLD, color=WHITE,
        ).set_stroke(WHITE, width=0.3, opacity=0.35)

        sub = Text(
            "cómo el descenso de gradiente proyectado\nguía la búsqueda de imágenes adversariales",
            font="Courier New", font_size=16, color=MUTED,
            line_spacing=1.4,
        ).next_to(title, DOWN, buff=0.30)

        accent = Line(LEFT * 2.8, RIGHT * 2.8, stroke_width=0.5, color=GRAD_C)
        accent.set_stroke(opacity=0.4).next_to(sub, DOWN, buff=0.35)

        header = VGroup(title, sub, accent).move_to(ORIGIN)

        self.play(FadeIn(tag, shift=RIGHT * 0.1), run_time=0.5)
        self.play(Write(title), run_time=1.0)
        self.play(
            FadeIn(sub,    shift=UP * 0.12),
            FadeIn(accent, shift=UP * 0.12),
            run_time=0.8,
        )
        self.wait(1.4)
        self.play(FadeOut(header), FadeOut(tag), run_time=0.7)

    def _block1_heatmap(self, ax, ax_lbl):
        self.play(Create(ax), Write(ax_lbl), run_time=1.0)

        lbl_d = self._mono("D(z)  —  función discriminadora", 13, BOUNDARY_C)
        lbl_d.to_corner(UL, buff=0.40)
        self.play(FadeIn(lbl_d, shift=RIGHT * 0.1), run_time=0.5)

        res = 0.35
        cells = VGroup()
        xs = np.arange(-3.8, 3.8 + res, res)
        ys = np.arange(-2.8, 2.8 + res, res)

        for x in xs:
            for y in ys:
                val = D(x, y)
                # val ≈ 1 → verde (REAL),  val ≈ 0 → rojo (FAKE)
                color = interpolate_color(ManimColor(FAKE_C), ManimColor(REAL_C), val)
                w = abs(ax.c2p(x + res, y)[0] - ax.c2p(x, y)[0])
                h = abs(ax.c2p(x, y + res)[1] - ax.c2p(x, y)[1])
                cell = Rectangle(
                    width=w, height=h,
                    fill_color=color, fill_opacity=0.30,
                    stroke_width=0,
                ).move_to(ax.c2p(x + res / 2, y + res / 2))
                cells.add(cell)

        self.play(FadeIn(cells, lag_ratio=0.002), run_time=2.2)
        self.wait(0.3)

        # curva de nivel D(z) = 0.5
        boundary = ParametricFunction(
            lambda t: ax.c2p(
                t,
                # despejar y numericamente: buscamos y tal que D(t,y)=0.5
                # D(t,y)=0.5 ⟺ val=0 ⟺ -0.18((t+1.2)²+(y-0.4)²)+1.1=0
                # ⟺ (y-0.4)² = (1.1/0.18) - (t+1.2)²
                0.4 + np.sqrt(max(0, 1.1 / 0.18 - (t + 1.2) ** 2))
                if abs(t + 1.2) < np.sqrt(1.1 / 0.18) else 0,
            ),
            t_range=[-4 + 1.2 - np.sqrt(1.1/0.18) + 0.05,
                     -1.2 + np.sqrt(1.1/0.18) - 0.05, 0.03],
            color=BOUNDARY_C, stroke_width=2.0,
        ).set_stroke(opacity=0.85)

        # circulo analitico exacto de la curva de nivel
        # D=0.5 ⟺ (x+1.2)²+(y-0.4)² = 1.1/0.18
        r_level = np.sqrt(1.1 / 0.18)
        boundary_circle = Circle(
            radius=ax.x_length / 8 * r_level,
            color=BOUNDARY_C, stroke_width=2.0,
        ).set_stroke(opacity=0.85).move_to(ax.c2p(-1.2, 0.4))

        lbl_boundary = MathTex(r"D(\mathbf{z}) = 0.5", font_size=18, color=BOUNDARY_C)
        lbl_boundary.next_to(boundary_circle, UR, buff=0.10)

        self.play(Create(boundary_circle), run_time=1.4)
        self.play(Write(lbl_boundary), run_time=0.6)
        self.wait(0.5)

        legend = VGroup(
            VGroup(
                Square(0.18, fill_color=REAL_C, fill_opacity=0.7, stroke_width=0),
                self._mono("D(z) → 1  REAL", 12, REAL_C),
            ).arrange(RIGHT, buff=0.12),
            VGroup(
                Square(0.18, fill_color=FAKE_C, fill_opacity=0.7, stroke_width=0),
                self._mono("D(z) → 0  DEEPFAKE", 12, FAKE_C),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        legend.to_corner(DR, buff=0.45)
        self.play(FadeIn(legend), run_time=0.6)
        self.wait(1.0)

        self._cells          = cells
        self._boundary_circ  = boundary_circle
        self._lbl_boundary   = lbl_boundary
        self._lbl_d          = lbl_d
        self._legend         = legend
        self._ax             = ax
        self._ax_lbl         = ax_lbl

    def _block2_gradient_field(self, ax):
        lbl_grad = self._mono("∇D(z)  —  campo de gradiente euclídeo", 13, GRAD_C)
        lbl_grad.to_corner(UL, buff=0.40)

        self.play(
            FadeOut(self._lbl_d),
            FadeIn(lbl_grad, shift=RIGHT * 0.1),
            run_time=0.5,
        )

        arrows = VGroup()
        scale = 0.55 
        for x in np.linspace(-3.2, 2.0, 9):
            for y in np.linspace(-2.2, 2.2, 7):
                gx, gy = grad_D(x, y)
                mag = np.sqrt(gx**2 + gy**2)
                if mag < 1e-6:
                    continue
                gx_n, gy_n = gx / mag, gy / mag
                start = ax.c2p(x, y)
                end   = ax.c2p(x + gx_n * scale * 0.45,
                               y + gy_n * scale * 0.45)
                arr = Arrow(
                    start, end,
                    buff=0,
                    stroke_width=1.8,
                    max_tip_length_to_length_ratio=0.35,
                    color=interpolate_color(ManimColor(FAKE_C), ManimColor(GRAD_C), D(x, y)),
                )
                arrows.add(arr)

        self.play(
            LaggedStartMap(FadeIn, arrows, lag_ratio=0.015),
            run_time=2.5,
        )
        self.wait(0.5)

        # anotación: el gradiente apunta hacia mayor D
        note = self._mono("∇D apunta hacia mayor confianza del detector", 13, MUTED)
        note_box = self._hud_box(note, GRAD_C)
        note_box.to_corner(DR, buff=0.45)
        self.play(FadeOut(self._legend), FadeIn(note_box), run_time=0.6)
        self.wait(1.2)

        self.play(FadeOut(arrows), FadeOut(note_box), run_time=0.8)

        self._lbl_grad = lbl_grad

    def _block3_tangent_projection(self, ax):
        lbl_proj = self._mono("∇_M D(z)  —  gradiente proyectado sobre M", 13, MANIFOLD_C)
        lbl_proj.to_corner(UL, buff=0.40)

        self.play(
            FadeOut(self._lbl_grad),
            FadeIn(lbl_proj, shift=RIGHT * 0.1),
            run_time=0.5,
        )

        # demostracion
        x0, y0 = -0.5, 1.2
        pos0 = ax.c2p(x0, y0)

        demo_dot = Dot(pos0, radius=0.11, color=WHITE)
        demo_label = MathTex(r"\mathbf{z}_0", font_size=20, color=WHITE)
        demo_label.next_to(demo_dot, UL, buff=0.10)

        self.play(GrowFromCenter(demo_dot), Write(demo_label), run_time=0.7)
        self.wait(0.3)

        # vector ∇D (euclideo)
        gx, gy = grad_D(x0, y0)
        mag = np.sqrt(gx**2 + gy**2)
        sc = 1.1
        arr_eucl = Arrow(
            pos0,
            ax.c2p(x0 + gx / mag * sc, y0 + gy / mag * sc),
            buff=0, color=GRAD_C,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.22,
        )
        lbl_eucl = MathTex(r"\nabla D", font_size=20, color=GRAD_C)
        lbl_eucl.next_to(arr_eucl.get_end(), UR, buff=0.08)

        self.play(FadeIn(arr_eucl), Write(lbl_eucl), run_time=0.9)
        self.wait(0.3)

        # vector ∇_M D (proyectado sobre el plano tangente)
        px, py = proj_tangent(gx, gy, x0, y0)
        pmag = np.sqrt(px**2 + py**2)
        arr_proj = Arrow(
            pos0,
            ax.c2p(x0 + px / pmag * sc * 0.9, y0 + py / pmag * sc * 0.9),
            buff=0, color=MANIFOLD_C,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.22,
        )
        lbl_proj_vec = MathTex(r"\nabla_{\!\mathcal{M}} D", font_size=20, color=MANIFOLD_C)
        lbl_proj_vec.next_to(arr_proj.get_end(), DR, buff=0.08)

        self.play(FadeIn(arr_proj), Write(lbl_proj_vec), run_time=0.9)
        self.wait(0.3)

        diff_line = DashedLine(
            arr_eucl.get_end(), arr_proj.get_end(),
            dash_length=0.08, color=GRAY_B, stroke_width=1.2,
        ).set_stroke(opacity=0.6)
        lbl_diff = self._mono("componente normal\neliminada", 11, GRAY_B)
        lbl_diff.next_to(diff_line.get_center(), RIGHT, buff=0.12)

        self.play(Create(diff_line), FadeIn(lbl_diff), run_time=0.7)
        self.wait(0.4)

        formula_proj = MathTex(
            r"\nabla_{\!\mathcal{M}} D = \nabla D"
            r"- \bigl(\nabla D \cdot \hat{n}\bigr)\,\hat{n}",
            font_size=22, color=WHITE,
            substrings_to_isolate=[r"\hat{n}"],
        )
        formula_proj.set_color_by_tex(r"\hat{n}", GRAY_B)
        box_proj = self._hud_box(formula_proj, MANIFOLD_C)
        box_proj.to_corner(DR, buff=0.45)

        self.play(FadeIn(box_proj, shift=UP * 0.1), run_time=0.8)
        self.wait(1.8)

        self.play(
            FadeOut(demo_dot, demo_label,
                    arr_eucl, lbl_eucl,
                    arr_proj, lbl_proj_vec,
                    diff_line, lbl_diff,
                    box_proj),
            FadeOut(lbl_proj),
            run_time=0.9,
        )

    def _block4_descent(self, ax):
        lbl_desc = self._mono("descenso de gradiente proyectado", 13, GRAD_C)
        lbl_desc.to_corner(UL, buff=0.40)
        self.play(FadeIn(lbl_desc, shift=RIGHT * 0.1), run_time=0.5)

        alpha = 0.38 
        z = np.array([-2.2, 1.5])
        n_steps = 12

        start_dot = Dot(ax.c2p(*z), radius=0.12, color=REAL_C)
        start_halo = Circle(radius=0.26, color=REAL_C, stroke_width=1.5)
        start_halo.set_fill(REAL_C, opacity=0.10).move_to(ax.c2p(*z))
        start_lbl = MathTex(r"\mathbf{z}_0", font_size=20, color=REAL_C)
        start_lbl.next_to(start_dot, UL, buff=0.10)

        self.play(
            GrowFromCenter(start_halo),
            GrowFromCenter(start_dot),
            Write(start_lbl),
            run_time=0.8,
        )
        self.wait(0.3)

        step_formula = MathTex(
            r"\mathbf{z}_{t+1} = \mathbf{z}_t"
            r"- \alpha\,\nabla_{\!\mathcal{M}}\,D(\mathbf{z}_t)",
            font_size=22, color=GRAD_C,
        )
        box_formula = self._hud_box(step_formula, GRAD_C)
        box_formula.to_corner(DR, buff=0.45)
        self.play(FadeIn(box_formula, shift=UP * 0.1), run_time=0.7)

        iter_text = self._mono("t = 0", 14, MUTED)
        iter_box  = self._hud_box(iter_text, DIM)
        iter_box.to_corner(UR, buff=0.40)
        self.play(FadeIn(iter_box), run_time=0.4)

        path_points = [ax.c2p(*z)]
        step_dots   = VGroup()
        step_arrows = VGroup()

        for t in range(n_steps):
            gx, gy = grad_D(*z)
            px, py = proj_tangent(gx, gy, *z)
            pmag = max(np.sqrt(px**2 + py**2), 1e-8)

            z_new = z - alpha * np.array([px, py])

            pos_old = ax.c2p(*z)
            pos_new = ax.c2p(*z_new)

            val = D(*z_new)
            col = interpolate_color(ManimColor(FAKE_C), ManimColor(REAL_C), val)

            step_arr = Arrow(
                pos_old, pos_new,
                buff=0.06,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.30,
                color=GRAD_C,
            )
            step_dot = Dot(pos_new, radius=0.08, color=col)

            step_arrows.add(step_arr)
            step_dots.add(step_dot)
            path_points.append(pos_new)

            new_iter = self._mono(f"t = {t+1}", 14, MUTED)
            new_box  = self._hud_box(new_iter, DIM).to_corner(UR, buff=0.40)

            self.play(
                FadeIn(step_arr),
                Transform(iter_box, new_box),
                run_time=0.38,
                rate_func=linear,
            )
            self.play(GrowFromCenter(step_dot), run_time=0.18)

            z = z_new

            if abs(D(*z) - 0.5) < 0.08 and t < n_steps - 2:
                crossed_lbl = self._mono("¡frontera cruzada!", 13, FAKE_C)
                crossed_box = self._hud_box(crossed_lbl, FAKE_C)
                crossed_box.to_corner(DL, buff=0.45)
                self.play(FadeIn(crossed_box, shift=UP * 0.1), run_time=0.4)
                self.wait(0.6)
                self.play(FadeOut(crossed_box), run_time=0.3)

        path_line = VMobject(stroke_color=GRAD_C, stroke_width=1.5)
        path_line.set_points_as_corners(path_points)
        path_line.set_stroke(opacity=0.45)
        self.add(path_line)

        # punto final z_adv
        final_dot = Dot(ax.c2p(*z), radius=0.13, color=FAKE_C)
        final_halo = Circle(radius=0.28, color=FAKE_C, stroke_width=1.5)
        final_halo.set_fill(FAKE_C, opacity=0.12).move_to(ax.c2p(*z))
        final_lbl = MathTex(r"\mathbf{z}_{\mathrm{adv}}", font_size=20, color=FAKE_C)
        final_lbl.next_to(final_dot, DR, buff=0.12)

        self.play(
            GrowFromCenter(final_halo),
            GrowFromCenter(final_dot),
            Write(final_lbl),
            run_time=0.8,
        )
        self.wait(0.5)

        d_final = D(*z)
        result_txt = self._mono(
            f"D(z_adv) ≈ {d_final:.2f}  →  clasificado como REAL",
            13, FAKE_C,
        )
        result_box = self._hud_box(result_txt, FAKE_C)
        result_box.next_to(box_formula, UP, buff=0.22)
        self.play(FadeIn(result_box, shift=UP * 0.1), run_time=0.6)
        self.wait(1.5)

        self._lbl_desc   = lbl_desc
        self._box_formula = box_formula
        self._iter_box   = iter_box
        self._result_box = result_box
        self._path_line  = path_line
        self._step_dots  = step_dots
        self._step_arrows = step_arrows
        self._start_dot  = start_dot
        self._start_halo = start_halo
        self._start_lbl  = start_lbl
        self._final_dot  = final_dot
        self._final_halo = final_halo
        self._final_lbl  = final_lbl


    def _block5_formula(self, ax):
        # fade out de todo lo anterior
        self.play(
            FadeOut(
                self._ax, self._ax_lbl,
                self._cells, self._boundary_circ, self._lbl_boundary,
                self._path_line, self._step_dots, self._step_arrows,
                self._start_dot, self._start_halo, self._start_lbl,
                self._final_dot, self._final_halo, self._final_lbl,
                self._box_formula, self._iter_box, self._result_box,
                self._lbl_desc,
            ),
            run_time=1.2,
        )

        col_data = [
            (
                GRAD_C,
                r"\nabla D(\mathbf{z})",
                "gradiente euclídeo\nen el espacio latente",
            ),
            (
                GRAY_B,
                r"- (\nabla D \cdot \hat{n})\,\hat{n}",
                "componente normal\neliminada",
            ),
            (
                MANIFOLD_C,
                r"\nabla_{\!\mathcal{M}} D(\mathbf{z})",
                "gradiente sobre\nel manifold",
            ),
        ]

        cols = VGroup()
        for color, math_str, desc_str in col_data:
            math_lbl = MathTex(math_str, font_size=26, color=color)
            desc_lbl = Text(
                desc_str, font="Courier New", font_size=13,
                color=MUTED, line_spacing=1.3,
            )
            col = VGroup(math_lbl, desc_lbl).arrange(DOWN, buff=0.28)
            cols.add(col)

        cols.arrange(RIGHT, buff=0.8, aligned_edge=UP)

        sep1 = Line(UP * 1.0, DOWN * 1.0, stroke_width=0.5, color=DIM).set_stroke(opacity=0.5)
        sep2 = sep1.copy()
        sep1.move_to(cols[0].get_right() + RIGHT * 0.40)
        sep2.move_to(cols[1].get_right() + RIGHT * 0.40)

        summary = VGroup(cols, sep1, sep2).move_to(ORIGIN + UP * 0.5)

        main_formula = MathTex(
            r"\mathbf{z}_{t+1} = \mathbf{z}_t"
            r"- \alpha \Bigl[\nabla D(\mathbf{z}_t)"
            r"- \bigl(\nabla D(\mathbf{z}_t) \cdot \hat{n}\bigr)\hat{n}\Bigr]",
            font_size=26, color=WHITE,
            substrings_to_isolate=[r"\hat{n}", r"\alpha"],
        )
        main_formula.set_color_by_tex(r"\hat{n}", GRAY_B)
        main_formula.set_color_by_tex(r"\alpha",  GRAD_C)

        formula_bg = SurroundingRectangle(
            main_formula, color=MANIFOLD_C, buff=0.28,
            fill_color="#0d0d22", fill_opacity=0.96,
            stroke_width=0.9, corner_radius=0.14,
        ).set_stroke(opacity=0.6)
        formula_group = VGroup(formula_bg, main_formula)
        formula_group.next_to(summary, DOWN, buff=0.55)

        self.play(
            LaggedStartMap(FadeIn, cols, shift=UP * 0.2, lag_ratio=0.25),
            run_time=1.4,
        )
        self.play(
            FadeIn(sep1, scale=0.8),
            FadeIn(sep2, scale=0.8),
            run_time=0.5,
        )
        self.wait(0.4)
        self.play(
            FadeIn(formula_bg),
            Write(main_formula),
            run_time=1.4,
        )
        self.wait(2.8)

        self.play(
            FadeOut(summary, formula_group, shift=UP * 0.3),
            run_time=1.1,
        )
        self.wait(0.4)