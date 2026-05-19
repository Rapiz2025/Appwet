"""
chatbot_dona_lila.py
=====================

Este script implementa un chatbot sencillo en la consola para el restaurante
Doña Lila Express. Está pensado como un prototipo que muestra el flujo de
conversación descrito en el reporte: permite al usuario ver el menú,
realizar un pedido paso a paso, añadir bebidas, calcular el total y
mostrar un resumen antes de confirmar.

El objetivo es ilustrar cómo se puede manejar la lógica del chatbot en
Python. No se conecta a WhatsApp ni a un panel de administración; toda
la interacción sucede en la terminal.

Funciones principales:

* `mostrar_menu()`: Presenta las categorías y productos disponibles.
* `hacer_pedido()`: Recoge la información del pedido a través de preguntas
  sucesivas y devuelve un diccionario con el pedido completo.
* `mostrar_resumen(pedido)`: Muestra el resumen del pedido y calcula el
  total.
* `main()`: Punto de entrada; gestiona el menú principal y permite
  realizar múltiples operaciones.

Nota: Los precios y productos se basan en el menú proporcionado en el
enunciado. El script está diseñado para ser fácil de leer y modificar.
"""

from __future__ import annotations

import sys
from typing import Dict, List, Tuple


# Definición del menú oficial con precios
MENU = {
    "yaroas": {
        "yaroa_de_pollo_papa": {
            "nombre": "Yaroa de pollo con papa",
            "precios": {"pequeña": 200, "mediana": 300, "grande": 400},
        },
        "yaroa_de_res_papa": {
            "nombre": "Yaroa de res con papa",
            "precios": {"pequeña": 250, "mediana": 350, "grande": 450},
        },
        "yaroa_de_pollo_maduro": {
            "nombre": "Yaroa de pollo con plátano maduro",
            "precios": {"pequeña": 250, "mediana": 350, "grande": 450},
        },
        "yaroa_de_res_maduro": {
            "nombre": "Yaroa de res con plátano maduro",
            "precios": {"pequeña": 295, "mediana": 395, "grande": 495},
        },
        "yaroa_mixta": {
            "nombre": "Yaroa mixta",
            "precios": {"pequeña": 295, "mediana": 395, "grande": 495},
        },
    },
    "pizzas": {
        "pizza_pequena": {
            "nombre": "Pizza pequeña (4 pedazos)",
            "sabores": {
                "pepperoni": 250,
                "jamon": 250,
                "completa": 295,
            },
            "ingrediente_adicional": 100,
        },
        "pizza_mediana": {
            "nombre": "Pizza mediana (8 pedazos)",
            "sabores": {
                "pepperoni": 385,
                "jamon": 385,
                "completa": 525,
            },
            "ingrediente_adicional": 100,
        },
        "pizza_grande": {
            "nombre": "Pizza grande (12 pedazos)",
            "sabores": {
                "pepperoni": 600,
                "jamon": 600,
                "completa": 700,
            },
            "ingrediente_adicional": 100,
        },
    },
    "favoritos": {
        "club_sandwich": {"nombre": "Club sándwich con papa", "precio": 300},
        "pechurina": {"nombre": "Pechurina con papa", "precio": 300},
        "alitas": {"nombre": "Alitas", "precio": 450},
        "carne_salada": {"nombre": "Carne salada", "precio": 450},
    },
    "especialidades": {
        "mofongo_camarones": {"nombre": "Mofongo de camarones", "precio": 450},
        "camarones_crema": {"nombre": "Camarones a la crema", "precio": 450},
    },
    "bebidas": {
        "batidas": {
            "precio": 150,
            "sabores": ["lechosa", "zapote", "fresa", "exclusividades"],
        },
        "jugos_naturales": {
            "precio": 100,
        },
        "refrescos": {
            "pequeño": 30,
            "mediano": 75,
            "grande": 100,
            "jumbo": 150,
        },
        "agua": {"precio": 20},
    },
}


def corregir_entrada(palabra: str) -> str:
    """Corrige errores comunes de escritura."""
    equivalencias = {
        "piza": "pizza",
        "yaro": "yaroa",
        "pechurina": "pechurina",
        "club": "club_sandwich",
        "refreco": "refrescos",
    }
    return equivalencias.get(palabra.lower(), palabra.lower())


