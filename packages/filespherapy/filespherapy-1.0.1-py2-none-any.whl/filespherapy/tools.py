# tools.py

import pprint
import os

"""
File path construction, conversion, and manipulation.

Usage:

 fsph = Filespere(filepath=FILEPATH)

 OR

 fsph = Filesphere(dirname=DIRNAME, basename=BASENAME)

 OR

 fsph = Filesphere(dirname=DIRNAME, rootname=ROOTNAME, extname=EXTNAME)

filepath = dirname + basename

  basename (filename)
    basename = rootname + extname (extension)

Use cases
1. update a filesphere object by altering one or more of its elements

  >>> fsphA = Filesphere(filepath='/my/dir/name/A/myrootnameA.myextnameA')
  >>> fsphA.print()
  /my/dir/name/A/myrootnameA.myextnameA
  >>> fsphA.update(extname='myextnameB')
  >>> fsphA.print()
  /my/dir/name/A/myrootnameA.myextnameB

  # create a new Filesphere object by cloning
  >>> fsphB = fsphB.clone()
  # clone and 
 
We define transformation as the process (a method) by which
an exiting filesphere object (a filepath) has one or more of
its elements replaced.

example

 given a 

  fsphA = Filesphere(filepath='/my/dir/name/A/myrootnameA.myextnameA')

 compute a new filepath string by replacing myextnameA with myextnameB:

 result = fsphA.path(extname='myextnameB')

 print result

  /my/dir/name/A/myrootnameA.myextnameB

 also might want to work with multiple Filesphere objects
 by cloning 




 e.g.
  filepathA -> filepathB:
    inputs are filepathA, B:{ dirname, extension }
    preserves the rootname, i.e. rootname preserving transformation

  filepathA -> dirnameA
  filepathA -> basenameA (filenameA)
  filepathA -> rootnameA
  filepathA -> extensionA

 change dirname only (replace dirname)
 change basename only (replace basename)
 change rootname only (replace rootname)
 change extension only (replace extension)

methods:
"""

DEBUGGING = True

pp = pprint.PrettyPrinter(indent=4)

class Filesphere(object):

	def __init__(self, **kwargs):

		if 'filepath' in kwargs:
			self.filepath = kwargs['filepath']
			self.dirname = os.path.dirname(self.filepath)
			self.basename = os.path.basename(self.filepath)
			self.rootname = os.path.splitext(self.basename)[0]
			if len(os.path.splitext(self.basename)) == 2:
				self.extname = os.path.splitext(self.basename)[1]

		if 'dirname' in kwargs:
			self.dirname = kwargs['dirname']

		if 'basename' in kwargs:
			self.basename = kwargs['basename']

		if 'rootname' in kwargs:
			self.rootname = kwargs['rootname']

		if 'extname' in kwargs:
			self.extname = kwargs['extname']

		if ('dirname' in kwargs and 'basename' in kwargs) and not 'filepath' in kwargs:
			self.filepath = "{}/{}".format(self.dirname, self.basename)

		elif ('dirname' in kwargs and 'rootname' in kwargs and 'extname' in kwargs) and not 'filepath' in kwargs:
			self.basename = "{}.{}".format(self.rootname, self.extname)
			self.filepath = "{}/{}".format(self.dirname, self.basename)

	def show(self):
		print self.filepath

	def get_filepath(self):
		return self.filepath

	def get_dirname(self):
		return self.dirname

	def get_basename(self):
		return self.basename

	def get_rootname(self):
		return self.rootname

	def get_extname(self):
		return self.extname

	def __repr__(self):

		s = '\n'
		for k in self.__dict__:
			s += "%5s%20s: %s\n" % (' ',k, self.__dict__[k])
		return s

	def update(self, **kwargs):

		if 'filepath' in kwargs:
			self.filepath = kwargs['filepath']
			self.dirname = os.path.dirname(self.filepath)
			self.basename = os.path.basename(self.filepath)
			self.rootname = os.path.splitext(self.basename)[0]
			if len(os.path.splitext(self.basename)) == 2:
				self.extname = os.path.splitext(self.basename)[1]

		if 'dirname' in kwargs:
			self.dirname = kwargs['dirname']
			self.filepath = "{}/{}".format(self.dirname, os.path.basename(self.filepath))

		if 'basename' in kwargs:
			self.basename = kwargs['basename']
			self.filepath = "{}/{}".format(os.path.dirname(self.filepath), self.basename)			

		if 'rootname' in kwargs:
			self.rootname = kwargs['rootname']
			if DEBUGGING:
				print " my new rootname: {}".format(self.rootname)

			tmp_basename = os.path.basename(self.filepath)
			if DEBUGGING:
				print " tmp_basename: {}".format(tmp_basename)

			if len(os.path.splitext(tmp_basename)) == 2:
				tmp_extname  = os.path.splitext(tmp_basename)[1]
				if DEBUGGING:
					print " tmp_extname: {}".format(tmp_extname)

				self.filepath = "{}/{}{}".format(
					os.path.dirname(self.filepath), 
					self.rootname, 
					tmp_extname
					)
			else:

				self.filepath = "{}/{}".format(
					os.path.dirname(self.filepath), 
					self.rootname
					)

		if 'extname' in kwargs:
			self.extname = kwargs['extname']
			if DEBUGGING:
				print " my new extname: {}".format(self.extname)

			tmp_basename = os.path.basename(self.filepath)
			tmp_rootname  = os.path.splitext(tmp_basename)[0]

			if DEBUGGING:
				print " basename: {}".format(tmp_basename)
				print " rootname: {}".format(tmp_rootname)

			self.filepath = "{}/{}.{}".format(
				os.path.dirname(self.filepath), 
				tmp_rootname, 
				self.extname
				)


if __name__ == '__main__':

	print
	print "create sphere A from filepath"
	fsphA = Filesphere(filepath='/my/dir/name/A/myrootnameA.myextnameA')
	fsphA.show()
	print

	print "create sphere B from dirname, basename"
	fsphB = Filesphere(dirname='/my/dir/name/B', basename='myrootnameB.myextnameB')
	fsphB.show()
	print

	print "create sphere C from dirname, rootname, extname"
	fsphC = Filesphere(dirname='/my/dir/name/C', rootname='myrootnameC', extname='myextnameC')
	fsphC.show()
	print

	print "update the dirname of A"
	fsphA.update(dirname='/my/new/dir/name')
	fsphA.show()
	print

	print "update the basename of B"
	fsphB.update(basename='mynew.basename')
	fsphB.show()
	print

	print "update the rootname of C"
	fsphC.update(rootname='newroot')
	fsphC.show()
	print

	print "finally, also update the extname of C"
	fsphC.update(extname='newext')
	fsphC.show()
	print


