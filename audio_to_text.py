from typing import Callable
import mesop as mp
import base64

@mp.stateclass
class State:
  name: str
  path: str
  size: int
  mime_type: str
  audio_data: str
  output: str
  textarea_key: int

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.3,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}



def generate(audio):
  vertexai.init(project="just-well-429210-n7", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""From the audio given, analyze the tone of the speaker and content, emphasize tone more than content and answer which emotion does it convey among (neutral, calm, happy, sad, angry, fear, disgust, surprise). Answer in one word"""]
  )
  responses = model.generate_content(
      [audio, """a"""],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )

  for response in responses:
    print(response.text, end="")
    return  response.text
  
  return ""

def audio_to_text(
  transform: Callable[[str], str],
  *,
  title: str | None = None,
):
  """Creates a simple UI which takes in a text input and returns an image output.

  This function creates event handlers for text input and output operations
  using the provided function `transform` to process the input and generate the image
  output.

  Args:
    transform: Function that takes in a string input and returns a URL to an image or a base64 encoded image.
    title: Headline text to display at the top of the UI.
  """


  def on_audio_upload(e: mp.UploadEvent):
    state = mp.state(State)
    state.audio_data = base64.b64encode(e.file.read()).decode()
    print("file ", e.file)
    state.name = e.file.name
    print("name ", e.file.name)

    # Decode base64 string
    decoded_data = base64.b64decode(state.audio_data)

    # Write binary data to a file
    # saving image as a file
    with open("decoded_audio.mp3", "wb") as audio_file:
        audio_file.write(decoded_data)

  def on_click_generate(e: mp.ClickEvent):
    state = mp.state(State)
    if state.audio_data:
      audio = Part.from_data(
      mime_type="audio/wav",
      data=base64.b64decode(state.audio_data))
    state.output = generate(audio)
    print("output is ", state.output)
    #state.output = transform(state.output)
  def on_click_clear(e: mp.ClickEvent):
    state = mp.state(State)
    state.audio_data = ""
    state.name = ""
    state.output = ""
    state.textarea_key += 1

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
      if title:
        mp.text(title,type="headline-5",style=mp.Style(
                        
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
        box_style = mp.Style(
          flex_basis="max(480px, calc(50% - 48px))",
          background="#fff",
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          padding=mp.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )

        with mp.box(style=mp.Style(
          flex_basis="max(360px, calc(60% - 48px))",
          background="#fff",
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          padding=mp.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )):
          mp.text("Input", style=mp.Style(font_weight=500))
          mp.box(style=mp.Style(height=16))
          mp.uploader(
            label="Upload Audio",
            accepted_file_types=["application/pdf"],
            on_upload=on_audio_upload,
            type="flat",
            color="primary",
            style=mp.Style(font_weight="bold"),
          )
          if mp.state(State).audio_data:
            with mp.box(style=box_style):
                with mp.box(
                    style=mp.Style(
                        display="grid",
                        justify_content="center",
                        justify_items="center",
                    )
                    ):
                    mp.audio(
                        src=f"data:audio/wav;base64,{mp.state(State).audio_data}",
                    )
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
              "Detect",
              color="primary",
              type="flat",
              on_click=on_click_generate,
            )
        with mp.box(style=mp.Style(
          flex_basis="max(360px, calc(30% - 48px))",
          background="#fff",
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          padding=mp.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )):
          mp.text("Output", style=mp.Style(font_weight=500))
          mp.markdown(mp.state(State).output)

