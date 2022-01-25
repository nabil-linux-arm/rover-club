#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Vector3
#from std_msgs.msg import String

#(1) create a message?

def imuTransmit():
    accel_pose = (3,5,10)
    acceleration_msg = Vector3()
    pub = rospy.Publisher('pose',Vector3,queue_size=10)
    rospy.init_node('imu_talker',anonymous=True)
    loop_rate = rospy.Rate(1) # 5hz, 5 messages a second

    while not rospy.is_shutdown():
        acceleration_msg.x = accel_pose[0]
        acceleration_msg.y = accel_pose[1]
        acceleration_msg.z = accel_pose[2]

        #acceleration_msg = accel_pose -> Doesnt work

        # Publishes the message onto the terminal
        rospy.loginfo(acceleration_msg)
        # Publishes the message into the topic
        pub.publish(acceleration_msg)
        loop_rate.sleep()


if __name__ == '__main__':
    try:
        imuTransmit()
    except rospy.ROSInterruptException:
        pass