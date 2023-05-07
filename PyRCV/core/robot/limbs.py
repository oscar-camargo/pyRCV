#Arm links - joints definition

class link():

    def __init__(self,name,type,origin,rpy,length,width,height):
        self.name = name
        self.type = type
        self.origin = origin
        self.rpy = rpy
        self.length = length
        self.width = width
        self.height = height

class joint():
    
    def __init__(self,name,parent,child,origin,rpy,axis,limits):
        self.name = name
        self.parent = parent
        self.child = child
        self.origin = origin
        self.rpy = rpy
        self.axis = axis
        self.limits = limits