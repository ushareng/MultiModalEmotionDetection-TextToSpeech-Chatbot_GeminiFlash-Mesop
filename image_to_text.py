from typing import Callable
import mesop as mp
import base64
import os
import google.generativeai as genaii

apikey = os.getenv("GOOGLE_API_KEY")
genaii.configure(api_key=apikey)
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model1 = genaii.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

@mp.stateclass
class State:
  name: str
  path: str
  size: int
  mime_type: str
  image_data: str
  output: str
  textarea_key: int


def image_classification(data: str):
    # Decode base64 string
    decoded_data = base64.b64decode(data)
    
    # Write binary data to a file
    with open("image.png", "wb") as image_file:
        image_file.write(decoded_data)

    file  = upload_to_gemini("image.png")
    response = model1.generate_content([
    "Analyse the emotion of the image, determine which emotion  best describes the image among ('Fear', 'Neutral', 'Surprise', 'Disgust', 'Desire', 'Affection', 'Happiness', 'Anger', 'Sadness', 'Optimism')",
    "image: ",
    file,
    "input 2: Answer in one word",
    
    ])
    print(response.text)
    
    return response.text

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genaii.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  #del os.environ["GOOGLE_API_KEY"]
  return file


def image_to_text(
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


  def on_image_upload(e: mp.UploadEvent):
    state = mp.state(State)
    state.image_data = base64.b64encode(e.file.read()).decode()
    print("file ", e.file)
    state.name = e.file.name
    print("name ", e.file.name)

    # Decode base64 string
    decoded_data = base64.b64decode(state.image_data)

    # Write binary data to a file
    # saving image as a file
    with open("decoded_image.png", "wb") as image_file:
        image_file.write(decoded_data)

  def on_click_generate(e: mp.ClickEvent):
    state = mp.state(State)
    state.output = image_classification(state.image_data)
    #state.output = transform(state.image_data)

  def on_click_clear(e: mp.ClickEvent):
    state = mp.state(State)
    state.image_data = ""
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
            label="Upload Image",
            accepted_file_types=["application/pdf"],
            on_upload=on_image_upload,
            type="flat",
            color="primary",
            style=mp.Style(font_weight="bold"),
          )
        #   mp.textarea(
        #     key=str(mp.state(State).textarea_key),
        #     on_input=on_input,
        #     rows=5,
        #     autosize=True,
        #     max_rows=15,
        #     style=mp.Style(width="100%"),
        #   )
          if mp.state(State).image_data:
            with mp.box(style=box_style):
                with mp.box(
                    style=mp.Style(
                        display="grid",
                        justify_content="center",
                        justify_items="center",
                    )
                    ):
                    mp.image(
                        src=f"data:image/jpeg;base64,{mp.state(State).image_data}",
                        style=mp.Style(width="100%", margin=mp.Margin(top=10)),
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
        