def mostrar_menu() -> None:
    """Muestra las categorías del menú."""
    print("\nCategorías disponibles:")
    print("1. Yaroas")
    print("2. Pizzas")
    print("3. Favoritos rápidos")
    print("4. Especialidades")
    print("5. Bebidas")


def seleccionar_categoria() -> str:
    """Pregunta al usuario la categoría y devuelve la clave interna."""
    while True:
        opcion = input("\nElige una categoría (1-5): ").strip()
        mapa = {
            "1": "yaroas",
            "2": "pizzas",
            "3": "favoritos",
            "4": "especialidades",
            "5": "bebidas",
        }
        if opcion in mapa:
            return mapa[opcion]
        print("Opción no válida. Intenta de nuevo.")


def elegir_yaroa() -> Tuple[str, str, int]:
    """Permite elegir un tipo de yaroa, tamaño y cantidad."""
    tipos = list(MENU["yaroas"].keys())
    print("\nTipos de yaroa:")
    for i, k in enumerate(tipos, 1):
        print(f"{i}. {MENU['yaroas'][k]['nombre']}")
    while True:
        i = input("Selecciona el tipo de yaroa (1-{}): ".format(len(tipos))).strip()
        if i.isdigit() and 1 <= int(i) <= len(tipos):
            tipo = tipos[int(i) - 1]
            break
        print("Entrada inválida.")
    tamanos = list(MENU["yaroas"][tipo]["precios"].keys())
    print("\nTamaños disponibles:")
    for j, t in enumerate(tamanos, 1):
        print(f"{j}. {t.title()} - RD${MENU['yaroas'][tipo]['precios'][t]}")
    while True:
        j = input("Elige un tamaño (1-{}): ".format(len(tamanos))).strip()
        if j.isdigit() and 1 <= int(j) <= len(tamanos):
            tamano = tamanos[int(j) - 1]
            break
        print("Entrada inválida.")
    while True:
        cant = input("Cantidad: ").strip()
        if cant.isdigit() and int(cant) > 0:
            cantidad = int(cant)
            break
        print("Ingresa un número entero positivo.")
    return tipo, tamano, cantidad


def elegir_pizza() -> Tuple[str, str, bool, int]:
    """Permite elegir una pizza, su sabor, ingrediente adicional y cantidad."""
    tamanos = list(MENU["pizzas"].keys())
    print("\nTamaños de pizza:")
    for i, k in enumerate(tamanos, 1):
        print(f"{i}. {MENU['pizzas'][k]['nombre']}")
    while True:
        i = input("Selecciona el tamaño de la pizza (1-{}): ".format(len(tamanos))).strip()
        if i.isdigit() and 1 <= int(i) <= len(tamanos):
            tipo = tamanos[int(i) - 1]
            break
        print("Entrada inválida.")
    sabores = list(MENU["pizzas"][tipo]["sabores"].keys())
    print("\nSabores de pizza:")
    for j, s in enumerate(sabores, 1):
        precio = MENU["pizzas"][tipo]["sabores"][s]
        print(f"{j}. {s.title()} - RD${precio}")
    while True:
        j = input("Elige un sabor (1-{}): ".format(len(sabores))).strip()
        if j.isdigit() and 1 <= int(j) <= len(sabores):
            sabor = sabores[int(j) - 1]
            break
        print("Entrada inválida.")
    add = input("¿Deseas ingrediente adicional? (s/n): ").strip().lower() == "s"
    while True:
        cant = input("Cantidad: ").strip()
        if cant.isdigit() and int(cant) > 0:
            cantidad = int(cant)
            break
        print("Ingresa un número entero positivo.")
    return tipo, sabor, add, cantidad


def elegir_favorito() -> Tuple[str, int]:
    """Permite elegir un favorito rápido y cantidad."""
    favs = list(MENU["favoritos"].keys())
    print("\nFavoritos rápidos:")
    for i, k in enumerate(favs, 1):
        print(f"{i}. {MENU['favoritos'][k]['nombre']} - RD${MENU['favoritos'][k]['precio']}")
    while True:
        i = input("Selecciona tu favorito (1-{}): ".format(len(favs))).strip()
        if i.isdigit() and 1 <= int(i) <= len(favs):
            fav = favs[int(i) - 1]
            break
        print("Entrada inválida.")
    while True:
        cant = input("Cantidad: ").strip()
        if cant.isdigit() and int(cant) > 0:
            cantidad = int(cant)
            break
        print("Ingresa un número entero positivo.")
    return fav, cantidad


