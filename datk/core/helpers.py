import functools
import termcolor
from termcolor import colored, cprint

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = args + tuple(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


"""
Helper functions to color the text output to console when running tests.
Set 'colorTests' to True in order to have the output of running datk.tests.tests appear in color in the terminal
and in iPython. Set 'colorTest' to False for the default (e.g. black) text output (the default settings will be
determined by your Terminal/iPython settings.)
"""

colorTests = True

def print_okay(text):
    if colorTests:
        print colored(text, "green")
    else:
        print text

def print_error(text):
    if colorTests:
        print colored(text, "red")
    else:
        print text

def print_with_underline(text):
	print text
	print ("="*len(text))

def print_error_with_underline(text):
	if colorTests:
	    print colored(text, "red")
	    print colored("="*len(text), "red")
	else:
		print text
		print "="*len(text)

def print_time_with_double_underline(text):
	if colorTests:
	    print colored(text, "green", attrs=['bold'])
	    print colored("="*len(text), "blue")
	    print colored("="*len(text), "blue")
	    print "\n"
	else:
		print text
		print "="*len(text)
		print "="*len(text)
		print "\n"