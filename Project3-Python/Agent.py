# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
from collections import OrderedDict
import random

def addToList(name, value, List):
		List[name] = value
					
class ObjectSemanticNetwork:
	# This class will define my Semantic Network representation for the objects.
	# I will use a dictionary as the key to my representation. The key will be the
	# ObjectName and the value will be the array of ObjectAttributes objects. So for
	# example, the first 2x1 matrix should have 2 ObjectAttribute objects in the array.
	def __init__(self,letter):
	    self.letter = letter
	    self.ObjectNames = OrderedDict()
	
	def checkData(self,networkLetter): # This will simply print the Semantic Network contents
	# to us.
		print "Network Name: ", networkLetter
		for key, value in self.ObjectNames.iteritems():
			print key
			for attributes in value:
				print "Name: ",attributes.getName(), " Value: ",attributes.getValue()
			#print(value)
			print("\n")
			
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
		self.Counter = 1
		self.Row1List = {}
		self.Row2List = {}
		self.Row3List = {}
		self.SizePatterns = {"very-small":1,"small":2,"medium":3,"large":4,"very-large":5}
		self.Answer = None
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
    # agent has called checkAnswer, it will *not* be able to change its answer.
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
    def FillAttributeArrays(self,Network1,Network2,Network3,RowList):
		ShapeList = []
		FillList = []
		SizeList = []
		AngleList = []
		for key,value in Network1.ObjectNames.iteritems():
			for attributes in value:
				if attributes.getName() == "shape":
					ShapeList.append(attributes.getValue())
				if attributes.getName() == "fill":
					FillList.append(attributes.getValue())
				if attributes.getName() == "size":
					SizeList.append(attributes.getValue())
				if attributes.getName() == "angle":
					AngleList.append(attributes.getValue())
		for key,value in Network2.ObjectNames.iteritems():
			for attributes in value:
				if attributes.getName() == "shape":
					ShapeList.append(attributes.getValue())
				if attributes.getName() == "fill":
					FillList.append(attributes.getValue())
				if attributes.getName() == "size":
					SizeList.append(attributes.getValue())
				if attributes.getName() == "angle":
					AngleList.append(attributes.getValue())
		for key,value in Network3.ObjectNames.iteritems():
			for attributes in value:
				if attributes.getName() == "shape":
					ShapeList.append(attributes.getValue())
				if attributes.getName() == "fill":
					FillList.append(attributes.getValue())
				if attributes.getName() == "size":
					SizeList.append(attributes.getValue())
				if attributes.getName() == "angle":
					AngleList.append(attributes.getValue())			
		print "ShapeList: ",ShapeList,"\nFillList: ",FillList,"\nSize: ",SizeList,"\nAngleList: ",AngleList
		self.FindAdditionPattern(Network1,Network2,Network3,RowList)
		self.FindRowPatterns(ShapeList,FillList,SizeList,AngleList,RowList)
	
    def FindRowPatterns(self,ShapeList,FillList,SizeList,AngleList,RowList):
		RowList["Shape"] = -1
		if ShapeList and all(shape == ShapeList[0] for shape in ShapeList):
			print "The shapes haven't changed across rows"
			RowList["Shape"] = 0
		else:
			self.FindShapePattern(ShapeList,RowList)
		
		RowList["Fill"] = -1
		if FillList and all(fill == FillList[0] for fill in FillList):
			print "The fill hasn't changed across rows"
			RowList["Fill"] = 0
		else:
			RowList["Fill"] = 1 # Fill has changed
		
		RowList["Size"] = -1
		if SizeList and all(size == SizeList[0] for size in SizeList):
			print "The size hasn't changed across rows"
			RowList["Size"] = 0
		else:
			self.FindSizePatterns(SizeList,RowList)
		
		RowList["Angle"] = -1
		if AngleList and all(angle == AngleList[0] for angle in AngleList):
			print "The Angles haven't changed rows"
			RowList["Angle"] = 0
		else:
			self.FindAnglePatterns(AngleList,RowList)
		
		print "RowList: ",RowList,"\n"
   
    def FindAdditionPattern(self,Network1,Network2,Network3,RowList):
		RowList["Addition"] = -1
		AddedList1 = []
		AddedList1.append(len(Network1.ObjectNames))
		AddedList1.append(len(Network2.ObjectNames))
		AddedList1.append(len(Network3.ObjectNames))
		print "AddedList1: ",AddedList1
		if (sum(AddedList1)/AddedList1[0] == 3):
			print "No Objects Added"
			RowList["Addition"] = 0
		elif ((AddedList1[0]+1) == AddedList1[1]) and ((AddedList1[1]+1) == AddedList1[2]):
			print "One Object Added"
			RowList["Addition"] = 1
		elif ((AddedList1[0]+AddedList1[0]) == AddedList1[1]) and (AddedList1[0]+AddedList1[1] ==
			AddedList1[2]):
			print "At Least Two Objects Added"
			RowList["Addition"] = 2 
		elif (AddedList1[0] > AddedList1[1] and AddedList1[1] > AddedList1[2]):
			print "Objects are being subtracted"
			RowList["Addition"] = 3
	
    def CheckRowPatterns(self,RowList1,RowList2,RowList3,Answer):
		RowPattern = True
		
		if RowList1["Shape"] != 1 and RowList2["Shape"] != 1:
			if (RowList1["Shape"] == RowList3["Shape"] and 
			RowList2["Shape"] == RowList3["Shape"]):
				print "Shapes Check Out"
			else: RowPattern = False
		
		if RowList1["Fill"] != 1 and RowList2["Fill"] != 1:
			if (RowList1["Fill"] == RowList3["Fill"] and 
			RowList2["Fill"] == RowList3["Fill"]):
				print "Fill Check Out"
			else: RowPattern = False
		
		if "Size" in RowList1:
			if RowList1["Size"] != 1 and RowList2["Size"] != 1:
				if (RowList1["Size"] == RowList3["Size"] and 
				RowList2["Size"] == RowList3["Size"]):
					print "Size Check Out"
				else: RowPattern = False
			
		if "Addition" in RowList1:
			if (RowList1["Addition"] == RowList3["Addition"] and 
			RowList2["Addition"] == RowList3["Addition"]):
				print "Addition Check Out"
			else: RowPattern = False
			
		if "Angle" in RowList1:
			if RowList1["Angle"] != 1 and RowList2["Angle"] != 1:
				if (RowList1["Angle"] == RowList3["Angle"] and 
				RowList2["Angle"] == RowList3["Angle"]):
					print "Angles Check Out"
				else: RowPattern = False
		if RowPattern == True:
			self.Answer=Answer
			
    def CheckNetworks(self,Network1,Network2,Network3,RowList):
		self.FillAttributeArrays(Network1,Network2,Network3,RowList)
		
    def FindAnglePatterns(self,AngleList,RowList):
		if AngleList:
			AngleList = map(int,AngleList)
			for i in range(1,len(AngleList)):
				if AngleList[i] == 0:
					AngleList[i] = 360
			Rotation1 = (AngleList[1] - AngleList[0])
			Rotation2 = (AngleList[2] - AngleList[1])
			if Rotation1 == Rotation2:
				RowList["Angle"] = Rotation1
				print RowList["Angle"]
		if AngleList == None:
			RowList["Angle"] = -1
	
    def FindSizePatterns(self,SizeList,RowList):
		if SizeList:
			if ((self.SizePatterns[SizeList[2]] > self.SizePatterns[SizeList[1]] and 
			self.SizePatterns[SizeList[1]] > self.SizePatterns[SizeList[0]] and
			self.SizePatterns[SizeList[2]] > self.SizePatterns[SizeList[0]])):
				print "We went up one Size Each Time"
				RowList["Size"] = 2
			elif (self.SizePatterns[SizeList[0]]+self.SizePatterns[SizeList[1]]+self.SizePatterns[SizeList[2]])%3==0:
				print "The Sizes have one of each going upwards"
				RowList["Size"] = 3
			else:
				RowList["Size"] = 1
		if SizeList == None:
			RowList["Size"] = -1
		
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
			
    def ContingencyCheck(self,RowList1,RowList2):
		if RowList1["Addition"] == 1 and RowList2["Addition"] == 2:
			RowList1["Addition"] = 2
			print "New RowList1 Addition: ", RowList1["Addition"]
			
    def Solve(self,problem):
		print "********************We are on Problem Number..... ",self.Counter,"********************"
		self.Counter = self.Counter + 1
		
		OSNA = ObjectSemanticNetwork("A")
		for object in problem.getFigures().get(OSNA.letter).getObjects():
			OSNA.ObjectNames[object.getName()] = object.getAttributes()
		#OSNA.checkData("A")
		
		OSNB = ObjectSemanticNetwork("B")
		for object in problem.getFigures().get(OSNB.letter).getObjects():
			OSNB.ObjectNames[object.getName()] = object.getAttributes()
		#OSNB.checkData("B")
		
		OSNC = ObjectSemanticNetwork("C")
		for object in problem.getFigures().get(OSNC.letter).getObjects():
			OSNC.ObjectNames[object.getName()] = object.getAttributes()
		#OSNC.checkData("C")
		
		OSND = ObjectSemanticNetwork("D")
		for object in problem.getFigures().get(OSND.letter).getObjects():
			OSND.ObjectNames[object.getName()] = object.getAttributes()
		#OSND.checkData("D")
		
		OSNE = ObjectSemanticNetwork("E")
		for object in problem.getFigures().get(OSNE.letter).getObjects():
			OSNE.ObjectNames[object.getName()] = object.getAttributes()
		#OSNE.checkData("E")
		
		OSNF = ObjectSemanticNetwork("F")
		for object in problem.getFigures().get(OSNF.letter).getObjects():
			OSNF.ObjectNames[object.getName()] = object.getAttributes()
		#OSNF.checkData("F")
		
		OSNG = ObjectSemanticNetwork("G")
		for object in problem.getFigures().get(OSNG.letter).getObjects():
			OSNG.ObjectNames[object.getName()] = object.getAttributes()
		#OSNG.checkData("G")
		
		OSNH = ObjectSemanticNetwork("H")
		for object in problem.getFigures().get(OSNH.letter).getObjects():
			OSNH.ObjectNames[object.getName()] = object.getAttributes()
		#OSNH.checkData("H")
		
		self.CheckNetworks(OSNA,OSNB,OSNC,self.Row1List)
		self.CheckNetworks(OSND,OSNE,OSNF,self.Row2List)
		self.ContingencyCheck(self.Row1List,self.Row2List)
		
		for i in range(1,7):
			self.Answer = None
			print "+++++++++++++++We are on a new Answer Choice.....",i,"+++++++++++++++"
			OSNAnswer = ObjectSemanticNetwork(str(i))
			for object in problem.getFigures().get(OSNAnswer.letter).getObjects():
				OSNAnswer.ObjectNames[object.getName()] = object.getAttributes()
			#OSNAnswer.checkData(str(i))
			self.CheckNetworks(OSNG,OSNH,OSNAnswer,self.Row3List)
			self.CheckRowPatterns(self.Row1List,self.Row2List,self.Row3List,str(i))
			if self.Answer is not None:
				print "Answer is: ", self.Answer
				return str(self.Answer)
			elif i == 6 and self.Answer is None:
				print "--------------I don't know!!!!!!!!!!!!!!!!!! -------------------"
				return str(0)
			else:
				continue