def elegir_especialidad() -> Tuple[str, int]:
    """Permite elegir una especialidad y cantidad."""
    esp = list(MENU["especialidades"].keys())
    print("\nEspecialidades:")
    for i, k in enumerate(esp, 1):
        print(f"{i}. {MENU['especialidades'][k]['nombre']} - RD${MENU['especialidades'][k]['precio']}")
    while True:
        i = input("Selecciona la especialidad (1-{}): ".format(len(esp))).strip()
        if i.isdigit() and 1 <= int(i) <= len(esp):
            e = esp[int(i) - 1]
            break
        print("Entrada inválida.")
    while True:
        cant = input("Cantidad: ").strip()
        if cant.isdigit() and int(cant) > 0:
            cantidad = int(cant)
            break
        print("Ingresa un número entero positivo.")
    return e, cantidad


def elegir_bebida() -> Tuple[str, str | None, int, int]:
    """Permite elegir bebidas (tipo, sabor/tamaño, cantidad) o no agregar."""
    # Lista de tipos de bebida
    opciones = ["batidas", "jugos_naturales", "refrescos", "agua", "ninguna"]
    print("\n¿Deseas agregar una bebida?")
    for i, b in enumerate(opciones, 1):
        nombre = b.replace("_", " ").title()
        print(f"{i}. {nombre}")
    while True:
        i = input("Selecciona una opción (1-{}): ".format(len(opciones))).strip()
        if i.isdigit() and 1 <= int(i) <= len(opciones):
            tipo = opciones[int(i) - 1]
            break
        print("Entrada inválida.")
    if tipo == "ninguna":
        return tipo, None, 0, 0
    # Batidas: elegir sabor
    if tipo == "batidas":
        sabores = MENU["bebidas"]["batidas"]["sabores"]
        print("\nSabores de batidas disponibles (verifica disponibilidad del día):")
        for j, s in enumerate(sabores, 1):
            print(f"{j}. {s.title()}")
        while True:
            j = input("Elige un sabor (1-{}): ".format(len(sabores))).strip()
            if j.isdigit() and 1 <= int(j) <= len(sabores):
                sabor = sabores[int(j) - 1]
                break
            print("Entrada inválida.")
        while True:
            c = input("Cantidad de batidas: ").strip()
            if c.isdigit() and int(c) > 0:
                cantidad = int(c)
                break
            print("Ingresa un número entero positivo.")
        precio = MENU["bebidas"]["batidas"]["precio"] * cantidad
        return tipo, sabor, cantidad, precio
    # Jugos naturales: sin sabores específicos, preguntar cantidad
    if tipo == "jugos_naturales":
        print("\nPregunta cuáles jugos naturales hay disponibles hoy.")
        while True:
            c = input("Cantidad de jugos: ").strip()
            if c.isdigit() and int(c) > 0:
                cantidad = int(c)
                break
            print("Ingresa un número entero positivo.")
        precio = MENU["bebidas"]["jugos_naturales"]["precio"] * cantidad
        return tipo, None, cantidad, precio
    # Refrescos: elegir tamaño
    if tipo == "refrescos":
        tamanos = list(MENU["bebidas"]["refrescos"].keys())
        print("\nTamaños de refrescos:")
        for j, t in enumerate(tamanos, 1):
            precio = MENU["bebidas"]["refrescos"][t]
            print(f"{j}. {t.title()} - RD${precio}")
        while True:
            j = input("Elige un tamaño (1-{}): ".format(len(tamanos))).strip()
            if j.isdigit() and 1 <= int(j) <= len(tamanos):
                tam = tamanos[int(j) - 1]
                break
            print("Entrada inválida.")
        while True:
            c = input("Cantidad de refrescos: ").strip()
            if c.isdigit() and int(c) > 0:
                cantidad = int(c)
                break
            print("Ingresa un número entero positivo.")
        precio = MENU["bebidas"]["refrescos"][tam] * cantidad
        return tipo, tam, cantidad, precio
    # Agua
    if tipo == "agua":
        while True:
            c = input("Cantidad de botellas de agua: ").strip()
            if c.isdigit() and int(c) > 0:
                cantidad = int(c)
                break
            print("Ingresa un número entero positivo.")
        precio = MENU["bebidas"]["agua"]["precio"] * cantidad
        return tipo, None, cantidad, precio


