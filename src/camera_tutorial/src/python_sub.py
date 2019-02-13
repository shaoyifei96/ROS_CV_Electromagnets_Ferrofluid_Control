#!/usr/bin/env python
import rospy
from image_transport_tutorial.msg import tracking2Dmsg
import time 
import serial
import numpy as np
import struct
import scipy as sp
import scipy.integrate
import scipy.optimize
from Phidget22.Devices.DCMotor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

ser1 = serial.Serial('/dev/ttyACM0', 9600)

try:
    from PhidgetHelperFunctions import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                      "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

import sys

class RandomDisplacementBounds(object):
    """random displacement with bounds"""
    def __init__(self, xmin, xmax, stepsize=np.pi/2):
        self.xmin = xmin
        self.xmax = xmax
        self.stepsize = stepsize

    def __call__(self, x):
        """take a random step but ensure the new position is within the bounds"""
        return np.clip( x + np.random.uniform(-self.stepsize, self.stepsize, np.shape(x)), self.xmin, self.xmax )

# Define locations of center of front face of electomagnet: top, bottom, right, left
electromagnet_locs = np.array([[0.0,0.02], [0.0,-0.02], [0.02,0.0], [-0.02,0.0]])
mu_0 = (np.pi)*4e-7 #H/m 
l = 0.0714 #m
a = 0.007 #m
N= 1570*.6#turns of magnet This is way off
I = 1.#A 
k = mu_0*N/4/np.pi/l
R = 100. #Ohms Internal Resistance in wire

nu = np.array([l/a,0])

Voltage_Vector = np.array([1, 1, 1, 1], dtype = float)

def B_point(Current_Array, Particle_Position):
    
    def integrand1(theta, vec):
        return vec[0]/((vec[1]-np.cos(theta))**2+np.sin(theta)**2)*(vec[1]*np.cos(theta)-1)/(vec[0]**2+(vec[1]-np.cos(theta))**2+np.sin(theta)**2)**(1/2)
    
    def integrand2(theta, vec):
        return (np.cos(theta))/(vec[0]**2+(vec[1]-np.cos(theta))**2+np.sin(theta)**2)**(1/2)
        
    local_vecs = np.zeros((4,2), dtype = float)
    # Convert Global X and Y into local x and y for all 4 electromagnets where x = distance from face, y = distance from outward normal vector from center of electromagnet
    local_vecs[0,:] = [np.abs(Particle_Position[1]-electromagnet_locs[0,1]), -(Particle_Position[0]-electromagnet_locs[0,0])]
    local_vecs[1,:] = [np.abs(Particle_Position[1]-electromagnet_locs[1,1]), Particle_Position[0]-electromagnet_locs[1,0]]
    local_vecs[2,:] = [np.abs(Particle_Position[0]-electromagnet_locs[2,0]), Particle_Position[1]-electromagnet_locs[2,1]]
    local_vecs[3,:] = [np.abs(Particle_Position[0]-electromagnet_locs[3,0]), -(Particle_Position[1]-electromagnet_locs[3,1])]
            
    #Calculate B components
    B11 = np.zeros(4)
    B12 = np.zeros(4)
    B21 = np.zeros(4)
    B22 = np.zeros(4)
    
    for i in range(4):        
        B11[i] = sp.integrate.quad(integrand1, 0, 2*np.pi,args=(local_vecs[i,:]/a))[0]
        B12[i] = sp.integrate.quad(integrand1, 0, 2*np.pi,args=(local_vecs[i,:]/a+nu))[0]
        B21[i] = sp.integrate.quad(integrand2, 0, 2*np.pi,args=(local_vecs[i,:]/a))[0]
        B22[i] = sp.integrate.quad(integrand2, 0, 2*np.pi,args=(local_vecs[i,:]/a+nu))[0]
    
    h_x = np.multiply(k*(B11-B12), Current_Array)   
    h_y = np.multiply(k*(B21-B22), Current_Array)
    
    B_point_x = h_x[3]-h_x[2]+h_y[1]-h_y[0]
    B_point_y = h_y[3]-h_y[2]+h_x[1]-h_x[0]
    
    return np.array([[-h_y[0], h_y[1], -h_x[2], h_x[3], B_point_x], [-h_x[0], h_x[1], -h_y[2], h_y[3], B_point_y]])

