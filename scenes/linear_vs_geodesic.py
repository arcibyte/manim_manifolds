from manim import *
import numpy as np
from scipy.integrate import solve_ivp
from palette import *

#funciones matematicas

def surface_func(u, v):
    """Manifold M: z = 0.4·sin(2u)·cos(2v)"""
    return np.array([u, v, 0.4 * np.sin(2 * u) * np.cos(2 * v)])


def metric_at(u, v, eps=1e-5):
    """
    Tensor métrico g_ij = <∂_i f, ∂_j f> en el punto (u,v).
    Calcula las derivadas parciales numéricamente.
    """
    fu = (surface_func(u + eps, v) - surface_func(u - eps, v)) / (2 * eps)
    fv = (surface_func(u, v + eps) - surface_func(u, v - eps)) / (2 * eps)
    g11 = np.dot(fu, fu)
    g12 = np.dot(fu, fv)
    g22 = np.dot(fv, fv)
    return np.array([[g11, g12], [g12, g22]])


def christoffel(u, v, eps=1e-4):
    def g(u_, v_):
        return metric_at(u_, v_)

    # derivadas del tensor métrico
    dg_du = (g(u + eps, v) - g(u - eps, v)) / (2 * eps)  # ∂g/∂u
    dg_dv = (g(u, v + eps) - g(u, v - eps)) / (2 * eps)  # ∂g/∂v
    dg = [dg_du, dg_dv]   # dg[k] = ∂g/∂x^k

    G = g(u, v)
    try:
        G_inv = np.linalg.inv(G)
    except np.linalg.LinAlgError:
        return np.zeros((2, 2, 2))

    Gamma = np.zeros((2, 2, 2))
    for k in range(2):
        for i in range(2):
            for j in range(2):
                # Γ^k_ij = ½ g^{kl}(∂_i g_{jl} + ∂_j g_{il} − ∂_l g_{ij})
                val = 0.0
                for l in range(2):
                    val += G_inv[k, l] * (
                        dg[i][j, l] + dg[j][i, l] - dg[l][i, j]
                    )
                Gamma[k, i, j] = 0.5 * val
    return Gamma

def geodesic_ode(t, y):
    """
    sistema de EDOs para las ecuaciones geodésicas:
      d²x^k/dt² + Γ^k_ij (dx^i/dt)(dx^j/dt) = 0

    estado: y = [u, v, du/dt, dv/dt]
    """
    u, v, du, dv = y
    G = christoffel(u, v)
    acc_u = -(G[0, 0, 0] * du * du +
               2 * G[0, 0, 1] * du * dv +
               G[0, 1, 1] * dv * dv)
    acc_v = -(G[1, 0, 0] * du * du +
               2 * G[1, 0, 1] * du * dv +
               G[1, 1, 1] * dv * dv)
    return [du, dv, acc_u, acc_v]


def compute_geodesic(p1_uv, p2_uv, n_points=120):
    u0, v0 = p1_uv
    u1, v1 = p2_uv
    # velocidad inicial: dirección paramétrica hacia p2
    # (aproximación lineal en el espacio de parámetros)
    T = 1.0
    du0 = (u1 - u0) / T
    dv0 = (v1 - v0) / T

    y0 = [u0, v0, du0, dv0]
    t_span = (0, T)
    t_eval = np.linspace(0, T, n_points)

    sol = solve_ivp(
        geodesic_ode, t_span, y0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-7, atol=1e-9,
        max_step=0.02,
    )

    pts = []
    for i in range(len(sol.t)):
        u, v = sol.y[0, i], sol.y[1, i]
        pts.append(surface_func(u, v))
    return np.array(pts)


