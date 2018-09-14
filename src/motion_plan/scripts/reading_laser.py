#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None

def take_action(regions):
	msg = Twist()
	linear_x = 0
	angular_z = 0

	state_description = ''

	if regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] > 1:
		state_description = 'case 1 - nothing'
		linear_x = 0.6
		angular_z = 0
	elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
		state_description = 'case 2 - front'
		linear_x = 0
		angular_z = 0.3
	elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
		state_description = 'case 3 - fright'
		linear_x = 0
		angular_z = 0.3
	elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
		state_description = 'case 4 - fleft'
		linear_x = 0
		angular_z = -0.3
	elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
		state_description = 'case 5 - front and fright'
		linear_x = 0
		angular_z = 0.3
	elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
		state_description = 'case 6 - front and fleft'
		linear_x = 0
		angular_z = -0.3
	elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
		state_description = 'case 7 - front and fleft and fright'
		linear_x = 0
		angular_z = 0.3
	elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
		state_description = 'case 8 - fleft and fright'
		linear_x = 0.3
		angular_z = 0
	else:
		state_description = 'unknown case'
		rospy.loginfo(regions)

	rospy.loginfo(state_description)
	msg.linear.x = linear_x
	msg.angular.z = angular_z
	pub.publish(msg)


def clbk_laser(msg):
	maxV = msg.range_max
	inc = 36
	regions = {
		'right':min(min(msg.ranges[int(inc/-2)-inc*3:int(inc/-2)-inc*2]),maxV),
		'fright':min(min(msg.ranges[int(inc/-2)-inc:int(inc/-2)]),maxV),
		'front':min(min(msg.ranges[int(inc/-2):]+ msg.ranges[:int(inc/2)]),maxV),
		'fleft':min(min(msg.ranges[int(inc/2)+inc:int(inc/2)+inc*2]),maxV),
		'left':min(min(msg.ranges[int(inc/2)+inc*2:int(inc/2)+inc*3]),maxV)
	}
	take_action(regions)

def main():
	global pub
	rospy.init_node('reading_laser')
	sub = rospy.Subscriber("/bot/scan",LaserScan, clbk_laser)
	pub = rospy.Publisher('/bot/cmd_vel', Twist, queue_size=1)

	rospy.spin()


#if __name__=='__main__':
main()