def Gradient_B_field(Current_Vector, Particle_Position, h):
    
    Gradient_X = (B_point(Current_Vector,Particle_Position+np.array([h/2, 0])) - B_point(Current_Vector,Particle_Position-np.array([h/2, 0])))/h
    Gradient_Y = (B_point(Current_Vector,Particle_Position+np.array([0, h/2])) - B_point(Current_Vector,Particle_Position-np.array([0, h/2])))/h
    
    return Gradient_X, Gradient_Y

def Linear_Controller(Particle_Position, Desired_Position, kp):
    return kp*(Desired_Position-Particle_Position)

def Non_Linear_Controller(Current_Array, Particle_Position, h, X, x_0):
    omega = np.identity(4)
    Hr=1/R*np.matmul(B_point(Current_Array, Particle_Position)[:,0:4],omega)
    Her = np.vstack((Hr, Gradient_B_field(Current_Vector, Particle_Position, h)[0][:,0:4], np.matmul(np.array([0.,1.]), Gradient_B_field(Current_Vector, Particle_Position, h)[1][:,0:4])))
   
    
    def y_star(phi, X, Her):
        e = np.transpose(np.array([1,0,0,0]))
        F = np.array([[np.cos(phi),np.sin(phi),0,0,0],
                  [-np.sin(phi),np.cos(phi),0,0,0],
                  [0,0,np.cos(phi),np.sin(phi),0],
                   [0,0,0,np.cos(phi),np.sin(phi)]], dtype = float)
        b1 =np.matmul(np.linalg.inv(np.matmul(F,Her)),e)
        E = np.transpose(np.concatenate((np.zeros((2,2)),.5*np.identity(2)), axis=1))
        B2 =np.matmul(np.linalg.inv( np.matmul(F ,Her)),E)
        eps = 0.01
        w = eps*np.identity(4)+ np.matmul((np.transpose(Her)),Her)/(np.linalg.norm(np.matmul((np.transpose(Her)),Her),ord=None))
        rho_star = (np.matmul(np.matmul(np.matmul(np.matmul(np.transpose(X),np.transpose(B2)),w),B2),X)/(np.matmul(np.matmul(np.transpose(b1),w),b1)))**(1/4)
        return rho_star*b1+np.matmul(B2,X)/rho_star, w
    
        
    def J_star(phi, X, Her):
        return np.matmul(np.matmul(np.transpose(y_star(phi, X, Her)[0]),y_star(phi, X, Her)[1]),y_star(phi, X, Her)[0])
    
    J_star_zero = J_star(0, X, Her)
    J_star_pi = J_star (np.pi, X, Her)
    
        
    def callback(x, f, accepted): #Stop after finding 2 minima
        if len(number_minima) == 0 and f< J_star_zero and f < J_star_pi:
            number_minima.append(x)
            
        elif len(number_minima) == 1  and f< J_star_zero and f < J_star_pi:
            if abs(x - number_minima[0]) >= 0.000001:
                return True
            
    number_minima = []
    take_step = RandomDisplacementBounds(0, np.pi)
    minimizer_kwargs = dict(method="L-BFGS-B", args = (X, Her), bounds = ((0, np.pi),))
    phi_star = sp.optimize.basinhopping(J_star, x_0, minimizer_kwargs=minimizer_kwargs, take_step=take_step, callback = callback).x   
    #print(phi_star)
    return y_star(phi_star, X, Her)[0], Her, phi_star

lamda = 0.1

