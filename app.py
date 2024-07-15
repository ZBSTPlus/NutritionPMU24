from fooditems import fi, ear_rda, description, article
import gradio as gr
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('nutrition.csv')
data_dict = data.set_index('Food/100g').T.to_dict()

def getData(food):
    return data_dict[food]

def suggest_options(input, options):
    if input == "":
        return []
    else:
        return [option for option in options if input.lower() in option.lower()]

def calculate_nutrition(name, gt, w, h, early_morning, em_gms, breakfast, bf_gms, mid_morning, mm_gms, lunch, lun_gms, evening_snacks, es_gms, dinner, din_gms, bed_time, bt_gms):
    # Split the grams input strings into lists and use 100 as default value
    meals = [early_morning, breakfast, mid_morning, lunch, evening_snacks, dinner, bed_time]
    gms_inputs = [em_gms, bf_gms, mm_gms, lun_gms, es_gms, din_gms, bt_gms]
    gms = []

    for meal, gm_input in zip(meals, gms_inputs):
        if meal is None:
            gm = []
        else:
            gm = list(map(int, gm_input.split(','))) if gm_input else [100]*len(meal)
            gm = gm + [100]*(len(meal)-len(gm))
        gms.append(gm)

    # Initialize total energy, protein, carbs, and fat
    total_e, total_p, total_c, total_f = 0, 0, 0, 0

    # Calculate nutrition for each meal
    for meal, gm in zip(meals, gms):
        if meal is not None:
            for item, gm in zip(meal, gm):
                if item is not None:
                    data = getData(item)
                    total_e += data['Energy(Kcal)'] * (gm / 100)
                    total_p += data['Protein(g)'] * (gm / 100)
                    total_c += data['Carbohydrate(g)'] * (gm / 100)
                    total_f += data['Fat(g)'] * (gm / 100)

    # Calculate EAR and RDA
    ear_energy = ear_rda[gt]["Energy"]
    rda_protein = ear_rda[gt]["Protein"]
    total_ear_energy = round(float(ear_energy) * float(w),3)
    total_rda_protein = round(float(rda_protein) * float(w),3)

    # Check if intake is adequate and calculate percentage
    energy_status = "adequate" if total_e >= total_ear_energy else "inadequate"
    energy_percentage = round((total_e / total_ear_energy) * 100, 2)
    protein_status = "adequate" if total_p >= total_rda_protein else "inadequate"
    protein_percentage = round((total_p / total_rda_protein) * 100, 2)

    return {
        "Energy Intake Status": f"{energy_status} ({energy_percentage}% of required intake)",
        "Protein Intake Status": f"{protein_status} ({protein_percentage}% of required intake)",
        "Total Energy (Kcal) Consumed in the Day": round(total_e,3),
        "Total Protein (g) Consumed in the Day": round(total_p,3),
        "Total EAR(Estimated Average Requirements) Energy for the Day (Kcal)": total_ear_energy,
        "Total RDA(Recommended Dietary Allowances) Protein for the Day (g)": total_rda_protein,
        "Total Carbohydrates (g) Consumed in a Day": round(total_c,3),
        "Total Fat (g) Consumption in a Day": round(total_f,3),
    }

iface = gr.Interface(
    # Function to calculate nutrition
    fn=calculate_nutrition, 
    # Define the inputs
    inputs=[
        gr.Textbox(label="Enter Your Name"),
        gr.Dropdown(ear_rda,label="Select Your Gender and Type of Work"),
        gr.Number(label="Enter Your Weight (in Kg)"),
        gr.Number(label="Enter Your Height (in cm)"),
        gr.Dropdown(fi, label="Select Early Morning Items", multiselect=True),
        gr.Textbox(label="Enter the Quantity of Each Early Morning Item in Grams  (separated by commas if multiple items are selected)"),
        gr.Dropdown(fi, label="Select Breakfast Items", multiselect=True),
        gr.Textbox(label="Enter the Quantity of Each Breakfast Item in Grams"),
        gr.Dropdown(fi, label="Select Mid Morning Items", multiselect=True),
        gr.Textbox(label="Enter the Quantity of Each Mid Morning Item in Grams"),
        gr.Dropdown(fi, label="Select Lunch Items", multiselect=True),
        gr.Textbox(label="Enter the Quantity of Each Lunch Item in Grams (separated by commas)"),
        gr.Dropdown(fi, label="Select Evening Snacks Items", multiselect=True),
        gr.Textbox(label="Enter the Quantity of Each Evening Snacks Item in Grams"),
        gr.Dropdown(fi, label="Select Dinner Items", multiselect=True),
        gr.Textbox(label="Enter the Quantity of Each Dinner Item in Grams"),
        gr.Dropdown(fi, label="Select Bed Time Items", multiselect=True),
        gr.Textbox(label="Enter the Quantity of Each Bed Time Item in Grams")
    ], 
    # Define the output
    outputs="json",
    # Set the title
    title="Nutrition Calculator",
    # Set the theme
    theme="gradio/monochrome",
    # Set the description
    description=description,
    # Disable flagging
    allow_flagging=False,
    # Hide the footer
    css="footer {display: none !important}",
    # Set the article
    article = article
)

iface.launch()