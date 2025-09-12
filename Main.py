"""
Máquina de Turing para operaciones aritméticas enteras.

Soporta:
 - Adición (a + b)
 - Sustracción (a - b)
 - Multiplicación (a * b)
 - División entera (a // b) -> devuelve (cociente, resto)
 - Potenciación entera (a ^ b) con b >= 0
 - Raíz cuadrada entera (floor(sqrt(a))) con a >= 0

Representación interna:
 - Cada entero se convierte a (signo, binstr) donde `binstr` es la parte absoluta en binario
   con MSB a la izquierda y sin ceros líderes (a menos que sea "0").
 - Las operaciones bit a bit se realizan sobre las cadenas binarias, simulando manipulación
   de cintas y movimientos de cabezas (concepto TM) aunque el código sea Python.
"""

from typing import Tuple


# ----------------------
# UTILITARIOS: conversiones y utils para binarios con signo
# ----------------------
def int_to_signed_bin(n: int) -> Tuple[str, str]:
    """
    Convierte un entero n a (signo, binstr).
    - signo: '+' o '-'
    - binstr: cadena binaria absoluta sin ceros iniciales, '0' si n == 0
    Ejemplo: -6 -> ('-', '110')
    """
    if n == 0:
        return '+', '0'
    sign = '-' if n < 0 else '+'
    b = bin(abs(n))[2:]  # '0b...' -> cortamos '0b'
    return sign, b


def signed_bin_to_int(sign: str, b: str) -> int:
    """
    Convierte (signo, binstr) a entero.
    Si binstr == '0' devuelve 0 (sin signo negativo).
    """
    v = int(b, 2) if b and b != '0' else 0
    return -v if sign == '-' and v != 0 else v


def strip_leading_zeros(b: str) -> str:
    """Quitar ceros a la izquierda; mantener '0' si el número es cero."""
    s = b.lstrip('0')
    return s if s != '' else '0'


def cmp_bin(a: str, b: str) -> int:
    """
    Compara dos strings binarios sin signo (MSB-left).
    Retorna 1 si a > b, 0 si iguales, -1 si a < b.
    Útil para comparaciones en división y resta.
    """
    a = strip_leading_zeros(a)
    b = strip_leading_zeros(b)
    if len(a) > len(b): return 1
    if len(a) < len(b): return -1
    if a > b: return 1
    if a < b: return -1
    return 0


# ----------------------
# OPERACIONES BINARIAS (manipulación de cadenas) — MSB a la izquierda
# Estas funciones simulan lo que una TM haría en la cinta (leer/escribir/avanzar).
# ----------------------
def bin_add(a: str, b: str) -> str:
    """
    Suma dos cadenas binarias sin signo (a + b) devolviendo el resultado sin ceros líderes.
    Algoritmo: suma bit a bit desde LSB con carry.
    Complejidad: O(max(len(a), len(b))).
    """
    a = strip_leading_zeros(a)
    b = strip_leading_zeros(b)
    ra = a[::-1]  # invertir para indexar desde LSB (simula mover cabeza a la derecha)
    rb = b[::-1]
    carry = 0
    res = []
    for i in range(max(len(ra), len(rb))):
        ai = int(ra[i]) if i < len(ra) else 0
        bi = int(rb[i]) if i < len(rb) else 0
        s = ai + bi + carry
        res.append(str(s % 2))
        carry = s // 2
    if carry:
        res.append('1')
    # reconstruir y quitar ceros a la izquierda
    return strip_leading_zeros(''.join(res[::-1]))


def bin_subtract(a: str, b: str) -> str:
    """
    Resta absoluta a - b asumiendo a >= b >= 0 (ambas sin signo).
    Algoritmo: resta bit a bit con borrow (prestado).
    Retorna resultado sin ceros líderes.
    """
    if cmp_bin(a, b) == 0:
        return '0'
    if cmp_bin(a, b) < 0:
        raise ValueError("bin_subtract: requiere a >= b")
    ra = a[::-1]
    rb = b[::-1]
    borrow = 0
    res = []
    for i in range(len(ra)):
        ai = int(ra[i])
        bi = int(rb[i]) if i < len(rb) else 0
        diff = ai - bi - borrow
        if diff < 0:
            diff += 2
            borrow = 1
        else:
            borrow = 0
        res.append(str(diff))
    return strip_leading_zeros(''.join(res[::-1]))


def bin_mul(a: str, b: str) -> str:
    """
    Multiplicación binaria por shift-and-add:
    Recorremos cada bit del multiplicador desde LSB; si es 1 añadimos el
    multiplicando desplazado (append de ceros al final).
    Ejemplo: 101 * 11 = 101 + 1010 = 1111 (en binario).
    """
    a = strip_leading_zeros(a)
    b = strip_leading_zeros(b)
    if a == '0' or b == '0':
        return '0'
    result = '0'
    L = len(b)
    # Iterar desde el LSB (b[L-1]) hasta MSB
    for i in range(L):
        bit = b[L - 1 - i]
        if bit == '1':
            # shift left i posiciones = añadir i ceros al final (MSB-left representation)
            shifted = a + ('0' * i)
            result = bin_add(result, shifted)
    return strip_leading_zeros(result)


