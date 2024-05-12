import gradio as gr

fi = ear_rda = ["Baked macoroni pasta",
               "Bread toast","Chapati","Cornflakes with milk",]

def greet(name,d,w,b,b1,l,l1,d1,d2):
    return d
  
demo = gr.Interface(
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
}```

<br>

** 📋 License Information **
<br> The Code is licensed under cc-by-4.0 License. <br> 
📧 Get in Touch <br> If you have any queries, please feel free to contact Dr.R.Bharathi or at <b>varun.codeq@gmail.com</b>.
"""
)


if __name__ == "__main__":
    demo.launch()   