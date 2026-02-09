import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from executor import ejecutar_plan  # 👈 LangGraph

st.title("ChatWorks - Agente con Grafos y Estados")

# --------- MODELO ----------
@st.cache_resource # Esto hace que cargue más rápido
def cargar_modelo():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = cargar_modelo()

# --------- FUNCIONES CON EJEMPLOS REALES ----------
funciones = [
    {
        "nombre": "buscar_producto",
        "ejemplos": ["¿Cuántas lámparas hay disponibles?", "¿Qué precio tiene la mesa?", "¿Hay sillas en stock?", "Muéstrame los productos", "¿Cuánto cuesta el televisor?"]
    },
    {
        "nombre": "crear_pedido",
        "ejemplos": ["Quiero comprar una lámpara", "Deseo ordenar una mesa", "Necesito adquirir una silla", "Quiero hacer un pedido"]
    },
    {
        "nombre": "buscar_cliente",
        "ejemplos": ["Muéstrame los datos del cliente Juan Pérez", "Buscar cliente María López", "Información del cliente Carlos Sánchez"]
    },
    {
        "nombre": "confirmar_pedido",
        "ejemplos": ["Sí, confirma el pedido", "Finalizar la compra", "Confirmar mi pedido", "Terminar pedido"]
    }
]

# --------- PREPARAR EMBEDDINGS ----------
frases = []
mapa_funciones = []
for f in funciones:
    for ejemplo in f["ejemplos"]:
        frases.append(ejemplo)
        mapa_funciones.append(f["nombre"])

embeddings_funciones = model.encode(frases)

# --------- LOGICA CONVERSACIONAL NATURAL ----------
def respuesta_natural_social(query):
    query = query.lower()
    if any(saludo in query for saludo in ["hola", "buenos dias", "buenas tardes"]):
        return "¡Hola! 👋 Bienvenido a ChatWorks. ¿En qué puedo ayudarte hoy?"
    elif any(animo in query for animo in ["como estas", "como vas", "que tal"]):
        return "¡Todo excelente por aquí! 🤖 Listos para procesar tus pedidos. ¿Y tú, qué tal va tu día?"
    elif any(gracias in query for gracias in ["gracias", "agradecido"]):
        return "¡De nada! Es un placer ayudarte. ¿Necesitas algo más?"
    else:
        return "¡Hola! No estoy seguro de entender esa solicitud, pero puedo ayudarte a buscar productos o crear pedidos. 😊"

# --------- SELECCION DE FUNCION ----------
def seleccionar_funcion(query, umbral=0.60):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings_funciones)[0]
    idx = scores.argmax()
    max_score = scores[idx]

    if max_score < umbral:
        return "conversacion", max_score
    return mapa_funciones[idx], max_score

# --------- INTERFAZ ----------
# --------- INTERFAZ ----------
query = st.text_input("¿Qué necesitas?")

if query:
    # 1. LIMPIEZA Y PRIORIDAD SOCIAL (Vía Rápida)
    query_minuscula = query.lower().strip()
    
    # Lista de frases sociales que queremos capturar SIEMPRE
    frases_sociales = ["como estas", "como vas", "que tal", "como va todo", "hola", "buenos dias"]
    
    if any(social in query_minuscula for social in frases_sociales):
        with st.expander("Ver logs del proceso (Interno)"):
            st.write("💬 Modo: Interacción Social Directa")
            st.write("🧠 Proceso: Respuesta natural activada por coincidencia de frase.")
        
        respuesta = respuesta_natural_social(query)
        st.info(respuesta)

    # 2. PROCESAMIENTO TÉCNICO (Solo si no fue un saludo simple)
    else:
        funcion, score = seleccionar_funcion(query)

        # Mostrar logs de proceso (Punto 1 de la guía)
        with st.expander("Ver logs del proceso (Interno)"):
            st.write(f"🔎 Función detectada: **{funcion}**")
            st.write(f"📊 Score de confianza: **{score:.2f}**")
            st.write("🧠 Proceso: Generación de embeddings y búsqueda semántica completada.")

        # RESPUESTA AL USUARIO BASADA EN EL SCORE
        if funcion == "conversacion":
            respuesta = respuesta_natural_social(query)
            st.info(respuesta)
        else:
            # Respuesta generada por el Grafo (Neo4j + LangGraph)
            with st.status("Ejecutando plan desde Neo4j..."):
                respuesta = ejecutar_plan(query, funcion)
            
            # Presentación natural del resultado
            st.success(respuesta)