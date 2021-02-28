from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import re

def isEntryLevelQ(job_title, job_description):

    # Define the patterns
    title_pattern = r"I{2,3}|IV|[sS]enior|[sS]r\.*|[lL]ead|[dD]irector|[Pp]rincipal|[mM]anage|[eE]xperienced"

    description_pattern = r"(?:[mM]inimum|[mM]in\.?|[aA]t least|[tT]otal|[iI]ncluding|[wW]ith).+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\+* (?:[yY]ears*|[yY]rs*)|[mM]aster'?s"

    # Try to find the patterns
    inTitleQ = re.search(title_pattern, job_title) != None
    inDescriptionQ = re.search(description_pattern, job_description) != None

    # Consider entry level if no matches
    return not (inTitleQ or inDescriptionQ)

def JobFilter(job_list):
    return [job for job in job_list if isEntryLevelQ(job['jobtitle'], job['description'])]

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    #This if statement handles the search requests both from index and the search page
    if request.method == 'POST':
        jobtitle = request.form.get('jobtitle')
        location = request.form.get('location')
        return redirect(url_for('search', jobtitle=jobtitle, location=location))
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')

@app.route('/credits/')
def credits():
    return render_template('credits.html')

@app.route('/search')
def search():
    if request.args:
        # We have our query string nicely serialized as a Python dictionary
        args = request.args

        if args["jobtitle"]:
            jobtitle = args["jobtitle"]
        else:
            jobtitle = "driver"

        if args["location"]:
            location = args["location"]
        else:
            location = "washington+dc"

    # Need to include end user ip and end user's "useragent"
    try:
        talent = json.loads(requests.get(f'https://neuvoo.com/services/api-new/search?ip=1.1.1.1&useragent=123asd&k={jobtitle}&l={location}&contenttype=all&format=json&publisher=92f7a67c&cpcfloor=1&subid=10101&jobdesc=1&country=us&radius=50').text)
    except:
        # This is a bare except statement, which are typically not ideal
        # We should have different behavior based on the error type
        # Possibly out of scope for MVP
        talent = json.loads(requests.get(f'https://neuvoo.com/services/api-new/search?ip=1.1.1.1&useragent=123asd&k={driver}&l={washington+dc}&contenttype=all&format=json&publisher=92f7a67c&cpcfloor=1&subid=10101&jobdesc=1&country=us&radius=50').text)
    # Filter the dictionary
    filtered_jobs = JobFilter(talent['results'])
    numjobs = len(filtered_jobs)

    # Create a description preview for the html rendering
    for job in filtered_jobs:
        job['description_preview'] = job['description'][0:180] + "..."

    return render_template('search.html', jobs=filtered_jobs, numjobs=numjobs, jobtitle=jobtitle, location=location)

@app.route('/howitworks/')
def howitworks():
    return render_template('howitworks.html')

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
