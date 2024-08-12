# Emotion detection from text, images, audio , Text to Speech and chatbot using Gemini API and Mesop

# Usecase :

1.Difficulty understanding emotions in multiple modalities like Face , Speech and Text forms important markers in the diagnosis of Autism spectrum Disorder(ASD) . This project aims to help autistic individuals identify emotions in multiple modalities using Gemini . 

2. Text to Speech Tool - This project helps Nonverbal Autistic individuals to convert the text which they type in to Speech .

3. Autism Chatbot - Chatbot to answer queries related to Autism and Neurodiversity .

## Demo Video
[mesop.webm](https://github.com/user-attachments/assets/1a140a12-c2bd-4574-8f95-db81623cf5a6)

## Workflow

![mesop (1)](https://github.com/user-attachments/assets/d106bc56-4b32-4d3a-ab74-766d340a4fab)

## Build and Run

Install Mesop `pip install mesop`

Set the Gemini API Key in the environment variable
* `export GOOGLE_API_KEY=<your_key>`
* Check if the Key is set by `echo $GOOGLE_API_KEY`

Clone repo
Install the dependencies
* `pip install google-generativeai`

Run: `mesop classification.py`