def Filter(X, Her, Yk_1, Z, phi_star):
    
  def psi(X, Her, w, phi_star):
    
    def B_vals(phi, X, Her):
        e = np.transpose(np.array([1,0,0,0]))
        F = np.array([[np.cos(phi),np.sin(phi),0,0,0],
                  [-np.sin(phi),np.cos(phi),0,0,0],
                  [0,0,np.cos(phi),np.sin(phi),0],
                   [0,0,0,np.cos(phi),np.sin(phi)]], dtype = float)
        b1 =np.matmul(np.linalg.inv(np.matmul(F,Her)),e)
        E = np.transpose(np.concatenate((np.zeros((2,2)),.5*np.identity(2)), axis=1))
        B2 =np.matmul(np.linalg.inv(np.matmul(F ,Her)),E)
        return b1, B2
    


    def Jqp_star(phi, X, Her, w):
        ro_zero = np.real(np.roots([np.matmul(np.transpose(B_vals(phi, X, Her)[0]),B_vals(phi, X, Her)[0]),np.matmul(-np.transpose(B_vals(phi, X, Her)[0]),w), 0, np.matmul(np.matmul(np.transpose(X),np.transpose(B_vals(phi, X, Her)[1])),w), np.matmul(np.matmul(np.matmul(-np.transpose(X),np.transpose(B_vals(phi, X, Her)[1])),B_vals(phi, X, Her)[1]),X)])[0])
        return np.matmul(np.transpose(B_vals(phi, X, Her)[0]),B_vals(phi, X, Her)[0])*ro_zero**2-\
            2*np.matmul(np.transpose(B_vals(phi, X, Her)[0]),w)*ro_zero-2*np.matmul(np.matmul(np.transpose(X),np.transpose(B_vals(phi, X, Her)[1])),w)/ro_zero+np.matmul(np.matmul(np.matmul(np.transpose(X),np.transpose(B_vals(phi, X, Her)[1])),B_vals(phi, X, Her)[1]),X)/ro_zero**2+2*np.matmul(np.matmul(np.transpose(B_vals(phi, X, Her)[0]),B_vals(phi, X, Her)[1]),X)+np.matmul(np.matmul(np.transpose(w),np.identity(4)),w)
    
    J_star_zero = Jqp_star(0, X, Her, w)
    J_star_pi = Jqp_star(np.pi, X, Her, w)
    
    def callback(x, f, accepted): #Stop after finding 2 minima
        if len(number_minima) == 0 and f< J_star_zero and f < J_star_pi:
            number_minima.append(x)
            
        elif len(number_minima) == 1  and f< J_star_zero and f < J_star_pi:
            if abs(x - number_minima[0]) >= 0.000001:
                return True
    
    number_minima = []
    take_step = RandomDisplacementBounds(0, np.pi)
    minimizer_kwargs = dict(method="L-BFGS-B", args = (X, Her, w), bounds = ((0, np.pi),))
    phi_zero = sp.optimize.basinhopping(Jqp_star, phi_star, minimizer_kwargs=minimizer_kwargs, take_step=take_step, callback = callback).x   
    ro_zero = np.real(np.roots([np.matmul(np.transpose(B_vals(phi_zero, X, Her)[0]),B_vals(phi_zero, X, Her)[0]),np.matmul(-np.transpose(B_vals(phi_zero, X, Her)[0]),w), 0, np.matmul(np.matmul(np.transpose(X),np.transpose(B_vals(phi_zero, X, Her)[1])),w), np.matmul(np.matmul(np.matmul(-np.transpose(X),np.transpose(B_vals(phi_zero, X, Her)[1])),B_vals(phi_zero, X, Her)[1]),X)])[0])
    
    return ro_zero*B_vals(phi_zero,X, Her)[0]+np.matmul(B_vals(phi_zero,X, Her)[1],X)/ro_zero
    
  return psi(X, Her, (1-lamda)*Yk_1+lamda*Z, phi_star)


Desired_Position = np.array([0.0001, 0.0001])
Current_Vector = np.array([.7,.7,.7,.7])
kp = .49
x_0 = np.pi/2