def bin_divmod(dividend: str, divisor: str) -> Tuple[str, str]:
    """
    División larga binaria (abs values). Retorna (quotient, remainder).
    Algoritmo (similar a división larga en base 2):
     - Recorre bits del dividendo de MSB a LSB
     - Mantiene un 'remainder' parcial; cada paso shift-left + añadir bit.
     - Si remainder >= divisor -> remainder -= divisor, quotient_bit = 1; else quotient_bit = 0
    Requisitos: divisor != '0'
    """
    dividend = strip_leading_zeros(dividend)
    divisor = strip_leading_zeros(divisor)
    if divisor == '0':
        raise ZeroDivisionError("División por cero")
    if cmp_bin(dividend, divisor) < 0:
        return '0', dividend
    quotient_bits = []
    remainder = '0'
    for bit in dividend:  # recorrido de MSB a LSB
        # remainder = (remainder << 1) + bit
        if remainder == '0':
            remainder = bit
        else:
            remainder = remainder + bit
        remainder = strip_leading_zeros(remainder)
        if cmp_bin(remainder, divisor) >= 0:
            remainder = bin_subtract(remainder, divisor)
            quotient_bits.append('1')
        else:
            quotient_bits.append('0')
    q = strip_leading_zeros(''.join(quotient_bits))
    r = strip_leading_zeros(remainder)
    return q, r


# ----------------------
# CLASE: TMSimulator — operaciones de alto nivel usando las funciones binarias
# ----------------------
class TMSimulator:
    """Encapsula operaciones aritméticas usando las funciones binarias definidas arriba."""

    @staticmethod
    def add(a: int, b: int) -> int:
        """
        Suma con soporte de signos:
        - Si los signos iguales => suma absoluta y mantener signo.
        - Si signos distintos => resta absoluta (mayor - menor) y signo del mayor.
        """
        sa, ba = int_to_signed_bin(a)
        sb, bb = int_to_signed_bin(b)
        # if both zero
        if ba == '0' and bb == '0':
            return 0
        if sa == sb:
            res_abs = bin_add(ba, bb)
            return signed_bin_to_int(sa, res_abs)
        # signos distintos: hacemos resta absoluta del mayor menos el menor
        cmpv = cmp_bin(ba, bb)
        if cmpv == 0:
            return 0
        if cmpv > 0:
            res_abs = bin_subtract(ba, bb)
            return signed_bin_to_int(sa, res_abs)
        else:
            res_abs = bin_subtract(bb, ba)
            return signed_bin_to_int(sb, res_abs)

    @staticmethod
    def subtract(a: int, b: int) -> int:
        """Resta simple: a - b = a + (-b)"""
        return TMSimulator.add(a, -b)

    @staticmethod
    def multiply(a: int, b: int) -> int:
        """
        Multiplicación con manejo de signos: signo = '-' si signos distintos.
        Usa bin_mul en las partes absolutas.
        """
        sa, ba = int_to_signed_bin(a)
        sb, bb = int_to_signed_bin(b)
        if ba == '0' or bb == '0':
            return 0
        res_abs = bin_mul(ba, bb)
        res_sign = '-' if (sa != sb) else '+'
        return signed_bin_to_int(res_sign, res_abs)

    @staticmethod
    def divide(a: int, b: int) -> Tuple[int, int]:
        """
        División entera con truncamiento hacia cero (como int(a/b) en C).
        Retorna (cociente, resto).
        - controla división por cero.
        - resto calculado como: remainder = a - (quotient * b) para coherencia.
        """
        if b == 0:
            raise ZeroDivisionError("División por cero")
        sa, ba = int_to_signed_bin(a)
        sb, bb = int_to_signed_bin(b)
        # si absolute divisor > absolute dividend -> cociente 0
        q_abs_bin, r_abs_bin = bin_divmod(ba, bb)
        q_abs = int(q_abs_bin, 2) if q_abs_bin != '0' else 0
        # signo del cociente = xor de signos de operandos
        q_sign = '-' if (a < 0) ^ (b < 0) else '+'
        quotient = -q_abs if q_sign == '-' and q_abs != 0 else q_abs
        # resto con signo del dividendo para consistencia:
        remainder = a - (quotient * b)
        return quotient, remainder

    @staticmethod
    def power(base: int, exp: int) -> int:
        """
        Potencia entera por exponentiation by squaring.
        Restricción: exp >= 0 (si exp < 0 se lanza ValueError).
        La función trabaja con las partes absolutas en binario y mantiene el signo final.
        """
        if exp < 0:
            raise ValueError("Exponentes negativos no admitidos (resultados fraccionarios).")
        if exp == 0:
            return 1
        sign_b, b_bin = int_to_signed_bin(base)
        # si la base es 0, resultado es 0 (para exp > 0)
        if b_bin == '0':
            return 0
        result_bin = '1'  # resultado absoluto en binario
        b_cur = b_bin
        e = exp
        # loop: si el bit actual de e es 1, multiplicamos result *= b_cur
        while e > 0:
            if e & 1:
                result_bin = bin_mul(result_bin, b_cur)
            b_cur = bin_mul(b_cur, b_cur)  # b_cur = b_cur^2
            e >>= 1
        res_sign = '+'
        if sign_b == '-' and (exp % 2 == 1):
            res_sign = '-'
        return signed_bin_to_int(res_sign, strip_leading_zeros(result_bin))

    @staticmethod
    def isqrt(n: int) -> int:
        """
        Raíz cuadrada entera (floor). Requiere n >= 0.
        Algoritmo: búsqueda binaria sobre [0, n] y comprobar mid*mid <= n usando bin_mul.
        """
        if n < 0:
            raise ValueError("Raíz cuadrada de número negativo no soportada.")
        low, high = 0, n
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            _, mid_bin = int_to_signed_bin(mid)
            mid_sq_bin = bin_mul(mid_bin, mid_bin)
            mid_sq = int(mid_sq_bin, 2) if mid_sq_bin != '0' else 0
            if mid_sq <= n:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans


