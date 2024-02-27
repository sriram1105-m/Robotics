#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

twist = Twist()

def callback(msg):
	regions = { 'right': min(min(msg.ranges[0:143]), 10),
		    'fright': min(min(msg.ranges[144:287]), 10),
 	            'front': min(min(msg.ranges[288:431]), 10),
	            'fleft': min(min(msg.ranges[432:575]), 10),
	            'left' : min(min(msg.ranges[576:713]), 10)}

	rule_base(regions)

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


def rule_base(regions):
	msg = Twist()
	linear_x = 0
	angular_z = 0

	if regions['front'] > 1 and regions['fleft'] >1 and regions['fright'] > 1:
		linear_x = 0.6
		angular_z = 0
	
	elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
		linear_x = 0
		angular_z = 0.3

	elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
		linear_x = 0
		angular_z = 0.3

	elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
		linear_x = 0
		angular_z = -0.3

	elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
		linear_x = 0
		angular_z = 0.3

	elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
		linear_x = 0
		angular_z = -0.3

	elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
		linear_x = 0
		angular_z = 0.3

	elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
		linear_x = 0.3
		angular_z = 0

	else:
		rospy.loginfo(regions)
		msg.linear.x  = linear_x
		msg.angular.z = -angular_z
		pub.publish(msg)

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

def main():
	global pub
	rospy.init_node('read_laser')
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
	rospy.Subscriber('obstacle_avoidance/laser/scan', LaserScan, callback_laser)
	rospy.spin()

if __name__ == '__main__':
	main()

