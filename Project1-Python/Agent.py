# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

import random

def addToList(name, value, List):
		List[name] = value
					
class ObjectSemanticNetwork:
	# This class will define my Semantic Network representation for the objects.
	# I will use a dictionary as the key to my representation. The key will be the
	# ObjectName and the value will be the array of ObjectAttributes objects. So for
	# example, the first 2x1 matrix should have 2 ObjectAttribute objects in the array.
	def __init__(self,name):
	    self.name = name
	    self.ObjectNames = {}
			
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
		self.Counter = 1
		
    def CheckNetworks(self,SemanticNetworkA,SemanticNetworkB,ChangeList,SameList,
	DeleteList,AddedList,LocationArray1,LocationArray2,AngleArray1,AngleArray2):
		if len(SemanticNetworkA.ObjectNames) < len(SemanticNetworkB.ObjectNames):
			for key in SemanticNetworkB.ObjectNames:
				if key not in SemanticNetworkA.ObjectNames:
					print "Object",key,"has been added"
					AddedList.append(key)
		if len(SemanticNetworkA.ObjectNames) > len(SemanticNetworkB.ObjectNames):
			for key in SemanticNetworkA.ObjectNames:
				if key not in SemanticNetworkB.ObjectNames:
					print "Object",key,"was deleted"
					DeleteList.append(key)
		if (len(SemanticNetworkA.ObjectNames) > len(SemanticNetworkB.ObjectNames) 
		or len(SemanticNetworkA.ObjectNames) == len(SemanticNetworkB.ObjectNames)):
			for key1,value1 in SemanticNetworkB.ObjectNames.iteritems():
				AttributeHolderChange = {}
				AttributeHolderSame = {}
				AttributeList1 = {}
				AttributeList2 = {}
				print SemanticNetworkA.name
				for j in SemanticNetworkA.ObjectNames[key1]:
					if j.getName() == "inside" or j.getName() == "above" or j.getName() == "left-of" or j.getName() == "right-of":
						LocationArray1[key1] = j
						print "LocationArray1 key:",key1,"Name:",LocationArray1[key1].getName(),"Value:",LocationArray1[key1].getValue()
					elif j.getName() == "angle":
						AngleArray1[key1] = j
						print "AngleArray1 key:",key1,"Name:",AngleArray1[key1].getName(),"Value:",int(AngleArray1[key1].getValue())
					else:
						AttributeList1[j.getName()] = j.getValue()
				print key1,"Printing List 1",AttributeList1,"\n"
				print SemanticNetworkB.name
				for i in SemanticNetworkB.ObjectNames[key1]:
					if i.getName() == "inside" or i.getName() == "above" or i.getName() == "left-of" or i.getName() == "right-of":
						LocationArray2[key1] = i
						print "LocationArray2 key:",key1,"Name:",LocationArray2[key1].getName(),"Value:",LocationArray2[key1].getValue()
					elif i.getName() == "angle":
						AngleArray2[key1] = i
						print "AngleArray2 key:",key1,"Name:",AngleArray2[key1].getName(),"Value:",int(AngleArray2[key1].getValue())
					else: 
						AttributeList2[i.getName()] = i.getValue()
				print key1,"Printing List 2",AttributeList2,"\n"
				for key in AttributeList1:
					if key in AttributeList2:
						if AttributeList1[key] != AttributeList2[key]:
							AttributeHolderChange[key] = AttributeList2[key]
						if AttributeList1[key] == AttributeList2[key]:
							AttributeHolderSame[key] = AttributeList2[key]
				addToList(key1,AttributeHolderChange,ChangeList)
				addToList(key1,AttributeHolderSame,SameList)
		print "-----------Printing ChangeList---------"
		for key,value in ChangeList.iteritems():
			print key,value
		print "-----------Ending ChangeList-----------"
		
		print "-----------Printing SameList---------"
		for key,value in SameList.iteritems():
			print key,value
		print "-----------Ending SameList-----------"
		
    def FindAnswer(self,Answer,ChangeListAB,ChangeListCD,SameListAB,
	SameListCD,AddedObjectsAB,AddedObjectsCD,DeletedObjectsAB,
	DeletedObjectsCD,LocationArrayA,LocationArrayB,LocationArrayC,
	LocationArrayD,AngleArrayA,AngleArrayB,AngleArrayC,AngleArrayD):
		print "AddedObjects",len(AddedObjectsAB),len(AddedObjectsCD)
		if len(AddedObjectsAB) != len(AddedObjectsCD):
			print "AddedObjects Arrays don't match!!"
			return None
		print "DeletedObjects",len(DeletedObjectsAB),len(DeletedObjectsCD)
		if len(DeletedObjectsAB) != len(DeletedObjectsCD):
			print "DeletedObjects Arrays don't match!!"
			return None
		Search = False
		if LocationArrayA and LocationArrayB:
			for key,value in LocationArrayA.iteritems():
				print "LocationArrayA Name:",LocationArrayA[key].getName(),"Value",LocationArrayA[key].getValue(),"for object",key
				print "LocationArrayB Name:",LocationArrayB[key].getName(),"Value",LocationArrayB[key].getValue(),"for object",key
				if LocationArrayA[key].getName() != LocationArrayB[key].getName():
					Search = True
		if not Search:
			print "LocationArrays haven't changed. Let's keep it movin'!!!"
		if Search:
			print "Time to search the LocationArrays"
			if LocationArrayA and LocationArrayC:
				for key,value in LocationArrayA.iteritems():
						print "LocationArrayA name",value.getName(),"Value",value.getValue(),"for object",key
						print "LocationArrayC name",LocationArrayC[key].getName(),"Value",LocationArrayC[key].getValue(),"for object",key
						if value.getName() != LocationArrayC[key].getName():
							print "LocationArrayA and C location don't match for",key
							return None
						if value.getName() == LocationArrayC[key].getName():
							print "LocationArrayA and C location match for",key,". Let's Continue"
			if LocationArrayA and LocationArrayB:
				if not LocationArrayC or not LocationArrayD:
					print "Location ArrayA and B exist; but C or D do not. This is a hazard; so we must move on."
					return None
			if LocationArrayB and LocationArrayD:
				for key,value in LocationArrayB.iteritems():
					if key not in LocationArrayD:
						continue
					print "LocationArrayB name",value.getName(),"Value",value.getValue(),"for object",key
					print "LocationArrayD name",LocationArrayD[key].getName(),"Value",LocationArrayD[key].getValue(),"for object",key
					if value.getName() != LocationArrayD[key].getName():
						print "LocationArrayB and D location don't match for",key
						return None
					if value.getName() == LocationArrayD[key].getName():
						print "LocationArrayB and D location for ",key,"match. Let's Continue"
		if AngleArrayD:
			if not AngleArrayC:
				print "There are rotations in D; but not in C"
				return None
		if AngleArrayA and AngleArrayB and AngleArrayC and AngleArrayD:
			print "Looking at the AngleArrays"
			for key,value in AngleArrayA.iteritems():
				print "AngleArrayA",key,"Value",AngleArrayA[key].getValue()
				print "AngleArrayB",key,"Value",AngleArrayB[key].getValue()
				print "AngleArrayC",key,"Value",AngleArrayC[key].getValue()
				print "AngleArrayD",key,"Value",AngleArrayD[key].getValue()
				result1 = abs(int(AngleArrayA[key].getValue()) - int(AngleArrayC[key].getValue()))
				result2 = abs(int(AngleArrayB[key].getValue()) - int(AngleArrayD[key].getValue()))
				print "Result 1 for key",key,"is",result1
				print "Result 2 for key",key,"is",result2
				FinalResult = result1 - result2
				if FinalResult != 0:
					print "The angles don't match A and B rotations"
					return None
				print "AngleArrays check out for",key,"!!!"
		for key1,value1 in SameListAB.iteritems():
			for key2,value2 in value1.iteritems():
				if key2 in SameListCD[key1]:
					if key2 == "shape":
						print "It's A Shape;","Let's Continue"
						continue
				if key2 not in SameListCD[key1]:
					print "SameLists don't match up"
					return None
				if value2 != SameListCD[key1][key2]:
					return None
		for key1,value1 in ChangeListAB.iteritems():
			for key2,value2 in value1.iteritems():
				if key2 not in ChangeListCD[key1]:
					print "ChangeLists don't match up"
					return None
				if key2 in ChangeListCD[key1]:
					if value2 != ChangeListCD[key1][key2]:
						return None
		return str(Answer)
				
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
    def Solve(self,problem):
		print "********************We are on Problem Number..... ",self.Counter,"********************"
		self.Counter = self.Counter + 1
		LocationArrayA = {}
		LocationArrayB = {}
		LocationArrayC = {}
		LocationArrayD = {}
		AngleArrayA = {}
		AngleArrayB = {}
		AngleArrayC = {}
		AngleArrayD = {}
		AddedObjectsAB = []
		AddedObjectsCD = []
		DeletedObjectsAB = []
		DeletedObjectsCD = []
		ChangeListAB = {}
		ChangeListCD = {}
		SameListAB = {}
		SameListCD = {}
		
		OSNA = ObjectSemanticNetwork("A")
		for object in problem.getFigures().get(OSNA.name).getObjects():
			OSNA.ObjectNames[object.getName()] = object.getAttributes()
		
		OSNB = ObjectSemanticNetwork("B")
		for object in problem.getFigures().get(OSNB.name).getObjects():
			OSNB.ObjectNames[object.getName()] = object.getAttributes()
		
		self.CheckNetworks(OSNA,OSNB,ChangeListAB,SameListAB,DeletedObjectsAB,
		AddedObjectsAB,LocationArrayA,LocationArrayB,AngleArrayA,AngleArrayB)
		
		OSNC = ObjectSemanticNetwork("C")
		for object in problem.getFigures().get(OSNC.name).getObjects():
			OSNC.ObjectNames[object.getName()] = object.getAttributes()
		
		for i in range(1,7):
			OSND = ObjectSemanticNetwork(str(i))
			for object in problem.getFigures().get(OSND.name).getObjects():
				OSND.ObjectNames[object.getName()] = object.getAttributes()
			self.CheckNetworks(OSNC,OSND,ChangeListCD,SameListCD,DeletedObjectsCD,AddedObjectsCD,
			LocationArrayC,LocationArrayD,AngleArrayC,AngleArrayD)
			Answer = self.FindAnswer(i,ChangeListAB,ChangeListCD,SameListAB,SameListCD,AddedObjectsAB,
			AddedObjectsCD,DeletedObjectsAB,DeletedObjectsCD,LocationArrayA,LocationArrayB,LocationArrayC,
			LocationArrayD,AngleArrayA,AngleArrayB,AngleArrayC,AngleArrayD)
			LocationArrayC = {}
			LocationArrayD = {}
			AddedObjectsCD = []
			DeletedObjectsCD = []
			AngleArrayC = {}
			AngleArrayD = {}
			print "Answer",Answer
			if Answer is not None:
				return str(Answer)
			if i == 6 and Answer is None:
				print "--------------I don't know!!!!!!!!!!!!!!!!!! -------------------"
				return str(0)
			else:
				continue