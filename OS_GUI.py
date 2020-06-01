from OS_Functions import processes_init, arrival_queue_init, FCFS_alg, SJF_alg, SRTF_alg, RR_alg, Average_WT, Average_TWT

from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, FormField, FieldList 
import random, string, glob, os, os.path, operator, ast
from flask_wtf import FlaskForm
# pip install Flask-Table
from flask_table import Table, Col


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class Form1(Form):
    nOfP = StringField('No of Processes', [validators.DataRequired()])
    # alg = HiddenField("alg")
    submit = SubmitField('GO')

class Form2(Form):
    nOfP = StringField('No of Processes', [validators.DataRequired()])
    # alg = HiddenField("alg")
    submit = SubmitField('GO')

class Form3(Form):
    nOfP = StringField('No of Processes', [validators.DataRequired()])
    # alg = HiddenField("alg")
    submit = SubmitField('GO')

class Form4(Form):
    nOfP = StringField('No of Processes', [validators.DataRequired()])
    quantum = StringField('Quantum Time', [validators.DataRequired()])
    submit = SubmitField('GO')

# Add input fields dynamically with wtforms
class TimesEntryForm(Form):
    busrtTime = StringField()
    arrivalTime = StringField()

class ProcessesListForm(Form):
    times = FieldList( FormField(TimesEntryForm), min_entries=1 )
    submit = SubmitField('Submit')




def p_init(nOfP, form):
    p = []
    for i in range(nOfP):
        p_part = []
        for j in range(6):
            p_part.append(0)
        p.append( p_part )

    # print( "P : " + str(p) + "\n" )

    i = -1
    for entry in form.times.entries:
        # print(form.times.entries)
        i += 1
        p[i][0] = i+1 
        p[i][1] = int( entry.data['busrtTime'] )
        p[i][2] = int( entry.data['arrivalTime'] )

    return p

def get_time_result(p):     # get list of WT & TAT 
    result = []
    for x in p :
        result.append( [ x[4] , x[5] ] )

    return result 


# Declare your table
class WT_Table(Table):
    process = Col('Process')
    time = Col('Wait Time')

class TAT_Table(Table):
    process = Col('Process')
    time = Col('Turn Around Time')

# Get some objects
class Item(object):
    def __init__(self, process, time):
        self.process = process
        self.time = time





@app.route("/", methods=['GET', 'POST'])
def index():
    form1 = Form1(request.form)
    form2 = Form2(request.form)
    form3 = Form3(request.form)
    form4 = Form4(request.form)

    if request.method == 'POST':
        if form1.validate() and 'FCFS' in request.form:
            nOfP = form1.nOfP.data
            return redirect( url_for('FCFS_GUI', nOfP=nOfP) )
        elif form2.validate() and 'SJF' in request.form :
            nOfP = form2.nOfP.data
            return redirect( url_for('SJF_GUI', nOfP=nOfP) )
        elif form3.validate() and 'SRTF' in request.form:
            nOfP = form3.nOfP.data
            return redirect( url_for('SRTF_GUI', nOfP=nOfP) )
        elif form4.validate() and 'RR' in request.form:
            nOfP = form4.nOfP.data
            quantum = form4.quantum.data
            return redirect( url_for('RR_GUI', nOfP=nOfP ,quantum=quantum) )
        else:
            print("\nERROR !!\n")
            return 

    return render_template('index.html', form1=form1, form2=form2, form3=form3, form4=form4)



# @app.route("/fcfs_alg", methods=['GET', 'POST'])
@app.route("/fcfs_alg/<nOfP>", methods=['GET', 'POST'])
# def FCFS_GUI():
def FCFS_GUI(nOfP):
    nOfP = int( nOfP )
    # form1 = Form1(request.form)
    # if form1.validate() :      
    #     nOfP = int( form1.nOfP.data )
    # else:
    #     print("\nERROR !!\n")
    #     return 

    if request.method == 'POST' :
        form = ProcessesListForm(request.form)
        if form.validate() :      
            p = p_init(nOfP, form)
            arrivalQueue = arrival_queue_init(nOfP, p)

            FCFS_alg(nOfP, arrivalQueue, p)
            AWT = Average_WT(p, nOfP)
            ATAT = Average_TWT(p, nOfP)
            result = get_time_result(p)
            return redirect(url_for('result', alg_name="FCFS", result=result, AWT=AWT, ATAT=ATAT))

    processes_Times = [None] * nOfP
    form = ProcessesListForm(times=processes_Times)
    return render_template("p_data.html", listFrom=form, alg_name="FCFS")


