from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from planner import obtener_plan
from funciones import ejecutar_funcion

# -------- ESTADO DEL AGENTE --------
class AgentState(TypedDict):
    query: str
    pasos: List[str]
    paso_actual: int
    respuesta: str
    finalizado: bool

# -------- NODO QUE EJECUTA CADA PASO --------
def ejecutar_paso(state: AgentState):
    if state["paso_actual"] >= len(state["pasos"]):
        state["finalizado"] = True
        return state

    paso = state["pasos"][state["paso_actual"]]
    print(f"➡️ Ejecutando paso: {paso}")

    resultado = ejecutar_funcion(paso, state["query"])

    # Agregamos el resultado con un formato más limpio
    state["respuesta"] += f"  \n- {resultado}" 
    state["paso_actual"] += 1

    return state

# -------- ROUTER --------
def continuar(state: AgentState):
    if state["finalizado"]:
        return END
    return "ejecutar_paso"

# -------- FUNCIÓN PRINCIPAL --------
def ejecutar_plan(query, funcion_detectada):
    pasos = obtener_plan(funcion_detectada)
    print("PLAN OBTENIDO:", pasos)

    if not pasos:
        return "Lo siento, parece que no tengo un flujo configurado para realizar esa acción aún. 😅"

    # Mensaje inicial para dar naturalidad
    mensaje_inicio = f"¡Claro! Con gusto te ayudo con **{funcion_detectada.replace('_', ' ')}**. Esto es lo que he hecho:"

    estado_inicial = AgentState(
        query=query,
        pasos=pasos,
        paso_actual=0,
        respuesta=mensaje_inicio, # Empezamos con el saludo natural
        finalizado=False
    )

    graph = StateGraph(AgentState)
    graph.add_node("ejecutar_paso", ejecutar_paso)
    graph.set_entry_point("ejecutar_paso")

    graph.add_conditional_edges(
        "ejecutar_paso",
        continuar,
        {
            END: END,
            "ejecutar_paso": "ejecutar_paso",
        }
    )

    app = graph.compile()
    resultado = app.invoke(estado_inicial)

    # Añadimos un cierre natural al final de todos los pasos
    respuesta_final = f"{resultado['respuesta']}\n\n¿Deseas realizar alguna otra gestión? 😊"

    return respuesta_final