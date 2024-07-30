from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import mesop as mp
import mesop.labs as mel
import chatlab 
import io

from typing import Callable
import base64

@mp.stateclass
class State:
  name: str
  path: str
  size: int
  mime_type: str
  pdf_data: str
  output: str
  textarea_key: int

load_dotenv()

apikey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=apikey)

# Reading the text from pdf page by page and storing it into various
def get_pdf_text(pdf):
    text=""
    with io.BytesIO(pdf) as open_pdf_file:
        pdf_reader = PdfReader(open_pdf_file)
    #pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

#Getting the text into number of chunks as it is helpful in faster processing
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

#Storing the text chunks into embeddings to retrive the answer for the query outoff it
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():

    prompt_template = """
    You are an expert assistance extracting information from context provided. 
       Answer the question as detailed as possible from the provided context, 
    make sure to provide all the details, Be concise and do not hallucinate. 
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def on_pdf_upload(e: mp.UploadEvent):
    state = mp.state(State)
    state.pdf_data = base64.b64encode(e.file.read()).decode()
    print("file ", e.file)
    state.name = e.file.name
    print("name ", e.file.name)

    # Decode base64 string
    decoded_data = base64.b64decode(state.pdf_data)

    # Write binary data to a file
    # saving image as a file
    with open("document.pdf", "wb") as pdf_file:
        pdf_file.write(decoded_data)

def on_click_generate(e: mp.ClickEvent):
    state = mp.state(State)
    raw_text = get_pdf_text(base64.b64decode(state.pdf_data))
    print("pdf text ", raw_text)
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)

    
    state.output = "hello ji"
    print("output is ", state.output)

def on_click_clear(e: mp.ClickEvent):
    state = mp.state(State)
    state.pdf_data = ""
    state.name = ""
    state.output = ""
    state.textarea_key += 1

def answer(input: str, history: list[mel.ChatMessage]):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(input)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": input}
        , return_only_outputs=True)

    print(response)

    return response['output_text']


def transform(s: str):

  with mp.box(
    style=mp.Style(
      background="#fdfdfd",  #lavender
      height="100%",
    )
  ):
    with mp.box(
      style=mp.Style(
        margin=mp.Margin(left="5%", right="5%"),
        background="#dcdcdc",  #purple 
        padding=mp.Padding(top=24, left=24, right=24, bottom=24),
        display="flex",
        flex_direction="column",
      )
    ):
      if s:
        mp.text(s,type="headline-5",style=mp.Style(
                        
                        font_family="Serif"
                        #padding=mp.Padding(left=5, right=5, bottom=5),
                    ))
      with mp.box(
        style=mp.Style(
          justify_content="space-between",
          padding=mp.Padding(top=24, left=24, right=24, bottom=24),
          background="#000", #green
          margin=mp.Margin(left="auto", right="auto"),
          width="min(1024px, 100%)",
          gap="24px",
          flex_grow=1,
          display="flex",
          flex_wrap="wrap",
        )
      ):
        with mp.box(style=mp.Style(
          flex_basis="max(360px, calc(30% - 48px))",
          background="#fff",
          height="20%",
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          padding=mp.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )):
          mp.text("Input", style=mp.Style(font_weight=500))
          mp.box(style=mp.Style(
             height=16))
          mp.uploader(
            label="Upload Your PDF files",
            accepted_file_types=["application/pdf"],
            on_upload=on_pdf_upload,
            type="flat",
            color="primary",
            style=mp.Style(font_weight="bold"),
          )
          
        #   if mp.state(State).pdf_data:
        #     with mp.box(style=box_style):
        #         with mp.box(
        #             style=mp.Style(
        #                 display="grid",
        #                 justify_content="center",
        #                 justify_items="center",
        #             )
        #             ):
        #             # mp.audio(
        #             #     src=f"data:audio/wav;base64,{mp.state(State).pdf_data}",
        #             # )
          mp.box(style=mp.Style(height=12))
          with mp.box(
            style=mp.Style(display="flex", justify_content="space-between")
          ):
            mp.button(
              "Clear",
              color="primary",
              type="stroked",
              on_click=on_click_clear,
            )
            mp.button(
              "Submit",
              color="primary",
              type="flat",
              on_click=on_click_generate,
            )
        with mp.box(style=mp.Style(
          flex_basis="max(480px, calc(60% - 48px))",
          background="#fff",
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          padding=mp.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )):
          chatlab.chat(answer , title="Get Your Queries Resolved", bot_user="Autism Bot")