@app.route("/sjf_alg/<nOfP>", methods=['GET', 'POST'])
def SJF_GUI(nOfP):
    nOfP = int( nOfP )

    # form1 = Form1(request.form1)
    # if form1.validate() :      
    #     nOfP = int( form1.nOfP.data )
    # else:
    #     print("\nERROR !!\n")
    #     return 

    if request.method == 'POST' :
        form = ProcessesListForm(request.form)
        if form.validate() :      
            p = p_init(nOfP, form)
            arrivalQueue = arrival_queue_init(nOfP, p)

            SJF_alg(nOfP, arrivalQueue, p)
            AWT = Average_WT(p, nOfP)
            ATAT = Average_TWT(p, nOfP)
            result = get_time_result(p)
            return redirect(url_for('result', alg_name="SJF", result=result, AWT=AWT, ATAT=ATAT))

    processes_Times = [None] * nOfP
    form = ProcessesListForm(times=processes_Times)
    return render_template("p_data.html", listFrom=form, alg_name="SJF")

@app.route("/srtf_alg/<nOfP>", methods=['GET', 'POST'])
def SRTF_GUI(nOfP):
    nOfP = int( nOfP )

    # form1 = Form1(request.form1)
    # if form1.validate() :      
    #     nOfP = int( form1.nOfP.data )
    # else:
    #     print("\nERROR !!\n")
    #     return 

    if request.method == 'POST' :
        form = ProcessesListForm(request.form)
        if form.validate() :      
            p = p_init(nOfP, form)
            arrivalQueue = arrival_queue_init(nOfP, p)

            SRTF_alg(nOfP, arrivalQueue, p)
            AWT = Average_WT(p, nOfP)
            ATAT = Average_TWT(p, nOfP)
            result = get_time_result(p)
            return redirect(url_for('result', alg_name="SRTF", result=result, AWT=AWT, ATAT=ATAT))

    processes_Times = [None] * nOfP
    form = ProcessesListForm(times=processes_Times)
    return render_template("p_data.html", listFrom=form, alg_name="SRTF")

@app.route("/rr_alg/<nOfP>/<quantum>", methods=['GET', 'POST'])
def RR_GUI(nOfP, quantum):
    nOfP = int( nOfP )
    quantum = int( quantum )

    # form2 = Form2(request.form2)
    # if form2.validate() :      
    #     nOfP = int( form2.nOfP.data )
    #     quantum = int( form2.quantum.data )
    # else:
    #     print("\nERROR !!\n")
    #     return 


    if request.method == 'POST' :
        form = ProcessesListForm(request.form)
        if form.validate() :      
            p = p_init(nOfP, form)
            arrivalQueue = arrival_queue_init(nOfP, p)

            RR_alg(quantum, nOfP, arrivalQueue, p)
            AWT = Average_WT(p, nOfP)
            ATAT = Average_TWT(p, nOfP)
            result = get_time_result(p)
            return redirect(url_for('result', alg_name="RR", result=result, AWT=AWT, ATAT=ATAT))

    processes_Times = [None] * nOfP
    form = ProcessesListForm(times=processes_Times)
    return render_template("p_data.html", listFrom=form, alg_name="RR")



#  alg_name="FCFS", p=p, AWT=AWT, ATAT=ATAT
@app.route("/result/<alg_name>/<result>/<AWT>/<ATAT>", methods=['GET', 'POST'])
def result(alg_name, result, AWT, ATAT):
    result = ast.literal_eval(result)
    print( "\n" + str(result) + "\n" )
    items = []
    for i in range( len(result) ):
        items.append( Item( 'P'+str(i+1) , result[i][0]) )  # WT
    # Populate the table
    table_WT = WT_Table(items)
    
    items = []  
    for i in range( len(result) ):
        items.append( Item( 'P'+str(i+1) , result[i][1]) )  # TAT
    # Populate the table
    table_TAT = TAT_Table(items)

    print(table_WT)
    print(table_TAT)

    return render_template('result.html', table_WT=table_WT, table_TAT=table_TAT, AWT=AWT, ATAT=ATAT, alg_name=alg_name)




"""
                    <!-- <p>{{ form2.submit(name="RR", class_='example_b') }}</p> -->

"""