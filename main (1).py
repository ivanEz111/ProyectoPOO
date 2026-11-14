# Francisco Ivan Cortes Ruvalcaba
# 3ro de cibersegurida
# Avance 3 
# contiene las importaciones, la instanciación de objetos y las pruebas

# Importación de las clases desde el módulo modelos.py
from modelos import ItemPedido, PedidoRestaurante, PedidoDomicilio

# Instanciación y pruebas
print("\n INICIANDO PEDIDOS")

# Objeto 1: clase base
pedido_1 = PedidoRestaurante(5, "Zoe", "Lopez")
pedido_1.agregar_articulo("Hamburguesa sirlon", 167)
pedido_1.agregar_articulo("Cerveza artesanal", 65)
pedido_1.avanzar_estado("Preparándose en cocina")

# Objetos 2 y 3: subclase (Herencia)
pedido_2 = PedidoDomicilio("D-01", "Dominic", "Cristian", "Av. Patria 123, Zapopan", 35)
pedido_2.agregar_articulo("Café americano", 45)
pedido_2.agregar_articulo("Rebanada de pastel", 67)
pedido_2.aplicar_descuento(10)
pedido_2.enviar_pedido()

pedido_3 = PedidoDomicilio("D-02", "Ivan", "Ana", "Calle Hidalgo 45, Tonalá", 50)
pedido_3.agregar_articulo("Pizza Jumbo", 250)
pedido_3.agregar_articulo("Limonada c/mineral", 40, 2)  # cantidad = 2
pedido_3.avanzar_estado("Pendiente por pagar")

# -Prueba de Composición :
print("\n PRUEBAS DE COMPOSICIÓN")
print(f"pedido_3 tiene {len(pedido_3.articulos)} tipos de artículo y {pedido_3.total_piezas()} piezas.")
# Se invoca un método del objeto contenido (ItemPedido) a través del pedido
primer_item = pedido_3.articulos[0]
print(f"Primer artículo de pedido_3: {primer_item.descripcion()}")
print(f"Subtotal del primer artículo: ${primer_item.subtotal():.2f}")
# Un ItemPedido también existe de forma independiente
item_suelto = ItemPedido("Agua natural", 25, 3)
print(f"Item independiente: {item_suelto.descripcion()}")

# -Prueba de Encapsulamiento:
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

pedido_1.agregar_articulo("", 30)       # Artículo inválido (lo rechaza ItemPedido)
pedido_1.agregar_articulo("Papas", 50, 0)  # Cantidad inválida
pedido_1.aplicar_descuento(150)         # Descuento inválido

# El atributo privado no es accesible directamente desde fuera de la clase
print(f"¿Existe pedido_1.__total_pagar? {hasattr(pedido_1, '__total_pagar')}")

# -Prueba de Independencia de datos (self):
print("\n INDEPENDENCIA DE DATOS ENTRE INSTANCIAS")
print(f"Total pedido_1: ${pedido_1.total_pagar:.2f} | "
      f"Total pedido_2: ${pedido_2.total_pagar:.2f} | "
      f"Total pedido_3: ${pedido_3.total_pagar:.2f}")

# -Prueba de Polimorfismo (método sobrescrito):
print("\n IMPRIMIENDO TICKETS (mismo método, distinto comportamiento)")
for pedido in (pedido_1, pedido_2, pedido_3):
    pedido.imprimir_cuenta()
