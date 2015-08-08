# DO NOT MODIFY THIS FILE.
#
# When you submit your project, an alternate version of this file will be used
# to test your code against the sample Raven's problems in this zip file, as
# well as other problems from the Raven's Test and former students.
#
# Any modifications to this file will not be used when grading your project.
# If you have any questions, please email the TAs.

# A single object in a RavensFigure -- typically, a single shape in a frame,
# such as a triangle or a circle -- comprised of a list of RavensAttributes.
class RavensObject:
    # Constructs a new RavensObject given a name.
    #
    # Your agent does not need to use this method.
    #
    # @param name the name of the object
    def __init__(self, name):
        self.name=name
        self.attributes=[]

    # The name of this RavensObject. Names are assigned starting with the
    # letter Z and proceeding backwards in the alphabet through the objects
    # in the Frame. Names do not imply correspondence between shapes in
    # different frames. Names are simply provided to allow agents to organize
    # their reasoning over different figures.
    #
    # Within a RavensFigure, each RavensObject has a unique name.
    #
    # @return the name of the RavensObject
    def getName(self):
        return self.name

    # Returns an ArrayList of RavensAttribute characterizing this RavensObject.
    #
    # @return an ArrayList of RavensAttribute
    def getAttributes(self):
        return self.attributes
