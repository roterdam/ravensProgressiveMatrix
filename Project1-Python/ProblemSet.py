# DO NOT MODIFY THIS FILE.
#
# When you submit your project, an alternate version of this file will be used
# to test your code against the sample Raven's problems in this zip file, as
# well as other problems from the Raven's Test and former students.
#
# Any modifications to this file will not be used when grading your project.
# If you have any questions, please email the TAs.
#
#

import random
import re
from RavensAttribute import RavensAttribute
from RavensFigure import RavensFigure
from RavensObject import RavensObject
from RavensProblem import RavensProblem

# A list of RavensProblems within one set.
#
# Your agent does not need to use this class explicitly.
class ProblemSet:
    # Initializes a new ProblemSet with the given name, an empty set of
    # problems, and a new random number generator.
    #
    # Your agent does not need to use this method.
    #
    # @param name The name of the problem set.
    def __init__(self,name):
        self.name=name
        self.problems=[]

    # Returns the name of the problem set.
    #
    # Your agent does not need to use this method.
    #
    # @return the name of the problem set as a String
    def getName(self):
        return self.name

    # Returns an ArrayList of the RavensProblems in this problem set.
    #
    # Your agent does not need to use this method.
    #
    # @return the RavensProblems in this set as an ArrayList.
    def getProblems(self):
        return self.problems

    # Adds a new problem to the problem set, read from an external file.
    #
    # Your agent does not need to use this method.
    #
    # @param problem the File containing the new problem.
    def addProblem(self, problem):
        name = self.getNextLine(problem)
        type = self.getNextLine(problem)
        currentAnswer = self.getNextLine(problem)
        #answer=""
        answer=currentAnswer

        figures=[]
        currentFigure=None
        currentObject=None
        options=["1","2","3","4","5","6"]

        line = self.getNextLine(problem)
        while not line=="":
            if not line.startswith("\t"):
                if self.tryParseInt(line):
                    i=random.randint(0,len(options)-1)
                    if currentAnswer==line:
                        answer=options[i]
                    line=options[i]
                    options.remove(options[i])
                newFigure=RavensFigure(line)
                figures.append(newFigure)
                currentFigure=newFigure
            elif not line.startswith("\t\t"):
                line=line.replace("\t","")
                newObject=RavensObject(line)
                currentFigure.getObjects().append(newObject)
                currentObject=newObject
            elif line.startswith("\t\t"):
                line=line.replace("\t","")
                split=re.split(":",line)
                newAttribute=RavensAttribute(split[0],split[1])
                currentObject.getAttributes().append(newAttribute)
            line=self.getNextLine(problem)
        newProblem = RavensProblem(name, type, answer)
        for figure in figures:
            newProblem.getFigures()[figure.getName()]=figure
        self.problems.append(newProblem)

    def tryParseInt(self, i):
        try:
            int(i)
            return True
        except:
            return False
    def getNextLine(self, r):
        return r.readline().rstrip()