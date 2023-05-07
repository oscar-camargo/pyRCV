import os

class robot():
    def __init__(self,name,links,joints):
        self.name = name
        self.links = links
        self.joints = joints
        self.path = os.path.dirname(__file__)

    def create(self):
        self.robotfile = open(self.path + "/" + self.name + ".urdf","w")
        self.robotfile.write("<robot name=" + "\"" + self.name + "\">\n")
        for link in self.links:
            if link.type == "cylinder":
                str2write = "   <link name=" + "\"" + link.name + "\">\n" \
                    + "     <visual>\n" + "             <origin xyz=" + "\"" + str(link.origin[0]) + " " \
                    +  str(link.origin[1]) + " " + str(link.origin[2]) + "\"" \
                    + " rpy=" + "\"" + str(link.rpy[0]) + " " \
                    +  str(link.rpy[1]) + " " + str(link.rpy[2]) + "\" />\n" \
                    + "         <geometry>\n" \
                    + "             <cylinder length=" + "\"" + str(link.length) + "\" radius=" + "\"" + str(link.width) + "\"/> \n" \
                    + "         </geometry>\n" + "      </visual>\n" + "    </link>\n\n"
            else:
                str2write = "   <link name=" + "\"" + link.name + "\">\n" \
                    + "     <visual>\n" + "             <origin xyz=" + "\"" + str(link.origin[0]) + " " \
                    +  str(link.origin[1]) + " " + str(link.origin[2]) + "\"" \
                    + " rpy=" + "\"" + str(link.rpy[0]) + " " \
                    +  str(link.rpy[1]) + " " + str(link.rpy[2]) + "\" />\n" \
                    + "         <geometry>\n" \
                    + "             <box size=" + "\"" + str(link.length) + " " + str(link.width) + " " + str(link.height) + "\" />" \
                    + "         </geometry>\n" + "      </visual>\n" + "    </link>\n\n"
                
            self.robotfile.write(str2write)

        for joint in self.joints:
            str2write = "   <joint name=" + "\"" + joint.name + "\" type = \"revolute\">\n" \
                    + "     <parent link=" + "\"" + joint.parent + "\"" + "/>\n" \
                    + "     <child link=" + "\"" + joint.child + "\"" + "/>\n" \
                    + "     <origin xyz=" + "\"" + str(joint.origin[0]) + " " \
                    +  str(joint.origin[1]) + " " + str(joint.origin[2]) + "\"" \
                    + " rpy=" + "\"" + str(joint.rpy[0]) + " " \
                    +  str(joint.rpy[1]) + " " + str(joint.rpy[2]) + "\" />\n" \
                    + "     <axis xyz=" + "\"" +str(joint.axis[0]) + " " + str(joint.axis[1]) + " " + str(joint.axis[2]) + "\"/>\n" \
                    + "     <limit lower=" + "\"" + str(joint.limits[0]) + "\" upper=" + "\"" + str(joint.limits[1]) + "\"/>\n" \
                    + "   </joint>\n\n"
            self.robotfile.write(str2write)
        self.robotfile.write("</robot>")
            