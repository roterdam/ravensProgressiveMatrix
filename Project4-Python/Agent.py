import os
from collections import OrderedDict
import numpy as np
import cv2
import time
from SimpleCV import Display, Image
from matplotlib import pyplot as plt
from PIL import Image, ImageFilter
import glob
import math

filename = "Project4/ImagesForProcessing/"
dir = os.path.dirname(filename)
if not os.path.exists(dir):
    os.makedirs(dir)

# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

DISTINCT_COLORS = [(0x00, 0xFF, 0x00), (0xFF, 0xFF, 0x00),(0x00, 0xFF, 0xFF),(0xFF, 0xFF, 0x00),(0xFF, 0xFF, 0x40),
(0xFF, 0xFF, 0x80),(0x00, 0xFF, 0x01),(0x00, 0xFF, 0x02),(0x00, 0xFF, 0x03),(0x00, 0xFF, 0x04),(0x00, 0xFF, 0x05),
(0x00, 0xFF, 0x06),(0x00, 0xFF, 0x07)]

def color_separator(im):
    if im.getpalette():
        im = im.convert('RGB')

    colors = im.getcolors()
    width, height = im.size
    colors_dict = dict((val[1],Image.new('RGB', (width, height), (0,0,0))) 
                        for val in colors)
    pix = im.load()    
    for i in xrange(width):
        for j in xrange(height):
            colors_dict[pix[i,j]].putpixel((i,j), pix[i,j])
    return colors_dict

