# ChatWorks: Agente Inteligente con Grafos de Conocimiento y LangGraph

ChatWorks is an intelligent agent designed for e-commerce environments that revolutionizes process management through the use of Knowledge Graphs. Unlike traditional chatbots, this agent doesn't have static workflows; it queries a Neo4j database in real time to determine the next steps, allowing business logic to evolve without requiring modifications to the source code.

## 📝 Summary

The project implements a system capable of understanding user intent through natural language processing (NLP). If the user makes a business query (stock, orders, customers), the system activates a Planner that extracts a state path from Neo4j. This path is executed by LangGraph, which manages a cyclical state machine to ensure that each task (verification, registration, confirmation) is successfully completed before delivering a humanized response to the user.

## 🛠️ Stack of libraries and technologies

- Frontend & UI

- Orchestration and logic (backend)

- Artificial Intelligence and Data

##  ⚙️ Process Flow


The agent operates under a five-stage lifecycle:

1. Detection of Intent (NLU): Embeddings of the user query are generated and compared using cosine similarity against known functions.

2. Planning: If a technical function is detected, a Cypher query is made to Neo4j to obtain the sequence of nodes (states) needed to meet the objective.

3. State Initialization: LangGraph initializes an AgentState with the original query and the list of steps obtained from the graph.

4. Cyclic Execution: The agent iterates through the states. For each step, it invokes a specific function in the functions.py file, updating the response history.

5. Natural Response: Once the states are completed, the system adds a layer of courtesy to deliver a friendly and interactive response to the user.

## 📐 Arquitectura del Sistema: ChatWorks AI Agent

The system uses a Graph-Aided Agent architecture, where the business logic is separated from the execution code.

![alt text](<imagen 2.png>)

## 📂 Repository Structure

![alt text](<imagen 1.png>)

- Notebooks/Application: Contains chatwork.ipynb for the graph population and the main scripts (app.py, executor.py, planner.py, functions.py).

- Core: db.py and neo4j_db.py for data persistence.

- Tests: test.py and test_plan.py for flow validation.

## 🛠️ Functions, Queries and Statuses (ChatWorks Orchestration)

| Function / Tool | Purpose | DB / Service | State Logic (LangGraph) | Query / Process (Cypher) | Embeddings (Model) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `search_product` | Checks availability and prices in the product catalog. | **Neo4j** | `verify_stock` → `show_stock` → `finish` | `MATCH (p:Producto {name: $prod}) RETURN p.stock, p.price` | `all-MiniLM-L6-v2` (Intent Detection) |
| `create_order` | Initiates the purchase flow and product reservation. | **Neo4j + Memory** | `create_draft` → `show_summary` → `finish_order` | `MATCH (p:Producto) WHERE p.id = $id CREATE (b:Draft)...` | `all-MiniLM-L6-v2` (Intent Detection) |
| `search_client` | Retrieves contact info and customer profile from CRM. | **Neo4j** | `search_customer_data` → `finish` | `MATCH (c:Customer {name: $name}) RETURN c.email, c.phone` | `all-MiniLM-L6-v2` (Intent Detection) |
| `conversation` | Handles greetings and social chat (Out-of-business logic). | **Local Memory** | `social_response` (Direct final state) | N/A (Python Courtesy Filter) | N/A (Threshold < 0.60) |}

## 📐 Data Architecture Explanation

To add more value to your project, you can include this technical summary:

1. NLP Intent Layer: Uses the all-MiniLM-L6-v2 model to transform user input into a mathematical vector. If the cosine similarity exceeds 0.60, the system triggers a Neo4j-orchestrated flow.

2. Planning Layer (Planner): The planner.py script queries Neo4j to retrieve the dynamic path of nodes (states) associated with a specific function.

3. Execution Layer (LangGraph): The executor.py engine processes the list of states using a StateGraph. Each "stop" in the graph executes specific business logic located in functions.py.

4. Persistence Layer (Neo4j): Unlike standard databases, here nodes represent agent states. This allows modifying business processes (adding or reordering steps) directly in the graph without changing the Python code.

## 📊 Database and Structure (Summary)

To follow your friend's format, here is the summary of your specific Graph and Embedding structure:

- Neo4j:

   - Nodes:

        - (:Function {name, description}): The main entry points for the agent.

        - (:State {name, action}): Individual steps within a workflow (e.g., verify_stock).

**Relationships:**

- (f:Function)-[:STARTS]->(s:State): Defines the first step of a process.

- (s1:State)-[:NEXT]->(s2:State): Defines the sequential flow of the execution plan.

**Embeddings:**

- Model: sentence-transformers/all-MiniLM-L6-v2

- Usage:

   - Input Query → Vector: User text is converted to a vector.

   - Cosine Similarity: Compared against pre-embedded function examples to route the user to the correct Neo4j plan.

   - Threshold: A score of 0.60 is used to separate technical tasks from social conversation.

