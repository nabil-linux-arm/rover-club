#!/usr/bin/env python
import rospy
import board
import adafruit_bno055
from rover_club.msg import imu_data

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

last_val = 0xFFFF

imu_msg = imu_data()
accel_pose = (3,5,10,50)

# Gets the linear acceleration (m/s) and angular veloctity(r/s)
def getAcceleration():
    #Linear acceleration (without gravity)
    imu_msg.linear.x = sensor.linear_acceleration[0]
    imu_msg.linear.y = sensor.linear_acceleration[1]
    imu_msg.linear.z = sensor.linear_acceleration[2]

    #Angular acceleration (gyroscope)
    imu_msg.angular.x = sensor.gyro[0]
    imu_msg.angular.y = sensor.gyro[1]
    imu_msg.angular.z = sensor.gyro[2]

# Gets the eular and quaternion data from IMU
def getPosition():
    #Eular angles
    imu_msg.position.x = sensor.euler[0]
    imu_msg.position.y = sensor.euler[1]
    imu_msg.position.z = sensor.euler[2]

    #Quaternion
    imu_msg.orientation.x = sensor.quaternion[1]
    imu_msg.orientation.y = sensor.quaternion[2]
    imu_msg.orientation.z = sensor.quaternion[3]
    imu_msg.orientation.w = sensor.quaternion[0]

# Main function which publishes imu data
def imuTransmit():

    pub = rospy.Publisher('pose',imu_data,queue_size=10)
    rospy.init_node('imu_talker',anonymous=True)
    loop_rate = rospy.Rate(5) # 5hz, 5 messages a second

    while not rospy.is_shutdown():
        getAcceleration()

        getPosition()

        # Publishes the message onto the terminal
        rospy.loginfo(f"Temperature = {temperature()}")

        # Publishes the message into the topic
        pub.publish()
        loop_rate.sleep()

# Gets temperature of IMU in C degrees
def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


if __name__ == '__main__':
    try:
        imuTransmit()
    except rospy.ROSInterruptException:
        pass