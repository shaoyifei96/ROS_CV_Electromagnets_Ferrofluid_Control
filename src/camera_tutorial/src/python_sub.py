#!/usr/bin/env python
import rospy
from image_transport_tutorial.msg import tracking2Dmsg
import time 
from Phidget22.Devices.DCMotor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

try:
    from PhidgetHelperFunctions import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                      "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

import sys


class Python_suber:

    def __init__(self,ch0,ch1):
        self.sub = rospy.Subscriber("/camera1/cv_image_pos", tracking2Dmsg, self.callback)
        self.past_pos_x = 0
        self.past_pos_y = 0
        self.dc_motor0   = ch0
        self.dc_motor1   = ch1

    def callback(self,data):
        diffx = data.x - self.past_pos_x
        diffy = data.y - self.past_pos_y
        # print("x"   +str(data.x))
        # print("y"   +str(data.y))
        # print("nx"  +str(data.nx))
        # print("ny"  +str(data.ny))
        # print(str(diffx))
        # print(str(diffy))
        self.past_pos_y = data.y
        self.past_pos_x = data.x
        print(data.x/data.nx)
        self.dc_motor0.setTargetVelocity(float(data.x)/data.nx)
        self.dc_motor1.setTargetVelocity(data.y/data.ny)

    def helper1(self):
        self.past_pos_x



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
    try:
        ch0 = DCMotor()
        ch1 = DCMotor()
    except PhidgetException as e:
        sys.stderr.write("Runtime Error -> Creating DCMotor: \n\t")
        DisplayError(e)
        raise
    except RuntimeError as e:
        sys.stderr.write("Runtime Error -> Creating DCMotor: \n\t" + e)
        raise

    """
    * Set matching parameters to specify which channel to open
    """
    #You may remove this line and hard-code the addressing parameters to fit your application
    #channelInfo = AskForDeviceParameters(ch)
    
    ch0.setDeviceSerialNumber(485540)
    #ch.setHubPort(channelInfo.hubPort)
    ch0.setIsHubPortDevice(0)
    ch0.setChannel(0)  
    
    ch1.setDeviceSerialNumber(485540)
    #ch.setHubPort(channelInfo.hubPort)
    ch1.setIsHubPortDevice(0)
    ch1.setChannel(1) 
    print("\nSetting OnVelocityUpdateHandler...")
    ch0.setOnVelocityUpdateHandler(onVelocityUpdateHandler)
    ch1.setOnVelocityUpdateHandler(onVelocityUpdateHandler)
  
    try:
        ch0.openWaitForAttachment(5000)
        ch1.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, ch)
        raise EndProgramSignal("Program Terminated: Open Failed")

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
    
  #this is now two_mag_push branch
        

    rospy.init_node('python_sub', anonymous=True)
    python_sub = Python_suber(ch0,ch1)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    ch0.setOnVelocityUpdateHandler(None)  
    ch1.setOnVelocityUpdateHandler(None)  

    print("Cleaning up...")
    ch0.close()
    ch1.close()
    print("\nExiting...")   


#if __name__ == '__main__':

listener()
