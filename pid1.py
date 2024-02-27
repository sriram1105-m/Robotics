#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


e_i = 0
e_prev = 0
last_right_sensor_reading = 0.5
current_dist = 0.58
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)  # creates publisher class

# function to control velocity of robot
def forwards(speed, turn):
	global pub
	vel_x = Twist() # initiates twist message
	vel_x.linear.x = speed  # sets linear speed of robot
	vel_x.angular.z = turn  # sets angle to turn to pid function output (turns left?)
	pub.publish(vel_x) #publishes velocity

class PID:
	def __init__(self, kp, ki,kd):
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.curr_err = 0
		self.prev_err = 0
		self.sum_err = 0
		self.prev_err_deriv = 0
		self.curr_err_deriv = 0
		self.control = 0
		self.dt = dt

	def update_control(self, current_error, reset_prev = False)
		self.prev_err = self.curr_err
		self.curr_err = current_error
		#Calculating the Integral error
		self.sum_err = self.sum_err + self.curr_err*self.dt
		#Calculating derivative error
		self.curr_err_deriv = (self.curr_err - self.prev_err) / self.dt
		#Calculating PID control
		self.control = self.kp * self.curr_err + self.ki * self.sum_error + self.kd * self.curr_err_deriv

class Wall_follower:
	def __init__(self):
		rospy.init_node('wall_follower', anonymous = True)
		self.forward_speed = rospy.get_param(base_speed)
		self.dist_from_wall = rospy.get_param(distance_from_wall)

		#creating cmd_pub publisher that will publist Twist msg to cmd_vel
		self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 50)
		self.msg = Twist()
		self.msg.linear.x = self.forward_speed
		self.cmd_pub.publish(self, self.msg)

		#creating a subscriber that will call laser_scan_callback every Laserscan
		self.laser_sub = rospy.Subscriber("/rosbot/laser/scan", LaserScan, self.laser_scan_callback)

	def laser_scan_callback(self, msg):
		for i in range(len(msg.ranges)):
			if msg.ranges[i] < distance_from_wall:
				distance_from_wall = msg.ranges[i] 

		cmd = Twist()
		cmd.linear.x = self.forward_speed
		self.cmd_pub.publish(cmd)


def callback(msg):
	global last_right_sensor_reading
	right_values = msg.ranges[540] # GET THE RANGES VALUE YOU WANT
	# important info about the laser readings 
	# 	540 element is reading to the right 
	# 	630 element is reading to the front right 
	#	450 element is reading to the back right
	last_right_sensor_reading = right_values # THE VALUE YOU ASSIGN HERE SHOULD BE A SINGLE VALUE
	
def controller():
	global last_right_sensor_reading
	rate = rospy.Rate(10)  # sleep in loop at rate 25hz
	base_speed = 0.3 # YOU CAN CHANGE THE BASE SPEED IF YOU WANT
	while not rospy.is_shutdown():
		pid_value = pid(last_right_sensor_reading)
		forwards(base_speed, pid_value)
		rate.sleep()  # pauses rate
		
if __name__ == '__main__':
    try:
        rospy.init_node('script', anonymous=True)
        sub = rospy.Subscriber('/scan', LaserScan, callback)
        controller()
    except rospy.ROSInterruptException:
		pass











