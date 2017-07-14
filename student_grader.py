#!/usr/bin/python
'''
This program is modified from:
SPIM Auto-grader
Owen Stenson
Grades every file in the 'submissions' folder using every test in the 'samples' folder.
Writes to 'results' folder.

Source: https://github.com/stensonowen/spim-grader
Licence: GPL 2.0
'''
import os, time, re, sys
from subprocess import Popen, PIPE, STDOUT

def run(fn, sample_input='\n'):
	proc = Popen(["spim", "-file", fn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	proc.stdin.write(sample_input)
	return proc 

def remove_header(output):
    #remove output header
    hdrs = []
    hdrs.append(re.compile("SPIM Version .* of .*\n"))
    hdrs.append(re.compile("Copyright .*, James R. Larus.\n"))
    hdrs.append(re.compile("All Rights Reserved.\n"))
    hdrs.append(re.compile("See the file README for a full copyright notice.\n"))
    hdrs.append(re.compile("Loaded: .*/spim/.*\n"))
    for hdr in hdrs:
        output = re.sub(hdr, "", output)
    return output

def poll_all(p):
	f = open("output", "w")
	for proc in p:
		time.sleep(.1)
		if proc.poll() is None:
			#process is either hanging or being slow
			time.sleep(.5)
			if proc.poll() is None:
				proc.kill()
				f.write("Process hung; no results to report\n")
				continue
		output = remove_header(proc.stdout.read())
		errors = proc.stderr.read()
		if errors == "":
			f.write(output + '\n')
		else:
			f.write(output + '\t' + errors + '\n')
	f.close() 

def grade():
	ins = open("inputs", "r")
	inputs = ins.readlines()
	ins.close()
	o = open("output", "r")
	output = o.readlines()
	o.close()
	e = open("expect", "r")
	expect = e.readlines()
	e.close()

	counter = 0
	o = open("output", "w")
	for i in range(len(output)):
		string = "Input: " + inputs[i].strip() + "; Expectation: " + expect[i].strip() + "; Output: " + output[i].strip() + "\n"
		o.write(string)
		if expect[i] == output[i]:
			counter += 1
	o.write("\n")
	o.write(str(counter) + "/" + str(len(output)) + " test cases passed.")
	o.close()
	return counter == len(output)

# ASSUMPTION: Git repos' names will contain the team name
#             since repos currently take the format "<team_name>_<lab>".
# ASSUMPTION: This script will be called from "<some_path>/<team_repo>/travis/"
def generate_filename(submission, sample):
    try:
        path = os.path.abspath(".")
        team = path[:path.rfind("_")]
        ID = team[team.rfind("/")+1:]
    except:
        ID = submission
    return ID + '_' + sample

# Heads the results file with a line saying whether the tests for that file passed
def update_results(output_file, passed):
    path = "./diagnostics/output"
    f = open(path, "r")
    results = f.read()
    f.close()
    f = open(path, "w")
    f.write("{}{}".format(str(passed), "\n"))
    f.write(results)
    f.close()

# Takes an input file that consists of a number of lines of input
# and feeds them into spim subprocesses.
def input_lines(lab):
	submission = open(lab, "r")
	expectations = open("expect", "r")
	inputs = open("inputs", "r")

	procs = []
	for line in inputs.readlines():
		sample_input = "{}{}".format(line.strip(), "\n")
		#create process
		p = run(lab, sample_input)
		procs.append(p)
	inputs.close()	

	poll_all(procs)
	grade()
	# update_results(output, passed)

def print_diagnostics():
    path = "./diagnostics/"
    files = os.listdir(path)
    for f in files:
        print "{}".format(f)
        f = open("{}{}".format(path, f), "r")
        print f.read()
        f.close()

# Austin intends to grade labs with a binary blob file
# TODO: Get that working.
def input_blob(test, subm, resl, diag):
    pass

def main(input_type="line"):
    if input_type == "line":
        input_lines("lab.s")
    else:
        input_blob(test, subm, resl, diag)
    # print_diagnostics()

       
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        main()

    if "-t" in args:
        t = args[args.index("-t")+1]
        main(t)

    if "-g" in args:
        if not passed_all():
            exit(1)

