import gradio as gr
from predict import *

def get_transcript_prediction(transcript):
    icd_codes = get_icd_codes(transcript)
    return ", ".join(icd_codes)

demo = gr.Interface(
    fn=get_transcript_prediction,
    inputs=["text"],
    outputs=["text"],
)

demo.launch()
