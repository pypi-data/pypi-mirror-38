#!/usr/bin/env python

# built-in libraries
from time import sleep
import os
import re
# external libraries
import numpy as np 
from PIL import Image

def sum_binary(experiment,progress_bar):
	setfolders = [_ for _ in os.listdir(experiment) if os.path.isdir(os.path.join(experiment,_))]
	setfolderpaths = [os.path.join(experiment,_) for _ in setfolders]
	for setidx, setid in enumerate(setfolderpaths):
		
		print(str(int(100*setidx/len(setfolderpaths)))+' %')
		progress_bar["value"] = int(100*setidx/len(setfolderpaths))
		progress_bar.update()

		imfolders = [_ for _ in os.listdir(setid) if os.path.isdir(os.path.join(setid,_))]
		imfolders.sort(key=lambda f: int(filter(str.isdigit,f)))
		imfolderpaths = [os.path.join(setid,_) for _ in imfolders]
		for imidx,imid in enumerate(imfolderpaths):
			masks = [_ for _ in os.listdir(imid) if _.lower().endswith('.tiff')]
			#maskpaths = [os.path.join(imid,_) for _ in masks]
			objectname = list(set([re.split('_+',_)[0] for _ in masks])) # [cell, nuclei]
			for objidx, obj in enumerate(objectname):
				objs = [_ for _ in masks if obj in _]
				objpaths = [os.path.join(imid,_) for _ in objs]
				for idx, im in enumerate(objpaths):
					addim = np.asarray(Image.open(im))  
					addim = addim.copy()
					addim[addim>0] = idx
					if idx == 0: ims = 0
					ims = addim + ims
				labeledim = Image.fromarray((ims).astype('uint16'))
				labeledimfolder = os.path.join(experiment,'labeled image')
				if not os.path.isdir(labeledimfolder):
					os.mkdir(labeledimfolder)
				labeledsetfolder = os.path.join(labeledimfolder,str(setidx+1))
				if not os.path.isdir(labeledsetfolder):
					os.mkdir(labeledsetfolder)
				dst = os.path.join(labeledsetfolder, obj+'_'+setfolders[setidx]+'_'+imfolders[imidx])
				labeledim.save(dst+'.tiff')
#sum_binary('/Users/jacquelinekumer/Desktop/cpoutput315/Experiment1')			
# sum_binary('C:\\Users\\kuki\\Desktop\\cpoutput315\\Experiment1')	

