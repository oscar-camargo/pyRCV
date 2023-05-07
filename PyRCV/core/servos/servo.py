class servo():
    def __init__(self,name,initial_position,angle):
        self.name = name
        self.initial_position = initial_position

    def rotate(self,angle):
        ServoBlaster = open('/dev/servoblaster', 'w')   # ServoBlaster is what we use to control the servo motors
        ServoBlaster.write(f'{servo}=' + str(self.initial_position + (angle/180)*100) + '%\n')   #
        ServoBlaster.flush()
        