# ----------------------
# INTERFAZ: Menú y control de flujo
# ----------------------
def preguntar_volver() -> bool:
    while True:
        resp = input("\n¿Deseas volver al menú? (S=Sí / N=No): ").strip().lower()
        if resp in ('s', 'S', 'si'):
            return True
        if resp in ('n', 'N', 'no'):
            return False
        print("Respuesta no reconocida. Escribe 'S' para sí o 'N' para no.")


def menu():
    """
    Menú principal:
    - Muestra las opciones.
    - Ejecuta la operación seleccionada.
    - Tras mostrar resultado pregunta si volver al menú o salir.
    """
    tmsim = TMSimulator()
    menu_text = (
        "\nMáquina de Turing aritmética (simulada)\n"
        "Elige operación:\n"
        " 1) Adición (a + b)\n"
        " 2) Sustracción (a - b)\n"
        " 3) Multiplicación (a * b)\n"
        " 4) División entera (a / b)\n"
        " 5) Potenciación (a ^ b)  (b debe ser entero >= 0)\n"
        " 6) Raíz cuadrada entera (sqrt(a)) (a debe ser >= 0)\n"
        " 0) Salir\n"
    )

    while True:
        print(menu_text)
        opt = input("Ingresa la opción: ").strip()
        if opt == '0':
            print("Saliendo.....")
            break
        if opt not in {'1', '2', '3', '4', '5', '6'}:
            print("Opción no válida. Intenta de nuevo.")
            continue

        try:
            # Opción 6 solicita solo un entero; el resto dos.
            if opt == '6':
                raw = input("Ingresa un entero (a >= 0): ").strip()
                try:
                    a = int(raw)
                except ValueError:
                    print("Entrada inválida. Debes ingresar un entero.")
                    if not preguntar_volver():
                        break
                    else:
                        continue
                try:
                    res = tmsim.isqrt(a)
                    print(f"\nsqrt({a}) → {res}")
                except ValueError as e:
                    print("Error:", e)
                # Preguntar al final si volver o salir
                if not preguntar_volver():
                    print("Saliendo.....")
                    break
                else:
                    continue

            # Para las demás opciones pedimos dos enteros
            raw_a = input("Ingresa primer entero (a): ").strip()
            raw_b = input("Ingresa segundo entero (b): ").strip()
            try:
                a = int(raw_a)
                b = int(raw_b)
            except ValueError:
                print("Entrada inválida; ingresa enteros válidos.")
                if not preguntar_volver():
                    break
                else:
                    continue

            # Ejecución según opción seleccionada
            if opt == '1':
                resultado = tmsim.add(a, b)
                print(f"\n{a} + {b} = {resultado}")
            elif opt == '2':
                resultado = tmsim.subtract(a, b)
                print(f"\n{a} - {b} = {resultado}")
            elif opt == '3':
                resultado = tmsim.multiply(a, b)
                print(f"\n{a} * {b} = {resultado}")
            elif opt == '4':
                try:
                    q, r = tmsim.divide(a, b)
                    print(f"\n{a} // {b} = {q}, resto = {r}")
                except ZeroDivisionError:
                    print("\nError: división por cero.")
            elif opt == '5':
                try:
                    resultado = tmsim.power(a, b)
                    print(f"\n{a} ^ {b} = {resultado}")
                except ValueError as e:
                    print("\nError:", e)

            # Preguntar tras ejecutar la operación si volver al menú o salir.
            if not preguntar_volver():
                print("Saliendo.....")
                break
            # else: continuar al principio del while y reimprimir el menú

        except Exception as e:
            # Capturamos cualquier excepción imprevista y permitimos al usuario decidir volver o salir.
            print("Ocurrió un error inesperado:", str(e))
            if not preguntar_volver():
                break
# ----------------------
# PUNTO DE ENTRADA
# ----------------------
if __name__ == '__main__':
    menu()