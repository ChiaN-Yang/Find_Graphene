import serial

class esp:
	def __init__(self, dev="COM3", b=921600, axis=1, reset=True, initpos = 0.0, useaxis=[], timeout=0.5):
		self.dev = serial.Serial(dev,b)
		self.inuse = useaxis
		if(len(self.inuse)==0):
			self.inuse = [axis]
		self.defaxis = axis
# =============================================================================
# 		if(reset):
# 			for n in self.inuse:
# 				self.reset(n)
# 				r = self.check_errors()
# 				if(r!=0):
# 					print("Error while setting up controller, error # %d"%r)
# 				if(initpos!=0):
# 					self.setpos(initpos)
# 					r = self.check_errors()
# 					if(r!=0):
# 						print("Error while setting up controller, error # %d"%r)
# =============================================================================

	def reset(self,axis):
		self.dev.write(b"%dOR;%dWS0\r"%(axis,axis))
	
	def check_errors(self):
		self.dev.write(b"TE?\r")
		return float(self.dev.readline())

	def getpos(self,axis=None):
		a = self.defaxis
		if(axis and axis>0):
			a = axis
		self.dev.write(b"%dTP\r"%a)
		return float(self.dev.readline())
	
	def setpos(self,pos,axis=None):
		a = self.defaxis
		if(axis and axis>0):
			a = axis
		print("setting to %f"%pos)
		self.dev.write(b"%dPA%.4f;%dWS1;%dTP\r"%(a,pos,a,a))
		return float(self.dev.readline())

	def position(self,pos=None,axis=None):
		if(isinstance(pos,(float,int))):
			self.setpos(pos,axis)
			self.getpos()
			self.setpos(pos,axis)
		return self.getpos(axis)

	def getvel(self):
		self.dev.write(b"2VA?\r")
		return float(self.dev.readline())

	def setvel(self,vel):
		print("setting xy velocity to %f"%vel)
		self.dev.write(b"2VA%f;WT1;2VA?\r;"%(vel))
		return float(self.dev.readline())
    
	def get_pos(self):
		Rotation_angle = self.getpos(1)
		X_pos = self.getpos(2)
		Y_pos = self.getpos(3)
		return X_pos, Y_pos
    
	def angle_move(self, rel_angle):
		angle = self.getpos(1)
		self.setpos(angle + rel_angle, 1)
    
	def x_move(self, rel_var_x):
		x_pos = self.getpos(2)
		self.setpos(x_pos + rel_var_x, 2)
        
	def y_move(self, rel_var_y):
		y_pos = self.getpos(3)
		self.setpos(y_pos + rel_var_y, 3)
        
	def x_y_move(self, abs_x, abs_y):
		self.setpos(abs_x, 2)
		self.setpos(abs_y, 3)
        
	def write_corrd(self, name):
		X_pos = self.getpos(2)
		Y_pos = self.getpos(3)
		path = str(name) + '_test.txt'
		f = open(path, 'a')
		f.write(str(X_pos))
		f.write(str(Y_pos))
		f.write('\n')
		f.close()
    
	def close(self):
		self.dev.close()
        
	def __del__(self):
		self.close()


class prior_motor:
    def __init__(self, port = "COM1"):
        self.motor = serial.Serial(port, 9600, timeout=0.5)
        
    def get_z_pos(self):
        cmd = "PZ\r"
        self.motor.write(cmd.encode())
        response = self.motor.readline().decode()
        c_z_pos = int(response.strip('\r')) / 500
        print('Current z position: ' + str(c_z_pos))
        return c_z_pos
    
    def move_z_pos(self, z_pos):      
        cmd_pos = z_pos * 500
        cmd = "V " + str(cmd_pos)
        cmd = cmd + "\r"

        self.motor.write(cmd.encode())
        temp = self.motor.readline().decode()
        self.get_z_pos()
        
    def command(self, string):
        cmd = str(string) + "\r"
        self.motor.write(cmd.encode())
        response = self.motor.readline().decode()
        print(str(response))
        
    def close(self):
        self.motor.close()

    def __del__(self):
        self.close()


class controller(esp, prior_motor):
	pass


if __name__ == '__main__':
	pass