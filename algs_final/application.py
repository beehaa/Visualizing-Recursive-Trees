
from flask import Flask, request, render_template, send_from_directory, url_for, Response
from rcviz.rcviz import CallGraph, viz
import time
import sys, os

import inspect
from types import FunctionType
import glob

"""

export FLASK_APP=application.py
export FLASK_ENV=development    #DEBUG MODE
flask run                       #LOCAL MACHINE
flask run --host=0.0.0.0        #USE YOUR MACHINE AS HOST, PORT = 5000 DEFAULT

"""

#point image folder to pics instead of static
app = Flask(__name__, static_folder='pics')
# app.run()
# app.run(host= '0.0.0.0')

#clear cache to reload image
response = Response()
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#callgraph object instance
cg = CallGraph()

"""             ADD MORE RECURSIVE FUNCTIONS HERE           """

@viz(cg) #viz to visualize and trace system stack
def quicksort(items): #takes list of strings
    # item = list(items) #use this if items is a string
    if len(items) <= 1:
        return items
    else:
        pivot = items[0]
        lesser = quicksort([x for x in items[1:] if x < pivot])
        greater = quicksort([x for x in items[1:] if x >= pivot])
        return lesser + [pivot] + greater

@viz(cg)
def LIS_smaller(seq, x):
    seq2 = seq
    seq = []
    for i in seq2:
        seq.append(int(i))
    size = len(seq)

    if size == 0:
        return 0
    seq_cut = seq[:size-1]
    n_val = seq[size-1]
    m = LIS_smaller(seq_cut,x)
    if n_val < x:
        m = max(m, 1+LIS_smaller(seq_cut,n_val))
    return m

@viz(cg)
def fib(n):
    if n <=1:
        return n
    else:
        return (fib(n-1)+fib(n-2))

@viz(cg)
def sumFirstN(n):
    if n==0:
        return 0
    else:
        return n + sumFirstN(n-1)

@viz(cg)
def LPS(seq):
    size = len(seq)
    i = 0
    j = size-1
    if size <= 0:
        return 0
    if size == 1:
        return 1
    elif seq[0] == seq[len(seq)-1]:
        return 2 + LPS(seq[1+i:j])
    else:
        return max(LPS(seq[i+1:]), LPS(seq[:j]))

@viz(cg)
def list_sum_recursive(input_list):
    # Base case
    if input_list == []:
        return 0
    else:
        head = input_list[0]
        smaller_list = input_list[1:]
        return head + list_sum_recursive(smaller_list)
@viz(cg)
def factorial(x):
    if x == 1:
        return 1
    else:
        return (x * factorial(x-1))

def extract_wrapped(decorated):
    closure = (c.cell_contents for c in decorated.__closure__)
    return next((c for c in closure if isinstance(c, FunctionType)), None)


def getCodeString(nameOfFunction):
    list1= (inspect.getsourcelines(extract_wrapped(nameOfFunction)))[0][1:]
    return ''.join(list1)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['GET','POST']) #DO WE NEED GET/?
def submit():
    cg.reset()
    #target folder, make new if not there
    target = os.path.join(APP_ROOT, 'pics/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    #get text from form
    x =request.form['text']
    y = request.form['text2']
    print(x)
    print(y)


    #selector for recursive functions
    code =[]

    if x == 'LIS':
        code= getCodeString(LIS_smaller)
        ex = [int(s) for s in y.split(',')]
        print(LIS_smaller(ex, sys.maxsize))
    if x == 'LPS':
        code= getCodeString(LPS)
        #ex = [str(s) for s in y.split(',')]
        print(LPS(y))
    if x == 'QuickSort':
        code= getCodeString(quicksort)
        print(quicksort(y))
    if x == 'Fibonacci':
        code= getCodeString(fib)
        print(fib(int(y)))
    if x == 'SumFirstN':
        code= getCodeString(sumFirstN)
        print(sumFirstN(int(y)))
    if x == 'Factorial':
        code= getCodeString(factorial)
        print(factorial(int(y)))
    if x == 'ListSum':
        code= getCodeString(list_sum_recursive)
        ex = [int(s) for s in y.split(',')]
        print(list_sum_recursive(ex))


    cg.render("sort.png")

    IMAGES =[]
    os.chdir(os.getcwd())
    for file in glob.glob("*.png"):
        IMAGES.append(file)
    IMAGES.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    # print(os.getcwd())
    filename = IMAGES[len(IMAGES)-1]
    # print(filename)
    cg.reset()
    # print(IMAGES)



    cg.reset() #reset callgraph object

    #file name for rendered pic
    # filename = '0callgraph.png'

    # return 'You entered: {}'.format(x+" : "+y)
    # return render_template('submit.html', image_name = filename)
    return render_template('submit.html', image_name = filename, codeRan = code, Title = x)
