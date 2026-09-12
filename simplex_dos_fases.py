from fractions import Fraction

def pivote(A, b, c, z, p_row, p_col):
    piv = A[p_row][p_col]
    A[p_row] = [x / piv for x in A[p_row]]
    b[p_row] = b[p_row] / piv
    for i in range(len(A)):
        if i != p_row:
            factor = A[i][p_col]
            A[i] = [A[i][j] - factor * A[p_row][j] for j in range(len(A[0]))]
            b[i] -= factor * b[p_row]
    factor_c = c[p_col]
    c[:] = [c[j] - factor_c * A[p_row][j] for j in range(len(c))]
    z[0] -= factor_c * b[p_row]

def imprimir_tabla(base, A, b, c, z, nombres):
    print(f"{'Base':<5} | " + " ".join(f"{n:>7}" for n in nombres) + f" | {'RHS':>7}")
    print("-" * (10 + 8 * len(nombres)))
    for i in range(len(base)):
        fila = " ".join(f"{str(A[i][j]):>7}" for j in range(len(nombres)))
        print(f"{base[i]:<5} | {fila} | {str(b[i]):>7}")
    print("-" * (10 + 8 * len(nombres)))
    fila_c = " ".join(f"{str(c[j]):>7}" for j in range(len(nombres)))
    print(f"{'Obj':<5} | {fila_c} | {str(z[0]):>7}\n")

# --- FASE I ---
cols_f1 = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 's1', 's2', 's3', 'a1']
A = [
    [Fraction(-1), Fraction(2), Fraction(0), Fraction(3), Fraction(1), Fraction(0), Fraction(2), Fraction(-1), Fraction(1), Fraction(0), Fraction(0)],
    [Fraction(1), Fraction(3), Fraction(-4), Fraction(-2), Fraction(0), Fraction(-6), Fraction(6), Fraction(-1), Fraction(0), Fraction(1), Fraction(0)],
    [Fraction(3), Fraction(8), Fraction(4), Fraction(5), Fraction(4), Fraction(2), Fraction(8), Fraction(-1), Fraction(0), Fraction(0), Fraction(1)]
]
b = [Fraction(40), Fraction(20), Fraction(120)]
c = [Fraction(-3), Fraction(-8), Fraction(-4), Fraction(-5), Fraction(-4), Fraction(-2), Fraction(-8), Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
z = [Fraction(-120)]
base = ['s2', 's3', 'a1']

print("FASE I - Tableau Inicial")
imprimir_tabla(base, A, b, c, z, cols_f1)

pivote(A, b, c, z, p_row=1, p_col=1)
base[1] = 'x2'
print("FASE I - Iteracion 1 (entra x2, sale s3)")
imprimir_tabla(base, A, b, c, z, cols_f1)

pivote(A, b, c, z, p_row=2, p_col=5)
base[2] = 'x6'
print("FASE I - Iteracion 2 (entra x6, sale a1)")
imprimir_tabla(base, A, b, c, z, cols_f1)

# --- FASE II ---
cols_f2 = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 's1', 's2', 's3']
A = [fila[:10] for fila in A]

c_orig = [Fraction(7), Fraction(3), Fraction(5), Fraction(2), Fraction(7), Fraction(3), Fraction(4), Fraction(0), Fraction(0), Fraction(0)]
c_b = {'s2': Fraction(0), 'x2': Fraction(3), 'x6': Fraction(3)}
cb_vec = [c_b[var] for var in base]

c = [c_orig[j] - sum(cb_vec[i] * A[i][j] for i in range(3)) for j in range(10)]
z = [-sum(cb_vec[i] * b[i] for i in range(3))]

print("FASE II - Tableau Inicial")
imprimir_tabla(base, A, b, c, z, cols_f2)

pivote(A, b, c, z, p_row=0, p_col=3)
base[0] = 'x4'
print("FASE II - Iteracion 1 (entra x4, sale s2)")
imprimir_tabla(base, A, b, c, z, cols_f2)

pivote(A, b, c, z, p_row=2, p_col=7)
base[2] = 's1'
print("FASE II - Tableau Final (entra s1, sale x6)")
imprimir_tabla(base, A, b, c, z, cols_f2)

print("Solucion Optima:")
for var, val in zip(base, b):
    print(f"{var} = {val} ({float(val)})")
print(f"Z* = {-z[0]} ({float(-z[0])})")
