import sys
import re
import time
import csv

def parsetimestring(timestring):
    timeobj = time.strptime(timestring, "%m/%d/%y (%a) %H:%M:%S")
    return timeobj

def parseaction(actionstring):
    result = {}
    delete = re.search(re.compile(r"[Dd]ele"), actionstring)
    post = re.search(re.compile(r"[Pp]ost"), actionstring)
    postno = re.search(re.compile(r"#\d{4,8}"), actionstring)
    ban = re.search(re.compile(r"[Bb]an"), actionstring)
    locked = re.search(re.compile(r"[Ll]ock"), actionstring)
    clear = re.search(re.compile(r"[Cc]lear"), actionstring)
    report = re.search(re.compile(r"[Rr]eport"), actionstring)
    file = re.search(re.compile(r"[Ff]ile"), actionstring)
    bumplock = re.search(re.compile(r"[Bb]umplock"), actionstring)
    dismiss = re.search(re.compile(r"[Dd]ismiss"), actionstring)
    spoiler = re.search(re.compile(r"[Ss]poiler"), actionstring)
    edit = re.search(re.compile(r"[Ee]dit"), actionstring)
    cycle = re.search(re.compile(r"([Cc]ycle)|([Cc]yclical)"), actionstring)
    demote = re.search(re.compile(r"[Dd]emote"), actionstring)
    settings = re.search(re.compile(r"[Ss]ettings"), actionstring)
    board = re.search(re.compile(r"[Bb]oard"), actionstring)
    thread = re.search(re.compile(r"[Tt]hread"), actionstring)
    promote = re.search(re.compile(r"[Pp]romote"), actionstring)
    unstickie = re.search(re.compile(r"[Uu]nstickie"), actionstring)
    stickie = re.search(re.compile(r"[Ss]tickie"), actionstring)
    volunteer = re.search(re.compile(r"[Vv]olunteer"), actionstring)
    created = re.search(re.compile(r"[Cc]reated"), actionstring)
    reopened = re.search(re.compile(r"[Rr]e-open"), actionstring)
    if postno:
        result["PostNumber"] = actionstring[postno.regs[0][0]:postno.regs[0][1]]
    if delete:
        if post:
            if file:
                result["Type"] = "File deletion"
            else:
                result["Type"] = "Post deletion"
        elif thread and file:
            result["Type"] = "Delete all posts in thread"
    elif spoiler and file:
        result["Type"] = "File spoiler"
    elif edit and post:
        result["Type"] = "Post edit"
    elif edit and board and settings:
        result["Type"] = "Edited board settings"
    elif cycle:
        result["Type"] = "Post cycled"
    elif ban:
        result["Type"] = "Ban"
        reason = re.search(re.compile(r"reason:"), actionstring)
        if reason:
            result["Reason"] = actionstring[reason.regs[0][0]:]
        length = re.search(re.compile(r"\d{1,4}.(([Dd]ay)|([Mn]onth)|([Hh]our)|([Yy]ear)|([Ww]eek))"), actionstring)
        if length:
            result["Length"] = actionstring[length.regs[0][0]:length.regs[0][1]]
    elif bumplock:
        result["Type"] = "Bumplock"
    elif locked:
        result["Type"] = "Lock thread"
    elif dismiss and report:
        result["Type"] = "Dismiss report"
    elif demote and report:
        result["Type"] = "Demoted report"
    elif promote and report:
        result["Type"] = "Promoted report"
    elif reopened and report:
        result["Type"] = "Re-opened report"
    elif clear and report:
        result["Type"] = "Clear reports"
    elif unstickie:
        result["Type"] = "Unstickied thread"
    elif stickie:
        result["Type"] = "Stickied thread"
    elif created and volunteer:
        result["Type"] = "Created volunteer"
    else:
        result["Type"] = "Unknown"
    return result


def parseline(inputline):
    result = {}
    repattern = re.compile(": ")
    splitindex = repattern.search(inputline)
    timestring = inputline[0:splitindex.regs[0][0]]
    timeobj = parsetimestring(timestring)
    result["time"] = timeobj
    actionstring = inputline[splitindex.regs[0][1]:].rstrip()
    result["actiondict"] = parseaction(actionstring)
    result["actionstring"] = inputline[splitindex.regs[0][1]:].rstrip()
    return result


def readfile(filename):
    try:
        with open(filename, "r+") as inputfile:
            lines = inputfile.readlines()
            result = []
            for line in lines:
                parsed = parseline(line)
                result.append(parsed)
            return result
    except:
        sys.exit("input file error")

def writecsv(timeactionlist):
    filename = "resultfile" + time.strftime("%Y:%m:%d-%H:%M:%S") + ".csv"
    with open(filename, "w") as outputfile:
        writer = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Type", "Post or Thread", "Reason", "Length"])
        for linedict in timeactionlist:
            line = linedict.get("actiondict")
            if line.get("Type"):
                type = line.get("Type")
            else:
                type = ""
            if line.get("PostNumber"):
                post = line.get("PostNumber")
            else:
                post = ""
            if line.get("Reason"):
                reason = line.get("Reason")
            else:
                reason = ""
            if line.get("Length"):
                length = line.get("Length")
            else:
                length = ""
            row = [type, post, reason, length]
            writer.writerow(row)

if len(sys.argv) is not 2:
    print("Usage: \"processdata.py <datafile>\"")
    sys.exit("No valid filename")
else:
    liststringdict = readfile(sys.argv[1])
    writecsv(liststringdict)

