import pandas as pd 
import numpy as np

from utils import *

def clean(filename):
	checkFileType(filename)
	data = openFile(filename)
	data = dropCols(data, features = ('PR', 'GROUP', 'YEAR'))
	validate(data)

	data = addId(data)
	data = dropCols(data, features = ('NAME', 'YEAR'))

	'''
		Script to ensure the output follows the listed expected behavior of the function

	'''

	toCSV(data)