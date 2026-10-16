# Tarea 3 - Optimizacion
# Mariana Alvarez, Carlos Diaz

from fractions import Fraction as F
import heapq
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, minimize

# ---------------- Ejercicio 1 ----------------
print("Ejercicio 1")
eps = 1e-4
c = -np.array([2, 4, 3])  # milp minimiza
A = np.array([[1, 2, 0],
              [-1, 1, 1],
              [1, -1, -(5 + eps)]])
cons = LinearConstraint(A, -np.inf, [4, 2, -1 - eps])

for d in (0, 1):
    r = milp(c, constraints=cons, integrality=[0, 0, 1],
             bounds=Bounds([0, 0, d], [np.inf, np.inf, d]))
    print(f"  delta={d}: z={-r.fun:.2f}, x={r.x[:2].round(4)}")
r = milp(c, constraints=cons, integrality=[0, 0, 1],
         bounds=Bounds(0, [np.inf, np.inf, 1]))
print(f"  optimo: z={-r.fun:.2f}, (x1, x2, delta)={r.x.round(4)}")

# ---------------- Ejercicio 2 ----------------
v = [2, 3, 4, 6, 8]
ing = [10, 14, 31, 48, 60]
V = 11
orden = sorted(range(5), key=lambda i: F(ing[i], v[i]), reverse=True)


def lp(fijas):
    # relajacion lineal con algunas variables fijas (voraz por r/v)
    cap = F(V) - sum(v[i] * val for i, val in fijas.items())
    if cap < 0:
        return None, None
    x = [F(fijas.get(i, 0)) for i in range(5)]
    for i in orden:
        if i not in fijas and cap > 0:
            x[i] = min(F(1), cap / v[i])
            cap -= x[i] * v[i]
    return sum(ing[i] * x[i] for i in range(5)), x


def txt(x):
    return "(" + ", ".join(map(str, x)) + ")"


print("\nEjercicio 2a")
z0, x0 = lp({})
print(f"  P0: z={float(z0):.2f} x={txt(x0)}")
cola = [(-z0, 0, {}, x0)]
k = 0
z_inc = x_inc = None
while cola:
    nz, padre, fijas, x = heapq.heappop(cola)
    if z_inc is not None and -nz <= z_inc:
        continue
    j = next(i for i in range(5) if x[i].denominator != 1)
    for val in (0, 1):
        k += 1
        hijo = {**fijas, j: val}
        z, xh = lp(hijo)
        rama = f"P{k} (P{padre}, x{j + 1}={val})"
        if z is None:
            print(f"  {rama}: infactible")
            continue
        estado = ""
        if all(t.denominator == 1 for t in xh):
            if z_inc is None or z > z_inc:
                z_inc, x_inc = z, xh
                estado = "-> entera, incumbente"
            else:
                estado = "-> entera, no mejora"
        elif z_inc is not None and z <= z_inc:
            estado = "-> poda por cota"
        else:
            heapq.heappush(cola, (-z, k, hijo, xh))
        print(f"  {rama}: z={float(z):.2f} x={txt(xh)} {estado}")
print(f"  optimo: z={z_inc}, x={txt(x_inc)}, nodos={k + 1}")

print("\nEjercicio 2b")
f = next(i for i in range(5) if 0 < x0[i] < 1)  # paquete fraccionario
y0 = F(ing[f], v[f])
y = [max(F(0), ing[i] - v[i] * y0) if x0[i] > 0 else F(0) for i in range(5)]
assert all(v[i] * y0 + y[i] >= ing[i] for i in range(5))
print(f"  y0={y0}, y={txt(y)}, w={V * y0 + sum(y)}")

print("\nEjercicio 2c")
hs = {}
for t in range(13):
    yt = [max(0, ing[i] - v[i] * t) for i in range(5)]
    hs[t] = (V * t + sum(yt), yt)
print("  h(y0):", {t: h for t, (h, _) in hs.items()})
t = min(hs, key=lambda s: hs[s][0])
w, yt = hs[t]
xi = [int(a) for a in x_inc]
print(f"  optimo: y0={t}, y={yt}, w={w}")
print("  y0(11 - v'x):", t * (V - sum(v[i] * xi[i] for i in range(5))))
print("  y_i(1 - x_i):", [yt[i] * (1 - xi[i]) for i in range(5)])
print("  x_i(v_i y0 + y_i - r_i):", [xi[i] * (v[i] * t + yt[i] - ing[i]) for i in range(5)])
print("  brecha:", w - z_inc)

# ---------------- Ejercicio 3 ----------------
print("\nEjercicio 3")
P = np.array([[13, 12, -2], [12, 17, 6], [-2, 6, 12]], dtype=float)
q = np.array([-22, -14.5, 13])
xs = np.array([1, 0.5, -1])
f0 = lambda x: 0.5 * x @ P @ x + q @ x + 1
g = P @ xs + q
print("  menores:", [round(np.linalg.det(P[:m, :m])) for m in (1, 2, 3)])
print("  eig(P):", np.linalg.eigvalsh(P).round(4))
print("  grad:", g, " f0(x*):", f0(xs))
yc = -np.sign(g)  # minimiza grad'(y - x*) sobre la caja
print("  min grad'(y - x*):", g @ (yc - xs))
res = minimize(f0, np.zeros(3), jac=lambda x: P @ x + q, bounds=[(-1, 1)] * 3)
print("  scipy:", res.x.round(6), round(res.fun, 6))

# ---------------- Ejercicio 4 ----------------
print("\nEjercicio 4")
H = np.array([[4, 1, 0], [1, 2, 1], [0, 1, 2]], dtype=float)
b = np.array([6, 7, 8])
ws = np.linalg.solve(H, b)
fw = lambda u: 0.5 * u @ H @ u - b @ u + 9
print("  w*:", ws, [str(F(a).limit_denominator(100)) for a in ws])
print("  menores:", [round(np.linalg.det(H[:m, :m])) for m in (1, 2, 3)])
print("  eig(H):", np.linalg.eigvalsh(H).round(4))
print("  f(w*):", round(fw(ws), 6))
