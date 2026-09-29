"""Resolver durante el bloque sin IA. No se usa en la aplicacion."""


def contar_pendientes(pedidos: list[dict]) -> int:
    total = 0
    for pedido in pedidos:
        if pedido['estado'] == 'pendiente':
            total += 1
        return total  # Revisar este comportamiento, incluido el caso de lista vacia.


if __name__ == '__main__':
    datos = [{'estado': 'pendiente'}, {'estado': 'completado'}, {'estado': 'pendiente'}]
    print('Resultado:', contar_pendientes(datos), '(esperado: 2)')
    print('Lista vacia:', contar_pendientes([]), '(esperado: 0)')
