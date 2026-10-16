# Francisco Ivan Cortes Ruvalcaba
#
# Avance 2 - Sistema de comandas para restaurante (POO)
# Descripción: el sistema modela los pedidos de un restaurante. La clase base
# PedidoRestaurante representa una orden en mesa (cliente, mesero, artículos,
# total y estado). La subclase PedidoDomicilio hereda de ella y agrega datos
# propios de un pedido a domicilio (dirección y costo de envío). Se aplican
# Encapsulamiento (atributos privados/protegidos con @property), Herencia
# (super()) y Polimorfismo (sobrescritura de métodos).


# ==========================================
# Creación de la clase base (Superclase)
# ==========================================
class PedidoRestaurante:
    def __init__(self, numero_mesa, nombre_mesero, cliente):
        self.numero_mesa = numero_mesa
        self.nombre_mesero = nombre_mesero
        self.cliente = cliente
        # Aplicación de Encapsulamiento:
        self.__total_pagar = 0      # Atributo privado (solo accesible vía property)
        self._articulos = []        # Atributo protegido (para la clase y sus subclases)
        self._estado = "en espera"  # Atributo protegido

    # Getter de total_pagar mediante @property
    @property
    def total_pagar(self):
        return self.__total_pagar

    # Setter de total_pagar con validación (no se permiten negativos ni valores no numéricos)
    @total_pagar.setter
    def total_pagar(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El total a pagar debe ser un número mayor o igual a 0.")
        self.__total_pagar = valor

    # Getter de estado
    @property
    def estado(self):
        return self._estado

    # Setter de estado con validación (no se permiten estados vacíos)
    @estado.setter
    def estado(self, nuevo_estado):
        if not isinstance(nuevo_estado, str) or not nuevo_estado.strip():
            raise ValueError("El estado del pedido no puede estar vacío.")
        self._estado = nuevo_estado

    # Método operativo 1: agregar artículos a la cuenta
    def agregar_articulo(self, nombre_articulo, precio):
        if not nombre_articulo.strip() or precio <= 0:
            print(f" No se pudo agregar el artículo: nombre vacío o precio inválido (${precio}).")
            return
        self._articulos.append(nombre_articulo)
        self.total_pagar += precio  # Pasa por el setter, que valida el valor
        print(f" Se agregó {nombre_articulo} a la mesa {self.numero_mesa}, +${precio}")

    # Método operativo 2: cambiar el estado del pedido
    def avanzar_estado(self, nuevo_estado):
        self.estado = nuevo_estado  # Pasa por el setter con validación
        print(f"Mesa {self.numero_mesa}: El pedido de {self.cliente} está {self.estado}.")

    # Método operativo 3: aplicar descuento (validando el porcentaje)
    def aplicar_descuento(self, porcentaje):
        if not 0 < porcentaje <= 100:
            print(f" Descuento inválido ({porcentaje}%). Debe estar entre 1 y 100.")
            return
        descuento = self.total_pagar * (porcentaje / 100)
        self.total_pagar -= descuento
        print(f"Se aplicó un descuento del {porcentaje}% a la Mesa {self.numero_mesa}. "
              f"Total nuevo: ${self.total_pagar:.2f}")

    # Método operativo 4: imprimir la cuenta (será sobrescrito en la subclase)
    def imprimir_cuenta(self):
        print("\n" + "=" * 34)
        print(f"  Cuenta - MESA {self.numero_mesa}")
        print("=" * 34)
        print(f"Cliente: {self.cliente}")
        print(f"Atendió: {self.nombre_mesero}")
        print(f"Estado del pedido: {self.estado}")
        print("Artículos del consumo:")
        for articulo in self._articulos:
            print(f" - {articulo}")
        print("-" * 34)
        print(f"TOTAL A PAGAR: ${self.total_pagar:.2f}")
        print("=" * 34 + "\n")


# ==========================================
# Uso de super() y Herencia (Subclase)
# ==========================================
class PedidoDomicilio(PedidoRestaurante):
    def __init__(self, numero_pedido, nombre_mesero, cliente, direccion_entrega, costo_envio):
        # super() reutiliza el constructor de la clase base
        super().__init__(numero_pedido, nombre_mesero, cliente)
        # Atributos nuevos propios de la subclase
        self.direccion_entrega = direccion_entrega
        self._costo_envio = costo_envio  # Atributo protegido

    # Getter del costo de envío
    @property
    def costo_envio(self):
        return self._costo_envio

    # Setter con validación (no se permiten envíos negativos)
    @costo_envio.setter
    def costo_envio(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El costo de envío no puede ser negativo.")
        self._costo_envio = valor

    # Método operativo 5 (propio de la subclase): total incluyendo el envío
    def total_con_envio(self):
        return self.total_pagar + self.costo_envio

    # Método operativo 6 (propio de la subclase): marcar salida del repartidor
    def enviar_pedido(self):
        self.avanzar_estado("En camino al domicilio")
        print(f" Pedido de {self.cliente} enviado a: {self.direccion_entrega}")

    # ==========================================
    # Sobrescritura de métodos (Polimorfismo)
    # ==========================================
    def imprimir_cuenta(self):
        print("\n" + "=" * 34)
        print(f"  Cuenta - DOMICILIO #{self.numero_mesa}")
        print("=" * 34)
        print(f"Cliente: {self.cliente}")
        print(f"Atendió: {self.nombre_mesero}")
        print(f"Dirección de entrega: {self.direccion_entrega}")
        print(f"Estado del pedido: {self.estado}")
        print("Artículos del consumo:")
        for articulo in self._articulos:
            print(f" - {articulo}")
        print("-" * 34)
        print(f"Subtotal: ${self.total_pagar:.2f}")
        print(f"Envío:    ${self.costo_envio:.2f}")
        print(f"TOTAL A PAGAR: ${self.total_con_envio():.2f}")
        print("=" * 34 + "\n")


# ==========================================
# Instanciación y pruebas
# ==========================================
print("\n INICIANDO PEDIDOS")

# Objeto 1: clase base
pedido_1 = PedidoRestaurante(5, "Zoe", "Lopez")
pedido_1.agregar_articulo("Hamburguesa sirlon", 167)
pedido_1.agregar_articulo("Cerveza artesanal", 65)
pedido_1.avanzar_estado("Preparándose en cocina")

# Objetos 2 y 3: subclase
pedido_2 = PedidoDomicilio("D-01", "Dominic", "Cristian", "Av. Patria 123, Zapopan", 35)
pedido_2.agregar_articulo("Café americano", 45)
pedido_2.agregar_articulo("Rebanada de pastel", 67)
pedido_2.aplicar_descuento(10)
pedido_2.enviar_pedido()

pedido_3 = PedidoDomicilio("D-02", "Ivan", "Ana", "Calle Hidalgo 45, Tonalá", 50)
pedido_3.agregar_articulo("Pizza Jumbo", 250)
pedido_3.agregar_articulo("Limonada c/mineral", 40)
pedido_3.agregar_articulo("Limonada c/mineral", 40)
pedido_3.avanzar_estado("Pendiente por pagar")

# --- Prueba de Encapsulamiento ---
print("\n PRUEBAS DE ENCAPSULAMIENTO")
print(f"Total de pedido_1 (getter): ${pedido_1.total_pagar}")

try:
    pedido_1.total_pagar = -100  # El setter rechaza valores negativos
except ValueError as error:
    print(f"Restricción aplicada: {error}")

try:
    pedido_1.estado = "   "  # El setter rechaza estados vacíos
except ValueError as error:
    print(f"Restricción aplicada: {error}")

try:
    pedido_3.costo_envio = -20  # El setter rechaza envíos negativos
except ValueError as error:
    print(f"Restricción aplicada: {error}")

pedido_1.agregar_articulo("", 30)       # Artículo inválido
pedido_1.aplicar_descuento(150)         # Descuento inválido

# El atributo privado no es accesible directamente desde fuera de la clase
print(f"¿Existe pedido_1.__total_pagar? {hasattr(pedido_1, '__total_pagar')}")

# --- Prueba de Independencia de datos (self) ---
print("\n INDEPENDENCIA DE DATOS ENTRE INSTANCIAS")
print(f"Total pedido_1: ${pedido_1.total_pagar:.2f} | "
      f"Total pedido_2: ${pedido_2.total_pagar:.2f} | "
      f"Total pedido_3: ${pedido_3.total_pagar:.2f}")

# --- Prueba de Herencia y método sobrescrito (Polimorfismo) ---
print("\n IMPRIMIENDO TICKETS (mismo método, distinto comportamiento)")
for pedido in (pedido_1, pedido_2, pedido_3):
    pedido.imprimir_cuenta()
