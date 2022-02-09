import serial
from utils.getCCDphoto import getphoto, CCD_save, tenengrad
from time import sleep

class esp:
	def __init__(self, dev="COM3", b=921600, axis=1, reset=True, initpos = 0.0, useaxis=[], timeout=0.5):
		self.dev = serial.Serial(dev,b)
		self.inuse = useaxis
		if(len(self.inuse)==0):
			self.inuse = [axis]
		self.defaxis = axis

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
		Rotation_angle = self.getpos(3)
		X_pos = self.getpos(1)
		Y_pos = self.getpos(2)
		return X_pos, Y_pos
    
	def angle_move(self, rel_angle):
		angle = self.getpos(3)
		self.setpos(angle + rel_angle, 3)
    
	def x_move(self, rel_var_x):
		x_pos = self.getpos(1)
		self.setpos(x_pos + rel_var_x, 1)
        
	def y_move(self, rel_var_y):
		y_pos = self.getpos(2)
		self.setpos(y_pos + rel_var_y, 2)
        
	def x_y_move(self, abs_x, abs_y):
		self.setpos(abs_x, 1)
		self.setpos(abs_y, 2)
        
	def write_corrd(self, name):
		X_pos = self.getpos(1)
		Y_pos = self.getpos(2)
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

    def focusLens(self, zNum, zRange, imgPath):
        """Perfrom Num times z scans to find the best figure ranging from -Range to Range"""
        image_Q = []
        origin_z = self.get_z_pos()
        for j in range(zNum):
            tar_z = origin_z - zRange + (j * 2.*zRange/(zNum-1.))
            sleep(0.2)
            self.move_z_pos(tar_z)
            CCD_save(getphoto(), imgPath)
            imageVar = tenengrad(imgPath)
            image_QVar = (imageVar, tar_z)
            image_Q.append(image_QVar)
        # Move to the z position which is corresponding to the best quality figure
        bestZ = max(image_Q)[1]
        self.move_z_pos(bestZ)
        sleep(0.2)
        # Save the original corner figure
        CCD_save(getphoto(), imgPath)
        return round(bestZ, 3)

    def focusLens_fast(self, zNum, zRange, imgPath, reverse):
        """Perfrom Num times z scans to find the best figure ranging from 0 to Range"""
        # Form the image-Quality list ot record the quality of the figure
        image_Q = []
        # get current z position
        current_z = self.get_z_pos()
        # Perfrom n times z scans to find the best figure ranging from 0 to d
        for j in range(zNum):
            tar_z = current_z + (j * zRange/(zNum-1.0)) * reverse
            self.move_z_pos(tar_z)
            CCD_save(getphoto(), imgPath)
            imageVar = tenengrad(imgPath)
            image_QVar = (imageVar, tar_z)
            image_Q.append(image_QVar)
        # Move to the z position which is corresponding to the best quality figure
        bestZ = max(image_Q)[1]
        self.move_z_pos(bestZ)
        sleep(0.2)
        # Save the figure again
        CCD_save(getphoto(), imgPath)
        return round(bestZ, 3)
        
    def focusLens_fast2(self, zNum, zRange, imgPath, reverse):
        """Perfrom Num times z scans to find the best figure ranging from 0 to Range"""
        # Form the image-Quality list ot record the quality of the figure
        image_Q = []
        # get current z position
        current_z = self.get_z_pos()
        CCD_save(getphoto(), imgPath)
        imageVar = tenengrad(imgPath)
        image_QVar = (imageVar, current_z)
        image_Q.append(image_QVar)
        # Perfrom n times z scans to find the best figure ranging from 0 to d
        for j in range(zNum):
            tar_z = current_z + ((j+1) * zRange/(zNum-1.0)) * reverse
            self.move_z_pos(tar_z)
            CCD_save(getphoto(), imgPath)
            imageVar = tenengrad(imgPath)
            image_QVar = (imageVar, tar_z)
            image_Q.append(image_QVar)
        # Move to the z position which is corresponding to the best quality figure
        bestZ = max(image_Q)[1]
        self.move_z_pos(bestZ)
        sleep(0.2)
        # Save the figure again
        CCD_save(getphoto(), imgPath)
        return round(bestZ, 3)
		
    def close(self):
        self.motor.close()

    def __del__(self):
        self.close()


class controller(esp, prior_motor):
	pass


if __name__ == '__main__':
	pass