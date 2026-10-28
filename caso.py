from abc import ABC, abstractmethod

# --- 1. CONSTRUCTOR, ENCAPSULAMIENTO Y ATRIBUTO PROTEGIDO (Lab 02 y 03) ---
class Matricula:
    def __init__(self, estudiante, reglas=(), base=60.00):  # método constructor
        if not estudiante:
            raise ValueError("El estudiante no puede estar vacío.")
        self._estudiante = estudiante  # atributo protegido
        self._reglas, self._base = list(reglas), base

    @property
    def estudiante(self):  # solo lectura desde afuera
        return self._estudiante

    def calcular_costo(self):
        monto = self._base
        for regla in self._reglas:  # sin reglas, paga solo el derecho base
            monto = regla.aplicar(monto)
        return monto

# --- 2. HERENCIA Y POLIMORFISMO (Lab 04 y 05) ---
class Extemporanea(Matricula):
    def calcular_costo(self):
        return super().calcular_costo() + 15.00

class IndiceDesaprobatorio(Matricula):
    def calcular_costo(self):
        return super().calcular_costo() + 15.00

class BecaViolencia(Matricula):
    def calcular_costo(self):
        return super().calcular_costo() * 0.5

# --- 3. HERENCIA MÚLTIPLE: LAS DOS VERSIONES DEL CASO ---
class CombinadaV1(BecaViolencia, IndiceDesaprobatorio, Extemporanea): pass  # Programador 1

class CombinadaV2(IndiceDesaprobatorio, Extemporanea, BecaViolencia): pass  # Programador 2

# --- 4. ABSTRACCIÓN: REDISEÑO CON REGLAS EXPLÍCITAS (Lab 04) ---
class Regla(ABC):  # clase abstracta: no se puede instanciar
    def __init__(self, valor):
        self._valor = valor

    @abstractmethod
    def aplicar(self, monto):
        pass

class Recargo(Regla):
    def aplicar(self, monto):
        return monto + self._valor

class Descuento(Regla):
    def aplicar(self, monto):
        return monto * (1 - self._valor)

# --- 5. BLOQUE DE PRUEBA PRINCIPAL ---
if __name__ == "__main__":
    for v in (CombinadaV1, CombinadaV2):  # MRO y monto de cada versión
        print(" -> ".join(c.__name__ for c in v.__mro__[:-1]), f"= S/ {v('Luis').calcular_costo():.2f}")
    try:
        class Invalida(Matricula, BecaViolencia): pass  # clase general escrita primero
    except TypeError as e:
        print(f"Error capturado correctamente: {e}")
    try:
        Matricula("")  # el constructor valida
    except ValueError as e:
        print(f"Error capturado correctamente: {e}")
    ext, ind, beca = Recargo(15), Recargo(15), Descuento(0.5)
    for nombre in ("Luis Huamaní", "Rosa Ccahuana"):  # misma situación, mismo orden
        m = Matricula(nombre, [ext, ind, beca])
        print(f"{m.estudiante}: S/ {m.calcular_costo():.2f}")
    print(f"Con beca primero: S/ {Matricula('Luis', [beca, ext, ind]).calcular_costo():.2f}")
