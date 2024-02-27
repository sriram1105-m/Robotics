#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

twist = Twist()

regions = { 'right': min(min(msg.ranges[0:143]), 10),
            'fright': min(min(msg.ranges[144:287]), 10),
            'front': min(min(msg.ranges[288:431]), 10),
            'fleft': min(min(msg.ranges[432:575]), 10),
            'left' : min(min(msg.ranges[576:713]), 10)
           }

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

def centroid(func, step = 0.1):
	points = func.points(step)
	num, den = 0, 0
	for x, y in points:
		num += x * y
		den += y
	return num / den

def rule_base_REF():

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


def rule_base_OA(regions):
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

if min('right', 'fright') < 0.6:
	rule_base_REF
else:
	rule_base_OA

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
	rospy.Subscriber('obstacle_avoidance/laser/scan', LaserScan, callback_laser)
        controller()
    except rospy.ROSInterruptException:
		pass
