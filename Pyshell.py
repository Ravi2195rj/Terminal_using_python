import os
import sys
import getpass
import socket
from pathlib import Path
import itertools
from more_itertools import *
import re
import fileinput
import difflib
import pwd
import grp
import time
def load():
	path = os.getcwd().split('/')
	str1 = "~"
	for i in path[3:]:
		str1 = str1 + "/" + i
	print ("\033[1;32;1m" + getpass.getuser() + "@" + socket.gethostname() + "\033[0;0m:\033[1;34;1m" + str1 + "\033[0;0m$ " , end = "")

def execute_cd(command):
	path = command[3:]
	if(os.path.exists(path) == False):
		print ("bash: cd: "+path+": No such file or directory")
	else:
		if(os.path.isdir(path) == True):
			os.chdir(path)
		else:
			print ("bash: cd: "+path+": Not a directory")
	load()

def execute_ls(words):
	files = [os.curdir, os.pardir] + os.listdir(os.getcwd())
	files.sort()
	sorted(files)
	l = 0
	a = 0
	h = 0
	if(len(words) == 1):
		for name in files[2:]:
			if(os.path.isdir(name)):
				print ("\033[1;34;1m"+name+"\033[0;0;0m")
			else:
				print (name)
	else:
		for i in words[1][1:]:
			if (i == 'a'):
				a = 1
			elif (i == 'h'):
				h = 1
			elif (i == 'l'):
				l = 1

		if(l == 1):
			
			dir_path = os.path.join(os.getcwd())
			dir_inode = os.stat(dir_path)
			if(h == 1):
				print('total {0:.1f}K'.format((dir_inode.st_size)/1024.0))
			else:
				print("total",dir_inode.st_size)
			if (a == 0):
				files = files[2:]
			for name in files:
			    full_path = os.path.join(os.getcwd(), name)
			    if os.path.isdir(full_path):
			        print('d',end="")
			    else:
			        print('-',end="")
			    
			    inode = os.stat(full_path)

			    user = format(int(oct(inode.st_mode)[-3:-2]), "b")
			    group = format(int(oct(inode.st_mode)[-2:-1]), "b")
			    other = format(int(oct(inode.st_mode)[-1:]), "b")

			    if (user[0] == '1'):
			    	print ("r",end="")
			    else:
			    	print ("-",end="")

			    if (user[1] == '1'):
			    	print ("w",end="")
			    else:
			    	print ("-",end="")

			    if (user[1] == '1'):
			    	print ("x",end="")
			    else:
			    	print ("-",end="")

			    if (group[0] == '1'):
			    	print ("r",end="")
			    else:
			    	print ("-",end="")

			    if (group[1] == '1'):
			    	print ("w",end="")
			    else:
			    	print ("-",end="")

			    if (group[1] == '1'):
			    	print ("x",end="")
			    else:
			    	print ("-",end="")

			    if (other[0] == '1'):
			    	print ("r",end="")
			    else:
			    	print ("-",end="")

			    if (other[1] == '1'):
			    	print ("w",end="")
			    else:
			    	print ("-",end="")

			    if (other[1] == '1'):
			    	print ("x",end="")
			    else:
			    	print ("-",end=" ")	
			    
			    print(str(inode.st_nlink) , end = " ")
			    print(pwd.getpwuid(inode.st_uid).pw_name , end = " ")
			    print(grp.getgrgid(inode.st_gid).gr_name , end = " ")
			    if(h == 0):
			    	print('{:>8} '.format(str(inode.st_size)),end="")
			    else:
			    	print('{:7.1f}K'.format((inode.st_size)/1024.0),end=" ")
			    print(time.ctime(inode.st_mtime)[:-8] , end = " ")
			    print(name)

		else:
			for name in files:
				if(os.path.isdir(name)):
					print ("\033[1;34;1m"+name+"\033[0;0;0m")
				else:
					print (name)
	load()

def execute_pwd():
	print (os.getcwd())
	load()

def execute_touch(command):
	file_name = command[6:]
	filename = Path(file_name)
	filename.touch(exist_ok = True)
	load()

