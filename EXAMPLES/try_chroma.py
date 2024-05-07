from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_core.documents.base import Document


def get_chroma():
    embedding = GPT4AllEmbeddings()

    db_path = "./db_path"  # Path to SQLite database
    chroma = Chroma(persist_directory=db_path, embedding_function=embedding, collection_name="rag-chroma")

    return chroma


def ingest_urls(urls: list):
    chroma = get_chroma()
    # urls = [
    #     "https://lilianweng.github.io/posts/2023-06-23-agent/",
    #     "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    #     "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    # ]

    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=100
    )
    all_splits = text_splitter.split_documents(docs)

     # Debug: print an example document to check its structure
    # print(all_splits[0].__dict__)  # This line helps to understand the structure of a split document


    # Convert each split into a Document format expected by Chroma
    chroma_documents = [Document(page_content=split.page_content, metadata={"source_url": url}) for split in all_splits]
    # Add documents to Chroma and get back their IDs
    ids = chroma.add_documents(chroma_documents)
    return ids



def query_chroma(query):
    chroma = get_chroma()
    retriever = chroma.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(query, top_k=5)

    if not retrieved_docs:
        print("No documents found")
        return

    for doc in retrieved_docs:
        print(doc.page_content)
        # print(doc.metadata)
        print("\n\n\n----\n\n\n")


if __name__ == "__main__":
    # ids = ingest_urls(["https://lilianweng.github.io/posts/2023-06-23-agent/"])
    # print(ids)

    # query = "What is the agent?"
    query = "What is the agent in reinforcement learning?"
    query_chroma(query)



ids = """
['7364569c-b234-4ecf-8d01-2afab13b74c6', '7ae6093a-73ba-443e-8f9e-0791e54fb787', '4a48233d-1348-43e1-9757-0ebd0a268638', '9258657d-fbe2-4254-b777-c838966f0118', '65ee1f7f-527e-4211-a39e-4e5a59101bef', 'e4cf01cf-46cc-4a75-a692-03359b499a0d', '35fe2f3b-e964-4d64-a35e-c3a9c2aefa1e', '2e57f654-eb5c-49c6-9111-b071ca69530d', 'c495dabf-2555-40b7-bd75-3d72abca83c7', 'eb379304-4a2d-4879-9750-5aeeb1c71ec7', '9eadcede-c6af-4ee6-a31c-82978ad0b37e', 'eab88276-d822-4e89-9282-f4315b484015', '2fd105cd-b0ca-494a-915f-00e8dfe549d0', '8a268aad-43b0-4e65-a42b-4fd526aeb7a5', '584ab57b-ccd1-4a2f-9bd4-4468e3c34e58', '2b0608a5-1731-48c1-92cf-379229553dc2', '8d288400-6276-43bc-b180-2d8fd5be39bf', '451092b3-2fef-4942-8dcb-8f3aa0616732', 'f0ecd978-a36f-4670-9db5-0f1ab8129c43', '56a931e6-13ba-46fd-a17e-ed616118840f', 'e33bbad6-6c52-4a12-9fb8-95b8bc43c62f', '1ad1f76a-3016-429b-9c2b-9bd5a21cff10', '76152918-27f6-451f-81fd-763db485c457', '610bf6a0-d76b-4e61-bdad-901f8213b0bd', 'a7931695-04d6-487b-85a7-24faed5de0bd', 'c5e3a4bc-186a-4650-94a8-ac1456132147', '78059ce8-e37e-4ebb-abdd-7da930a19e95', '21956318-c0f4-4821-9b04-33dd5efd639e', 'c047b5d2-8cb3-4863-b8ec-10a58aee2ea7', 'ec9c4954-3eda-469b-8989-6833670b8e38', '27afb285-d97d-493b-94ef-e856b7f9a3a7', '30d8c31d-ddd0-4675-a365-7e578fca5e5e', '9615584b-f98a-4082-9e46-8c8f02d46410']
"""