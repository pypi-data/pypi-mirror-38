#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-04 18:37:13
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import sys
"""This is the "nester.py" module and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""
def print_lol(the_list, intent=False, level=0, fh=sys.stdout):
	"""This function takes one positional argument called "the_list", which is 
	   any Python list (of - possibly - nested lists). Each data item in the 
	   provided list is (recursively) printed to the screen on it's own lines.
	   A Second argument called "intent" is used as a switch to turn on/off tab-stops.
	   A Third argument called "level" is used to insert tab-stops when a 
	   nested list is encountered."""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item,intent,level+1,fh)
		else:
			if intent:
				for num in range(level):
					print("\t",end='',file=fh)
			print(each_item,file=fh)