class Python_suber:

    def __init__(self):
        self.sub = rospy.Subscriber("/camera1/cv_image_pos", tracking2Dmsg, self.callback)
        self.past_pos_x = 0
        self.past_pos_y = 0
        # self.dc_motor0   = ch0
        # self.dc_motor1   = ch1
        self.Yk_1 = np.array([0,0,0,0])
        self.iteration = 0

    def callback(self,data):

        name = "255,0,0,0"
        # diffx = data.x - self.past_pos_x
        # diffy = data.y - self.past_pos_y
        data.x = data.x-80
        data.y = data.y-100
        ppm = 98.0/0.04
        use_this_x = data.x/ppm
        use_this_y = -(data.y/ppm)
        self.iteration += .002
        use_this_x = -self.iteration
        use_this_y = self.iteration
        delta = 0.001  
        print("x= ",use_this_x, "  y= ",use_this_y) 
        if abs(use_this_x) < delta:  use_this_x = delta
        if abs(use_this_y) < delta:  use_this_y = delta
        Particle_Position = np.array([use_this_x, use_this_y])
        X_out = Linear_Controller(Particle_Position, Desired_Position, kp)
        Z, Her, phi_star = Non_Linear_Controller(Current_Vector, Particle_Position, 1e-10, X_out, x_0)
        Y = Filter(X_out, Her, self.Yk_1, Z, phi_star)
        self.Y_k_1 = Y
        Y = Y*np.min([30,np.max(abs(Y))])/np.max(abs(Y))/30*255
        print("Voltage Values: " + str(Y/255*30))
        values = Y.astype(int)
        signs = np.zeros((4), dtype = np.uint8)
        for i in range(len(values)):
            values[i] = int(values[i])
            if values[i] >= 0:
                signs[i] = 1
            else:
                pass
        valuesToWrite = struct.pack("BBBBBBBB", np.uint8(abs(values[0])), np.uint8(signs[0]), np.uint8(abs(values[1])), np.uint8(signs[1]), np.uint8(abs(values[2])), np.uint8(signs[2]), np.uint8(abs(values[3])), np.uint8(signs[3]))    
        ser1.write(valuesToWrite)
        return 
        # print("x"   +str(data.x))
        # print("y"   +str(data.y))
        # print("nx"  +str(data.nx))
        # print("ny"  +str(data.ny))
        # print(str(diffx))
        # print(str(diffy))
        # 0 on the right
        # 1 on the left
        # percent = float(data.x)/data.nx
        # if percent > 0.5:
        #     m1_output = 1
        #     m0_output = 0
        # elif percent < 0.5:
        #     m0_output = 1
        #     m1_output = 0
        # else:
        #     m0_output = 0
        #     m1_output = 0
        # self.dc_motor0.setTargetVelocity(m0_output)
        # self.dc_motor1.setTargetVelocity(m1_output)
        # if (data.x>data.nx/2.0):
        #     self.dc_motor0.setTargetVelocity(0.0)
        #     self.dc_motor1.setTargetVelocity(1.0)

        # self.past_pos_y = data.y
        # self.past_pos_x = data.x
        # self.dc_motor0.setTargetVelocity(float(data.x)/data.nx)
        # self.dc_motor1.setTargetVelocity(float(data.y)/data.ny)



# def onAttachHandler(self):
    
#     ph = self

#     try:
#         #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
#         #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
#         print("\nAttach Event:")
        
#         """
#         * Get device information and display it.
#         """
#         channelClassName = ph.getChannelClassName()
#         serialNumber = ph.getDeviceSerialNumber()
#         channel = ph.getChannel()
#         if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
#             hubPort = ph.getHubPort()
#             print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
#                 "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
#         else:
#             print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
#                     "\n\t-> Channel:  " + str(channel) + "\n")
    
