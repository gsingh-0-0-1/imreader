from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
import sys
import time
import os
import numpy as np
import codecs
import ephem
import datetime
import pytz
import pandas as pd
import requests
import csv
from flask import Response
import werkzeug
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import img_utils


app = Flask(__name__, template_folder="public/templates/")

@app.route("/")
def main():
	return render_template("main.html")

@app.route('/uploadimg', methods=['POST'])
def uploadfile():
	if request.method == "POST":
		file = request.files['image']
		if file.filename == '' or file == None:
			return "No image file found"
		filename = secure_filename(file.filename)
		ip = request.remote_addr
		targetname = ip + "_" + str(round(time.time()) * 10000) + "_" + filename

		if targetname in os.listdir("images/"): #the chances of this are astronomically low...
			targetname = "n__" + targetname

		file.save("images/" + targetname)


		lang = request.form["lang"]

		if lang == None:
			return "Error finding language."

		text = img_utils.convert_to_text("images/" + targetname, lang)

		text = text.replace("\n", "<br>")

		return text

	return "Failure"

try:
	app.run(host = sys.argv[1], debug = True, port = int(sys.argv[2])) 
except IndexError:
	raise IndexError("Please enter the target IP as the first argument, and the target port as the second.")