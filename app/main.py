# Run by typing python3 main.py

## **IMPORTANT:** only collaborators on the project where you run
## this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os

# import stuff for our web server
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from flask import jsonify
from utils import get_base_url, allowed_file, and_syntax
from flask import session, app
from datetime import timedelta
import re

# import stuff for our models
import torch
from aitextgen import aitextgen

'''
Coding center code - comment out the following 4 lines of code when ready for production
'''
# load up the model into memory
# you will need to have all your trained model in the app/ directory.
# EDIT THIS LINE TO LOAD IN YOUR MODEL INSTEAD
ai = aitextgen(to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
#port = 41233
#base_url = get_base_url(port)
#app = Flask(__name__, static_url_path=base_url+'static')

'''
Deployment code - uncomment the following line of code when ready for production
'''
app = Flask(__name__)

@app.route('/')
#@app.route(base_url)
def home():
    return render_template('webpages/combined/index.html', generated=None)

@app.route('/index', methods=['POST'])
#@app.route(base_url + "/index")
def home_post():
    return redirect(url_for('home'))

@app.route('/', methods=['POST'])
#@app.route(base_url, methods=['POST'])
def redirect_results():
    return redirect(url_for('results'))

@app.route('/results')
#@app.route(base_url + '/results')
def results():
    return render_template('webpages/combined/index.html', generated=None)

@app.route('/team')
#@app.route(base_url + '/team')
def Team():
    return render_template('webpages/combined/Team.html', generated=None)

app.route('/about')
#@app.route(base_url + '/about')
def About():
    return render_template('webpages/combined/About.html', generated=None)

@app.route('/resources')
#@app.route(base_url + '/resources')
def resources():
    return render_template('webpages/combined/Resources.html', generated=None)

@app.route('/howitworks')
#@app.route(base_url + '/howitworks')
def howitworks():
    return render_template('webpages/combined/How-It-Works.html', generated=None)


@app.route('/generate_text', methods=["POST"])
#@app.route(base_url + '/generate_text', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """
    #print("I am thinking...")
    #print(request.form.keys())
    prompt = request.form['final']
#     jrequest = request.get_json()
#     print(jrequest)
#     prompt = jrequest['final']
#     print(prompt)
    if prompt is not None:
        generated = ai.generate(
            n=1,
            batch_size=4,
            prompt=str(prompt),
            max_length=100,
            temperature=0.7,
            top_p = 1,
            return_as_list=True
        )
    #######HERE WE MAKE A LARGE CHANGE. 
    #######IN ORDER TO GET OUR THING WORKING, WE HAVE TO MAKE THE GENERATED TEXT
    #######NOT INCLUDE THE PROMPT ITSELF SO HERE WE REMOVE THE PROMPT FROM GENERATED
    #print(generated)
    toremove = request.form['toremove']
    length_of_toremove = len(toremove)
    generated[0] = (generated[0])[length_of_toremove:]

    generated[0] = re.sub(r"[^\x00-\x7F]", "", generated[0])
            #[^\x00-\x7F] means all nonascii characters

    data = {'generated_ls': generated}
    #print("I have generated!")
    #print(generated)
    #print("\n")
    #print(jsonify(data))
    return jsonify(data)

if __name__ == "__main__":
    '''
    coding center code
    '''
    # IMPORTANT: change the cocalcx.ai-camp.org to the site where you are editing this file.
    website_url = 'cocalc5.ai-camp.org'
    print(f"Try to open\n\n    https://{website_url}" + base_url + '\n\n')

    app.run(host = '0.0.0.0', port=port, debug=True)
    import sys; sys.exit(0)

    '''
    scaffold code
    '''
    # Only for debugging while developing
    # app.run(port=80, debug=True)