class ObjectSemanticNetwork: 
	def __init__(self,letter):
		self.letter = letter
		self.ObjectNames = OrderedDict()
		self.imageCount = 0
		
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().

	def __init__(self):
		self.ImageArray1 = ["A","B","C"]
		self.ImageArray2 = ["A","B","C","D","E","F","G","H"]
		self.RowPattern1 = {}
		self.RowPattern2 = {}
		self.RowPattern3 = {}
		self.count = 0
		self.Answer = None
		self.ProblemCount = 1
	
	def filter(self,value):
		if value == 255:
			return 255
		else:
			return 0
		
	# Walk through an image pixel by pixel
	def walk(self,image):
		width, height = image.size
		# Go through each pixel sequentially
		for index, pixel in enumerate(image.getdata()):
			# Calculate the current position
			x = index % width
			y = index / width
			# Yield the current position and value
			yield (x,y,pixel)
			
    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem

	def findRowPatterns3(self,Network1,Network2,Network3,RowList):
		RowList["Shape"] = -1
		ShapeList = Network1.ObjectNames["Shape"] + Network2.ObjectNames["Shape"]+Network3.ObjectNames["Shape"]
		if ShapeList and all(shape == ShapeList[0] for shape in ShapeList):
			print "The shapes haven't changed across rows"
			RowList["Shape"] = 0
		else:
			self.FindShapePattern(ShapeList,RowList)
		
		FillList = Network1.ObjectNames["Fill"] + Network2.ObjectNames["Fill"] + Network3.ObjectNames["Fill"]
		RowList["Fill"] = -1
		if FillList and all(fill == FillList[0] for fill in FillList):
			print "The fill hasn't changed across rows"
			RowList["Fill"] = 0
		else:
			RowList["Fill"] = 1 # Fill has changed
		
		SizeList = Network1.ObjectNames["Size"] + Network2.ObjectNames["Size"] + Network3.ObjectNames["Size"]
		RowList["Size"] = -1
		if SizeList and all(size == SizeList[0] for size in SizeList):
			print "The size hasn't changed across rows"
			RowList["Size"] = 0
		else:
			self.FindSizePatterns(SizeList,RowList)
		
		AngleList = Network1.ObjectNames["Angle"] + Network2.ObjectNames["Angle"] + Network3.ObjectNames["Angle"]
		RowList["Angle"] = -1
		if AngleList and RowList["Shape"] == 2 and all(angle == AngleList[0] for angle in AngleList):
			print "The Angles haven't changed rows"
			RowList["Angle"] = 0
		else:
			print "Angles have changed!"
			RowList["Angle"] = 1
		print "RowList: ",RowList,"\n"
	
	def findRowPatterns(self,Network1,Network2,RowList):
		RowList["Shape"] = -1
		ShapeList = Network1.ObjectNames["Shape"] + Network2.ObjectNames["Shape"]
		if ShapeList and all(shape == ShapeList[0] for shape in ShapeList):
			print "The shapes haven't changed across rows"
			RowList["Shape"] = 0
		else:
			self.FindShapePattern(ShapeList,RowList)
		
		FillList = Network1.ObjectNames["Fill"] + Network2.ObjectNames["Fill"]
		RowList["Fill"] = -1
		if FillList and all(fill == FillList[0] for fill in FillList):
			print "The fill hasn't changed across rows"
			RowList["Fill"] = 0
		else:
			RowList["Fill"] = 1 # Fill has changed
		
		SizeList = Network1.ObjectNames["Size"] + Network2.ObjectNames["Size"]
		RowList["Size"] = -1
		if SizeList and all(size == SizeList[0] for size in SizeList):
			print "The size hasn't changed across rows"
			RowList["Size"] = 0
		else:
			self.FindSizePatterns(SizeList,RowList)
		
		AngleList = Network1.ObjectNames["Angle"] + Network2.ObjectNames["Angle"]
		RowList["Angle"] = -1
		if AngleList and RowList["Shape"] == 2 and all(angle == AngleList[0] for angle in AngleList):
			print "The Angles haven't changed rows"
			RowList["Angle"] = 0
		else:
			print "Angles have changed!"
			RowList["Angle"] = 1
		print "RowList: ",RowList,"\n"
	
	def FindShapePattern(self,ShapeList,RowList):
		if ShapeList:
			print "Length ShapeList: ",len(ShapeList),"\n","Length of setShapeList: ",len(set(ShapeList)),"\n"
			if len(ShapeList) == len(set(ShapeList)): # All Shapes are different; number of shapes hasn't changed
				RowList["Shape"] = 2
			elif len(ShapeList) % len(set(ShapeList)) == 0:
				RowList["Shape"] = 4
			elif all(ShapeList[0] == ShapeList[i] for i in xrange(0,len(ShapeList),2)) and (len(ShapeList)-2) == len(set(ShapeList)):
				RowList["Shape"] = 3
			else:
				RowList["Shape"] = 1
				
	def FindSizePatterns(self,SizeList,RowList):
		# if SizeList:
			#if SizeList
				# print "We went up one Size Each Time"
				# RowList["Size"] = 2
			# elif (self.SizePatterns[SizeList[0]]+self.SizePatterns[SizeList[1]]+self.SizePatterns[SizeList[2]])%3==0:
				# print "The Sizes have one of each going upwards"
				# RowList["Size"] = 3
			#else:
		RowList["Size"] = 1 # Nothing special with sizes
		if SizeList == None:
			RowList["Size"] = -1
			
	# def FindAnglePatterns(self,AngleList,RowList):
		# if RowList["Shape"] == 2 and 
		
	def CheckRowPatterns3(self,RowList1,RowList2,RowList3,Answer):
		RowPattern = True
		
		#if RowList1["Shape"] != 1 and RowList2["Shape"] != 1:
		if (RowList1["Shape"] == RowList3["Shape"] and 
			RowList2["Shape"] == RowList3["Shape"]):
			print "Shapes Check Out"
		else: RowPattern = False
		
		#if RowList1["Fill"] != 1 and RowList2["Fill"] != 1:
		if (RowList1["Fill"] == RowList3["Fill"] and 
			RowList2["Fill"] == RowList3["Fill"]):
			print "Fill Check Out"
		else: RowPattern = False
		
		#if "Size" in RowList1:
		#if RowList1["Size"] != 1 and RowList2["Size"] != 1:
		if (RowList1["Size"] == RowList3["Size"] and 
				RowList2["Size"] == RowList3["Size"]):
			print "Size Check Out"
		else: RowPattern = False
			
		# if "Addition" in RowList1:
			# #if RowList1["Addition"] != 1 and RowList2["Addition"] != 1:
			# if (RowList1["Addition"] == RowList3["Addition"] and 
			# RowList2["Addition"] == RowList3["Addition"]):
				# print "Addition Check Out"
			# else: RowPattern = False
			
		if "Angle" in RowList1:
				if (RowList1["Angle"] == RowList3["Angle"] and 
				RowList2["Angle"] == RowList3["Angle"]):
					print "Angles Check Out"
				else: RowPattern = False
		print "RowPattern: ",RowPattern
		if RowPattern == True:
			self.Answer=Answer
	 
	def CheckRowPatterns(self,RowList1,RowList2,Answer):
		RowPattern = True
		
		#if RowList1["Shape"] != 1 and RowList2["Shape"] != 1:
		if RowList1["Shape"] == RowList2["Shape"]:
			print "Shapes Check Out"
		else: RowPattern = False
		
		#if RowList1["Fill"] != 1 and RowList2["Fill"] != 1:
		if RowList1["Fill"] == RowList2["Fill"]:
			print "Fill Check Out"
		else: RowPattern = False
		
		#if "Size" in RowList1:
		#if RowList1["Size"] != 1 and RowList2["Size"] != 1:
		if RowList1["Size"] == RowList2["Size"]:
			print "Size Check Out"
		else: RowPattern = False
			
		# if "Addition" in RowList1:
			# #if RowList1["Addition"] != 1 and RowList2["Addition"] != 1:
			# if (RowList1["Addition"] == RowList3["Addition"] and 
			# RowList2["Addition"] == RowList3["Addition"]):
				# print "Addition Check Out"
			# else: RowPattern = False
			
		if "Angle" in RowList1:
				if RowList1["Angle"] == RowList2["Angle"]:
					print "Angles Check Out"
				else: RowPattern = False
		print "RowPattern: ",RowPattern
		if RowPattern == True:
			self.Answer=Answer
	
	def checkArea(self,area):
		if area < 1500:
			return 1
		elif area >= 1501 and area <= 10000:
			return 2
		elif area >= 10000:
			return 3
		else:
			return "no area"
	
	def checkAngle(self,M):
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		a = int(M['m20']-M['m00']*cx*cx)
		b = int(2*M['m11']-M['m00']*(cx*cx+cy*cy))
		c = int(M['m02']-M['m00']*cy*cy)
		if a == c:
			return 0
		else:
			return math.degrees(math.atan2(b,a-c))
		
	def getAttributesFromNetwork(self,Network,image):
		# The arrays above will hold the attribute information for the Network
		ShapeList = []
		AngleList = []
		FillList = []
		SizeList = [] # The scale will be 1-5; with 5 being the biggest
		AdditionList = []
		print Network.letter
		# Open the image path from the Problems (Image Data) folder
		image = Image.open(image)
		# Convert it to grayscale for easy processing
		grayscale = image.convert("L")
		# Convert it to black and white to ensure that there aren't any pixels of any
		# other color.
		blackwhite = grayscale.point(self.filter,"1")
		image = blackwhite
		image = image.convert("RGB")
		width,height = image.size
		colorindex = 0
		# Translate the image into pictures with various colors
		while True:
			color = DISTINCT_COLORS[colorindex]
			colorindex += 1
			blackpixel = None
			for x,y,pixel in self.walk(image):
				if pixel == (0,0,0):
					blackpixel = (x,y)
					break
			if not blackpixel:
				break
			
			neighbors = [blackpixel]
			while len(neighbors) > 0:
				processing = list(neighbors)
				neighbors = []
				for x,y in processing:
					image.putpixel((x,y),color)
					new = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
					for x,y, in new:
						if (x,y) in neighbors:
							continue
						if x < 0 or x >= width:
							continue
						if y < 0 or y >= height:
							continue
						if image.getpixel((x,y)) != (0,0,0):
							continue
						neighbors.append((x,y))
		# We use the count to save each network as a different image
		self.count = str(self.count)
		# Save the network image
		image.save("Project4/ImagesForProcessing/colored"+self.count+".png")
		# Open the network image; here, we'll convert it to a bunch of different 
		# images with different shapes representing the networks
		im = Image.open("Project4/ImagesForProcessing/colored"+self.count+".png")
		# Separate the images
		colors_dict = color_separator(im)
		imageCount = 0
		# Iterate through the color dictionary for all of the images
		for key,value in colors_dict.iteritems():
			if key == (255, 255, 255):
				imageCount += 1
				continue
			imageCount = str(imageCount)
			# grab the individual image,
			# save it,
			value.save("Project4/ImagesForProcessing/"+Network.letter+"coloredSmall"+imageCount+".png")
			# then read it back with OpenCV for processing
			img = cv2.imread("Project4/ImagesForProcessing/"+Network.letter+"coloredSmall"+imageCount+".png")
			# Convert it to grayscale; it processes better this way
			imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			ret,thresh = cv2.threshold(imgray,127,255,0)
			# find the contours in the image
			contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			# iterate through the contours,
			#print "Contour Length: ",len(contours)
			#if not contours:
				#print "No Contours"
			for cnt in contours:
				if (len(contours)) == 1:
					FillList.append("yes")
				else:
					FillList.append("no")
				#print "Looking through contours"
				#if (count%2) == 1:
					#count = count + 1
					#print "Count2: ",count
					#continue
				# approximate how many sides it has
				approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
				print len(approx)
				area = cv2.contourArea(cnt)
				if len(approx) == 5:
					print "Half-Arrow"
					ShapeList.append("Half-Arrow")
				if len(approx) == 7:
					print "Arrow"
					ShapeList.append("Arrow")
				elif len(approx) == 3:
					print "Triangle"
					ShapeList.append("Triangle")
				elif len(approx) == 4:
					print "Square"
					ShapeList.append("Square")
				elif len(approx) == 12 and area >= 1000:
					print "Cross"
					ShapeList.append("Cross")
				elif len(approx) >= 8:
					print "Circle"
					ShapeList.append("Circle")
				#(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
				#AngleList.append(angle)
				#count = count + 1
				#print "Count: ",count3
				area = cv2.contourArea(cnt)
				SizeList.append(self.checkArea(area))
				print "Area: ",area,"\n"
				if len(approx) == 12 and area >= 1000:
					(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
					print "Angle: ",round(angle,0)
					AngleList.append(round(angle,0))
				else:
					M = cv2.moments(cnt)
					angle = self.checkAngle(M)
					print "Angle: ",round(angle,0)
					AngleList.append(round(angle,0))
				break
			#cv2.imshow("img",img)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows()
			imageCount = int(imageCount)
			imageCount += 1
		self.count = int(self.count)
		self.count = self.count + 1
		
		Network.ObjectNames["Shape"] = ShapeList
		Network.ObjectNames["Angle"] = AngleList
		Network.ObjectNames["Objects"] = colorindex-1
		Network.ObjectNames["Fill"] = FillList
		Network.ObjectNames["Size"] = SizeList
		print "Shapes: ",Network.ObjectNames["Shape"]
		print "Angles: ",Network.ObjectNames["Angle"]
		print "Fill: ",Network.ObjectNames["Fill"]
		print "Size: ",Network.ObjectNames["Size"]
		print "Objects: ",Network.ObjectNames["Objects"],"\n"
		
	def Solve(self,problem):
		type = problem.getProblemType()
		if (type == "2x1 (Image)" or type == "2x2 (Image)"):
			imageA = problem.getFigures().get("A").getPath()
			imageB = problem.getFigures().get("B").getPath()
			imageC = problem.getFigures().get("C").getPath()
			NetworkA = ObjectSemanticNetwork("A")
			NetworkB = ObjectSemanticNetwork("B")
			NetworkC = ObjectSemanticNetwork("C")
			print "******************** 2x1 or 2x2 Problem",self.ProblemCount,"********************"
			self.getAttributesFromNetwork(NetworkA,imageA)
			self.getAttributesFromNetwork(NetworkB,imageB)
			self.findRowPatterns(NetworkA,NetworkB,self.RowPattern1)
			self.getAttributesFromNetwork(NetworkC,imageC)
			
			for i in range(1,7):
				self.Answer = None
				print "+++++++++++++++We are on a new Answer Choice.....",i,"+++++++++++++++"
				NetworkD = ObjectSemanticNetwork(str(i))
				imageD = problem.getFigures().get(NetworkD.letter).getPath()
				self.getAttributesFromNetwork(NetworkD,imageD)
				self.findRowPatterns(NetworkC,NetworkD,self.RowPattern2)
				self.CheckRowPatterns(self.RowPattern1,self.RowPattern2,str(i))
				self.RowPattern2 = {}
				if self.Answer is not None:
					print "Answer is: ", self.Answer
					self.ProblemCount += 1
					self.RowPattern1 = {}
					return str(self.Answer)
				elif i == 6 and self.Answer is None:
					print "--------------I don't know!!!!!!!!!!!!!!!!!! -------------------"
					self.ProblemCount += 1
					self.RowPattern1 = {}
					return str(0)
				else:
					continue
				
		if (type == "3x3 (Image)"):
			imageA = problem.getFigures().get("A").getPath()
			imageB = problem.getFigures().get("B").getPath()
			imageC = problem.getFigures().get("C").getPath()
			imageD = problem.getFigures().get("D").getPath()
			imageE = problem.getFigures().get("E").getPath()
			imageF = problem.getFigures().get("F").getPath()
			imageG = problem.getFigures().get("G").getPath()
			imageH = problem.getFigures().get("H").getPath()
			NetworkA = ObjectSemanticNetwork("A")
			NetworkB = ObjectSemanticNetwork("B")
			NetworkC = ObjectSemanticNetwork("C")
			NetworkD = ObjectSemanticNetwork("D")
			NetworkE = ObjectSemanticNetwork("E")
			NetworkF = ObjectSemanticNetwork("F")
			NetworkG = ObjectSemanticNetwork("G")
			NetworkH = ObjectSemanticNetwork("H")
			print "******************** 3x1 Problem",self.ProblemCount,"********************"
			self.getAttributesFromNetwork(NetworkA,imageA)
			self.getAttributesFromNetwork(NetworkB,imageB)
			self.getAttributesFromNetwork(NetworkC,imageC)
			self.findRowPatterns3(NetworkA,NetworkB,NetworkC,self.RowPattern1)
			self.getAttributesFromNetwork(NetworkD,imageD)
			self.getAttributesFromNetwork(NetworkE,imageE)
			self.getAttributesFromNetwork(NetworkF,imageF)
			self.findRowPatterns3(NetworkD,NetworkE,NetworkF,self.RowPattern2)
			self.getAttributesFromNetwork(NetworkG,imageG)
			self.getAttributesFromNetwork(NetworkH,imageH)
			
			for i in range(1,7):
				self.Answer = None
				print "+++++++++++++++We are on a new Answer Choice.....",i,"+++++++++++++++"
				NetworkI = ObjectSemanticNetwork(str(i))
				imageI = problem.getFigures().get(NetworkI.letter).getPath()
				self.getAttributesFromNetwork(NetworkI,imageI)
				self.findRowPatterns3(NetworkG,NetworkH,NetworkI,self.RowPattern3)
				self.CheckRowPatterns3(self.RowPattern1,self.RowPattern2,self.RowPattern3,str(i))
				self.RowPattern3 = {}
				if self.Answer is not None:
					print "Answer is: ", self.Answer
					self.ProblemCount += 1
					self.RowPattern1 = {}
					self.RowPattern2 = {}
					return str(self.Answer)
				elif i == 6 and self.Answer is None:
					print "--------------I don't know!!!!!!!!!!!!!!!!!! -------------------"
					self.ProblemCount += 1
					self.RowPattern1 = {}
					return str(0)
				else:
					continue