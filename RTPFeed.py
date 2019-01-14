import time
import subprocess
import os
import argparse

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

# this will change to be dynamically attained
pixhawk_pipe_isarmed = True

def main(cam_options):

    # 3s delay to ensure ffserver completely starts before this python script gets rolling.
    # The reason for they are both called in background at boot.
    time.sleep(3)

    # initialize stream subprocess handle
    stream_sp = None

    if cam_options.record != None:
        # check if file path directory exists
        if os.path.isdir(cam_options.record) == True:
            print "Recording local copy to: " + cam_options.record
        else :
            # value error is raised, so it we should not proceed further
            raise ValueError("The requested directory is invalid or does not exist")

    while True:
        # check if the flight controller is armed here
        # if it is, then try to start up the see3cam feed
        if pixhawk_pipe_isarmed == True:

            print "Pix hawk is armed. Verifying video device is available ... "
            # verify that video device is available

            if os.path.exists("/dev/video0"):

                print ("/dev/video0 is available. Beginning video stream ... ")
                print ("Stream options loaded from: /home/rpi_rtsp_server/ffserver.conf")

                if cam_options.verbose:
                    ffmpeg_start_command =  ['ffmpeg',\
                                             '-f','v4l2',\
                                             '-input_format','mjpeg',\
                                             '-i','/dev/video0', \
                                             '-preset','ultrafast',\
                                             '-tune','zerolatency',\
                                             'http://localhost:8090/see3cam.ffm']
                else:
                    ffmpeg_start_command =  ['ffmpeg',\
                                             '-loglevel','panic',\
                                             '-f','v4l2',\
                                             '-input_format','mjpeg',\
                                             '-i','/dev/video0',\
                                             '-preset','ultrafast',\
                                             '-tune','zerolatency',\
                                             'http://localhost:8090/see3cam.ffm']


                stream_sp = subprocess.Popen(ffmpeg_start_command)

                while stream_sp.poll() == None:
                    # wait while rpi is streaming
                    time.sleep(1)

                exit(0)
            else:
                print ("/dev/video0 not available. Connect video device, then restart raspberry pi")
                exit(1)
        else :
            time.sleep(1) # sleep for one second, and then try again

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "rpi video stream")
    parser.add_argument("-r","--record", help="Directory to record local copy of stream", metavar ="")
    parser.add_argument("-v","--verbose", help="Verbosely print out state of ffmpeg", action="store_true")
    # To do:
    # -add IP address and port
    # -add feed name as dictated by the ffserver configuration
    # -add

    args = parser.parse_args()
    main(args)



