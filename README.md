# Visualizing-Recursive-Trees

This project is to help visualize recursion by tracking recursive calls using a stack trace. Recursion may be a difficult concept to grasp for beginners and therefore this tool is meant to help picture recursion trees.

Web based application that allows users to choose from a list of recursive functions and give a valid input to render a picture of the recursive tree for that algorithm. 

Application.py currently has predefined recursive functions to choose from, but it should work with any recursive function. 

To run this: 

install Flask, graphviz

export FLASK_APP= application.py
export FLASK_ENV = development 

flask run
flask run --host=0.0.0.0 #to host from your IP address


Sample Image:
![0callgraph](https://user-images.githubusercontent.com/26440404/49846215-391f2980-fd98-11e8-9eed-981a790d914b.png)
