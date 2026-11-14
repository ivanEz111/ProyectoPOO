# Francisco Ivan Cortes Ruvalcaba
#
# Clases del sistema de comandas para restaurante
# Contiene:
#   - ItemPedido: clase auxiliar usada para Composición (un pedido "tiene" artículos).
#   - PedidoRestaurante: clase base (Encapsulamiento + Composición).
#   - PedidoDomicilio: subclase (Herencia + Polimorfismo).

# Clase auxiliar para Composición
class ItemPedido:
    def __init__(self, nombre, precio, cantidad=1):
        # Validaciones: el artículo debe tener nombre, precio positivo y cantidad >= 1
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El artículo debe tener un nombre.")
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError(f"Precio inválido para '{nombre}': ${precio}.")
        if not isinstance(cantidad, int) or cantidad < 1:
            raise ValueError(f"Cantidad inválida para '{nombre}': {cantidad}.")
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    # Calcula el subtotal del artículo (precio * cantidad)
    def subtotal(self):
        return self.precio * self.cantidad

    # Texto descriptivo del artículo (usado por el pedido de forma delegada)
    def descripcion(self):
        return f"{self.cantidad} x {self.nombre} (${self.precio:.2f} c/u) = ${self.subtotal():.2f}"


# Creación de la clase base (Superclase):
class PedidoRestaurante:
    def __init__(self, numero_mesa, nombre_mesero, cliente):
        self.numero_mesa = numero_mesa
        self.nombre_mesero = nombre_mesero
        self.cliente = cliente
        # Aplicación de Encapsulamiento:
        self.__total_pagar = 0      # Atributo privado (solo accesible vía property)
        self._estado = "en espera"  # Atributo protegido
        # COMPOSICIÓN: un pedido "tiene" una colección de objetos ItemPedido
        self._articulos = []

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

    # Acceso de solo lectura a los artículos (tupla, para que no se modifique desde fuera)
    @property
    def articulos(self):
        return tuple(self._articulos)

    # Método operativo 1: agregar artículos (crea un ItemPedido y lo guarda: composición)
    def agregar_articulo(self, nombre_articulo, precio, cantidad=1):
        try:
            item = ItemPedido(nombre_articulo, precio, cantidad)
        except ValueError as error:
            print(f" No se pudo agregar el artículo: {error}")
            return
        self._articulos.append(item)
        # Delegación: el subtotal lo calcula el objeto ItemPedido
        self.total_pagar += item.subtotal()
        print(f" Se agregó {item.cantidad} x {item.nombre} al pedido {self.numero_mesa}, "
              f"+${item.subtotal():.2f}")

    # Método operativo 2: cambiar el estado del pedido
    def avanzar_estado(self, nuevo_estado):
        self.estado = nuevo_estado  # Pasa por el setter con validación
        print(f"Pedido {self.numero_mesa}: El pedido de {self.cliente} está {self.estado}.")

    # Método operativo 3: aplicar descuento (validando el porcentaje)
    def aplicar_descuento(self, porcentaje):
        if not 0 < porcentaje <= 100:
            print(f" Descuento inválido ({porcentaje}%). Debe estar entre 1 y 100.")
            return
        descuento = self.total_pagar * (porcentaje / 100)
        self.total_pagar -= descuento
        print(f"Se aplicó un descuento del {porcentaje}% al pedido {self.numero_mesa}. "
              f"Total nuevo: ${self.total_pagar:.2f}")

    # Método operativo 4: cantidad total de piezas (delegando en cada ItemPedido)
    def total_piezas(self):
        return sum(item.cantidad for item in self._articulos)

    # Método operativo 5: imprimir la cuenta (será sobrescrito en la subclase)
    def imprimir_cuenta(self):
        print("\n" + "=" * 46)
        print(f"  Cuenta - MESA {self.numero_mesa}")
        print("=" * 46)
        print(f"Cliente: {self.cliente}")
        print(f"Atendió: {self.nombre_mesero}")
        print(f"Estado del pedido: {self.estado}")
        print("Artículos del consumo:")
        for item in self._articulos:
            print(f" - {item.descripcion()}")  # Delegación a ItemPedido
        print("-" * 46)
        print(f"TOTAL A PAGAR: ${self.total_pagar:.2f}")
        print("=" * 46 + "\n")

# Uso de super() y Herencia (Subclase)
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

    # Método propio de la subclase: total incluyendo el envío
    def total_con_envio(self):
        return self.total_pagar + self.costo_envio

    # Método propio de la subclase: marcar salida del repartidor
    def enviar_pedido(self):
        self.avanzar_estado("En camino al domicilio")
        print(f" Pedido de {self.cliente} enviado a: {self.direccion_entrega}")

    # Sobrescritura de métodos (Polimorfismo)
    def imprimir_cuenta(self):
        print("\n" + "=" * 46)
        print(f"  Cuenta - DOMICILIO #{self.numero_mesa}")
        print("=" * 46)
        print(f"Cliente: {self.cliente}")
        print(f"Atendió: {self.nombre_mesero}")
        print(f"Dirección de entrega: {self.direccion_entrega}")
        print(f"Estado del pedido: {self.estado}")
        print("Artículos del consumo:")
        for item in self._articulos:
            print(f" - {item.descripcion()}")  # Delegación a ItemPedido
        print("-" * 46)
        print(f"Subtotal: ${self.total_pagar:.2f}")
        print(f"Envío:    ${self.costo_envio:.2f}")
        print(f"TOTAL A PAGAR: ${self.total_con_envio():.2f}")
        print("=" * 46 + "\n")
