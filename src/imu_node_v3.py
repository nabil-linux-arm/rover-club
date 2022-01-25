#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Accel
from rover_club.msg import imu_data

# Accel message has linear and angular components

def imuTransmit():
    accel_pose = (3,5,10)

    acceleration_msg = Accel()
    imu_msg = imu_data()

    pub = rospy.Publisher('pose',Accel,queue_size=10)
    rospy.init_node('imu_talker',anonymous=True)
    loop_rate = rospy.Rate(1) # 5hz, 5 messages a second

    while not rospy.is_shutdown():
        acceleration_msg.linear.x = accel_pose[0]
        acceleration_msg.linear.y = accel_pose[1]
        acceleration_msg.linear.z = accel_pose[2]

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