def hacer_pedido() -> Dict:
    """Realiza el proceso completo de tomar un pedido y devuelve los datos."""
    pedido: Dict[str, any] = {
        "productos": [],
        "bebidas": None,
        "tipo_pedido": None,
        "direccion": None,
        "cliente": None,
        "telefono": None,
        "pago": None,
    }
    # Seleccionar productos (se puede repetir)
    while True:
        mostrar_menu()
        categoria = seleccionar_categoria()
        if categoria == "yaroas":
            tipo, tamano, cantidad = elegir_yaroa()
            precio_unit = MENU["yaroas"][tipo]["precios"][tamano]
            pedido["productos"].append(
                {
                    "categoria": "yaroa",
                    "nombre": MENU["yaroas"][tipo]["nombre"],
                    "tamano": tamano,
                    "cantidad": cantidad,
                    "precio_unit": precio_unit,
                    "subtotal": precio_unit * cantidad,
                }
            )
        elif categoria == "pizzas":
            tipo, sabor, add, cantidad = elegir_pizza()
            base_price = MENU["pizzas"][tipo]["sabores"][sabor]
            extra = MENU["pizzas"][tipo]["ingrediente_adicional"] if add else 0
            precio_unit = base_price + extra
            pedido["productos"].append(
                {
                    "categoria": "pizza",
                    "nombre": MENU["pizzas"][tipo]["nombre"],
                    "sabor": sabor,
                    "ingrediente_adicional": add,
                    "cantidad": cantidad,
                    "precio_unit": precio_unit,
                    "subtotal": precio_unit * cantidad,
                }
            )
        elif categoria == "favoritos":
            fav, cantidad = elegir_favorito()
            precio_unit = MENU["favoritos"][fav]["precio"]
            pedido["productos"].append(
                {
                    "categoria": "favorito",
                    "nombre": MENU["favoritos"][fav]["nombre"],
                    "cantidad": cantidad,
                    "precio_unit": precio_unit,
                    "subtotal": precio_unit * cantidad,
                }
            )
        elif categoria == "especialidades":
            esp, cantidad = elegir_especialidad()
            precio_unit = MENU["especialidades"][esp]["precio"]
            pedido["productos"].append(
                {
                    "categoria": "especialidad",
                    "nombre": MENU["especialidades"][esp]["nombre"],
                    "cantidad": cantidad,
                    "precio_unit": precio_unit,
                    "subtotal": precio_unit * cantidad,
                }
            )
        elif categoria == "bebidas":
            tipo, detalle, cantidad, precio = elegir_bebida()
            if tipo != "ninguna":
                pedido["bebidas"] = {
                    "tipo": tipo,
                    "detalle": detalle,
                    "cantidad": cantidad,
                    "precio": precio,
                }
        otra = input("\n¿Deseas agregar otro producto? (s/n): ").strip().lower()
        if otra != "s":
            break
    # Preguntar bebidas si aún no hay
    if not pedido["bebidas"]:
        tipo, detalle, cantidad, precio = elegir_bebida()
        if tipo != "ninguna":
            pedido["bebidas"] = {
                "tipo": tipo,
                "detalle": detalle,
                "cantidad": cantidad,
                "precio": precio,
            }
    # Tipo de pedido
    tipos = ["delivery", "recoger", "local"]
    print("\nTipo de pedido:")
    for i, t in enumerate(tipos, 1):
        print(f"{i}. {t.title()}")
    while True:
        t = input("Elige una opción (1-3): ").strip()
        if t.isdigit() and 1 <= int(t) <= 3:
            pedido["tipo_pedido"] = tipos[int(t) - 1]
            break
        print("Entrada inválida.")
    # Dirección
    if pedido["tipo_pedido"] == "delivery":
        direccion = input("\nDirección (o ubicación): ").strip()
        pedido["direccion"] = direccion
    # Datos del cliente
    nombre = input("\nNombre del cliente: ").strip()
    telefono = input("Teléfono: ").strip()
    pedido["cliente"] = nombre
    pedido["telefono"] = telefono
    # Método de pago
    pagos = ["efectivo", "transferencia", "tarjeta"]
    print("\nMétodo de pago:")
    for i, p in enumerate(pagos, 1):
        print(f"{i}. {p.title()}")
    while True:
        p = input("Elige una opción (1-3): ").strip()
        if p.isdigit() and 1 <= int(p) <= 3:
            pedido["pago"] = pagos[int(p) - 1]
            break
        print("Entrada inválida.")
    return pedido


