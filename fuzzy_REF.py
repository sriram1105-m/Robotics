#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import sys

twist = Twist()

#Inputs
rfs = 630
rbs = 450

#Fuzzy membership function - trapezoidal
def trap_mf(points, xrange):
	values = []
	for x in xrange:
	if x <= points['a']:
		values.append(0)
	elif (x >= points['a'] and x <= points['b']):
		values.append((x - points['a']) / (points['b'] - points['a']))
	elif (x >= points['b'] and x <= points['c']):
		values.append(1)
	elif (x >= points['c'] and x <= points['d']):
		values.append((points['d'] - x) / (points['d'] - point['c']))
	elif (x >= points['d']):
		values.append(0)
	return values
pass

#Rule base function for right wall following robot
def rule_base():
	rfs = 630
	rbs = 450

	if (rfs == near and rbs == near):
		speed = slow
		steering = Left
	
	if (rfs == near and rbs == medium):
		speed = slow
		steering = Left

	if (rfs == near and rbs == far):
		speed = medium
		steering = Left

	if (rfs == medium and rbs == near):
		speed = medium
		steering = right

	if (rfs == medium and rbs == medium):
		speed = 0
		steering = 0

	if (rfs == medium and rbs == far):
		speed = medium
		steering = Left

	if (rfs == far and rbs == near):
		speed = slow
		steering = right

	if (rfs == far and rbs == medium):
		speed = medium
		steering = right

	if (rfs == far and rbs == far):
		speed = fast
		steering = right

#Function to calculate the centroid
def centroid(func, step = 0.1):
	points = func.points(step)
	num, den = 0, 0
	for x, y in points:
		num += x * y
		den += y
	return num / den

def forwards(speed, turn):
	global pub
	vel_x = Twist() 
	vel_x.linear.x = speed  
	vel_x.angular.z = turn 
	pub.publish(vel_x) 

def right(speed, turn):
	twist.linear.y = -1.0
	twist.angular.z = 0.0
	twist.linear.x = 0.0

def left(speed, turn):
	twist.linear.y = 1.0
	twist.angular.z = 0.0
	twist.linear.x = 0.0

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
	right_values = msg.ranges[540] 
	last_right_sensor_reading = right_values 
	
def controller():
	global last_right_sensor_reading
	rate = rospy.Rate(10)  # sleep in loop at rate 25hz
	base_speed = 0.3 
	while not rospy.is_shutdown():
		forwards(base_speed)
		rate.sleep()  # pauses rate
		
if __name__ == '__main__':
    try:
        rospy.init_node('script', anonymous=True)
        sub = rospy.Subscriber('/scan', LaserScan, callback)
        controller()
    except rospy.ROSInterruptException:
		pass
	
	