#         """
#         * Set the DataInterval inside of the attach handler to initialize the device with this value.
#         * DataInterval defines the minimum time between VelocityUpdate events.
#         * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
#         """
#         print("\tSetting DataInterval to 1000ms")
#         try:
#             ph.setDataInterval(1000)
#         except PhidgetException as e:
#             sys.stderr.write("Runtime Error -> Setting DataInterval: \n\t")
#             DisplayError(e)
#             return
        
#     except PhidgetException as e:
#         print("\nError in Attach Event:")
#         DisplayError(e)
#         traceback.print_exc()
#         return

# """
# * Displays info about the detached Phidget channel.
# * Fired when a Phidget channel with onDetachHandler registered detaches
# *
# * @param self The Phidget channel that fired the attach event
# """
# def onDetachHandler(self):

#     ph = self

#     try:
#         #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
#         #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
#         print("\nDetach Event:")
        
#         """
#         * Get device information and display it.
#         """
#         channelClassName = ph.getChannelClassName()
#         serialNumber = ph.getDeviceSerialNumber()
#         channel = ph.getChannel()
#         if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
#             hubPort = ph.getHubPort()
#             print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
#                 "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
#         else:
#             print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
#                     "\n\t-> Channel:  " + str(channel) + "\n")
        
#     except PhidgetException as e:
#         print("\nError in Detach Event:")
#         DisplayError(e)
#         traceback.print_exc()
#         return

# """
# * Writes Phidget error info to stderr.
# * Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
# *
# * @param self The Phidget channel that fired the attach event
# * @param errorCode the code associated with the error of enum type ph.ErrorEventCode
# * @param errorString string containing the description of the error fired
# """
# def onErrorHandler(self, errorCode, errorString):

#     sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

# """
# * Outputs the DCMotor's most recently reported velocity.
# * Fired when a DCMotor channel with onVelocityUpdateHandler registered meets DataInterval criteria
# *
# * @param self The DCMotor channel that fired the VelocityUpdate event
# * @param velocity The reported velocity from the DCMotor channel
# """
def onVelocityUpdateHandler(self, velocity):

    #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #www.phidgets.com/docs/Using_Multiple_Phidgets for information

    print("[Velocity Event] -> Velocity: " + str(velocity))

       
# def dc_main():
   
#         print("\nSetting OnVelocityUpdateHandler...")
#         ch.setOnVelocityUpdateHandler(onVelocityUpdateHandler)
        
#         """
#         * Open the channel with a timeout
#         """
#         print("\nOpening and Waiting for Attachment...")
        
#         try:
#             ch.openWaitForAttachment(5000)
#         except PhidgetException as e:
#             PrintOpenErrorMessage(e, ch)
#             raise EndProgramSignal("Program Terminated: Open Failed")

#         print("--------------------\n"
#         "\n  | DC motor speed can be controlled by setting its Target Velocity (ie its duty cycle).\n"
#         "  | The target velocity can be a number from -1.0 to +1.0, where sign indicates direction of rotation.\n"
#         "  | For this example, acceleration has been fixed to 1.0Hz, but can be changed in custom code.\n"

#         "\nInput a desired velocity between -1.0 and 1.0 and press ENTER\n"
#         "Input Q and press ENTER to quit\n")

#         end = False

#         while (end != True):
#             buf = sys.stdin.readline(100)
#             if not buf:
#                 continue

#             if (buf[0] == 'Q' or buf[0] ==  'q'):
#                 end = True
#                 continue
            
#             try:
#                 velocity = float(buf)
#             except ValueError as e:
#                 print("Input must be a number, or Q to quit.")
#                 continue

#             if (velocity > 1.0):
#                 velocity = 1.0
#                 print("MAXIMUM velocity is +/-1.0")

#             if (velocity < -1.0):
#                 velocity = -1.0
#                 print("MAXIMUM velocity is +/-1.0")

#             print("Setting DCMotor TargetVelocity to " + str(velocity))
#             ch.setTargetVelocity(velocity)

#         '''
#         * Perform clean up and exit
#         '''

