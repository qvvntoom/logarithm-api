# === METODA SIŁOWA (brute-force) ===
def brute_force_method(a, b, n, details=False):
    """
    Metoda siłowa rozwiązująca równanie a^x ≡ b (mod n).
    Przechodzi po kolei wszystkie potęgi a modulo n aż znajdzie b.
    """
    if details:
        print(f"Rozważamy zagadnienie: {a}^x = {b} (mod {n})\n")

    y = 1
    i = 1
    while True:
        y = (y * a) % n
        if y == b % n:
            break
        i += 1

    if details:
        print(f"Wynik końcowy x = {i}")

    return i


# === ODWROTNOŚĆ MODULARNA ===
def modinv(a, n):
    """
    Oblicza odwrotność modularną liczby a modulo n przy użyciu rozszerzonego algorytmu Euklidesa.
    """
    t, newt = 0, 1
    r, newr = n, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise ValueError("Liczba nieodwracalna modulo n")
    return t + n if t < 0 else t


# === ALGORYTM MAŁYCH I WIELKICH KROKÓW ===
from math import ceil, sqrt

def baby_step_giant_step(a, b, n, details=False, sets_display=False):
    """
    Rozwiązuje równanie a^x ≡ b (mod n) przy użyciu algorytmu małych i wielkich kroków.
    """
    m = ceil(sqrt(n))
    a_inv = modinv(a, n)

    # Zbiór małych kroków
    baby_steps = {(b * pow(a_inv, r, n)) % n: r for r in range(m)}

    # Wielkie kroki
    factor = pow(a, m, n)
    y = 1
    delty = []

    if details:
        print(f"Rozważamy zagadnienie: {a}^x = {b} (mod {n})\n")
        print(f"m = {m}\n")

    for j in range(1, m + 1):
        y = (y * factor) % n
        delty.append(y)
        if y in baby_steps:
            i = baby_steps[y]
            x = j * m + i
            if details:
                if sets_display:
                    print("Zbiór małych kroków:")
                    print(list(baby_steps.keys()))
                    print("\nZbiór wielkich kroków:")
                    print(delty)
                    print("")
                print(f"Pierwszy wspólny element: {y}")
                print(f"j = {j}, i = {i}")
                print(f"Zgodnie ze wzorem: x = {j} * {m} + {i} = {x}")
                print(f"\nWynik końcowy: x = {x}")
            return x
    return None


# === ALGORYTM POHLIGA–HELLMANA (zgodny z SageMath) ===
from sympy import factorint
from sympy.ntheory.modular import crt

def pohlig_hellman_algorithm(a, b, n, details=False):
    """
    Algorytm Pohliga–Hellmana zgodny z wersją SageMath.
    Obsługuje poprawnie przypadki p^e z e > 1, budując rozwiązania iteracyjnie.
    """
    if details:
        print(f"Zagadnienie: {a}^x = {b} (mod {n}), można zastąpić przez:\n")

    factors = factorint(n - 1)
    x_list = []
    mod_list = []

    for p, e in factors.items():
        pe = p ** e
        x_pe = 0
        a_inv = modinv(a, n)

        for k in range(e):
            exp = (n - 1) // (p ** (k + 1))

            a_k = pow(a, exp, n)
            b_k = pow(b * pow(a_inv, x_pe, n), exp, n)

            d_k = baby_step_giant_step(a_k, b_k, n)
            if d_k is None:
                raise ValueError(f"Nie udało się rozwiązać logarytmu dyskretnego mod {p}^{k+1}")

            x_pe += d_k * (p ** k)

        x_list.append(x_pe)
        mod_list.append(pe)

        if details:
            print(f"x ≡ {x_pe} (mod {pe})")

    result, _ = crt(mod_list, x_list)
    x_final = int(result % (n - 1))

    if details:
        print("\nZgodnie z twierdzeniem:")
        for i in range(len(x_list)):
            print(f"x = {x_list[i]} (mod {mod_list[i]})")
        print(f"\nWynik końcowy: x = {x_final}")

    return x_final


# === ALGORYTM RHO POLLARDA ===
import random
import time
from math import gcd

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y

def pollard_rho_dlog(a, b, n, details=False):
    start_time = time.time()
    N = n - 1

    while True:
        e, f = 0, random.randint(0, N - 1)
        x = pow(b, f, n)

        tortoise = (e, f, x)
        hare = (e, f, x)

        def iterate(state):
            e, f, x = state
            if x % 3 == 1:
                return ((e + 1) % N, f, a * x % n)
            elif x % 3 == 2:
                return ((2 * e) % N, (2 * f) % N, x * x % n)
            else:
                return (e, (f + 1) % N, b * x % n)

        for _ in range(1, N * 2):
            tortoise = iterate(tortoise)
            hare = iterate(iterate(hare))

            if tortoise[2] == hare[2]:
                break

        ei, fi, _ = tortoise
        ej, fj, _ = hare

        s = (ei - ej) % N
        t = (fj - fi) % N

        g, v, w = extended_gcd(s, N)
        if g == 0:
            continue

        try:
            x0 = (v * t // g) % N
        except:
            continue

        candidates = [(x0 + k * (N // g)) % N for k in range(g)]
        for x in candidates:
            if pow(a, x, n) == b % n:
                elapsed = round(time.time() - start_time, 5)
                if details:
                    print("Algorytm rho Pollarda:\n")
                    print(f"Powtórzenie dla x = {tortoise[2]}")
                    print(f"e_i = {ei}, f_i = {fi}")
                    print(f"e_j = {ej}, f_j = {fj}")
                    print("")
                    print(f"Równanie: ({ei} - {ej})x ≡ {fj} - {fi} (mod {N})")
                    print("")
                    print(f"Rozwiązujemy: {s}x ≡ {t} (mod {N})")
                    print(f"NWD({s}, {N}) = {g}, v = {v}, w = {w}")
                    print("")
                    print("Rozwiązanie: x ≡", f"{v}*{t}//{g} mod {N}")
                    print("")
                    print(f"Kandydaci: {candidates}")
                    print(f"Wybrany logarytm x = {x}")
                return x

        continue
