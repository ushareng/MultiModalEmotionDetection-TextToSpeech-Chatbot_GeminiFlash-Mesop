import types
from typing import Callable, Generator, Literal, cast

import mesop as me
import google.generativeai as genai

from dotenv import load_dotenv
import os

@me.stateclass
class State:
  input: str
  output: str
  textarea_key: int

load_dotenv()



def text_classifier(s: str):
    apikey = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=apikey)
    
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }



    load_dotenv()
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    response = model.generate_content([
    "input:  determine which emotion  best describes the sentence among ('Fear', 'Neutral', 'Surprise', 'Disgust', 'Desire', 'Affection', 'Happiness', 'Anger', 'Sadness', 'Optimism') {}. Answer in one word only".format(s),
    "output: ",
    ])
    return response.text


def text_io(
  transform: Callable[[str], Generator[str, None, None] | str],
  *,
  title: str | None = None,
  transform_mode: Literal["append", "replace"] = "replace",
):
  """Deprecated: Use `text_to_text` instead which provides the same functionality
  with better default settings.

  This function creates event handlers for text input and output operations
  using the provided transform function to process the input and generate the output.

  Args:
    transform: Function that takes in a string input and either returns or yields a string output.
    title: Headline text to display at the top of the UI
    transform_mode: Specifies how the output should be updated when yielding an output using a generator.
                  - "append": Concatenates each new piece of text to the existing output.
                  - "replace": Replaces the existing output with each new piece of text.
  """
  print(
    "\033[93m[warning]\033[0m text_io is deprecated, use text_to_text instead"
  )
  text_to_text(transform=transform, title=title, transform_mode=transform_mode)


def text_to_text(
  transform: Callable[[str], Generator[str, None, None] | str],
  *,
  title: str | None = None,
  transform_mode: Literal["append", "replace"] = "append",
):
  """Creates a simple UI which takes in a text input and returns a text output.

  This function creates event handlers for text input and output operations
  using the provided transform function to process the input and generate the output.

  Args:
    transform: Function that takes in a string input and either returns or yields a string output.
    title: Headline text to display at the top of the UI
    transform_mode: Specifies how the output should be updated when yielding an output using a generator.
                  - "append": Concatenates each new piece of text to the existing output.
                  - "replace": Replaces the existing output with each new piece of text.
  """

  def on_input(e: me.InputEvent):
    state = me.state(State)
    state.input = e.value

  def on_click_generate(e: me.ClickEvent):
    state = me.state(State)
    print("input ", state.input)
    output = text_classifier(state.input)
    if isinstance(output, types.GeneratorType):
      for val in output:
        if transform_mode == "append":
          state.output += val
        elif transform_mode == "replace":
          state.output = val
        else:
          raise ValueError(f"Unsupported transform_mode: {transform_mode}")
        yield
    else:
      # `output` is a str, however type inference doesn't
      # work w/ generator's unusual ininstance check.
      state.output = cast(str, output)
      yield

  def on_click_clear(e: me.ClickEvent):
    state = me.state(State)
    state.input = ""
    state.textarea_key += 1

  with me.box(
    style=me.Style(
      background="#fdfdfd",  #lavender
      height="100%",
    )
  ):
    with me.box(
      style=me.Style(
        margin=me.Margin(left="5%", right="5%"),
        background="#dcdcdc",  #purple 
        padding=me.Padding(top=24, left=24, right=24, bottom=24),
        display="flex",
        flex_direction="column",
      )
    ):
      if title:
        me.text(title,type="headline-5",style=me.Style(
                        
                        font_family="Serif"
                        #padding=mp.Padding(left=5, right=5, bottom=5),
                    ))
      with me.box(
        style=me.Style(
          justify_content="space-between",
          padding=me.Padding(top=24, left=24, right=24, bottom=24),
          background="#000", #green
          margin=me.Margin(left="auto", right="auto"),
          width="min(1024px, 100%)",
          gap="24px",
          flex_grow=1,
          display="flex",
          flex_wrap="wrap",
        )
      ):
        box_style = me.Style(
          flex_basis="max(480px, calc(50% - 48px))",
          background="#fff",
          border_radius=12,
          box_shadow="0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f",
          padding=me.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )
        with me.box(style=me.Style(
          flex_basis="max(360px, calc(60% - 48px))",
          background="#fff",
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          padding=me.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )):
          me.text("Input", style=me.Style(font_weight=500))
          me.box(style=me.Style(height=16))
          me.textarea(
            key=str(me.state(State).textarea_key),
            on_input=on_input,
            rows=5,
            autosize=True,
            max_rows=15,
            style=me.Style(width="100%"),
          )
          me.box(style=me.Style(height=12))
          with me.box(
            style=me.Style(display="flex", justify_content="space-between")
          ):
            me.button(
              "Clear", color="primary", type="stroked", on_click=on_click_clear
            )
            me.button(
              "Detect",
              color="primary",
              type="flat",
              on_click=on_click_generate,
            )
        with me.box(style=me.Style(
          flex_basis="max(360px, calc(30% - 48px))",
          background="#fff",
          border_radius=12,
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          padding=me.Padding(top=16, left=16, right=16, bottom=16),
          display="flex",
          flex_direction="column",
        )):
          me.text("Output", style=me.Style(font_weight=500))
          me.markdown(me.state(State).output)