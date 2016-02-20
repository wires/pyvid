#! /usr/bin/env python

import glob,os

def isSource(file):
	if('.html' in file):
		return False;
	return ('.cc' in file) or ('.h' in file) or ('.py' in file)

def stripSrc(file):
	return file[len('src/'):]

files = glob.glob('src/*')
files = filter(isSource, files)

f = open('src/index.html', 'w')
html = ['<html><body><p><a href="html/index.html">Doxygen</a></p>']
html.append('<p><a href="python/index.html">Pydoc</a></p>')
html.append('<p>')

for file in files:
	if(file[-4:]=='.pyc') or (file[-5:]=='.html'):
		continue
	os.system('/usr/local/bin/source-highlight -f html %s' % file)
	html.append('<a href="%s.html">%s</a><br>' % (stripSrc(file), file))

html.append('</p>')
f.writelines(html)
f.close()

#run doxygen
os.system("doxygen")

#run pydoc
os.chdir("src/")
os.system("mkdir -p python")
os.chdir("python")
os.system("pydoc -w ../")

files = glob.glob("*.html")
f = open('index.html', 'w')
html = ['<html><body><p><a href="../../index.html">home</a></p>','<p>']
for file in files:
	html.append('<a href="%s">%s</a><br>' % (file, file))
html.append('</p>')
f.writelines(html)
f.close()
