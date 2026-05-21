from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os

cities_data = [
    {
        "city": "Tokyo",
        "content": "Tokyo is Japan's capital known for anime, technology, and sushi. It offers an incredible mix of traditional culture and futuristic innovation."
    },
    {
        "city": "Paris",
        "content": "Paris is famous for the Eiffel Tower and art museums like the Louvre. It is known as the city of romance and exquisite cuisine."
    },
    {
        "city": "New York",
        "content": "New York is known for Times Square, Broadway, and skyscrapers. It is a bustling metropolis that never sleeps."
    }
]

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def get_vectorstore():

    store = Chroma(
        collection_name="travel_cities",
        embedding_function=embedding_model,
        persist_directory="./chroma_db"
    )
    
    if store._collection.count() == 0:
        docs = [Document(page_content=d["content"], metadata={"city": d["city"]}) for d in cities_data]
        store.add_documents(docs)
    
    return store

def retrieve_city_info(city: str) -> str:
    store = get_vectorstore()
    results = store.similarity_search(city, k=1)
    if results:
        doc = results[0]
        if city.lower() in doc.metadata.get("city", "").lower() or city.lower() in doc.page_content.lower():
            return doc.page_content
    return None