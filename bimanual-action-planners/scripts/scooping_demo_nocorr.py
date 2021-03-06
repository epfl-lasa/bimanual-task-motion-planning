#! /usr/bin/env python

# Script for testing PLN2CTRL client 
import roslib; roslib.load_manifest('bimanual_action_planners')
import sys
import rospy
import numpy
import actionlib

# Import the messages
import bimanual_action_planners.msg
import tf
import geometry_msgs.msg
from kuka_fri_bridge.msg    import JointStateImpedance

 
def query_init_attractors():
	# Phase 0 ==== Initial Reach ===

	# Phase 0 Right Arm Attractor in Task RF >> Right Arm reaches directly in the good pose
	rA_p0_attr = geometry_msgs.msg.Transform()
	rA_p0_attr.translation.x = -0.060 
	rA_p0_attr.translation.y = -0.113 
	rA_p0_attr.translation.z =  0.247
	rA_p0_attr.rotation.x    =  0.275 
	rA_p0_attr.rotation.y    = -0.123 
	rA_p0_attr.rotation.z    =  0.264
	rA_p0_attr.rotation.w    =  0.916


	# Phase 0 Left Arm Attractor in Task RF
	lA_p0_attr = geometry_msgs.msg.Transform()
	lA_p0_attr.translation.x = -0.040 
	lA_p0_attr.translation.y = -0.382 
	lA_p0_attr.translation.z =  0.494
	lA_p0_attr.rotation.x    =  0.639 
	lA_p0_attr.rotation.y    = -0.468 
	lA_p0_attr.rotation.z    = -0.435
	lA_p0_attr.rotation.w    = -0.429


	return rA_p0_attr, lA_p0_attr

def query_scooping_attractors():
	# Compute Attractors for Reach to Peel/Peel Action
	# -> Read Master Robot Position and Compute Fixed Attractors				

	# Phase 1 ==== Reach to Scoop ===
	lA_p1_attr = geometry_msgs.msg.Transform()
	lA_p1_attr.translation.x = -0.0899
	lA_p1_attr.translation.y = -0.2583
	lA_p1_attr.translation.z =  0.4334
#	lA_p1_attr.rotation.x    =  0.113
#	lA_p1_attr.rotation.y    =  0.919
#	lA_p1_attr.rotation.z    =  0.376
#	lA_p1_attr.rotation.w    = -0.036
	lA_p1_attr.rotation.x    =  0.4691
	lA_p1_attr.rotation.y    =  0.4511
	lA_p1_attr.rotation.z    =  0.5763
	lA_p1_attr.rotation.w    =  0.4943

	# Phase 2 ==== Scoop ===
	lA_p2_attr = geometry_msgs.msg.Transform()
	lA_p2_attr.translation.x = -0.1133
	lA_p2_attr.translation.y = -0.2671
	lA_p2_attr.translation.z =  0.3881
	lA_p2_attr.rotation.x    =  0.0180
	lA_p2_attr.rotation.y    = -0.2310
	lA_p2_attr.rotation.z    =  0.7431
	lA_p2_attr.rotation.w    =  0.6278

	return lA_p1_attr,lA_p2_attr


def query_depart_attractors():
	# Compute Attractors for Reach to Peel/Peel Action
	# -> Read Master Robot Position and Compute Fixed Attractors				

	# Phase 3 ==== Depart and reach on top of the bowl ===
	rA_p3_attr = geometry_msgs.msg.Transform()
	rA_p3_attr.translation.x = -0.216
	rA_p3_attr.translation.y =  0.065
	rA_p3_attr.translation.z =  0.211
	rA_p3_attr.rotation.x    =  0.370
	rA_p3_attr.rotation.y    = -0.021
	rA_p3_attr.rotation.z    =  0.147 
	rA_p3_attr.rotation.w    =  0.917

	lA_p3_attr = geometry_msgs.msg.Transform()
	lA_p3_attr.translation.x = -0.027
	lA_p3_attr.translation.y = -0.225
	lA_p3_attr.translation.z =  0.347
	lA_p3_attr.rotation.x    = -0.317
	lA_p3_attr.rotation.y    =  0.740
	lA_p3_attr.rotation.z    =  0.520
	lA_p3_attr.rotation.w    =  0.283

	return rA_p3_attr,lA_p3_attr	


def query_trash_attractors():
        # Phase 4 ==== Trash ===

	# Phase 4 Right Arm Attractor in Task RF
	rA_p4_attr = geometry_msgs.msg.Transform()
	rA_p4_attr.translation.x = -0.220
	rA_p4_attr.translation.y =  0.290
	rA_p4_attr.translation.z =  0.201
	rA_p4_attr.rotation.x    =  0.378
	rA_p4_attr.rotation.y    = -0.067
	rA_p4_attr.rotation.z    =  0.107
	rA_p4_attr.rotation.w    =  0.917
 
	lA_p4_attr = geometry_msgs.msg.Transform()
	lA_p4_attr.translation.x = -0.067
	lA_p4_attr.translation.y = -0.250
	lA_p4_attr.translation.z =  0.211
	lA_p4_attr.rotation.x    = -0.692
	lA_p4_attr.rotation.y    =  0.397
	lA_p4_attr.rotation.z    =  0.309
	lA_p4_attr.rotation.w    =  0.517
	
	return rA_p4_attr, lA_p4_attr