def mostrar_resumen(pedido: Dict) -> None:
    """Muestra el resumen del pedido y calcula el total."""
    print("\n===== Resumen de tu pedido =====")
    print(f"Cliente: {pedido['cliente']}")
    print(f"Teléfono: {pedido['telefono']}")
    print(f"Tipo de pedido: {pedido['tipo_pedido'].title()}")
    if pedido["tipo_pedido"] == "delivery":
        print(f"Dirección: {pedido['direccion']}")
    print("\nPedido:")
    total = 0
    for i, prod in enumerate(pedido["productos"], 1):
        linea = f" {i}. {prod['nombre']}"
        if prod.get("tamano"):
            linea += f" ({prod['tamano']})"
        if prod.get("sabor"):
            linea += f" sabor {prod['sabor']}"
        if prod.get("ingrediente_adicional"):
            linea += " + ingrediente adicional"
        linea += f" x{prod['cantidad']} = RD${prod['subtotal']}"
        print(linea)
        total += prod["subtotal"]
    # Bebidas
    if pedido.get("bebidas"):
        beb = pedido["bebidas"]
        detalle = beb["detalle"]
        detalle_str = f" sabor {detalle}" if detalle else ""
        linea_beb = f" Bebida: {beb['tipo'].replace('_', ' ')}{detalle_str} x{beb['cantidad']} = RD${beb['precio']}"
        print(linea_beb)
        total += beb["precio"]
    # Total
    print(f"\nTotal a pagar: RD${total}")
    pedido["total"] = total


def main() -> None:
    """Función principal del programa."""
    print("Hola 👋 Bienvenido a Doña Lila Express ❤️")
    print("Rápido, rico y hecho para ti.")
    while True:
        print("\n¿Qué deseas hacer hoy?")
        print("1. Ver menú")
        print("2. Hacer un pedido")
        print("3. Ver bebidas")
        print("4. Ver ofertas")
        print("5. Consultar mi pedido (no implementado)")
        print("6. Hablar con una persona")
        print("7. Salir")
        opcion = input("Elige una opción (1-7): ").strip()
        if opcion == "1":
            mostrar_menu()
        elif opcion == "2":
            pedido = hacer_pedido()
            mostrar_resumen(pedido)
            confirm = input("\n¿Confirmas tu pedido? (s/n): ").strip().lower()
            if confirm == "s":
                print("\nPerfecto ✅ Tu pedido fue recibido correctamente.")
                print("Ya lo estamos preparando con amor ❤️")
                print("Tiempo estimado: 30 minutos (aprox.)\n")
            else:
                print("\nPedido cancelado o modificado. Volviendo al menú principal.\n")
        elif opcion == "3":
            # Muestra únicamente las bebidas
            print("\nBebidas disponibles:")
            print("Batidas (RD$150) sabores: ", ", ".join(MENU['bebidas']['batidas']['sabores']))
            print("Jugos naturales (RD$100) - pregunta cuáles hay disponibles hoy.")
            print("Refrescos - Pequeño: RD$30, Mediano: RD$75, Grande: RD$100, Jumbo: RD$150")
            print("Agua (RD$20)")
        elif opcion == "4":
            print("\nOfertas actuales: (no hay ofertas por ahora)")
        elif opcion == "5":
            print("\nFuncionalidad no implementada en el prototipo.")
        elif opcion == "6":
            print("\nClaro, te voy a comunicar con una persona del equipo de Doña Lila. Por favor espera un momento.")
        elif opcion == "7":
            print("\nGracias por visitar Doña Lila Express. ¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