def execute_head(words):
	v = 0
	n = 0
	N = 10
	c = 0
	if(len(words) == 2):
		N = 10
		file = words[1]
	else:
		for i in words[1:-1]:
			if (i == '-v'):
				v = 1
			elif (i == '-n'):
				n = 1
			elif (i == '-c'):
				c = 1
			else:
				N = int(i)
	file = words[-1]
	if(os.path.exists(file)):
		with open(file) as myfile:
			if(v == 1):
				print ("==> " + file + " <==")
			if (c == 1):
				file_size = os.path.getsize(file)
				if (N < 0):
					file_size += N
					if (file_size > 0):
		 				byte = myfile.read(file_size)
		 				for b in byte:
		 					print (b,end="")
				else:
					if(file_size < N):
						N = file_size
					byte = myfile.read(N)
					for b in byte:
						print (b,end="")

			else:
				num_lines = sum(1 for line in myfile)
				if(N < 0):
					num_lines += N
					if(num_lines > 0):
						myfile.seek(0, 0)
						for x in range(num_lines):
							print (next(myfile) , end = "")
				else:
					if(num_lines > 0):
						myfile.seek(0, 0)
						for x in range(N):
							if(x == num_lines):
								break
							else:
								print (next(myfile) , end = "")
	else:
		print ("head: cannot open '"+file+"' for reading: No such file or directory")
	load()

def execute_tail(words):
	v = 0
	n = 0
	N = 10
	c = 0
	if(len(words) == 2):
		N = 10
		file = words[1]
	else:
		for i in words[1:-1]:
			if (i == '-v'):
				v = 1
			elif (i == '-n'):
				n = 1
			elif (i == '-c'):
				c = 1
			else:
				N = int(i)
	file = words[-1]
	if(os.path.exists(file)):
		with open(file) as myfile:
			if(v == 1):
				print ("==> " + file + " <==")
			if (c == 1):
				file_size = os.path.getsize(file)
				file_size -= abs(N)
				if(file_size > 0):
					myfile.seek(file_size,0)
				else:
					myfile.seek(0,0)
				byte = myfile.read(abs(N))
				for b in byte:
					print (b,end="")
			else:
				num_lines = sum(1 for line in myfile)
				myfile.seek(0, 0)
				if(N > num_lines):
					for lines in myfile:
						print (lines)
				else:
					rest_of_file = itertools.islice(myfile,num_lines-N,None,1)
					for lines in rest_of_file:
						print (lines , end = "")
	else:
		print ("tail: cannot open '"+file+"' for reading: No such file or directory")
	load()

def execute_grep(words):
	i = 0
	v = 0
	c = 0
	w = 0
	for i in words:
		if (i == '-i'):
			i = 1
		elif (i == '-v'):
			v = 1
		elif (i == '-c'):
			c = 1
		elif (i == '-w'):
			w = 1

	if (words[-2] == "<<<"):
		file = words[-1][1:-1]
		if(i == 1):
			pattern = re.compile(words[-3][1:-1],re.IGNORECASE)
		else:
			pattern = re.compile(words[-3][1:-1])
		if(c == 1):
			if(w == 0):
				if ((re.search(pattern,file) and v == 0) or (not(re.search(pattern,file)) and v == 1)):
					print ("1")
				else:
					print ("0")
			else:
				if(len(file.split()) == 1):
					if ((re.match(pattern,file) and v == 0) or (not (re.match(pattern,file)) and v == 1)):
						print ("1")
					else:
						print ("0")
				else:
					flag = 1
					for word in file:
						if ((re.match(pattern,word) and v == 0) or (not (re.match(pattern,word)) and v == 1)):
							print ("1")
							flag = 0
							break
					if(flag):
						print ("0")
		else:
			if(w == 0):
				if ((re.search(pattern,file) and v == 0) or (not (re.search(pattern,file)) and v == 1)):
					print (file)
			else:
				if(len(file.split()) == 1):
					if ((re.match(pattern,file) and v == 0) or (not (re.match(pattern,file)) and v == 1)):
						print (file)
				else:
					for word in file:
						if ((re.match(pattern,word) and v == 0) or (not (re.match(pattern,word)) and v == 1)):
							print (file)
							break
	else:
		file = words[-1]
		if(os.path.exists(file)):
			if(i == 1):
				pattern = re.compile(words[-2][1:-1],re.IGNORECASE)
			else:
				pattern = re.compile(words[-2][1:-1])
			if(c == 1):
				result = 0
				for i,line in enumerate(open(file)):	
					if ((re.search(pattern,line) and v == 0) or (not(re.search(pattern,line)) and v == 1)):
						result +=1
				print (result)
			else:
				for i,line in enumerate(open(file)):
					if ((re.search(pattern,line) and v == 0) or (not(re.search(pattern,line)) and v == 1)):
						print (line,end = "")
		else:
			print ("grep: "+file+": No such file or directory")
	load()

