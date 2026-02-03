import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.title("ChatWorks - Function Selection Agent")

# --------- MODELO ----------
model = SentenceTransformer('all-MiniLM-L6-v2')

# --------- FUNCIONES ----------
funciones = [
    {
        "nombre": "buscar_producto",
        "descripcion": """
        El usuario quiere saber cuántos productos hay, consultar stock,
        precio, disponibilidad o información de artículos como lámparas,
        mesas, sillas, televisores o cualquier objeto físico del inventario.
        """
    },
    {
        "nombre": "crear_pedido",
        "descripcion": """
        El usuario quiere comprar, adquirir, ordenar o pedir productos.
        """
    },
    {
        "nombre": "buscar_cliente",
        "descripcion": """
        El usuario quiere consultar datos de un cliente, su información personal
        o historial en el sistema.
        """
    },
    {
        "nombre": "confirmar_pedido",
        "descripcion": """
        El usuario quiere confirmar o finalizar un pedido ya realizado.
        """
    }
]

descripciones = [f["descripcion"] for f in funciones]
embeddings_funciones = model.encode(descripciones)

def seleccionar_funcion(query, umbral=0.65):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings_funciones)[0]

    idx = scores.argmax()
    max_score = scores[idx]

    if max_score < umbral:
        return "conversacion", max_score

    return funciones[idx]["nombre"], max_score


def ejecutar_funcion(funcion, query):

    if funcion == "conversacion":
        return "Hola 👋 Soy el asistente. Puedo ayudarte con clientes, productos y pedidos."

    elif funcion == "buscar_producto":
        return "Encontré las lámparas en stock: 12 unidades, precio $15."

    elif funcion == "crear_pedido":
        return "Pedido creado correctamente. ¿Deseas confirmar el pedido?"

    elif funcion == "buscar_cliente":
        return "Cliente encontrado: Juan Pérez, historial activo."

    elif funcion == "confirmar_pedido":
        return "Pedido confirmado y registrado en la base de datos."


# --------- STREAMLIT UI (VA FUERA DE LAS FUNCIONES) ----------
query = st.text_input("¿Qué necesitas?")

if query:
    funcion, score = seleccionar_funcion(query)
    respuesta = ejecutar_funcion(funcion, query)

    st.write("Función detectada:", funcion)
    st.write("Score:", score)
    st.success(respuesta)
