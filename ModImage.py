'''
20/04/2020 - Wander Damasceno Rodrigues
Class to modify images
'''

import multiprocessing as mp
from PIL import Image
import os
import re

def parallel_execute(file, function, end_folder, args):
	"""
	Function used to execute in parallel.
	Use ModImage.parallel_processing() or your own parallel call.
	"""
	obj = ModImage()
	obj.open(file)

	if function == 'rubik':
		obj.rubik()
	elif function == 'black_white':
		obj.black_white(args[0])
	elif function == 'gray_scale':
		obj.gray_scale()
	
	obj.save(end_folder)

class ModImage:
	"""
	Class used to Modify images

	Functions:
		open(path)
			Open the image to start modifying

		save(path)
			Save modified image to given path/filename
		
		rubik()
			Generate an image that can be done with rubik cube

		black_white(mod)
			Generate an image just with black and white

		gray_scale()
			Generate an image using gray scale

		parallel_processing(function, start_folder, end_folder, args)
			Execute a specific modifying method to all files in a
			folder using parallel execution
	"""

	def __init__(self):
		self.image = ''
		self.__path = ''

	def parallel_processing(self, function, start_folder, end_folder, args=[]):
		"""
		Attributes:
			function: function to use (rubik, black_white or gray_scale)
			start_folder: input folder
			end_folder: output folder
			args: array containing arguments of the method

		Uses multiprocessing library to create a pool and start
		executing everything in parallel
		"""

		#Start freeze support
		mp.freeze_support()
		
		#Start args array 
		map_args =[]
		for file_name in os.listdir(start_folder):
			name = start_folder + '/' + file_name
			#Check if it's a valid file to modify
			if os.path.isfile(name) and name.lower().endswith(('.jpg', '.jpeg', '.png')):
				#Make the tuple and add it to array
				map_args.append((name, function, end_folder, args))

		#Generate a pool with the max number of CPU
		pool = mp.Pool(mp.cpu_count())
		#Assign CPUs to function and arguments
		pool.starmap(parallel_execute, map_args)
		#Close the pool
		pool.close()
		#Start executing
		pool.join()

	def open(self, path):
		"""
		Attributes:
			path: file to open

		Open a file to start modifying
		"""
		self.image = Image.open(path)
		self.__path = path

		if self.image.mode != 'RGB':
			self.image = self.image.convert('RGB')

	def save(self, path=''):
		"""
		Attributes:
			path: path to save the image

		Save the current image to the provided path.
		If already exist a file in the given path, it will look for 
		an available name
		"""
		if os.path.isdir(path):
			if not path.endswith(('/', '\\')):
				path += '/'
			filename = re.sub(r'.+[\/\\]', '', self.__path)
			path = path + filename
		elif path == '':
			path = self.__path

		filename = re.sub(r'.+[\/\\]', '', path)
		folder = re.sub(r'[\w\. ]+$', '', path)

		counter = 1
		while os.path.isfile(path):
			new_filename = filename[:-4] + '_' + str(counter) + filename[-4:]
			path = folder + new_filename
			counter += 1

		self.image.save(path)

	def rubik(self):
		"""
		Generate an image that can be build with Rubik Cubes using
		colors: blue, red, orange, green, yellow and white. :)
		"""
		pix = self.image.load()
		for y in range(self.image.size[1]):
			for x in range(self.image.size[0]):
				pixel = pix[x,y]
				total = pixel[0] + pixel[1] + pixel[2]
				if total <= 127: #blue
					pix[x,y] = (0,0,200)
				elif total <= 254: #red
					pix[x,y] = (200,0,0)
				elif total <= 381: #orange
					pix[x,y] = (255,128,0)
				elif total <= 428: #green
					pix[x,y] = (0,255,0)
				elif total <= 555: #yellow
					pix[x,y] = (255,255,0)
				else: #white
					pix[x,y] = (255,255,255)

	def black_white(self, acceptance=0.385):
		"""
		Attributes:
			acceptance: acepptance to be black - from 0 to 1
			            higher the acceptance, darker the image
			            (default: 0.385)

		Generate a black and white image.
		"""
		pix = self.image.load()

		acceptance = 0.385 if acceptance == '' else acceptance
		tolerance = 382

		for y in range(self.image.size[1]):
			for x in range(self.image.size[0]):
				pixel = pix[x,y]

				if pixel[0] + pixel[1] + pixel[2] <= tolerance * acceptance * 2:
					pix[x,y] = (0,0,0)
				else:
					pix[x,y] = (255,255,255)

	def gray_scale(self):
		"""
		Generate a gray-scale image using just 6 shades.
		@TODO: use a parameter to determine the quantity of shades
		"""
		pix = self.image.load()
		for y in range(self.image.size[1]):
			for x in range(self.image.size[0]):
				pixel = pix[x,y]
				total = pixel[0] + pixel[1] + pixel[2]

				if total <= 100:
					pix[x,y] = (0,0,0)
				elif total <= 200:
					pix[x,y] = (51,51,51)
				elif total <= 300:
					pix[x,y] = (102,102,102)
				elif total <= 400:
					pix[x,y] = (153,153,153)
				elif total <= 500:
					pix[x,y] = (204,204,204)
				else:
					pix[x,y] = (255,255,255)

if __name__ == '__main__':
	#Examples below
	path = 'C:/Users/WanderRodrigues/Desktop/image'
	output_path = path + '/output'

	obj = ModImage()
	obj.parallel_processing('black_white', path, output_path, [100])

	obj = ModImage()
	obj.open(path + '/1.jpg')
	obj.black_white()
	obj.save(output_path)