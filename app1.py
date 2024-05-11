from fooditems import fi
import gradio as gr
from fuzzywuzzy import process


# Function to find most similar food item
def find_most_similar_food1(user_input):
    most_similar_food = process.extractOne(user_input, fi)
    return most_similar_food[0]


# Assuming you have a function like this:
def calculate_nutrition(breakfast, lunch, dinner):
    bf = find_most_similar_food1(breakfast)
    lun = find_most_similar_food1(lunch)
    din = find_most_similar_food1(dinner)

    # Your function that calculates energy and carbohydrates etc.
    # This is just a placeholder
    return {"Energy": 2000, "Carbohydrates": 300, "bf": bf, "lun": lun, "din":din}

def suggest_options(input, options):
    if input == "":
        return []
    else:
        return [option for option in options if input.lower() in option.lower()]

iface = gr.Interface(
    fn=calculate_nutrition, 
    inputs=[
        gr.Dropdown(fi, label="Breakfast"),
        gr.Dropdown(fi, label="Lunch"),
        gr.Dropdown(fi, label="Dinner"),
    ], 
    outputs="json",
    examples=[
        [fi[0], fi[1], fi[2]],
        [fi[10], fi[11], fi[12]],
        # Add more examples here
    ],
    theme="compact",
    title="Nutrition Calculator",
    description="Enter what you ate for breakfast, lunch, and dinner to calculate your nutrition intake.",
)


iface.launch()
