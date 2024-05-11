import gradio as gr
from transformers import pipeline
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# Load TableQA pipeline
table_qa = pipeline('table-question-answering', model='google/tapas-base-finetuned-wtq')

# Load the CSV file
data = pd.read_csv('nutrition.csv')
# Convert the DataFrame to a list of dictionaries
data = data.astype(str)
def answer_question(question):
    # Use TableQA to answer the question
    result = table_qa(query=question, table=data)
    return result['answer']

iface = gr.Interface(
    fn=answer_question, 
    inputs=gr.Textbox(lines=2, label="Question"), 
    outputs="text",
    title="Nutrition Expert Chat Interfacee",
    description="""
    This interface allows you to ask questions about the nutritional content of various foods. 
    The QA Model is based on a Nutrition dataset collected by Padmavathi University Dept which includes information about the energy (in Kcal), protein (in g), carbohydrates (in g), and fat (in g) content per 100g of various foods. 
    You can ask questions like 'What is the energy content of baked macaroni pasta?' or 'Which food has the highest protein content?'.
    """,
)

iface.launch()