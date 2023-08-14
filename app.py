import streamlit as st
from ocr import OCRProcessor
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os
import streamlit.components.v1 as components
from PIL import Image

os.environ['OPENAI_API_KEY'] = "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"

def ocr_func(img):
    ocr_processor = OCRProcessor()
    image_path = img
    layout = ocr_processor.extract_layout(image_path)
    return layout

custom_prompt_template = = """This is a layout of a handwriting website design, including text and their coordinates of four outer vertices. 
        Make an HTML modern sans-serif website that reflects these elements and decide which 
        CSS can be used to match their relative positions, try to use proper layout tags to match
         their font size and relative placement based on their coordinates. 
         Use <ul> and <li> if the elements look like as menu list. 
         Smartly use function tags like <button> <input> if their names look like that.
         Your design should be prior to the coordinates, 
         then you should also use some imagination for the layout and CSS from common web design principle.
         Remember, don't use absolute coordinates in your HTML source code. 
         Generate only source code file, no description: {layout}.\n
"""