def query_retract_attractors():
        # Phase 5 ==== Retract ===

	# Phase 5 Right Arm Attractor in Task RF
	rA_p5_attr = geometry_msgs.msg.Transform()
	rA_p5_attr.translation.x = -0.213
	rA_p5_attr.translation.y =  0.458
	rA_p5_attr.translation.z =  0.184

	rA_p5_attr.rotation.x    =  0.384
	rA_p5_attr.rotation.y    = -0.129
	rA_p5_attr.rotation.z    =  0.119
	rA_p5_attr.rotation.w    =  0.906
  
	lA_p5_attr = geometry_msgs.msg.Transform()
	lA_p5_attr.translation.x = -0.211
	lA_p5_attr.translation.y = -0.655
	lA_p5_attr.translation.z =  0.329

	lA_p5_attr.rotation.x    = -0.372
	lA_p5_attr.rotation.y    =  0.791
	lA_p5_attr.rotation.z    =  0.484
	lA_p5_attr.rotation.w    =  0.020

	return rA_p5_attr, lA_p5_attr

def send_goal(action_type, phase, task_frame, right_attractor_frame, left_attractor_frame, timeout):
    print "Phase:", phase
    print "Task Frame: ", task_frame
    print "Right Attractor Frame:", right_attractor_frame
    print "Left Attractor Frame:", left_attractor_frame
    print "Timeout: ", timeout
   
    #Waits until the action server has started up and started listening for goals.
    print "waiting for server"
    client.wait_for_server()
    
    #-----------------------------------------------#
    #----- Set of Goals for the Motion Planner -----#
    #-----------------------------------------------#    
    goal = bimanual_action_planners.msg.PLAN2CTRLGoal(action_type= action_type, action_name = phase, task_frame = task_frame, right_attractor_frame = right_attractor_frame, left_attractor_frame = left_attractor_frame, timeout = timeout)
        
    # Sends the goal to the action server.
    print "sending goal", goal
    client.send_goal(goal)
    
    # Waits for the server to finish performing the action.
    print "waiting for result"
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()

def execute_scooping_planner():
	
	#Task Frame in world
	task_frame = geometry_msgs.msg.Transform()
	task_frame.translation.x = -0.403
	task_frame.translation.y = -0.426
	task_frame.translation.z = 0.013
	task_frame.rotation.x = 0
	task_frame.rotation.y = 0
	task_frame.rotation.z = 0
	task_frame.rotation.w = 1

	# print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
	# raw_input('Press Enter to Run Bimanual REACH with Coordinated Reaching DS')
	# print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="

	rA_p0_attr, lA_p0_attr = query_init_attractors()

	# Reach with Coordinated DS
	# action_type = 'BIMANUAL_REACH'  
	# result = send_goal(action_type, 'phase0', task_frame, rA_p0_attr, lA_p0_attr, 10)
	# print "Result:"		
	# print result.success
	

	while True:

		print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = ="
		raw_input('Press Enter to Run Reach-To-Scoop with Coupled CDS')
		print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = ="

		lA_p1_attr,lA_p2_attr = query_scooping_attractors()

		# Reach To Scoop with Coupled CDS
		action_type = 'COUPLED_LEARNED_MODEL'  
		result = send_goal(action_type, 'phase1', task_frame, rA_p0_attr, lA_p1_attr, 10)
		print "Result:"		
		print result.success

		print "\n\n= = = = = = = = = = = = = = = = = = ="
		raw_input('Press Enter To Scoop with Coupled CDS')
		print "\n\n= = = = = = = = = = = = = = = = = = ="

		# Scooping with Coupled CDS
		action_type = 'COUPLED_LEARNED_MODEL'  
		result = send_goal(action_type, 'phase2', task_frame, rA_p0_attr, lA_p2_attr, 10)
		print "Result:"		
		print result.success

		print "\n\n= = = = = = = = = = = = = = = = = = ="
		raw_input('Press Enter To Depart with Coupled CDS')
		print "\n\n= = = = = = = = = = = = = = = = = = ="

		# Departing with Coupled CDS - to prepare for the trashing action
		action_type = 'COUPLED_LEARNED_MODEL'  
		rA_p3_attr,lA_p3_attr = query_depart_attractors()
		result = send_goal(action_type, 'phase3', task_frame, rA_p3_attr, lA_p3_attr, 10)
		print "Result:"		
		print result.success

		print "\n\n= = = = = = = = = = = = = = = = = = ="
		raw_input('Press Enter To Trash with Coupled CDS')
		print "\n\n= = = = = = = = = = = = = = = = = = ="

		# Trashing with Coupled CDS 
		action_type = 'COUPLED_LEARNED_MODEL'  
		rA_p4_attr,lA_p4_attr = query_trash_attractors()
		result = send_goal(action_type, 'phase4', task_frame, rA_p4_attr, lA_p4_attr, 10)
		print "Result:"		
		print result.success

		scoop_var = raw_input("Do you want to scoop again(any), or end(e)?")

		if scoop_var != 'e':		
			print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
			raw_input('Restarting Scooping Task')
			print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = "
		
		if scoop_var == 'e':
			break

	print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="
	raw_input('Press Enter to Run Bimanual RETRACT with Coordinated Reaching DS')
	print "\n\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ="

	# Retract with Decoupled DS
	rA_p5_attr, lA_p5_attr = query_retract_attractors()
	action_type = 'BIMANUAL_REACH'  
	result = send_goal(action_type, 'phase5',  task_frame, rA_p5_attr, lA_p5_attr, 10)
	print "Result:"
	print result.success


if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('plan2ctrl_client')
        
        # Creates the SimpleActionClient, passing the type of action to the constructor.
        client = actionlib.SimpleActionClient('bimanual_plan2ctrl', bimanual_action_planners.msg.PLAN2CTRLAction)

        #Waits until the action server has started up and started listening for goals.
        print "waiting for server"
        client.wait_for_server()

		#Execute Action Planner for Scooping Task
        execute_scooping_planner()

    except rospy.ROSInterruptException:
        print "program interrupted before completion"
