# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 12:22:02 2022

@author: Ramachandran S S
"""
import os
import json
from flask import Flask, request, render_template
from flask import redirect
from flask import url_for

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
static_path = os.path.join(project_root, './static')


app = Flask(__name__,template_folder=template_path,static_folder=static_path)
f = open('question.json')
questions_json = json.load(f)
global count
count = 1
global answers
answers = []


@app.route('/')
def hello_world():
   # image_qc = os.path.join(project_root,'static','img','qc.jpg')
   # print(static_path)
   # print(image_qc)
   return render_template('./main_screen.html')

@app.route('/quiz_page/<num>')
def quiz_page(num):
    # if(request.method == 'POST'):
    #     print('POST')
    #     if request.form['A'] == 'A':
    #         print('A')
    #     elif request.form['B'] == 'B':
    #         print('B')
    #     elif request.form['C'] == 'C':
    #         print('C')
    #     elif request.form['D'] == 'D':
    #         print('D')
    #     elif request.form['E'] == 'E':
    #         print('E')
            
    #else:
    global count
    if(int(num)!=count):
        return redirect(url_for('quiz_page',num=count))
    
    if int(num)<len(questions_json)+1:
        option_len = int(questions_json.get('Q'+str(num)).get('options'))
        option_1 = questions_json.get('Q'+str(num)).get('a',None)
        option_2 = questions_json.get('Q'+str(num)).get('b',None)
        option_3 = questions_json.get('Q'+str(num)).get('c',None)
        option_4 = questions_json.get('Q'+str(num)).get('d',None)
        option_5 = questions_json.get('Q'+str(num)).get('e',None)
        option_6 = questions_json.get('Q'+str(num)).get('f',None)
        pb_width = (int(num) / (len(questions_json)+1)) * 100
        return render_template('./quiz_screen.html',question_num='Question Num: '+str(num),question=questions_json.get('Q'+str(num)).get('question'),option_length=option_len,
                               option_1=option_1,option_2=option_2,option_3=option_3,option_4=option_4,
                               option_5=option_5,option_6=option_6,pb_width=pb_width)
    else:
        return redirect(url_for('results'))

@app.route('/action/<option>')
def action(option):
    print(option)
    global answers
    answers.append(option)
    global count
    count = count + 1
    print(answers)
    return redirect(url_for('quiz_page',num = count))

@app.route('/results')
def results():
    f = open('results.json')
    results_json_format = json.load(f)
    option = ""
    global answers
    if len(answers) != len(questions_json):
        return redirect(url_for('hello_world'))
    
    option = option.join(answers)
    print(option)
    result_string = results_json_format[option]
    description = {
        "hardware happener" : "you push the limits of nature to make possible a new type of computer",
        "software strategist" : "you engineer the bridge from hardware to algorithm",
        "algorithm ace" : "you're the top of the stack and carry the team's aspirations",
        "computer architecture cartographer" : "you map out unexplored territory",
        "chemistry clairvoyant" : "you saw the future where you will be among the first users of commercial quantum computers",
        "communication climb-tack" : "you pave the way to courier information to hard-to-reach places",
        "cryptography craftsmaster" : "you refine protocols to protecc us all",
        "theory thoughtcaster" : "you build our foundations of quantum mechanics and information",
        "sensing sleuth" : "you chase leads detecting defects or synthesizing more sophisticated sensors",
        "applications afficionado" : "you have the joy of using emerging technologies to tackle problems from new angles"        
        }
    answers.clear()
    global count
    count = 1
    return render_template('./results.html',category=result_string,desc=description[result_string])

if __name__ == '__main__':
    app.run()