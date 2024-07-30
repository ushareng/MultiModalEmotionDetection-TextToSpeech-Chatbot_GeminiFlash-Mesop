import mesop as mp
import mesop.labs as mel
import  base64
from typing import Callable
import image_to_text
import audio_to_text
import text_to_text
import text_to_speech
import chatbot
import os

from PIL import Image
import pathlib
#from gemma_text import ModelClass


import google.generativeai as genai



def nav_gemini():
#    with mp.box(
#         style=mp.Style(
#         background="#302b2b",
#         height="5%",
#         border_radius=12,
#           box_shadow=(
#             "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f")
#         )
#     ):
        with mp.box(
                    style=mp.Style(display="flex", justify_content="right",
                                padding=mp.Padding(top=16, left=16, right=16, bottom=16),
                                    #box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"), 
                                    margin=mp.Margin(left="auto", right="auto"),
                                    width="min(1024px, 100%)",)
                ):    
                for example in ['text', 'image', 'speech']:
                    path = f"/gemini/{example}"
                    if example =='image':
                        example = 'Facial'
                    mp.button(
                    example.title()+" Emotion",
                    color="accent",
                    type="raised",
                        style=mp.Style(font_family="Serif", cursor="pointer"),
                        on_click=set_demo,
                        key=path,
                    )
                mp.button(
                    "Text to Audio",
                    color="accent",
                    type="raised",
                    
                        style=mp.Style(font_family="Serif", cursor="pointer"),
                        on_click=set_demo,
                        key='/gemini/textspeech',
                    )
                mp.button(
                    "Autism Chatbot",
                    color="accent",
                    type="raised",
                    
                        style=mp.Style(font_family="Serif", cursor="pointer"),
                        on_click=set_demo,
                        key='/gemini/chatbot',
                    )
   

def nav_section():
    with mp.box(
        style=mp.Style(justify_content="space-between",
          padding=mp.Padding(top=5,left=5, right=2, bottom=5),
          background="#123456", #green
          
          margin=mp.Margin(left="auto", right="auto"),
          width="max(1024px, 100%)",
          gap="24px",
          flex_grow=1,
          display="flex",
          flex_wrap="wrap",
          )
    ):
        with mp.box(
                style=mp.Style(display="flex", justify_content="right",
                               background="#f2f2f2",
                               flex_basis="max(360px, calc(30% - 48px))",
                            padding=mp.Padding(top=16, left=16, right=6, bottom=16),
                                #box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"), 
                                #margin=mp.Margin(left="auto", right="200px"),
                                width="min(360px, 30%)",
                                border_radius=12,
                                flex_direction="column",
                                )
            ):
            mp.text("AI for Autism", style=mp.Style(
                font_family="Serif",
                font_size="30px"
            ))
        with mp.box(
                style=mp.Style(display="flex",
                                background="#123456",
                                padding=mp.Padding(top=16, left=16, right=6, bottom=16),
                                #box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"), 
                                #margin=mp.Margin(left="auto", right="200px"),
                                width="max(480px, 60%)",
                                justify_content="right",
                                gap="24px",
                                flex_grow=1,
                                flex_wrap="wrap",
                                #flex_direction="column",
                                )
            ):   
            
            #for example in ['gemini', 'gemma', 'paligemma']:
            for example in ["gemini"]:
                path = f"/{example}"
                if example == 'gemini':
                    path = f"/{example}/text"

                with mp.content_button(
                
                color="warn",
                type="raised",
                    style=mp.Style(color="#000", cursor="pointer", align_self="center", margin=mp.Margin(
                        left="3px", right="3px"
                    )),
                    on_click=set_demo,
                    key=path,
                ):
                    mp.text(text=example.title(), type="button", style=mp.Style(
                        font_weight="bold",
                        font_size="18px",
                        font_family="Serif"
                        #padding=mp.Padding(left=5, right=5, bottom=5),
                    ))
        

def set_demo(e: mp.ClickEvent):
  mp.navigate(e.key)


########### HOME ###############################
  
@mp.page(
  security_policy=mp.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/",
  title="AIForAutism",
)

def app():
  nav_section()
  #pathlib.Path().resolve()             current directory path 
  print("path ",  os.path.abspath(__file__))
  image = Image.open("autism_new.png")
  image.save("background.png")
  with open("background.png", "rb") as image:
    f = image.read()
  with mp.box(
      style= mp.Style(
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"),
            margin=mp.Margin(right=8, left=8)

      )
  ):

    mp.image(
        src=f"data:image/png;base64,{base64.b64encode(f).decode()}",
        style=mp.Style(
            height="100%",
            width="100%",
            display="flex",
            flex_wrap="wrap",
        )
        )
    




###############  FOR TEXT ##########################

@mp.page(
  security_policy=mp.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/gemini/text",
  title="AIForAutism",
)

def app():
  nav_section()
  with mp.box(
        style=mp.Style(
        background="#302b2b",
        height="100%",
        border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f")
        )):
            nav_gemini()
            text_to_text.text_to_text(
                text2_classifier,
                title="Detect Emotion of the Sentence",
            )


############## FOR TEXT TO SPEECH   ###################


@mp.page(
  security_policy=mp.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/gemini/textspeech",
  title="AIForAutism",
)

def app():
  nav_section()
  with mp.box(
        style=mp.Style(
        background="#302b2b",
        height="100%",
        border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f")
        )):
            nav_gemini()
            text_to_speech.text_to_text(
                text2_classifier,
                title="Generate Audio From Text Input",
            )



#############   FOR IMAGE   ##########################


@mp.stateclass
class State:
  name: str
  path: str
  size: int
  mime_type: str
  image_data: str
  output: str
  textarea_key: int
  sidenav_open: bool


@mp.page(path="/gemini/image")
def app():
  nav_section()
  with mp.box(
        style=mp.Style(
        background="#302b2b",
        height="100%",
        border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f")
        )):
            nav_gemini()
            image_to_text.image_to_text(
                image_classification,
                title="Detect Facial Emotion from the Image",
            )
  

def image_classification(data: str):
    # Decode base64 string
    return data

################  FOR SPEECH ###################

@mp.page(
  security_policy=mp.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/gemini/speech",
  title="AIForAutism",
)

def app():
  nav_section()
  with mp.box(
        style=mp.Style(
        background="#302b2b",
        height="100%",
        border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f")
        )):
            nav_gemini()
            audio_to_text.audio_to_text(
                audio,
                title="Detect Emotion of the Speech",
            )
  
def audio(s: str):
   return s


############# CHAT BOT #######################

@mp.page(
  security_policy=mp.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/gemini/chatbot",
  title="AIForAutism",
)

def app():
  nav_section()
  with mp.box(
        style=mp.Style(
        background="#302b2b",
        height="100%",
        border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f")
        )):
            nav_gemini()
            chatbot.transform("Autism Chat Bot")
    #mel.chat(transform, title="Autism Chat Bot", bot_user="Autism Bot" )
#   audio_to_text.audio_to_text(
#     audio,
#     title="Get Emotion of the Audio",
# )
  
########### GEMMA ###############################
@mp.page(
  security_policy=mp.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/gemma",
  title="AIForAutism",
)

def app():
  nav_section()
  with mp.box(
        style=mp.Style(
        background="#302b2b",
        height="100%",
        border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f")
        )):
            nav_gemini()
            text_to_text.text_to_text(
                text2_classifier,
                title="Detect Emotion of the Sentence",
            )


def text2_classifier(s: str):
  return s
  #return ModelClass.predict(s)
