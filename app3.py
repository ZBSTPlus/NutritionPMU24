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
    title="Nutrition Information Chat Interface",
    description="""
    This interface allows you to ask questions about the nutritional content of various foods. 
    The data is based on a fixed CSV file which includes information about the energy (in Kcal), protein (in g), carbohydrates (in g), and fat (in g) content per 100g of various foods. 
    You can ask questions like 'What is the energy content of baked macaroni pasta?' or 'Which food has the highest protein content?'.
    """,
    theme="huggingface",
)

chat_interface.launch()
