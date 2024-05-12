from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain_community.vectorstores.chroma import Chroma

from langchain_core.documents.base import Document

import streamlit as st


import chromadb

import math












##############################################################################
#
#
#
#
#           UTILITY FUNCTIONS
#
#
#
##############################################################################

@st.cache_resource
def get_chroma():
    # if 'client' not in st.session_state:

    #     embedding = GPT4AllEmbeddings()

    #     db_path = "./db_path"  # Path to SQLite database
    #     chroma = Chroma(persist_directory=db_path,
    #                     embedding_function=embedding,
    #                     collection_name=st.session_state.get("selected collection")
    #             )
    #     return chroma
    # else:
    #     return st.session_state.client

    settings = chromadb.Settings(is_persistent=True, persist_directory="./db_path")


    chroma_client = chromadb.Client(settings=settings)
    return chroma_client




def get_collection_names():
    client = get_chroma()
    
    ls = client.list_collections()

    # with st.expander("Collections", expanded=True):
    #     for x in ls:
    #         st.write(x.name)
    collections = [x.name for x in ls]
    print(collections)

    return collections




def create_collection(name):
    client = get_chroma()

    try:
        client.create_collection(name)
    except Exception as e:
        # raise Exception(f"Error creating collection {name}")
        raise e

    # return True




def delete_collection(name):
    client = get_chroma()
    print(f"Deleting {name}")
    client.delete_collection(name)



def get_unique_sources():
    client = get_chroma()

    if not st.session_state.selected_collection:
        return []

    selected_collection = client.get_collection(st.session_state.selected_collection)

    if not selected_collection:
        return []

    metadata_sources = selected_collection.get(include=["metadatas"])['metadatas']
    unique_urls = []

    for url in metadata_sources:
        if url['source'] not in unique_urls:
            unique_urls.append(url['source'])

    return unique_urls













##############################################################################
#
#
#
#
#           INGESTION FUNCTIONS
#
#
#
##############################################################################
def ingest_url(url):
    """
https://lilianweng.github.io/posts/2023-06-23-agent/
https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/
    """

    # check if url is already in collection
    # name = st.session_state.get('selected_collection')
    # selected_collection = client._client.get_collection(name)

    # metadata_sources = selected_collection.get(include=["metadatas"])['embeddings']['metadatas']
    # st.write(metadata_sources)
    # if url in metadata_sources:
    #     st.error(f"URL {url} already in collection")
    #     return

    client = get_chroma()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=0
    )

    st.write(f"Loading {url}")
    doc = WebBaseLoader(url).load()

    st.write(doc)

    all_splits = text_splitter.split_documents(doc)

    # chroma_documents = [Document(page_content=str(split.page_content), metadata={"source": str(url)}) for split in all_splits]
    # client.add_documents(
    
    docs = [split.page_content for split in all_splits]

    metadata = [{"source": url} for split in all_splits]

    # ids = [f"{url}_{str(i).zfill(math.log10(len(docs)))}" for i in range(len(docs))]
    # Calculate the padding width based on the number of documents
    num_digits = math.ceil(math.log10(len(docs))) if len(docs) > 0 else 1

    ids = [f"{url}_{str(i).zfill(num_digits)}" for i in range(len(docs))]

    col = client.get_collection(st.session_state.selected_collection)
    col.add(
            ids=ids,
            documents=docs,
            metadatas=metadata
            # collection_name=st.session_state.get("selected collection")
        )

















##############################################################################
#
#
#
#
#           USER INTERFACE FUNCTIONS
#
#
#
##############################################################################
def show_collection_selector():
    col_names = get_collection_names()
    # st.write(col_names)
    st.selectbox("Select Collection", col_names, key="selected_collection")
    # st.write(st.session_state.selected_collection)




def show_url_ingestor():
    with st.popover("Ingest URL"):
        url = st.text_input("Enter URL")
        if st.button("Ingest"):
            if not url:
                st.error("No URLs provided")
                return

            if url in get_unique_sources():
                st.error(f"URL {url} already in collection")
                return

            ids = ingest_url(url)
            st.write(ids)






def show_new_collection_popover():
    with st.popover("New Collection"):
        new_collection_name = st.text_input("New Collection Name")
        if st.button("Create Collection"):
            # col_names = get_collection_names()
            # if new_collection_name in col_names:
                # st.error(f"Collection {new_collection_name} already exists")
            # else:
                # create_collection(new_collection_name)
                # st.write(f"Collection {new_collection_name} created")
            try:
                create_collection(new_collection_name)
                # st.write(f"Collection {new_collection_name} created")
                st.rerun()
            except Exception as e:
                # TODO show error details
                st.toast(f"ERROR creating {new_collection_name} - already exists?")
                st.toast(e)






def show_delete_collection_popover():
    with st.popover(":red[Delete This Collection]"):
        st.error("This will delete the selected collection")
        if st.button("Delete Collection"):
            # selected_collection = st.session_state.get("selected collection")
            # if selected_collection:
                # client._client.delete_collection(selected_collection)
            delete_collection(st.session_state.selected_collection)
            st.write(f"Collection {st.session_state.selected_collection} deleted")
            st.rerun()





def cmp_show_collection_details():
    client = get_chroma()

    selected_collection_name = st.session_state.get("selected_collection")
    if not selected_collection_name:
        return

    # collection = st.session_state.get("selected_collection")
    collection = client.get_collection(selected_collection_name)


    st.header("unique sources")
    sources = get_unique_sources()
    st.write(sources)

    st.selectbox("Select Source", sources, key="selected_source", index=None)
    if st.session_state.selected_source:

        with st.popover("Delete Source"):
            if st.button("Delete Source"):
                collection.delete(where={"source": st.session_state.selected_source})
                st.rerun()



        docs = collection.get(
                # include=["metadatas"]
                where={"source": st.session_state.selected_source},
            )


        st.header("Documents")
        # st.write(docs) # dict_keys(['ids', 'embeddings', 'metadatas', 'documents', 'uris', 'data'])



        for d in docs["documents"]:
            # with st.expander(f"Document {str(d.get('documents'))[:10]}"):
            # st.write(f"Source {d['metadatas']}")
            st.write(d)













##############################################################################
#
#
#
#
#           MAIN
#
#
#
##############################################################################
if __name__ == "__main__":
    st.title("Chroma")

    st.write("https://lilianweng.github.io/posts/2023-06-23-agent/")

    show_collection_selector()


    show_new_collection_popover()
    show_delete_collection_popover()
    show_url_ingestor()
    cmp_show_collection_details()




    st.write(get_collection_names())
    st.write(get_unique_sources())
