# Form-Statistics-Analyzer
The Form Statistics Analyzer is a Flask-based web application that allows users to submit a form with various data fields such as time, mission, goal, goal point, pleasure point, and notes. The application saves the submitted form data to an Excel file and provides statistical analysis and insights based on the collected data.

## Screenshots
![screencapture-127-0-0-1-5000-2023-05-07-19_13_44](https://user-images.githubusercontent.com/46647858/236690342-41936c94-f3ec-44bb-9616-cee352370b01.png)
![screencapture-127-0-0-1-8080-2023-05-09-22_10_39](https://github.com/asaykal/Form-Statistics-Analyzer/assets/46647858/68dbcd15-5d17-4dec-99cb-b712a9b68862)
![screencapture-127-0-0-1-8080-statistics-2023-05-09-22_01_17](https://github.com/asaykal/Form-Statistics-Analyzer/assets/46647858/df2b2f95-df70-402d-a93e-ac0bb1e9ccbf)
![screencapture-127-0-0-1-8080-talk-about-statistics-2023-05-09-22_10_10](https://github.com/asaykal/Form-Statistics-Analyzer/assets/46647858/18e288ac-22f2-4fca-9db7-e3e5f8d2022d)


## Technologies Used
- Python
- Flask
- OpenPyXL
- Matplotlib
- OpenAI GPT-3.5

## Usage
1. Clone the repository:
2. Navigate to the project directory
3. Add your OpenAI API key into the config.yaml
4. python app.py
6. Open your web browser and visit http://localhost:5000 or http://127.0.0.1:5000 to access the application.
6. Fill out the form fields with the required information and submit the form.
7. Navigate to the statistics page to view the analyzed statistics and insights.

## Features
- Submission of form data and saving to an Excel file
- Statistical analysis of goal points and pleasure points
- Visualization of goal point and pleasure point distributions
- Calculation of average and maximum goal points and pleasure points
- Analysis of mission occurrences and suggestions based on collected data
- Integration with OpenAI GPT-3.5 for generating insights and suggestions
- Interactive talking about statistics and performance via OpenAI GPT-3.5 LLM
