# Atlas - Multi-Modal Agentic Travel Assistant

Atlas is an intelligent travel assistant powered by a complex LangGraph agentic workflow. It combines destination insights, weather forecasting, and visual exploration into a unified, clean, and dynamic Streamlit UI.

![Topology](/graph.png)

## Architecture & Concepts

This project demonstrates advanced LangGraph orchestration using manual node transmissions, parallel fan-outs, and contextual memory.
Because of the absence of API keys (openai, anthropic, openweather, tavily, etc.), I have used LLMs of Gemini and GroqCloud, and implemented mock services for web search. For image fetching, it dynamically queries the official Unsplash API (if configured), falling back to high-quality mock data when no key is present.

### 1. The Workflow (LangGraph)
- **City Extraction (`extract_city_node`)**: Uses Llama-3.3-70b (via Groq) to accurately extract the target destination city from a raw user prompt.
- **Conditional Routing**: Determines whether the city exists in our internal ChromaDB vector store or if an external mock search is required.
- **Parallel Fan-Out (`parallel_fetch_node`)**: The assistant gathers a 7-day weather forecast (via Open-Meteo) and fetches dynamic destination images (via the Unsplash API) concurrently using `asyncio.gather`. This drastically minimizes latency.
- **Summary Generation (`summary_node`)**: Uses Gemini 2.5 Flash to synthesize the retrieved information into an engaging travel guide.

### 2. Services & APIs
- **Vector Retrieval**: Local ChromaDB loaded with starter data (Tokyo, Paris, New York). Simulates a RAG-based proprietary knowledge base.
- **Mock Web Search**: A mock Python service mimicking external engines (like Tavily or DuckDuckGo) with simulated latency to fetch fallback data for missing cities.
- **Dynamic Weather**: Uses the open-source, keyless Open-Meteo API to fetch real coordinates and dynamic 7-day temperature trends.
- **Dynamic Images**: Integrates the official Unsplash API for fetching beautiful, real-time CDN photos of queried cities, gracefully falling back to a pre-defined local catalog if the API key is absent.

### 3. Conversational Memory
- Utilizes LangGraph's `MemorySaver()` checkpointer. If a user searches for a city (e.g., "London") and follows up with "What about next week?", the agent retains the previous city context to fetch new data without needing the city repeated.

## Project Structure
```
TravelAgent/
├── app/
│   ├── graph/
│   │   ├── builder.py       # Assembles the StateGraph and MemorySaver
│   │   ├── nodes.py         # The raw execution logic for each agent node
│   │   ├── router.py        # Logic determining internal RAG vs Web Search
│   │   └── state.py         # Defines the TravelState TypedDict
│   ├── services/
│   │   ├── image_service.py   # Dynamic Unsplash CDN image fetching
│   │   ├── search_service.py  # Mock web search fallback
│   │   ├── vector_store.py    # Local ChromaDB operations
│   │   └── weather_services.py# Open-Meteo API integrations
│   └── main.py              # Streamlit UI Entrypoint
├── .env                     # API Keys (Gemini, Groq, Unsplash)
├── generate_graph.py        # Script to generate topology visual
└── README.md
```

## Setup & Execution

### Prerequisites
- Python 3.10+
- `uv` (for fast package management)

### Installation
1. Clone the repository.
2. Initialize the environment and install dependencies:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Running the App
The backend and frontend are tightly coupled via Streamlit. To run the app:
```bash
uv run streamlit run app/main.py
```
Open your browser to `http://localhost:8501`.
