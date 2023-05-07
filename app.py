from flask import Flask, render_template, request, jsonify
from openpyxl import Workbook, load_workbook
from datetime import date
import os, statistics, base64, openai, yaml, matplotlib

matplotlib.use('Agg')  

import matplotlib.pyplot as plt
from io import BytesIO
from collections import Counter

app = Flask(__name__)

class formApp:
    def __init__(self):
        self.time = ""
        self.mission = ""
        self.goal = ""
        self.goal_point = 0
        self.pleasure_point = 0
        self.notes = ""

def save_to_excel(time, mission, goal, goal_point, pleasure_point, notes):
    today = date.today()
    file_name = f"form_results_{today}.xlsx"

    if os.path.exists(file_name):
        wb = load_workbook(file_name)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.append(["Time", "Mission", "Goal", "Goal Point", "Pleasure Point", "Notes"])

    next_row = ws.max_row + 1

    ws.cell(row=next_row, column=1).value = time
    ws.cell(row=next_row, column=2).value = mission
    ws.cell(row=next_row, column=3).value = goal
    ws.cell(row=next_row, column=4).value = goal_point
    ws.cell(row=next_row, column=5).value = pleasure_point
    ws.cell(row=next_row, column=6).value = notes

    wb.save(file_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def form_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'})

    time = data.get('time')
    mission = data.get('mission')
    goal = data.get('goal')
    goal_point = data.get('goal_point')
    pleasure_point = data.get('pleasure_point')
    notes = data.get('notes')

    if not time or not mission or not goal:
        return jsonify({'error': 'Missing required form data'})

    try:
        goal_point = int(goal_point)
        pleasure_point = int(pleasure_point)
    except ValueError:
        return jsonify({'error': 'Invalid form data type'})

    form_app = formApp() 

    form_app.time = time
    form_app.mission = mission
    form_app.goal = goal
    form_app.goal_point = goal_point
    form_app.pleasure_point = pleasure_point
    form_app.notes = notes

    save_to_excel(form_app.time, form_app.mission, form_app.goal, form_app.goal_point, form_app.pleasure_point, form_app.notes)

    return jsonify({'response': 'Form is submitted'})

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

api_key = config["openai"]["api_key"]
openai.api_key = api_key

def analyze_statistics(times, mission_names, goal_points, pleasure_points, notes):
    times_str = '\n'.join(times)
    mission_names_str = '\n'.join(mission_names)
    goal_points_str = '\n'.join(str(point) for point in goal_points)
    pleasure_points_str = '\n'.join(str(point) for point in pleasure_points)
    notes_str = '\n'.join(notes)

    prompt = f"""
    
    Today is {date.today()}.
    
    Times:
    {times_str}
    
    (Times mean : If 15 - 16 = mission has done in 15:00 - 16:00 in 24 hour format )
    
    Mission Names:
    {mission_names_str}

    Goal Points:
    {goal_points_str}

    Pleasure Points:
    {pleasure_points_str}

    Notes:
    {notes_str}

    Analyze the statistics and provide insights.
    And give activity, topic or things(book, movie, food etc.) sugesstions based on the statistics.

    1-

    2-

    3-

    4-
    
    5-
    """

    completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [
                    {"role" : "system", "content" :   
                                                    """ 
                                                    You are an Statistician and Psychologist. You analyze the daily statistics of people and provide insights. You also give them advice on how to improve their lives. And similar missions that person had good performance.
                                                    """ 
                                                    },
                    {"role" : "user", "content" : f" {prompt} "}, 
                    {"role" : "assistant", "content" : "Assistant : "}
                            ],
                n=1,
                stop=None, 
                temperature=0.4,
            )
    analyzed_statistics = completion['choices'][0]['message']['content']

    return analyzed_statistics

@app.route('/statistics')
def statistics_endpoint():
    file_name = f"form_results_{date.today()}.xlsx"

    if not os.path.exists(file_name):
        return render_template('statistics.html', error='No data available')

    wb = load_workbook(file_name)
    ws = wb.active
    
    mission_names = [cell.value for cell in ws['B'][1:]]
    times = [cell.value for cell in ws['A'][1:]]

    goal_points = [cell.value for cell in ws['D'][1:]]
    pleasure_points = [cell.value for cell in ws['E'][1:]]
    
    goal_points = [int(point) for point in goal_points if point is not None]
    pleasure_points = [int(point) for point in pleasure_points if point is not None]

    mission_counts = Counter(mission_names)
    unique_missions = list(mission_counts.keys())
    mission_occurrences = list(mission_counts.values())

    if not goal_points or not pleasure_points:
        return render_template('statistics.html', error='No data available')

    goal_point_avg = statistics.mean(goal_points)
    pleasure_point_avg = statistics.mean(pleasure_points)
    goal_point_max = max(goal_points)
    pleasure_point_max = max(pleasure_points)

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(goal_points)), goal_points)
    plt.xticks(range(len(goal_points)), [f'{mission}\n{time}' for mission, time in zip(mission_names, times)], rotation='vertical')
    plt.xlabel('Görev ve Zaman Aralığı')
    plt.ylabel('Hedefe Ulaşma Puanı')
    plt.title('Hedef Puanı Dağılımı')
    plt.tight_layout()

    goal_points_buffer = BytesIO()
    plt.savefig(goal_points_buffer, format='png')
    goal_points_buffer.seek(0)
    goal_points_data = base64.b64encode(goal_points_buffer.getvalue()).decode('utf-8')

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(pleasure_points)), pleasure_points)
    plt.xticks(range(len(pleasure_points)), [f'{mission}\n{time}' for mission, time in zip(mission_names, times)], rotation='vertical')
    plt.xlabel('Yapılan ve Zaman Aralığı')
    plt.ylabel('Keyif Alma Puanı')
    plt.title('Keyif Puanı Dağılımı')
    plt.tight_layout()

    pleasure_points_buffer = BytesIO()
    plt.savefig(pleasure_points_buffer, format='png')
    pleasure_points_buffer.seek(0)
    pleasure_points_data = base64.b64encode(pleasure_points_buffer.getvalue()).decode('utf-8')

    plt.figure(figsize=(8, 6))
    plt.pie(mission_occurrences, labels=unique_missions, autopct='%1.1f%%')
    plt.title('Mission Occurrences')
    plt.tight_layout()

    mission_occurrences_buffer = BytesIO()
    plt.savefig(mission_occurrences_buffer, format='png')
    mission_occurrences_buffer.seek(0)
    mission_occurrences_data = base64.b64encode(mission_occurrences_buffer.getvalue()).decode('utf-8')
    
    notes = [cell.value for cell in ws['F'][1:]]
    
    analyzed_statistics = analyze_statistics(times, mission_names, goal_points, pleasure_points, notes)

    return render_template('statistics.html', goal_point_avg=goal_point_avg,
                        pleasure_point_avg=pleasure_point_avg,
                        goal_point_max=goal_point_max,
                        pleasure_point_max=pleasure_point_max,
                        goal_points_data=goal_points_data,
                        pleasure_points_data=pleasure_points_data,
                        mission_occurrences_data=mission_occurrences_data,
                        analyzed_statistics=analyzed_statistics
                        )

if __name__ == '__main__':
    app.run()
