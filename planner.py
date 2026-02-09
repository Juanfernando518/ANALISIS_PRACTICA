from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "chatworks123")
)


def obtener_plan(funcion_objetivo):
    pasos = []

    with driver.session() as session:
        # 1️⃣ Obtener el primer estado
        result = session.run("""
            MATCH (f:Funcion {nombre:$nombre})-[:INICIA]->(e:Estado)
            RETURN e.nombre AS estado_inicial
        """, nombre=funcion_objetivo)

        record = result.single()

        if not record:
            return []

        estado_actual = record["estado_inicial"]
        pasos.append(estado_actual)

        # 2️⃣ Caminar manualmente por los SIGUIENTE
        while True:
            result = session.run("""
                MATCH (a:Estado {nombre:$nombre})-[:SIGUIENTE]->(b:Estado)
                RETURN b.nombre AS siguiente
            """, nombre=estado_actual)

            record = result.single()

            if not record:
                break

            estado_actual = record["siguiente"]
            pasos.append(estado_actual)

    print("PLAN GENERADO DESDE NEO4J:", pasos)
    return pasos
