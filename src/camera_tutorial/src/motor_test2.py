import sys
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

'''
* Configures the device's DataInterval
* Displays info about the attached Phidget channel.  
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
'''
def onAttachHandler(self):
    
    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nAttach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
    
        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between VelocityUpdate events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        print("\tSetting DataInterval to 1000ms")
        try:
            ph.setDataInterval(1000)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting DataInterval: \n\t")
            DisplayError(e)
            return
        
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Displays info about the detached Phidget channel.
* Fired when a Phidget channel with onDetachHandler registered detaches
*
* @param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):

    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nDetach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
        
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

"""
* Outputs the DCMotor's most recently reported velocity.
* Fired when a DCMotor channel with onVelocityUpdateHandler registered meets DataInterval criteria
*
* @param self The DCMotor channel that fired the VelocityUpdate event
* @param velocity The reported velocity from the DCMotor channel
"""
def onVelocityUpdateHandler(self, velocity):

    #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #www.phidgets.com/docs/Using_Multiple_Phidgets for information

    print("[Velocity Event] -> Velocity: " + str(velocity))
    
"""
* Prints descriptions of how events related to this class work
"""
def PrintEventDescriptions():

    print("\n--------------------\n"
        "\n  | Velocity update events will call their associated function every time new velocity data is received from the device.\n"
        "  | The rate of these events can be set by adjusting the DataInterval for the channel.\n"
        "  | Press ENTER once you have read this message.")
    readin = sys.stdin.readline(1)
    
    print("\n--------------------")
            
"""
* Creates, configures, and opens a DCMotor channel.
* Provides interface for controlling TargetVelocity of the DCMotor.
* Closes out DCMotor channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def main():
    try:
        """
        * Allocate a new Phidget Channel object
        """
        try:
            ch = DCMotor()
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
        
        ch.setDeviceSerialNumber(485540)
        #ch.setHubPort(channelInfo.hubPort)
        ch.setIsHubPortDevice(0)
        ch.setChannel(0)   
        
        
        # print("\n--------------------------------------")
        # print("\nSetting OnAttachHandler...")
        # ch.setOnAttachHandler(onAttachHandler)
        
        # print("Setting OnDetachHandler...")
        # ch.setOnDetachHandler(onDetachHandler)
        
        # print("Setting OnErrorHandler...")
        # ch.setOnErrorHandler(onErrorHandler)

        # #This call may be harmlessly removed
        # PrintEventDescriptions()
        
        print("\nSetting OnVelocityUpdateHandler...")
        ch.setOnVelocityUpdateHandler(onVelocityUpdateHandler)
        
        """
        * Open the channel with a timeout
        """
        print("\nOpening and Waiting for Attachment...")
        
        try:
            ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch)
            raise EndProgramSignal("Program Terminated: Open Failed")


        end = False

        while (end != True):

            ch.setTargetVelocity(0.4)

        '''
        * Perform clean up and exit
        '''

        #clear the VelocityUpdate event handler 
        ch.setOnVelocityUpdateHandler(None)  

        print("Cleaning up...")
        ch.close()
        print("\nExiting...")
        return 0

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        #clear the VelocityUpdate event handler 
        ch.setOnVelocityUpdateHandler(None)  
        ch.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        #clear the VelocityUpdate event handler 
        ch.setOnVelocityUpdateHandler(None)  
        ch.close()
        return 1
    finally:
        print("Press ENTER to end program.")
        readin = sys.stdin.readline()

main()
