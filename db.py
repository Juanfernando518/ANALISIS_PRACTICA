from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "chatworks123"   # la que pusiste

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def test_connection():
    with driver.session(database="chatworks") as session:
        result = session.run("RETURN 'Conectado a ChatWorks' AS msg")
        print(result.single()["msg"])

def cargar_datos_iniciales():
    with driver.session(database="chatworks") as session:

        session.run("""
        CREATE (:Producto {nombre:'Lámpara LED', precio:15, stock:12})
        CREATE (:Producto {nombre:'Mesa de Madera', precio:80, stock:5})
        CREATE (:Cliente {nombre:'Juan Perez', telefono:'0999999999'})
        """)

def obtener_stock_producto(nombre_producto):
    with driver.session(database="chatworks") as session:
        result = session.run("""
        MATCH (p:Producto)
        WHERE toLower(p.nombre) CONTAINS toLower($nombre)
        RETURN p.nombre AS nombre, p.stock AS stock, p.precio AS precio
        """, nombre=nombre_producto)

        record = result.single()
        if record:
            return record["nombre"], record["stock"], record["precio"]
        else:
            return None, None, None

