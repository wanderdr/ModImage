from PIL import Image
import os
import re

class ModImage:
	"""	Class used to Modify images

	Attributes:
		path: image path to be modified 

	Functions:
		save(path)
			Save modified image to given path
		
		rubik()
			Generate an image that can be done with rubik cube

		black_white(mod)
			Generate an image just with black and white

		gray_scale()
			Generate an image using gray scale
	"""

	def __init__(self, path):
		self.image = Image.open(path)

	def save(self, path):
		"""
		Attributes:
			path: path to save the image

		Save the current image to the provided path.
		If already exist a file in the given path, it will look for 
		an available name
		"""
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

	def black_white(self, acceptance=75):
		"""
		Attributes:
			acceptance: acepptance to be black - from 0 to 200.
			            higher the acceptance, darker the image

		Generate a black and white image.
		"""
		pix = self.image.load()

		acceptance = 75 if acceptance == '' else acceptance
		tolerance = 382

		for y in range(self.image.size[1]):
			for x in range(self.image.size[0]):
				pixel = pix[x,y]
				if pixel[0] + pixel[1] + pixel[2] <= tolerance * acceptance / 100:
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