import rospy
import time
from std_msgs.msg import Float64
from std_srvs.srv import Empty


class Robot:
    JOINT_COMMAND_TOPICS = [
        ['lff', '/allbot/leg_lf_foot_joint_position_controller/command'],
        ['rff', '/allbot/leg_rf_foot_joint_position_controller/command'],
        ['lbf', '/allbot/leg_lb_foot_joint_position_controller/command'],
        ['rbf', '/allbot/leg_rb_foot_joint_position_controller/command'],
        ['lfl', '/allbot/leg_lf_leg_joint_position_controller/command'],
        ['rfl', '/allbot/leg_rf_leg_joint_position_controller/command'],
        ['lbl', '/allbot/leg_lb_leg_joint_position_controller/command'],
        ['rbl', '/allbot/leg_rb_leg_joint_position_controller/command']
    ]

    def __init__(self):
        self.pubs = {}
        self.command_queue = []
        self.reset_world = None

        self.init_robot_publications()
        self.init_service_calls()

        # print self.pubs
        # print self.reset_bot

    def init_robot_publications(self):
        for topic in self.JOINT_COMMAND_TOPICS:
            pub = rospy.Publisher(topic[1], Float64, queue_size=10)
            rospy.init_node(topic[1].split("/")[1], anonymous=True)

            self.pubs[topic[0]] = pub

    def init_service_calls(self):
        rospy.wait_for_service('gazebo/reset_world')
        try:
            self.reset_world = rospy.ServiceProxy('gazebo/reset_world', Empty)
        except rospy.ServiceException as e:
            print ("Service call failed: %s" % e)

    def send_command(self, cmd=None):
        if cmd is not None:
            for key in cmd.keys():
                self.pubs[key].publish(cmd[key])

    def queue_command(self, joint_positions=None):
        self.command_queue.append(joint_positions)

    def execute_queue(self, rate=1):
        rate = rospy.Rate(rate)
        while not rospy.is_shutdown():
            if not self.command_queue:
                break

            command = self.command_queue.pop(0)
            self.send_command(command)
            rate.sleep()

    def reset(self):
        self.send_command({
            'lff': 0.0,
            'rff': 0.0,
            'lbf': 0.0,
            'rbf': 0.0,
            'lfl': 0.0,
            'rfl': 0.0,
            'lbl': 0.0,
            'rbl': 0.0
        })

    def reset_bot(self):
        try:
            self.reset_world()
        except rospy.ServiceException as e:
            print ("Service call failed: %s" % e)


if __name__ == '__main__':
    r = Robot()
    r.reset_bot()
    r.reset()
    # for i in range(1):
    #     r.reset()
    #     time.sleep(1)
