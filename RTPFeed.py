import time
import subprocess
import os
import argparse

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

class See3CamFeed:

    def __init__(self):
        self.server_sp = None
        self.stream_sp = None


    def start_server(self, ffmpeg_config_path=CUR_DIR + "/ffserver.conf"):

        #default ffserver configuration: CUR_DIR/ffserver.conf
        self.server_sp = subprocess.Popen("ffserver -f " + ffmpeg_config_path, stdin = subprocess.PIPE,
                                          stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    def start_stream(self):

        # For now, this will have to do, but in the future, this will have to change depending on how video cameras are
        # read and presented in the file system i.e. the /dev/video0 may need to be dynamically determined
        self.stream_sp = subprocess.Popen("ffmpeg -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency " +
                                          "http://localhost:8090/see3cam.ffm")

    def close_server(self):
        self.server_sp.terminate()

    def close_stream(self):
        self.sream_sp.terminate()


def main(test_args):
    print "Loading ffserver.conf at: \n" + test_args

    #initialize see3camfeed here, with anything else you might need

    #while True:
        # check if the flight controller is armed here
        # if it is, then start up the see3cam feed
        # if(pixhawk_pipe.isarmed):
            # while True:
                # check that the server and feed are both operational.
                # if they are operational, do nothing
                # else kill any other operatioanl subprocess if any, then exit
                    #break
        # else not armed:
            #time.sleep(1) # sleep for one second, and then try again



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'see3cam stream')
    parser.add_argument('ffserver_fp', help='full path to ffserver configruation')
    # To do:
    # -add IP address and port
    # -add feed name as dictated by the ffserver configuration
    # -add

    args = parser.parse_args()
    main(args.ffserver_fp)



