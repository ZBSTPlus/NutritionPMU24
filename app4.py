import gradio as gr
from transformers import pipeline
import pandas as pd

# Load TableQA pipeline
table_qa = pipeline('table-question-answering', model='google/tapas-base-finetuned-wtq')

# Load the CSV file
data = pd.read_csv('nutrition.csv')

def answer_question(question):
    # Use TableQA to answer the question
    result = table_qa(question=question, table=data)
    return result['answer']

chat_interface = gr.ChatInterface(
    fn=answer_question, 
    inputs=gr.inputs.Textbox(lines=2, label="Question"), 
    outputs="text",
    title="TableQA Chat Interface",
    description="Ask a question about the data in the fixed CSV file.",
)

chat_interface.launch()
