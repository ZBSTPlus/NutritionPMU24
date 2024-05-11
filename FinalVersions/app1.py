from fooditems import fi
import gradio as gr
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('nutrition.csv')
data_dict = data.set_index('Food/100g').T.to_dict()


def getData(food):
    return data_dict[food]

def calculate_nutrition(breakfast, lunch, dinner):
    bf = getData(breakfast)
    lun = getData(lunch)
    din = getData(dinner)
    
    total_e = round(sum([bf['Energy(Kcal)'],lun['Energy(Kcal)'],din['Energy(Kcal)']]),2)
    total_p = round(sum((bf['Protein(g)'],lun['Protein(g)'],din['Protein(g)'])),2)
    total_c = round(sum((bf['Carbohydrate(g)'],lun['Carbohydrate(g)'],din['Carbohydrate(g)'])),2)
    total_f = round(sum((bf['Fat(g)'],lun['Fat(g)'],din['Fat(g)'])),2)

    return {"Total Energy(Kcal) consumed in the day": total_e, 
    "Total Carbohydrates(g) consumed in a day": total_c, 
    "Total Protein(g) consumed in the day": total_p ,
      "Total Fat(g) consumption in a day": total_f , 
      "breakfast": bf, "lunch": lun, "dinner":din, 
      "Avg Energy Consumption": round(total_e/3,3),
      "Avg Fat Consumption": round(total_f/3,3),
      "Avg Carbohydrates Consumption": round(total_c/3,3),
      "Avg Protein Consumption": round(total_p/3,3),
      }

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
        [fi[10], fi[11], fi[129]],
        [fi[210], fi[110], fi[132]],
        [fi[199], fi[101], fi[312]],
    ],
    title="Nutrition Calculator",
    description="Enter what you ate for breakfast, lunch, and dinner to calculate your nutrition intake.",
)


iface.launch()