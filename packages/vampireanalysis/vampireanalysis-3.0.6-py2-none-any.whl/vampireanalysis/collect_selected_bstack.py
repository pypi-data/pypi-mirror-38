#!/usr/bin/env python

# built-in libraries
import os
from time import sleep
# external libraries
import pandas as pd
import numpy as np

def collect_seleced_bstack(folder,buildmodel):
	print('## collect_selected_bstack.py')
	if buildmodel: uiname = 'image sets for building model.csv'
	else: uiname = 'image sets for applying model.csv'
	UI = pd.read_csv(os.path.join(folder,uiname))
	setpaths = UI['boundary stack location']
	cell_stacks = []
	nuclei_stacks = []
	for setpath in setpaths:
		pickles = [_ for _ in os.listdir(setpath) if _.lower().endswith('pickle')]
		cell_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if 'Cells' in pkl]
		nuclei_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if 'Nuclei' in pkl]
		cell_stacks = cell_stacks + cell_stack
		nuclei_stacks = nuclei_stacks + nuclei_stack

	df_cell = pd.concat(cell_stacks,ignore_index=True)
	df_nuclei = pd.concat(nuclei_stacks,ignore_index=True)
	return df_cell,df_nuclei

# folder = 'C:\\Users\\kuki\\Desktop\\cpoutput315'
# buildmodel = True
# cell,nuc = collect_seleced_bstack(folder,buildmodel)
