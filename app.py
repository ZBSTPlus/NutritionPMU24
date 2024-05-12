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
        # "Average Energy Consumption": round(total_e / 3, 3),
        # "Average Fat Consumption": round(total_f / 3, 3),
        # "Average Carbohydrates Consumption": round(total_c / 3, 3),
        # "Average Protein Consumption": round(total_p / 3, 3),
        # "breakfast": bf,
        # "lunch":lun,
        # "dinner":din
    }

def suggest_options(input, options):
    if input == "":
        return []
    else:
        return [option for option in options if input.lower() in option.lower()]

iface = gr.Interface(
    # Function to calculate nutrition
    fn=calculate_nutrition, 
    # Define the inputs
    inputs=[
        gr.Textbox(label="Enter Your Name"),
        gr.Dropdown(ear_rda,label="Select Your Gender and Type of Work"),
        gr.Number(label="Enter Your Weight (in Kg)"),
        gr.Dropdown(fi, label="Select Breakfast Items", multiselect=True),
        gr.Number(label="Enter the Quantity of Each Breakfast Item in Grams (separated by commas if multiple items are selected)"),
        gr.Dropdown(fi, label="Select Lunch Items", multiselect=True),
        gr.Number(label="Enter the Quantity of Each Lunch Item in Grams"),
        gr.Dropdown(fi, label="Select Dinner Items", multiselect=True),
        gr.Number(label="Enter the Quantity of Each Dinner Item in Grams")
    ], 
    # Define the output
    outputs="json",
    # Set the title
    title="Nutrition Calculator",
    # Set the theme
    theme="gradio/monochrome",
    # Set the description
    description="""
<h2>Purpose:</h2>
<h3>We aim to provide a detailed analysis of your daily nutrient intake, including Energy, Protein, Carbohydrate, and Fat content of various food items consumed throughout the day.</h3>

<h3>Besides calculating your total nutrient intake, we also compare your intake against the Estimated Average Requirements (EAR) of Calorie Intake and Recommended Dietary Allowances (RDA) of Proteins. This comparison helps you understand whether your nutrient intake is adequate for your body weight and activity level.</h3>

<h4>Developed by:</h4>
<ul>
<h4><li>Dr.R.Bharathi, Assistant Professor, Department of Home Science, SPMVV, Tirupati</li></h4>
<h4><li>Dr.N.Rajani, Registrar, SPMVV, Tirupati</li></h4>
<h4><li>Ms. Kaipa Chandana Sree, Academic Consultant, Dept. of Computer science, SPMVV, Tirupati</li></h4>
</ul>

<h5>Financial Support by DST-CURIE Artificial Intelligence Centre, SPMVV, Tirupati</h5>
<h5>Technical Support by Venkata Viswanath L</h5>

<hr>

<h3>To begin, input what you consumed for breakfast, lunch, and dinner, along with the respective quantities. The calculator will provide a detailed breakdown of your nutrition intake and compare it against the EAR and RDA values.</h3>
""",
    # Disable flagging
    allow_flagging=False,
    # Hide the footer
    css="footer {display: none !important}",
    # Set the article
    article = r"""
📝 **How to Cite Our Work**
<br>
If our work is beneficial for your research, please consider citing:
```bibtex
@article{VLNutritionCalculator,
  title={Nutrition Calculator: A Tool for Calculating Total Nutrient Intake per day and Comparing against Estimated Average Requirements (EAR) of Calorie Intake and Recommended Dietary Allowances (RDA)},
  author={Dr.R.Bharathi, Dr.N.Rajani and Ms. Kaipa Chandana Sree},
  year={2024}
}
```

<br>

**📋 License Information**
<br> The Code is licensed under cc-by-4.0 License. <br> 
**📧 Get in Touch** 
<br> 
If you have any queries, please feel free to contact Dr.R.Bharathi or Venkata Viswanath at <b>varun.codeq@gmail.com</b>.
"""
)
iface.launch()