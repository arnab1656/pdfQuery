import os

from dotenv import load_dotenv

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')


def generate_text_from_pdf(question: str, filename: str):
    # fetching data from the pdf

    print("filename from the answer gene")
    print("filename from the answer gene")
    print(filename)

    document_directory = "uploaded_files"

    loader = PyPDFLoader(f"{document_directory}/{filename}.pdf")
    pages = loader.load_and_split()

    # debugging purpose
    # print("documents")
    # print(pages[0].page_content)

    # getting text chunks

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(pages)

    # debugging purpose

    # print("texts")
    # print(texts)

    # embedding of the text

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create unique subdirectory for this PDF's index

    # pdf_filename = os.path.basename(pdf_path)
    # pdf_name_without_extension = os.path.splitext(pdf_filename)[0]
    persist_directory = os.path.join('db', filename)

    # Create index
    # persist_directory = 'db'
    db = Chroma.from_documents(documents=texts,
                               embedding=embedding_function,
                               persist_directory=persist_directory)

    # Dummy query it
    # query = "What is name of applicant"
    # docs = db.similarity_search(query)

    # debugging purpose
    # print results of similarity
    # print("docs[0].page_content")
    # print(docs[0])

    # Load llm

    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id, max_length=128, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
    )

    # Create retriever from index and chain it with LLM

    retriever = db.as_retriever(search_kwargs={"k": 3})
    qa = RetrievalQA.from_chain_type(llm=llm,
                                     chain_type="stuff",
                                     retriever=retriever,
                                     return_source_documents=True)

    # Query the chain
    # question = "What is the qualification of the applicant"
    generated_text = qa(question)

    # debugging purpose
    # print("generated_text")
    # print(generated_text)

    # debugging purpose
    # print("generated_result")
    # print(generated_text["result"])

    return generated_text["result"]
