import gradio as gr
from transformers import pipeline
import pandas as pd

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
    theme="compact",
    title="TableQA Chat Interface",
    description="Ask a question about the data in the fixed CSV file.",
)

iface.launch()