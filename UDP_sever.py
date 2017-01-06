import SocketServer
import cv2
import numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rospy


rospy.init_node('image_converter', anonymous=True)
image_pub = rospy.Publisher("/camera/image_raw",Image)
bridge = CvBridge()

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    
    """
    def handle(self):
        data = self.request[1].recv(691200).strip()
        socket = self.request[1]
        nparr = numpy.fromstring(data, numpy.uint8)
	try:
            img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
            if img != None:
                image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
            else:
                print None
            
        except RuntimeError as e:
            print e

if __name__ == "__main__":
    HOST, PORT = "192.168.1.116", 8080
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


