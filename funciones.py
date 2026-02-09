def ejecutar_funcion(paso, query):

    if paso == "verificar_stock":
        print("Verificando stock del producto...")
        return "Stock verificado correctamente."

    elif paso == "mostrar_stock":
        print("Mostrando stock...")
        return "Hay stock disponible para su solicitud."

    elif paso == "crear_borrador_pedido":
        print("Creando borrador del pedido...")
        return "Borrador de pedido creado."

    elif paso == "buscar_datos_cliente":
        print("Buscando datos del cliente...")
        return "Datos del cliente encontrados."

    elif paso == "confirmar_pedido":
        print("Confirmando pedido...")
        return "Pedido confirmado y registrado con éxito."

    elif paso == "finalizar_pedido":
        print("Finalizando pedido...")
        return "Pedido finalizado exitosamente."

    elif paso == "finalizar":
        print("Finalizando proceso...")
        return "Proceso finalizado correctamente."
    
    # Esta línea es el salvavidas para no ver "None" nunca más
    return f"⚠️ Paso '{paso}' ejecutado, pero no tiene mensaje definido."