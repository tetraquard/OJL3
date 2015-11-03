import os
import subprocess
import math

OJL3_DIR = os.path.dirname(os.path.abspath(__file__))
SANDBOX_PATH = os.path.join(OJL3_DIR, "OJ_sandbox")
SAFEEXEC_PATH = os.path.join(OJL3_DIR, "safeexec")
INPR_PATH = os.path.join(OJL3_DIR, "inprs")

SAFEEXEC_ARGS = ["--gid", "10000", "--nproc", "5"]

def run_prog(inpr_path, source_path, in_path=None, inpr_options=None, cmd_options=None, exec_path=None, report_path=None, time_lim_s=10, mem_lim_k=80000):
	"""
	Runs a program using safeexec

	Input parameters:
	inpr_path: Path to an interpreter if the program to be run is a script. To execute programs without an interpreter (execute bit will have to be set on the  program), set inpr_path to None.
	source_path: Path to the program that is to be run
	in_path: Path to file which is to be passed as STDIN of the program
	inpr_options: Command-line arguments to be passed to the interpreter (ignored if there is no interpreter)
	cmd_options: Command-line arguments to be passed to the program
	exec_path: Path to the directory where the program required to be executed
	report_path: Path of the file which will store the report generated by safeexec
	time_lim_s: time limit in seconds
	mem_lim_k: memory limit in KiB

	Return value: a 5-tuple of the form (verdict, out, err, time_s, mem_k)
	verdict: verdict given by parse_report
	out: output of the program (STDOUT)
	err: STDERR of the program
	time_s: CPU time of the program in seconds
	mem_k: Memory used by the program in KiB
	"""
	if not cmd_options:
		cmd_options = []
	if not inpr_options:
		inpr_options = []
	if inpr_path:
		cmdline = [inpr_path] + inpr_options + [source_path] + cmd_options
	else:
		cmdline = [source_path] + cmd_options

	if report_path:
		report_args = ["--report_file", os.path.abspath(report_path)]
	else:
		report_args = []

	run_path = [SAFEEXEC_PATH] + SAFEEXEC_ARGS + ["--clock", str(math.ceil(time_lim_s)), "--mem", str(mem_lim_k)] + report_args + ["--exec"] + cmdline

	if in_path: file_obj = open(in_path)
	else: file_obj = None

	sp = subprocess.Popen(run_path, stdin=file_obj, cwd=exec_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	(out,err) = sp.communicate()
	verdict, time_s, mem_k = parse_report(open(report_path).read().strip().split('\n'), time_lim_s=time_lim_s)
	return (verdict, out, err, time_s, mem_k)

def parse_report(report_lines, time_lim_s):
	"""
	Reads report generated by safeexec.

	Pass the lines read from the file as arguments:
	open(report_path).read().strip().split('\n')

	Returns a triplet (verdict, time_s, mem_k):
	verdict: OK, TLE, NZEC or name of signal which terminated the program
	time_s: CPU time of program in seconds
	mem_k: memory used by the program in KiB
	"""
	mem_k = int(report_lines[2].split()[2])
	time_s = float(report_lines[3].split()[2])
	if report_lines[0] == "OK":
		verdict = "OK"
		if time_s>time_lim_s:
			verdict = "TLE"
	elif report_lines[0] == "Time Limit Exceeded":
		verdict = "TLE"
	elif report_line[0] == "Invalid Function":
		verdict = "RF"
	elif report_lines[0] == "Internal Error":
		verdict = "IE"
	elif report_lines[0].startswith("Command exited with non-zero status"):
		verdict = "NZEC"
	elif report_lines[0].startswith("Command terminated by signal"):
		verdict = report_lines[0].rsplit(maxsplit=1)[1][:-1]
	else:
		raise Exception("Unknown verdict "+report_lines[0])
	return (verdict, time_s, mem_k)
