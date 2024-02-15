#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <html>
     <head>
         <style>
             body {
                 display: flex;
                 align-items: center;
                 justify-content: center;
                 height: 100vh;
                 margin: 0;
             }

             form {
                 text-align: center;
             }
         </style>
     </head>
     <body>
         <form action="/echo_user_input" method="POST">
             <input name="user_input">
             <input type="submit" value="Submit!">
         </form>
     </body>
     </html>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text
