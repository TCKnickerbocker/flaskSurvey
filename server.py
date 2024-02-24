from flask import Flask, request, render_template, url_for, jsonify, redirect
from markupsafe import escape
import dbFuncs as dbFuncs
from datetime import date

app = Flask(__name__)

# Setup DB
dbFuncs.setup()


@app.route('/', methods=['GET'])
def homepage():
  return render_template('index.html.jinja') 


@app.route('/declineSurvey', methods=['GET'])
def declineSurvey():
  return render_template('decline.html.jinja') 


@app.route('/survey', methods =["GET", "POST"])
def survey():
  if request.method == "GET":  # If user trying to reroute from index page
    return render_template('survey.html.jinja')
  # Post request:
  curDay = date.today()
  id = dbFuncs.add_survey(request.form, curDay)
  print(id)
  return redirect(url_for('completedSurvey'))


@app.route('/thanks', methods=['GET'])
def completedSurvey():
  return render_template('thanks.html.jinja') 

@app.route('/admin/summary', methods=['GET'])
def viewResults():
  return render_template('results.html.jinja') 


@app.route('/api/results', methods=['GET'])
def getSurveyResults():
  reverse_order = request.args.get('reverse', False)
  # Query the database based on the reverse parameter
  if reverse_order and reverse_order.lower() == 'true':
    survey_responses = dbFuncs.get_surveys(True)
  else:
    survey_responses = dbFuncs.get_surveys()
  return jsonify(survey_responses)


@app.route('/api/counts', methods=['GET'])
def getCounts(key):
  res = dbFuncs.getCounts(key)
  return jsonify({'data': res})


# if __name__ == '__main__':
#     app.run(debug=True, port=8001)