class LinearVsGeodesic(ThreeDScene):

    def setup(self):
        self.camera.background_color = BG
    #parametros
    U1, V1 = -1.5, -1.5   # punto de inicio en parámetros
    U2, V2 =  1.5,  1.5   # punto de fin en parámetros

    def _mono(self, s, size=20, color=MUTED):
        return Text(s, font="Courier New", font_size=size, color=color)

    def _hud_box(self, mob, border_color=GRAD_C):
        bg = SurroundingRectangle(
            mob, color=border_color, buff=0.18,
            fill_color="#0d0d22", fill_opacity=0.95,
            stroke_width=0.8, corner_radius=0.12,
        ).set_stroke(opacity=0.55)
        return VGroup(bg, mob)

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.88)

        self._block0_title()
        self._block1_surface()
        self._block2_points()
        self._block3_linear()
        self._block4_geodesic()
        self._block5_particles()
        self._block6_comparison()
        self._block7_formula()

    def _block0_title(self):
        tag = self._mono("02 / interpolación en el manifold", 14, DIM)
        tag.to_corner(UL, buff=0.40)
        self.add_fixed_in_frame_mobjects(tag)

        title = Text(
            "Interpolación Lineal vs Geodésica",
            font_size=34, weight=BOLD, color=WHITE,
        ).set_stroke(WHITE, width=0.3, opacity=0.3)
        title.to_edge(UP, buff=0.35)
        self.add_fixed_in_frame_mobjects(title)

        self.play(
            FadeIn(tag,   shift=RIGHT * 0.1),
            Write(title),
            run_time=1.0,
        )
        self.wait(0.4)

        self._title  = title
        self._tag    = tag

    def _block1_surface(self):
        surface = Surface(
            lambda u, v: surface_func(u, v),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(42, 42),
            fill_opacity=0.52,
            checkerboard_colors=[MANIFOLD_C + "55", MANIFOLD_C + "33"],
        )
        surface.set_style(
            stroke_width=0.35,
            stroke_color=WHITE,
            stroke_opacity=0.18,
        )

        # Etiqueta del manifold
        manifold_lbl = self._mono("manifold  M ⊂ ℝ³", 15, MANIFOLD_C)
        manifold_lbl.to_corner(UR, buff=0.40)
        self.add_fixed_in_frame_mobjects(manifold_lbl)

        self.play(
            Create(surface, run_time=2.2),
            FadeIn(manifold_lbl, shift=LEFT * 0.1),
        )
        self.wait(0.5)

        self._surface      = surface
        self._manifold_lbl = manifold_lbl

    # puntos z₁ y z₂
    def _block2_points(self):
        p1 = surface_func(self.U1, self.V1)
        p2 = surface_func(self.U2, self.V2)

        dot1 = Dot3D(point=p1, color=REAL_C, radius=0.11)
        dot2 = Dot3D(point=p2, color=REAL_C, radius=0.11)

        # halos 3D
        halo1 = Sphere(radius=0.20, color=REAL_C).move_to(p1)
        halo1.set_opacity(0.12)
        halo2 = Sphere(radius=0.20, color=REAL_C).move_to(p2)
        halo2.set_opacity(0.12)

        lbl1 = MathTex(r"\mathbf{z}_1", font_size=26, color=REAL_C)
        lbl2 = MathTex(r"\mathbf{z}_2", font_size=26, color=REAL_C)
        lbl1.to_corner(UL, buff=0.95)
        lbl2.next_to(self._manifold_lbl, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(lbl1, lbl2)

        self.play(
            FadeIn(halo1), FadeIn(halo2),
            FadeIn(dot1),  FadeIn(dot2),
            Write(lbl1),   Write(lbl2),
            run_time=0.9,
        )
        self.wait(0.4)

        self._p1   = p1
        self._p2   = p2
        self._dot1 = dot1
        self._dot2 = dot2
        self._halo1 = halo1
        self._halo2 = halo2
        self._lbl1 = lbl1
        self._lbl2 = lbl2

    # interpolacion lineal
    def _block3_linear(self):
        p1, p2 = self._p1, self._p2

        linear_path = ParametricFunction(
            lambda t: p1 + t * (p2 - p1),
            t_range=[0, 1, 0.005],
            color=WRONG_PATH if hasattr(
                __builtins__, 'WRONG_PATH') else "#f87171",
        )
        linear_path.set_stroke(color=FAKE_C, width=4.5, opacity=0.92)

        linear_lbl = self._mono("interpolación lineal", 16, FAKE_C)
        linear_lbl.next_to(self._title, DOWN, buff=0.28)
        self.add_fixed_in_frame_mobjects(linear_lbl)

        # Nota: atraviesa el espacio ambiente
        note_linear = self._mono("⚠  atraviesa el espacio ambiente ℝ³", 13, FAKE_C)
        note_box = self._hud_box(note_linear, FAKE_C)
        note_box.to_corner(DL, buff=0.42)
        self.add_fixed_in_frame_mobjects(note_box)

        self.play(
            Create(linear_path, run_time=1.6),
            Write(linear_lbl),
        )
        self.play(FadeIn(note_box, shift=UP * 0.1), run_time=0.6)
        self.wait(0.6)

        self._linear_path  = linear_path
        self._linear_lbl   = linear_lbl
        self._note_linear  = note_box

    # geodesica real (scipy)
    def _block4_geodesic(self):
        geo_pts = compute_geodesic(
            (self.U1, self.V1),
            (self.U2, self.V2),
            n_points=150,
        )

        geo_path = VMobject()
        geo_path.set_points_as_corners(geo_pts)
        geo_path.set_stroke(color=REAL_PATH, width=5.5, opacity=0.96)

        geo_lbl = self._mono("geodésica sobre M  (RK45)", 16, REAL_PATH)
        geo_lbl.next_to(self._linear_lbl, DOWN, buff=0.20)
        self.add_fixed_in_frame_mobjects(geo_lbl)

        note_geo = self._mono("✓  permanece sobre el manifold", 13, REAL_PATH)
        note_geo_box = self._hud_box(note_geo, REAL_PATH)
        note_geo_box.next_to(self._note_linear, UP, buff=0.22)
        self.add_fixed_in_frame_mobjects(note_geo_box)

        self.play(
            Create(geo_path, run_time=2.2),
            Write(geo_lbl),
        )
        self.play(FadeIn(note_geo_box, shift=UP * 0.1), run_time=0.6)
        self.wait(0.5)

        self._geo_path     = geo_path
        self._geo_pts      = geo_pts
        self._geo_lbl      = geo_lbl
        self._note_geo_box = note_geo_box

    def _block5_particles(self):
        p1, p2 = self._p1, self._p2
        geo_pts = self._geo_pts
        n = len(geo_pts)

        # particula lineal
        sphere_linear = Sphere(radius=0.09).move_to(p1)
        sphere_linear.set_color(FAKE_C).set_opacity(0.92)

        # particula geodesica
        sphere_geo = Sphere(radius=0.09).move_to(p1)
        sphere_geo.set_color(REAL_PATH).set_opacity(0.92)

        self.add(sphere_linear, sphere_geo)

        def update_linear(mob, alpha):
            mob.move_to(p1 + alpha * (p2 - p1))

        def update_geo(mob, alpha):
            idx = min(int(alpha * (n - 1)), n - 1)
            mob.move_to(geo_pts[idx])

        self.play(
            UpdateFromAlphaFunc(sphere_linear, update_linear),
            UpdateFromAlphaFunc(sphere_geo,    update_geo),
            run_time=4.5,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.5)

        self._sphere_linear = sphere_linear
        self._sphere_geo    = sphere_geo

    #texto comparativo + rotacion de camara
    def _block6_comparison(self):
        comparison = Text(
            font="Courier New", font_size=17, color=WHITE,
            line_spacing=1.45,
            t2c={
                "geodésica":  REAL_PATH,
                "línea recta": FAKE_C,
                "longitud intrínseca": MANIFOLD_C,
            },
        )
        comp_bg = SurroundingRectangle(
            comparison, color=GRAY_A, buff=0.26,
            fill_color="#0d0d20", fill_opacity=0.95,
            stroke_width=0.7, corner_radius=0.14,
        ).set_stroke(opacity=0.55)
        comp_group = VGroup(comp_bg, comparison)
        comp_group.to_edge(DOWN, buff=0.38)
        self.add_fixed_in_frame_mobjects(comp_group)

        self.play(FadeIn(comp_group, shift=UP * 0.12), run_time=0.9)

        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(5.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)

        self._comp_group = comp_group

    def _block7_formula(self):
        self.play(
            FadeOut(self._surface),
            FadeOut(self._linear_path),
            FadeOut(self._geo_path),
            FadeOut(self._dot1), FadeOut(self._dot2),
            FadeOut(self._halo1), FadeOut(self._halo2),
            FadeOut(self._sphere_linear), FadeOut(self._sphere_geo),
            FadeOut(self._comp_group),
            FadeOut(self._note_linear), FadeOut(self._note_geo_box),
            FadeOut(self._manifold_lbl),
            FadeOut(self._lbl1), FadeOut(self._lbl2),
            FadeOut(self._linear_lbl), FadeOut(self._geo_lbl),
            FadeOut(self._title), FadeOut(self._tag),
            run_time=1.2,
        )

        # forrmula principal
        formula = MathTex(
            r"L(\gamma) = \int_0^1 \sqrt{\,g_{ij}(\gamma(t))\,"
            r"\dot{\gamma}^{\,i}(t)\,\dot{\gamma}^{\,j}(t)\,}\;\mathrm{d}t"
            r"\;\longrightarrow\;\min",
            font_size=32, color=WHITE,
            substrings_to_isolate=[r"g_{ij}", r"\min"],
        )
        formula.set_color_by_tex(r"g_{ij}", MANIFOLD_C)
        formula.set_color_by_tex(r"\min",   REAL_PATH)

        formula_bg = SurroundingRectangle(
            formula, color=MANIFOLD_C, buff=0.30,
            fill_color="#0d0d22", fill_opacity=0.97,
            stroke_width=0.9, corner_radius=0.15,
        ).set_stroke(opacity=0.65)
        formula_group = VGroup(formula_bg, formula).move_to(UP * 0.5)
        desc = Text(
            "La geodésica es la curva γ que minimiza esta integral\n"
            "con el tensor métrico g_ij inducido por el manifold",
            font="Courier New", font_size=15, color=MUTED,
            line_spacing=1.4,
            t2c={"g_ij": MANIFOLD_C, "γ": REAL_PATH},
        )
        desc.next_to(formula_group, DOWN, buff=0.50)

        self.play(
            FadeIn(formula_bg),
            Write(formula),
            run_time=1.6,
        )
        self.play(FadeIn(desc, shift=UP * 0.1), run_time=0.8)
        self.wait(3.0)

        self.play(
            FadeOut(formula_group, shift=UP * 0.3),
            FadeOut(desc,          shift=UP * 0.3),
            run_time=1.0,
        )
        self.wait(0.4)