## ✨ Features

**1. Semantic Intent Detection**

- Vector Embeddings: Uses all-MiniLM-L6-v2 to transform user queries into high-dimensional vectors.

- Contextual Routing: Distinguishes between "social talk" (greetings) and "business intent" (orders/stock) using a 0.60 confidence threshold.

- Fuzzy Matching: Understands user needs even with non-exact phrasing or typos.

**2. Graph-Based Workflow Orchestration**

- Dynamic Planning: Workflows are not hardcoded; the agent queries Neo4j to retrieve the specific sequence of steps for each function.

- Stateful Execution: Powered by LangGraph, allowing the agent to maintain a strict state machine during complex processes.

- Adaptive Logic: Modifying a business process is as simple as updating a relationship in the Graph Database, with no code changes required.

**3. Knowledge Graph Infrastructure**

- Node-Based Logic: Functions and States are stored as nodes (:Function, :State).

- Relational Mapping: Uses :STARTS and :NEXT relationships to define the logical flow of the assistant.

- Scalable Architecture: Easily expands to include new modules like "Customer Support" or "Returns" by adding nodes to the existing graph.

**4. Advanced AI Agent Capabilities**

- Multi-Step Reasoning: Executes sequential tasks such as "Verify Stock -> Create Draft -> Show Summary" in a single interaction.

- Internal Process Logging: Features an expandable "Internal Logs" view to show real-time confidence scores and detected functions.

- Graceful Fallbacks: If the confidence score is low, the agent reverts to a friendly conversational mode instead of failing.

**5. Interactive UI (Streamlit)**


- Real-Time Feedback: Uses st.status and st.expander to provide transparency into the agent's "thought process."

- Native Chat Experience: Clean and professional interface designed for a seamless user experience.

- Humanized Responses: Merges technical backend data with natural language for a polished final output.}

## 🚀 Getting Started

**Prerequisites**

- Python 3.9+: Required for LangGraph and Streamlit compatibility.

- Neo4j Database: You can use Neo4j Desktop (local) or Neo4j AuraDB (cloud).

- Virtual Environment: Recommended to avoid dependency conflicts.

**Environment Variables**

Create a .env file in the project root to store your credentials securely:

## Neo4j Configuration

NEO4J_URI=bolt://localhost:7687

NEO4J_USER=neo4j

NEO4J_PASSWORD=your_password

- Model Configuration (Local)
- The system uses SentenceTransformers (all-MiniLM-L6-v2)
- which runs locally on your CPU/GPU.

## 🛠️ Setup Instructions

1. Clone the Repository

https://github.com/Juanfernando518/ANALISIS_PRACTICA.git

2. Install Dependencies

- Create a virtual environment

python -m venv venv

- Activate it

- On Windows:

venv\Scripts\activate

- On Linux/Mac:

source venv/bin/activate

- Install required packages

pip install -r requirements.txt

## 🏃 Running the Project

Start the Streamlit Application

Run the following command in your terminal:

streamlit run app.py

**Accessing the System**

- Frontend UI: Open your browser at http://localhost:8501.

- Neo4j Browser: Access your database at http://localhost:7474 to monitor the graph execution in real-time.

## 📄 License

This project is developed as part of the Stochastic Models course - 6th Cycle.

## 👥 Authors

Juan Fernando Alvarez Picon - Computer Science Engineering

## 🙏 Acknowledgments

- Neo4j for the graph database technology and Cypher query language.

- LangChain & LangGraph for the state-based agent orchestration framework.

- Hugging Face for the all-MiniLM-L6-v2 transformer models.

- Streamlit for the rapid deployment of the conversational user interface.

- Scikit-learn for the cosine similarity implementation in intent classification.

Last Updated: February 9, 2026

## ⚡ Quick Commands Reference

🚀 Start the Application

streamlit run app.py 

## 🔍 Database Management (Neo4j)

- Access Browser: http://localhost:7474

- Check Active Flows: ```cypher
MATCH (f:Funcion)-[:INICIA]->(s:Estado) RETURN f, s

## 🛠️ Development & Debugging

- Run intent classification tests

python test.py

- Run workflow logic tests

python test_plan.py

## 🧹 Cleanup

- Deactivate virtual environment

deactivate

- Stop Neo4j (if using Docker)

docker stop neo4j_container_name

## 💡 Conclusions

ChatWorks' architecture stands out for its extreme flexibility, allowing business processes to be modified by changing relationships in Neo4j without altering the source code, while simultaneously ensuring scalability and efficiency in handling complex states thanks to LangGraph. This design achieves effective separation of responsibilities by decoupling the user interface, semantic planning, and technical execution, significantly facilitating maintenance, debugging, and continuous evolution of the intelligent agent.