def execute_sed(words):
	N = 1
	texts = words[1][1:-1].split('/')
	if (texts[3] == "G"):
		N = 0
	pattern = re.compile(texts[1])
	if(os.path.exists(words[2])):
		for line in fileinput.input(words[2]):
			print (pattern.sub(texts[2],line, count = N),end = "")
	else:
		print ("sed: can't read "+words[2]+": No such file or directory")
	load()

def execute_diff(words):
	flag1 = 1
	flag2 = 1
	if(os.path.exists(words[1]) == False):
		print ("diff: "+words[1]+": No such file or directory")
		flag1 = 0
	if(os.path.exists(words[2]) == False):
		print ("diff: "+words[2]+": No such file or directory")
		flag1 = 0
	if (flag1 and flag2):
		with open(words[1], 'r') as hosts0:
			with open(words[2], 'r') as hosts1:
				diff = difflib.unified_diff(hosts0.readlines(),hosts1.readlines(),fromfile=words[1],tofile=words[2],)
				for line in diff:
					print (line,end="")
	load()

def execute_tr(words):
	if (words[0] == "cat"):
		if(os.path.exists(words[1]) == False):
			print ("cat: "+words[1]+": No such file or directory")
			load()
			return

				
	if (words[5] == "[:upper:]" or words[5] == "[:A-Z:]"):
		if (words[4] == "[:lower:]" or words[4] == "[:a-z:]"):
			if(words[0] == "echo"):
				print (words[1][1:-1].lower())
			else:
				file  = open(words[1])
				for line in file:
					print(line,end = "").lower()
				file.close()

	elif (words[4] == "[:lower:]" or words[4] == "[:a-z:]"):
		if (words[5] == "[:upper:]" or words[5] == "[:A-Z:]"):
			if(words[0] == "echo"):
				print (words[1][1:-1].upper())
			else:
				file  = open(words[1])
				for line in file:
					print(line,end = "").upper()
				file.close()

	elif (words[4] == "-d"):
		if(words[0] == "echo"):
			print (words[1][1:-1].translate(str.maketrans('','',words[5][1:-1])),end = "")
		else:
			file  = open(words[1])
			for line in file:
				print (line.translate(str.maketrans('','',words[5][1:-1])),end = "")
			file.close()

	else:
		if(words[0] == "echo"):
			print (words[1][1:-1].translate(str.maketrans(words[4][1:-1],words[5][1:-1])),end = "")
		else:
			file  = open(words[1])
			# print ("yes")
			for line in file:
				print (line.translate(str.maketrans(words[4][1:-1],words[5][1:-1])),end = "")
			file.close()
	# print ("yes")
	load()






def execute_clear():
	print ("\033[3J", end = '')
	print ("\033[H\033[J", end = '')
	load()

def main():
    print ("\033[3J", end = '')
    print ("\033[H\033[J", end = '')
    load()
    while(1):
    	command = input()
    	words = command.split()

    	if(len(words)):

    		if(words[0] == "cd"):
	    		execute_cd(command)
	    	elif(words[0] == "ls"):
	    		execute_ls(words)
	    	elif(words[0] == "pwd"):
	    		execute_pwd()
	    	elif(words[0] == "touch"):
	    		execute_touch(command)
	    	elif(words[0] == "grep"):
	    		execute_grep(words)
	    	elif(words[0] == "head"):
	    		execute_head(words)
	    	elif(words[0] == "tail"):
	    		execute_tail(words)
	    	elif "tr" in words:
	    		execute_tr(words)
	    	elif(words[0] == "sed"):
	    		execute_sed(words)
	    	elif(words[0] == "diff"):
	    		execute_diff(words)
	    	elif(words[0] == "clear"):
	    		execute_clear()
	    	elif(words[0] == "exit"):
	    		exit()
	    	else:
	    		print (words[0]+ ": command not found")
	    		load()
    	
    	else:
    		load()

if __name__=="__main__":
	main()