import os
import jax

# The Keras 3 distribution API is only implemented for the JAX backend for now
os.environ["KERAS_BACKEND"] = "jax"
# Pre-allocate 100% of TPU memory to minimize memory fragmentation and allocation overhead
os.environ["XLA_PYTHON_CLIENT_MEM_FRACTION"] = "1.0"

import torch
import numpy as np
#from transformers import AutoTokenizer, GemmaForSequenceClassification
from transformers import (
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoModelForSequenceClassification, 
    )

import bitsandbytes as bnb

import numpy as np



os.environ['HF_TOKEN']='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'
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,  # Enables 4-bit quantization
    bnb_4bit_use_double_quant=True,  # Use double quantization for potentially higher accuracy (optional)
    bnb_4bit_quant_type="nf4",  # Quantization type (specifics depend on hardware and library)
    bnb_4bit_compute_dtype=torch.bfloat16  # Compute dtype for improved efficiency (optional)
)
NUM_CLASSES=10
id2label={0: 'Sadness',
 1: 'Neutral',
 2: 'Happiness',
 3: 'Anger',
 4: 'Affection',
 5: 'Fear',
 6: 'Surprise',
 7: 'Disgust',
 8: 'Desire',
 9: 'Optimism'}

label2id= {'Sadness': 0,
 'Neutral': 1,
 'Happiness': 2,
 'Anger': 3,
 'Affection': 4,
 'Fear': 5,
 'Surprise': 6,
 'Disgust': 7,
 'Desire': 8,
 'Optimism': 9}

class ModelClass:
    _model = None  # Class-level variable to store the model
    _tokenizer = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            model_id = 'akshay-k/gemma_2b_cls_10classes'
            model = AutoModelForSequenceClassification.from_pretrained(
            model_id,  # "google/gemma-2b-it"
            num_labels=NUM_CLASSES,  # Number of output labels (2 for binary sentiment classification)
            quantization_config=bnb_config,  # configuration for quantization 
            device_map={"": 0}  # Optional dictionary specifying device mapping (single GPU with index 0 here)
            )
            tokenizer = AutoTokenizer.from_pretrained(model_id,truncation=True)
            print("Loading the model...")
            cls._model = model  # Simulate loading the model
            cls._tokenizer = tokenizer
        return (cls._model, cls._tokenizer)

    @classmethod
    def predict(cls, text):
        (model, tokenizer) = cls.load_model()
        inputs = tokenizer(text, return_tensors="pt").to("cuda")  # Convert to PyTorch tensors and move to GPU (if available)
        with torch.no_grad():
            outputs = model(**inputs).logits  # Get the model's output logits
        y_prob = torch.sigmoid(outputs).tolist()[0]  # Apply sigmoid activation and convert to list
        print(y_prob)
        print('score : '+str(y_prob[np.argmax(np.round(y_prob, 5))]))
        return id2label[np.argmax(np.round(y_prob, 5))]


model = None
tokenizer = None
model_id = 'akshay-k/gemma_2b_cls_10classes'
def load_model():
   
    model = AutoModelForSequenceClassification.from_pretrained(
        model_id,  # "google/gemma-2b-it"
        num_labels=NUM_CLASSES,  # Number of output labels (2 for binary sentiment classification)
        quantization_config=bnb_config,  # configuration for quantization 
        device_map={"": 0}  # Optional dictionary specifying device mapping (single GPU with index 0 here)
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id,truncation=True)


