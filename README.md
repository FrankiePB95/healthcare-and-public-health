# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Healthcare and Public Health

** This project is a data analysis venture undertaken in attempts to create an application that addresses the question regarding lifestyle factors and cognitive issues presented to an aged population, and how these factors relate to the risk of Alzheimer's disease. Employing a real world clinical dataset, we explore characteristic features (biomarkers) such as age, gender and ethnicity; lifestyle habits such as physical activity, alcohol consumption and diet quality; as well as potential cognition afflictions, such as depression, memory lapse, behavioural problems and personality changes and their relations to dementia. The project leans from data extraction and cleaning, towards machine learning, predictive modelling and AI integration, spanning a wide breadth, with hopes to better allow for risk indication, and the pre-emptive provision of actionable insights towards intervention. 


## Table of Contents

- [Project Plan](#project-plan)
- [Hypothesis](#hypothesis)
- [Business Requirements](#business-requirements)
- [Target Audience](#target-audience)
- [User Stories](#user-stories)
- [Variables](#variables)
- [Dashboard Design](#dashboard-design)
- [Deployment](#deployment)
- [Features](#features)
- [Main Data Analysis Libraries](#main-data-analysis-libraries)
- [Analysis Techniques Used](#analysis-techniques)
- [Bugs](#bugs)
- [Development Roadmap](#development-roadmap)
- [Ethical Considerations](#ethical-considerations)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)
- [Kaggle Citation](#kaggle-citation)

## Project Plan
The project followed these steps:
* 1. Data Extraction: Data was retrieved from Kaggle and loaded to notebook using Pandas.
* 2. Data Cleaning and Transformation: Cleaning included checking or missing values, dropping duplicated and capitalising columns. 
3. Data loading: Loaded data to notebook, cleaned it, created transformers with Feature Engine and used SciKit-Learn to fit pipelines to clean data.
* 3. Data visualization: Used Matplotlib, Seaborn and Plotly to generate visualizations that allow for the exploration of relationships and patterns. Created a dashboard using Streamlit tools and deployed with Heroku.
* 4. Analysis and Interpretation: Dashboard has advanced visualisations that help answer the hypothesis as well as further tools that serve the business requirements and user stories.

## Hypothesis
There lies a correlation between age, cognitive ability and lifestyle factors in relation to Alzheimer's Disease.

###Consider the following 4 validations:
 - **Validation** Created tabular chart within the dashboard that allows for statistical insights revolving lifestyle factors such as smoking, diet, quality and alcohol consumption. Users can observe frequently prevent values, minimum values, standard deviation and more.
 - **Validation** Created an interactive 3D scatter matrix that consider age, MMSE score and BMI in its relation to overall health to gauge relationships between these.
 - **Validation** Created a risk factor correlation matrix that plots factors against each other, including cholesterol total, physical activity and activities in daily life and age to gauge their relationships with dementia risk.
 - **Validation** Created an interactive bar chart and pie chart that filters along a slider fitted with all factors within a dataset, including personality changes, memory complaints and gender to find what combinations of factors may seen individuals more or less at risk.

## Business Requirement
1. Risk assessment and early detection for early intervention
2. Statistics for certain factors that might contribute to higher dementia risk 
3. Identify high risk patients for resource management
4. Consider certain factors that when existing together, contribute to higher risks for further insights

## Target Audience
The target audience are health professionals ranging from entry level to highly skilled. The dashboard provides easy to use visuals, narratives as well as some more technical data (that is explained) that fits the range of these individuals. It's easy to use, uses minimal jargon, descriptive and lightweight.

## User Stories
	* As an registered nurse working with elderly patients, I want to be able to prioritize the care I serve to my patients via what ails them and what might ail, as such I'd to know what potential risk levels they are at of developing Alzheimer's.
	* As a healthcare assistant, I want know which service users I should pay better attention to, due to the potential factors they face surrounding dementia risk.
	*As a geriatrician, I want an application that will help me deduce which of my patients is more at risk of dementia so I can better take steps in providing specialist support.

From the dashboard, I would consider recommending:
1. The real time reporting
2. Statistical insights
3. Predictive modelling 

## Variables
Patient Information

###Patient ID
PatientID: A unique identifier assigned to each patient - 4751 to 6900.

###Demographic Details
Patient Age: The age of the patients ranges from 60 to 90 years.
Gender: Gender of the patients - Male and Female.
Ethnicity: The ethnicity of the patients - Caucasian, African American, Asian and Other

###Lifestyle Factors
BMI: Body Mass Index of the patients - 15 to 40.
Smoking: Smoking status - Yes and No.
Alcohol_Consumption: Weekly alcohol consumption in units - 0 to 20.
Physical_Activity: Weekly physical activity in hours - 0 to 10.
Diet_Quality: Diet quality score -  0 to 10.

###Medical History
Cardiovascular_Disease: Presence of cardiovascular disease - Yes and No.
Depression: Presence of depression - Yes and No.
Cholesterol_Total: Total cholesterol levels - 150 to 300 mg/dL.

###Cognitive and Functional Assessments
MMSE: Mini-Mental State Examination score - 0 to 30 (lower scores indicate cognitive impairment).
Functional_Assessment: Functional assessment score - 0 to 10 (lower scores indicate greater impairment).
Memory_Complaints: Presence of memory complaints - Yes and No.
Behavioral_Problems: Presence of behavioral problems - Yes and No.
Activities_Of_Daily_Living score- 0 to 10. (lower scores indicate greater impairment).

Symptoms
Personality_Changes: Presence of personality changes - Yes and No.
Difficulty_Completing_Tasks: Presence of difficulty completing tasks - Yes and No.
Diagnosis: Diagnosis status for Alzheimer's Disease - Yes and No. 

## Dashboard Design
### Page 1: Home Page
* Home Page
	* Provide an overview of the app
	* Provides the app's key features

### Page 2: Summary Page
*Summary Page
	* Further information on key features such as machine learning and statistical analysis.
	* Technical stacks used
	* How to use the dashboard

### Page 3: Alzheimer's Disease Dashboard
* Alzheimer's Disease Dashboard
	*Tabular statistical data
	*Patient filters
	*Infographics
	*Insights and findings
	*Methodology
	*Narratives

### Page 4: Conclusion
*Conclusion
	*Project achievement
	*Key findings
	*Future applications

## Deployment
### Prerequisites

- Python 3.12.8 recommended
- pip

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/frankiepb95/health-care-and-public-health.git
cd health-care-and-public-health

### Heroku

* The App live link is: https://healthcare-and-public-health-7e119d1e6a3c.herokuapp.com/ 
* The project was deployed to Heroku using the following steps.

1. Log in to Heroku and create an App
2. At the Deploy tab, select GitHub as the deployment method.
3. Select your repository name and click Search. Once it is found, click Connect.
4. Select the branch you want to deploy, then click Deploy Branch.
5. The deployment process should happen smoothly in case all deployment files are fully functional. Click now the button Open App on the top of the page to access your App.

## Features
- Data Loading: Import dataset from CSV.
- Data Cleaning: Handling of outliers, missing values and automatic capitalization.
Statistical Analysis: Normality test, correlation analysis, t-tests, hypothesis testing, and more.
- Visualisation: Generate bar charts, histograms, scatter plots, and custom visualisations.
- Export: Save analysis results in various formats, including CSV and txt.
- Risk scoring based on age, BMI, lifestyle factors
- Correlation between MMSE scores and functional assessment
- High-risk patient identification filters
- Risk score calculation
- Interactive filtering by age groups, lifestyle factors etc.
-Color-coded risk levels (Low/Medium/High)
-Export high-risk patient lists

## Main Data Analysis Libraries
* NumPy for number manipulations
* Pandas – for data loading, cleaning and transformation
* Matplotlib – for static plots
* Seaborn – for statistical visualisations
* Plotly – for interactive charts
* Feature-Engine - for creating transformers
* SciKit-Learn - for fitting the pipeline

## Analysis Techniques Used
* Descriptive statistics to describe what was taking place within different visualizations
* Correlation analysis to identify relationships with risk factors
* Charts for comparisons
* Mean, median and standard deviation for centric data considerations
**Limitations**: Possibly consider a larger dataset next time with more factors for a wider range of views
**Use of AI tools**: Copilot was used also

## Bugs
There was many times code didn't load or I had to be introduced to new concepts. I had to figure out ways to better structure and order my code and decide what to use and what not to use and this began increasingly taxing, especially when AI didn't have the answers either. But it wasn't all that bad, VS Code does provide some help with definitions, and elsewhere I did have help from facilitators who provided templates to better documents such as my README, for instance.

## Reflection
The challenge was fun to take on. Though there were challenges. For instance, finding the right time, or not understanding something presented to me. I had to fit a lot of time around my schedule and come to grips with a lot of technical jargon online, or via libraries within application such as VS Code.

The project kept me busy and given the timeframe and circumstances, I'm pleased with the overall results, though, and I look towards many more to come.

## Development Roadmap
**Challenges faced**:
* Package conflicts.
* Kernel not loading.
* Code note generating.
**Overcoming them**:
* I had to go through cycles of package upgrade and downgrade, or not using a package or 
* I had to go through cycles or kernel restarts. 
* I had to shuffle through different code, omit using specific code or opt for more simplistic or complex code at times.
**Next steps**:
* I plan to explore more packages, languages and applications, such as Scipy, SQL and Google Analytics. These may help me better develop more data analytical skills. 

## Ethical Considerations
* The GDPR stipulates certain data handling necessities when using other's data, including how long you can hold it for and requiring permission for its use. In the original dataset, doctor's names were withheld and minimal to no identifying patient data was provided. The creator of the dataset had stipulated including a line for the set's use, which was included at the end of this document.

## Credits 
### Content 
- **GitHub Copilot**  
GitHub Copilot in VS Code allowed for better coding structure and syntax, design thinking, recommendations and less code repetition. It was very useful, helping me optimise my code and properly lay out my ideas.

  I used Copilot to guide me through the project when I encountered issues. Specific examples include:
  - Troubleshooting errors such as:
    - Syntax errors - fixes included using alternative code code.
    - Package conflict errors errors - fixes included test other packages, downgrading or upgrading pages.
  - Helping with visualizations, like:
    - Creation
    - Labelling
  - Explaining technical concepts including:
    - What packages such as Scipy are used for.
  - Helping with my dashboard creation
    - Ideation
    - Design thinking
    - Creating narratives
    - Summarising key findings
    - Infographics
    - Business requirements

## Acknowledgements
Thanks to:
* Code Institute for the project structure
* Kaggle for providing the dataset
* Monday for project management tools
* Streamlit for dashboard tools
* GitHub Copilot for coding support
* Code Institute peers for being there throughout

## Kaggle Citation
@misc{rabie_el_kharoua_2024,
title={Alzheimer's Disease Dataset},
url={https://www.kaggle.com/dsv/8668279},
DOI={10.34740/KAGGLE/DSV/8668279},
publisher={Kaggle},
author={Rabie El Kharoua},
year={2024}
}