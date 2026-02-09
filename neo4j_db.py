from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "chatworks123")
)

def obtener_producto(nombre):
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Producto {nombre:$nombre})
            RETURN p.nombre AS nombre, p.stock AS stock, p.precio AS precio
        """, nombre=nombre)

        return result.single()


def obtener_cliente(nombre):
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Cliente {nombre:$nombre})
            RETURN c.nombre AS nombre, c.historial AS historial
        """, nombre=nombre)

        return result.single()
