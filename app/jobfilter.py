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
