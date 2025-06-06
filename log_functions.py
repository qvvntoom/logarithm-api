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


from math import gcd
from sympy import factorint
from sympy.ntheory.modular import crt

def power_mod(a, b, n):
    """Oblicza a^b mod n efektywnie"""
    return pow(a, b, n)

def discrete_log(b, a, n):
    """Oblicza dyskretny logarytm b = a^x mod n (naive implementation)"""
    # Uwaga: To jest naiwna implementacja, działająca tylko dla małych wartości
    # W SageMath używa się bardziej zaawansowanych algorytmów
    m = int(n ** 0.5) + 1
    table = {pow(a, j, n): j for j in range(m)}
    
    a_m = pow(a, m * (n - 2), n)  # a^(-m) mod n using Fermat's little theorem
    
    for i in range(m):
        y = (b * pow(a_m, i, n)) % n
        if y in table:
            return i * m + table[y]
    return None

def pohlig_hellman_algorithm(a, b, n, details=False):
    if details:
        print(f"Zagadnienie: {a}^x = {b} (mod {n}), można zastąpić przez: \n")
    
    # Factorize n-1
    factors = factorint(n-1)
    fa = [(p, e) for p, e in factors.items()]
    fl = len(fa)
    
    x = []
    y = []
    p_list = []
    e_list = []
    
    for i in range(fl):
        p = fa[i][0]
        e = fa[i][1]
        np = (n-1) // (p**e)
        bp = power_mod(b, np, n)
        ap = power_mod(a, np, n)
        
        disc = discrete_log(bp, ap, n)
        
        p_list.append(p)
        e_list.append(e)
        x.append(disc)
        y.append(p**e)
        
        if details:
            print(f"{ap}^x({p}) = {bp} (mod {n}) z rozwiązaniem x({p}) = {disc}")
    
    if details:
        print("\nZgodnie z twierdzeniem:")
        for i in range(fl):
            print(f"x = {x[i]} (mod {p_list[i]}^{e_list[i]})")
        
        # Oblicz wynik końcowy
        moduli = [p**e for p, e in zip(p_list, e_list)]
        result = crt(moduli, x)[0]
        print(f"\nWynik końcowy: x = {result}")
    
    # Oblicz wynik końcowy za pomocą Chińskiego Twierdzenia o Resztach
    moduli = [p**e for p, e in zip(p_list, e_list)]
    return crt(moduli, x)[0]
