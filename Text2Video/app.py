import streamlit as st
import requests
from utils.gpt import GPT
from utils.text2speech import TextToSpeech
from utils.pdf_reader import PDF_Reader
from utils.generate_images import generate_images
from utils.esrgan import enchance_images
from utils.video_generation import video_generation
from dotenv import load_dotenv
load_dotenv()

def main():
    st.set_page_config(page_title="Text to video",
                       page_icon=":books:")
    st.write( unsafe_allow_html=True)

    st.header("Text to video :film_projector:")
    prompt = st.text_input("Enter the prompt:")

    pdf = st.file_uploader("Upload your PDF")

    if st.button('submit'):
        text=PDF_Reader(pdf)
        # st.write(text)
        with st.spinner('Generating Summary...'):
            prompt= text + """
                \nSummarize the above text IN LESS THAN OR EQUAL TO 512 WORDS.DO NOT EXCEED 512 words.Identify keywords from the text and 
                generate prompts(maximum 5 prompts) for each keyword that will help in finding an image thorugh google search.
                You MUST ALWAYS return just a json with the summarized text with the key of summarized_text and image prompts as
                an array of objects with key image_prompts and the every object inside the array should have just one key with the 
                name prompt.Do not return the data in any other format. Do not return in markdown or plain text. Only return in JSON format don't give any other"""
            # print(prompt)
            res=GPT(prompt)
            st.title("Summary :")
            st.write(res['summarized_text'])
            print(res['image_prompts'])

        with st.spinner('Generating Audio...'):
            text=res['summarized_text']
            gender = "male"  # or "female"
            source_language = "en"  # Replace with your source language code
            audio ,file_path= TextToSpeech(text, gender, source_language)
            st.title("Audio :")
            st.audio(audio)
        with st.spinner('Generating Images...'):
            j=1
            for i in res['image_prompts']:
                img=i['prompt']
                image_list=generate_images(img,j,1)
                j+=1
            print(image_list)
        with st.spinner('Enhancing Images...'):
            enchance_images(image_list)
        with st.spinner('Generating video...'):
            video=video_generation()
            st.title("Video :")
            st.video(video)



if __name__ == '__main__':
    main()