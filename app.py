from fooditems import fi, ear_rda
import gradio as gr
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('nutrition.csv')
data_dict = data.set_index('Food/100g').T.to_dict()

def getData(food):
    return data_dict[food]

def calculate_nutrition(name, gt, w, breakfast, bf_gms, lunch, lun_gms, dinner, din_gms):
    bf = getData(breakfast)
    lun = getData(lunch)
    din = getData(dinner)

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
    total_ear_energy = round(float(ear_energy) * float(w),3)
    total_rda_protein = round(float(rda_protein) * float(w),3)

    energy_status = "adequate" if total_e >= total_ear_energy else "inadequate"
    protein_status = "adequate" if total_p >= total_rda_protein else "inadequate"

    return {
        "Energy Intake Status": energy_status,
        "Protein Intake Status": protein_status,
        "Total Energy (Kcal) Consumed in the Day": total_e,
        "Total Protein (g) Consumed in the Day": total_p,
        "Total EAR(Estimated Average Requirements) Energy for the Day (Kcal)": total_ear_energy,
        "Total RDA(Recommended Dietary Allowances) Protein for the Day (g)": total_rda_protein,
        "Total Carbohydrates (g) Consumed in a Day": total_c,
        "Total Fat (g) Consumption in a Day": total_f,
        "Average Energy Consumption": round(total_e / 3, 3),
        "Average Fat Consumption": round(total_f / 3, 3),
        "Average Carbohydrates Consumption": round(total_c / 3, 3),
        "Average Protein Consumption": round(total_p / 3, 3),
        "breakfast": bf,
        "lunch":lun,
        "dinner":din
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
        gr.Number(label="Weight(Kg)"),
        gr.Dropdown(fi, label="Breakfast"),
        gr.Number(label="Breakfast consumption in gms"),
        gr.Dropdown(fi, label="Lunch"),
        gr.Number(label="Lunch consumption in gms",),
        gr.Dropdown(fi, label="Dinner"),
        gr.Number(label="Dinner consumption in gms")
    ], 
    outputs="json",
    title="Nutrition Calculator",
    description="""
<h2>Objective:</h2>
<h3>Our goal is to provide a comprehensive analysis of your daily nutrient intake. This includes Energy, Protein, Carbohydrate, and Fat content of various food items consumed throughout the day.</h3>

<h3>In addition to calculating your total nutrient intake, we also compare your intake against the Estimated Average Requirements (EAR) of Calorie Intake and Recommended Dietary Allowances (RDA) of Proteins. This helps you understand whether your nutrient intake is adequate for your body weight and activity level.</h3>

<h4>Created by:</h4>
<ul>
<h4><li>Dr.R.Bharathi, Assistant Professor, Department of Home Science, SPMVV, Tirupati</li></h4>
<h4><li>Dr.N.Rajani, Registrar, SPMVV, Tirupati</li></h4>
<h4><li>Ms. Kaipa Chandana Sree, Academic Consultant, Dept. of Computer science, SPMVV, Tirupati</li></h4>
</ul>

<h5>Financial Assistance by DST-CURIE Artificial Intelligence Centre, SPMVV, Tirupati</h5>
<h5>Technical Assistance by Venkata Viswanath L</h5>

<hr>

<h3>To get started, enter what you ate for breakfast, lunch, and dinner, along with the respective quantities. The calculator will provide a detailed breakdown of your nutrition intake and compare it against the EAR and RDA values.</h3>
""",
allow_flagging=False,
css="footer {display: none !important}",
article = r"""
📝 **Citation**
<br>
If our work is useful for your research, please consider citing:
```bibtex
@article{VLNutritionCalculator,
  title={Nutrition Calculator: Calculating Total Nutrient Intake per day and comparing against Estimated Average Requirements (EAR) of Calorie Intake and Recommended Dietary Allowances (RDA)},
  author={Dr.R.Bharathi, Dr.N.Rajani and Ms. Kaipa Chandana Sree},
  year={2024}
}
```
📋 **License**
<br>
The Code is under cc-by-4.0 License. 
<br>
📧 **Contact**
<br>
If you have any questions, please feel free to reach out to Dr.R.Bharathi  or at <b>varun.codeq@gmail.com</b>.
"""
)

iface.launch()