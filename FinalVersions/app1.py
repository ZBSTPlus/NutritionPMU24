from fooditems import fi, ear_rda
import gradio as gr
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('nutrition.csv')
data_dict = data.set_index('Food/100g').T.to_dict()


def getData(food):
    return data_dict[food]

# def calculate_nutrition(name,gt,h,w,breakfast,bf_gms, lunch, lun_gms, dinner, din_gms):
#     bf = getData(breakfast)
#     lun = getData(lunch)
#     din = getData(dinner)

#     total_e = round(sum([bf['Energy(Kcal)'],lun['Energy(Kcal)'],din['Energy(Kcal)']]),2)
#     total_p = round(sum((bf['Protein(g)'],lun['Protein(g)'],din['Protein(g)'])),2)
#     total_c = round(sum((bf['Carbohydrate(g)'],lun['Carbohydrate(g)'],din['Carbohydrate(g)'])),2)
#     total_f = round(sum((bf['Fat(g)'],lun['Fat(g)'],din['Fat(g)'])),2)

#     ear_energy = ear_rda[gt]["Energy"]
#     rda_protein = ear_rda[gt]["Protein"]
#     total_ear_energy = float(ear_energy) * float(w)
#     total_rda_protein = float(rda_protein) * float(w)

#     print(total_e,total_ear_energy)
#     print(total_p,total_rda_protein)
#     energy_status = "adequate" if total_e >= total_ear_energy else "inadequate"
#     protein_status = "adequate" if total_p >= total_rda_protein else "inadequate"
#     return {"Total Energy(Kcal) consumed in the day": total_e, 
#     "Total Carbohydrates(g) consumed in a day": total_c, 
#     "Total Protein(g) consumed in the day": total_p ,
#       "Total Fat(g) consumption in a day": total_f , 
#       "breakfast": bf, "lunch": lun, "dinner":din, 
#       "Avg Energy Consumption": round(total_e/3,3),
#       "Avg Fat Consumption": round(total_f/3,3),
#       "Avg Carbohydrates Consumption": round(total_c/3,3),
#       "Avg Protein Consumption": round(total_p/3,3),
#     "Total EAR Energy for the day": total_ear_energy,
#     "Total RDA Protein for the day": total_rda_protein,
#     "Energy Intake Status": energy_status,
#     "Protein Intake Status": protein_status,
#       }

def calculate_nutrition(name, gt, w, breakfast, bf_gms, lunch, lun_gms, dinner, din_gms):
    bf = getData(breakfast)
    lun = getData(lunch)
    din = getData(dinner)

    # Adjust the energy, protein, carbohydrate, and fat values based on the amount consumed
    bf_e = bf['Energy(Kcal)'] * (bf_gms / 100)
    bf_p = bf['Protein(g)'] * (bf_gms / 100)
    bf_c = bf['Carbohydrate(g)'] * (bf_gms / 100)
    bf_f = bf['Fat(g)'] * (bf_gms / 100)

    lun_e = lun['Energy(Kcal)'] * (lun_gms / 100)
    lun_p = lun['Protein(g)'] * (lun_gms / 100)
    lun_c = lun['Carbohydrate(g)'] * (lun_gms / 100)
    lun_f = lun['Fat(g)'] * (lun_gms / 100)

    din_e = din['Energy(Kcal)'] * (din_gms / 100)
    din_p = din['Protein(g)'] * (din_gms / 100)
    din_c = din['Carbohydrate(g)'] * (din_gms / 100)
    din_f = din['Fat(g)'] * (din_gms / 100)

    total_e = round(sum([bf_e, lun_e, din_e]), 2)
    total_p = round(sum([bf_p, lun_p, din_p]), 2)
    total_c = round(sum([bf_c, lun_c, din_c]), 2)
    total_f = round(sum([bf_f, lun_f, din_f]), 2)

    ear_energy = ear_rda[gt]["Energy"]
    rda_protein = ear_rda[gt]["Protein"]
    total_ear_energy = float(ear_energy) * float(w)
    total_rda_protein = float(rda_protein) * float(w)

    energy_status = "adequate" if total_e >= total_ear_energy else "inadequate"
    protein_status = "adequate" if total_p >= total_rda_protein else "inadequate"

    return {
        # "Name": name,
        # "Gender & Activity Level": gt,
        # "Height (cm)": h,
        # "Weight (kg)": w,
        "Total Energy (Kcal) Consumed in the Day": total_e,
        "Total Carbohydrates (g) Consumed in a Day": total_c,
        "Total Protein (g) Consumed in the Day": total_p,
        "Total Fat (g) Consumption in a Day": total_f,
        "Average Energy Consumption": round(total_e / 3, 3),
        "Average Fat Consumption": round(total_f / 3, 3),
        "Average Carbohydrates Consumption": round(total_c / 3, 3),
        "Average Protein Consumption": round(total_p / 3, 3),
        "Total EAR Energy for the Day (Kcal)": total_ear_energy,
        "Total RDA Protein for the Day (g)": total_rda_protein,
        "Energy Intake Status": energy_status,
        "Protein Intake Status": protein_status,
    }

def suggest_options(input, options):
    if input == "":
        return []
    else:
        return [option for option in options if input.lower() in option.lower()]

iface = gr.Interface(
    fn=calculate_nutrition, 
    inputs=[
        gr.Textbox(label="Name"),
        gr.Dropdown(ear_rda,label="Gender - Type of work"),
        # gr.Number(label="Height(m)"),
        gr.Number(label="Weight(Kg)"),
        gr.Dropdown(fi, label="Breakfast"),
        gr.Number(label="Breakfast consumption in gms"),
        gr.Dropdown(fi, label="Lunch"),
        gr.Number(label="Lunch consumption in gms",),
        gr.Dropdown(fi, label="Dinner"),
        gr.Number(label="Dinner consumption in gms")
    ], 
    outputs="json",
    examples=[
        [fi[0], fi[1], fi[2]],
        [fi[10], fi[11], fi[129]],
        [fi[210], fi[110], fi[132]],
        [fi[199], fi[101], fi[312]],
    ],
    title="Nutrition Calculator & Chatbot",
    description="""<p><strong>Objective:</strong> To calculate nutrient intake (Energy, Protein, Carbohydrate, Fat) of various food stuff taken by the respondents per day.</p>
    <p><strong>Developed by:</strong></p>
    <ul>
    <li>Dr.R.Bharathi, Assistant Professor, Department of Home Science, SPMVV, Tirupati</li>
    <li>Dr.N.Rajani, Registrar, SPMVV, Tirupati</li>
    <li>Ms. Kaipa Chandana Sree, Academic Consultant, Dept. of Computer science, SPMVV, Tirupati</li>
    </ul>
    <p>Financial Assistance by DST-CURIE Artificial Intelligence Centre, SPMVV, Tirupati</p>

    Enter what you ate for breakfast, lunch, and dinner to calculate your nutrition intake.""",
)


iface.launch()