#! /usr/bin/env python

import rospy
import time
import tf, math
import geometry_msgs.msg

if __name__ == '__main__':
	rospy.init_node('tf_listener_turtle')
	listener = tf.TransformListener()

	follower = 'turtlebot3_burger_fol'
	followed = 'turtlebot3_burger_esc'

	turtle_vel = rospy.Publisher('/fol/cmd_vel', geometry_msgs.msg.Twist, queue_size = 1)

	rate = rospy.Rate(10.0)
	ctrl_c = False

	follower_frame = '/'+follower
	followed_frame = '/'+followed

	def shutdownhook():
		global ctrl_c
		print "shut down"
		cmd = geometry_msgs.msg.Twist()
		cmd.linear.x = 0
		cmd.angular.z = 0
		turtle_vel.publish(cmd)
		ctrl_c = True

	while not ctrl_c:
		try:
			(tran,rot) = listener.lookupTransform(follower_frame,followed_frame, rospy.Time(0))
		except:
			continue

		angular = 4 * math.atan2(tran[1],tran[0])
		linear = 0.5 * math.sqrt(tran[0]**2 + tran[1]**2)
		cmd = geometry_msgs.msg.Twist()
		cmd.linear.x = linear
		cmd.angular.z = angular
		turtle_vel.publish(cmd)
		rate.sleep()