#         #clear the VelocityUpdate event handler 
#         ch.setOnVelocityUpdateHandler(None)  

#         print("Cleaning up...")
#         ch.close()
#         print("\nExiting...")
#         return 0

#     except PhidgetException as e:
#         sys.stderr.write("\nExiting with error(s)...")
#         DisplayError(e)
#         traceback.print_exc()
#         print("Cleaning up...")
#         #clear the VelocityUpdate event handler 
#         ch.setOnVelocityUpdateHandler(None)  
#         ch.close()
#         return 1
#     except EndProgramSignal as e:
#         print(e)
#         print("Cleaning up...")
#         #clear the VelocityUpdate event handler 
#         ch.setOnVelocityUpdateHandler(None)  
#         ch.close()
#         return 1
#     finally:
#         print("Press ENTER to end program.")
#         readin = sys.stdin.readline()
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    #dc_main()

    # try:
    #     ch0 = DCMotor()
    #     ch1 = DCMotor()
    # except PhidgetException as e:
    #     sys.stderr.write("Runtime Error -> Creating DCMotor: \n\t")
    #     DisplayError(e)
    #     raise
    # except RuntimeError as e:
    #     sys.stderr.write("Runtime Error -> Creating DCMotor: \n\t" + e)
    #     raise

    # """
    # * Set matching parameters to specify which channel to open
    # """
    # #You may remove this line and hard-code the addressing parameters to fit your application
    # #channelInfo = AskForDeviceParameters(ch)
    
    # ch0.setDeviceSerialNumber(485540)
    # #ch.setHubPort(channelInfo.hubPort)
    # ch0.setIsHubPortDevice(0)
    # ch0.setChannel(0)  
    
    # ch1.setDeviceSerialNumber(485540)
    # #ch.setHubPort(channelInfo.hubPort)
    # ch1.setIsHubPortDevice(0)
    # ch1.setChannel(1) 
    # print("\nSetting OnVelocityUpdateHandler...")
    # ch0.setOnVelocityUpdateHandler(onVelocityUpdateHandler)
    # ch1.setOnVelocityUpdateHandler(onVelocityUpdateHandler)
  
    # try:
    #     ch0.openWaitForAttachment(5000)
    #     ch1.openWaitForAttachment(5000)
    # except PhidgetException as e:
    #     PrintOpenErrorMessage(e, ch0)
    #     PrintOpenErrorMessage(e, ch1)
    #     raise EndProgramSignal("Program Terminated: Open Failed")

        # if(channelInfo.netInfo.isRemote):
        #     ch.setIsRemote(channelInfo.netInfo.isRemote)
        #     if(channelInfo.netInfo.serverDiscovery):
        #         try:
        #             Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)
        #         except PhidgetException as e:
        #             PrintEnableServerDiscoveryErrorMessage(e)
        #             raise EndProgramSignal("Program Terminated: EnableServerDiscovery Failed")
        #     else:
        #         Net.addServer("Server", channelInfo.netInfo.hostname,
        #             channelInfo.netInfo.port, channelInfo.netInfo.password, 0)
        
    """
        * Add event handlers before calling open so that no events are missed.
        """
    # print("\n--------------------------------------")
    # print("\nSetting OnAttachHandler...")
    # ch.setOnAttachHandler(onAttachHandler)
    
    # print("Setting OnDetachHandler...")
    # ch.setOnDetachHandler(onDetachHandler)
    
    # print("Setting OnErrorHandler...")
    # ch.setOnErrorHandler(onErrorHandler)

    # #This call may be harmlessly removed
    # PrintEventDescriptions()
    
  
        

    rospy.init_node('python_sub', anonymous=True)
    python_sub = Python_suber()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    #ch0.setOnVelocityUpdateHandler(None)  
    #ch1.setOnVelocityUpdateHandler(None)  

    #print("Cleaning up...")
    #ch0.close()
    #ch1.close()
    #print("\nExiting...")   


if __name__ == '__main__':

    listener()
