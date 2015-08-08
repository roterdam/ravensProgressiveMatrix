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

import os
from VisualRavensFigure import VisualRavensFigure
from VisualRavensProblem import VisualRavensProblem

# A list of RavensProblems within one set.
#
# Your agent does not need to use this class explicitly.
class VisualProblemSet:
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
    def addProblem(self, set, problem):
        fullpath = "Problems (Image Data)" + os.sep + set + os.sep + problem + os.sep
        problemInfo = open(fullpath + problem + ".txt")
        name = self.getNextLine(problemInfo)
        type = self.getNextLine(problemInfo)
        currentAnswer = self.getNextLine(problemInfo)
        #answer=""
        answer=currentAnswer

        newProblem = VisualRavensProblem(name, type, answer)
        newProblem.getFigures()["A"]=VisualRavensFigure("A",fullpath + "A.png")
        newProblem.getFigures()["B"]=VisualRavensFigure("B",fullpath + "B.png")
        newProblem.getFigures()["C"]=VisualRavensFigure("C",fullpath + "C.png")
        newProblem.getFigures()["1"]=VisualRavensFigure("1",fullpath + "1.png")
        newProblem.getFigures()["2"]=VisualRavensFigure("2",fullpath + "2.png")
        newProblem.getFigures()["3"]=VisualRavensFigure("3",fullpath + "3.png")
        newProblem.getFigures()["4"]=VisualRavensFigure("4",fullpath + "4.png")
        newProblem.getFigures()["5"]=VisualRavensFigure("5",fullpath + "5.png")
        newProblem.getFigures()["6"]=VisualRavensFigure("6",fullpath + "6.png")
        if(type.startswith("3x3")):
            newProblem.getFigures()["D"]=VisualRavensFigure("D",fullpath + "D.png")
            newProblem.getFigures()["E"]=VisualRavensFigure("E",fullpath + "E.png")
            newProblem.getFigures()["F"]=VisualRavensFigure("F",fullpath + "F.png")
            newProblem.getFigures()["G"]=VisualRavensFigure("G",fullpath + "G.png")
            newProblem.getFigures()["H"]=VisualRavensFigure("H",fullpath + "H.png")

        self.problems.append(newProblem)

    def tryParseInt(self, i):
        try:
            int(i)
            return True
        except:
            return False
    def getNextLine(self, r):
        return r.readline().rstrip()
