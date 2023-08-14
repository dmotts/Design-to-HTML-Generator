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

custom_prompt_template = """This is a layout of a handwriting website design, including text and their coordinates of four outer vertices. 
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
def html_generation(layout):
    prompt = PromptTemplate(
        template = custom_prompt_template,
        input_variables = ['layout']
    )

    llm = ChatOpenAI(
        model = 'gpt-3.5-turbo-16k',
        temperature = 0,
        max_tokens = 2096
    )

    chain = LLMChain(
         llm = llm,
         prompt = prompt
    )
    output = chain.run(layout=layout)
    print(output)
    return output

if "html" not in st.session_state:
    st.session_state.html = ""

if "image" not in st.session_state:
    st.session_state.image = ""

def image_run():
    html_code = ""
    layout = ocr_func(st.session_state.image)
    if layout != []:
        html_code = html_generation(layout)

        st.session_state.html = html_code
        st.session_state.image = st.session_state.image

st.set_page_config(layout = "wide")
st.markdown("<h1 style='text-align:center; color:black;'>Design to Website App<h1>", unsafe_allow_html=True)

col1, col2 = st.columns([0.5, 0.5], gap="medium")

with col1:
    uploaded_file = st.file_uploader("Upload your design", type=['jpg', 'png', 'jpeg'])

    if uploaded_file is not None:
        image_filename = uploaded_file.name
        
        st.image(uploaded_file, caption="Your Design", use_column_width=True)

        image = Image.open(image_filename)

        st.session_state.image = image_filename

        st.button("Run", on_click=image_run)

with col2:
    if st.session_state.html != '':
        with st.expander("See source code"):
            st.code(st.session_state.html)

        with st.container():
            components.html(st.session_state.html,  height=600, scrolling=True)