# DO NOT MODIFY THIS FILE.
#
# When you submit your project, an alternate version of this file will be used
# to test your code against the sample Raven's problems in this zip file, as
# well as other problems from the Raven's Test and former students.
#
# Any modifications to this file will not be used when grading your project.
# If you have any questions, please email the TAs.

# A single variable-value pair that describes some element of a RavensObject.
# For example, a circle might have the attributes shape:circle, size:large, and
# filled:no.
class RavensAttribute:
    # Creates a new RavensAttribute.
    #
    # Your agent does not need to use this method.
    #
    # @param name the name of the attribute
    # @param value the value of the attribute
    def __init__(self, name, value):
        self.name=name
        self.value=value

    # Returns the name of the attribute. For example, 'shape', 'size', or
    # 'fill'.
    #
    # @return the name of the attribute
    def getName(self):
        return self.name

    # Returns the value of the attribute. For example, 'circle', 'large', or
    # 'no'.
    #
    # @return the value of the attribute
    def getValue(self):
        return self.value