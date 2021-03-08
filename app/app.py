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

def AELScore(job_title, job_description):
    count = 0
    title_exclusions = [r"I{2,3}| IV$| V$",
                    r" 2$| 3$| 4$",
                    r"[sS]enior|SENIOR",
                    r"[sS]r\.*|SR\.",
                    r"[lL]ead|LEAD",
                    r"[dD]irector|DIRECTOR",
                    r"[Pp]rincipal|PRINCIPAL",
                    r"([mM]anage|MANAGE)",
                    r"[eE]xperienced|EXPERIENCED",
                    r"[mM]aster "]

    description_exclusions = [r"(?:[mM]inimum|[mM]in\.?|[aA]t least|[tT]otal|[iI]ncluding|[wW]ith).+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\+* (?:[yY]ears*|[yY]rs*)",
                         r"[mM]aster'?s| M\.S\. |MS, ",
                         r"Leads in"
                         r"\d-\d\+ years as a "]

    title_inclusions = [r"Junior",
                        r"[eE]ntry [lL]evel",
                        r"[eE]ntry-[lL]evel"]

    description_inclusions = [r"entry level",
                              r"[nN]o [eE]xperience"]

    # Subtracting points for exclusions
    for excl in title_exclusions:
        if re.search(excl, job_title) != None:
            count -= 1
    for excl in description_exclusions:
        if re.search(excl, job_description) != None:
            count -= 1
    # Adding points for inclusions
    for incl in title_inclusions:
        if re.search(incl, job_title) != None:
            count += 1
    for incl in description_inclusions:
        if re.search(incl, job_description) != None:
            count += 1
    return count

def clearanceCheck(job_description):
    return (re.search(r"TS/SCI|[cC]learance req|(DoD|DOD)|[cC]learance|[tT]op [sS]ecret", job_description) != None)


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
    talent = json.loads(requests.get(f'https://neuvoo.com/services/api-new/search?ip=1.1.1.1&useragent=123asd&k={jobtitle}&l={location}&contenttype=all&format=json&publisher=92f7a67c&cpcfloor=1&subid=10101&jobdesc=1&country=us&radius=50').text)
    try:
        # Error handling is based on the assumption that talent['results'] will
        # return an error because Talent.com will return a list for errors, not
        # a dict. This assumption might not be valid in all cases.
        filtered_jobs = talent['results'] #JobFilter(talent['results'])
    except:
        # This is a bare except statement, which are typically not ideal
        # We should have different behavior based on the error type
        # Possibly out of scope for MVP
        jobtitle = "driver"
        location = "washington+dc"
        talent = json.loads(requests.get(f'https://neuvoo.com/services/api-new/search?ip=1.1.1.1&useragent=123asd&k={jobtitle}&l={location}&contenttype=all&format=json&publisher=92f7a67c&cpcfloor=1&subid=10101&jobdesc=1&country=us&radius=50').text)
        filtered_jobs = talent['results'] #JobFilter(talent['results'])
    # Filter the dictionary

    numjobs = len(filtered_jobs)

    # Create a description preview for the html rendering
    for job in filtered_jobs:
        job['description_preview'] = job['description'][0:180] + "..."
        job['AELScore'] = AELScore(job['jobtitle'], job['description'])
        job['clearance_check'] = clearanceCheck(job['description'])

    sorted_jobs = sorted(filtered_jobs, key = lambda job: job['AELScore'], reverse=True)

    return render_template('search.html', jobs=sorted_jobs, numjobs=numjobs, jobtitle=jobtitle, location=location)

@app.route('/howitworks/')
def howitworks():
    return render_template('howitworks.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', error=e), 404

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
