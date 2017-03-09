from bluetooth import BluetoothSocket, RFCOMM
#from scipy.interpolate import interp1d


addr = '20:15:12:04:20:74'
port = 1


class Allbot:
    JOINTS = {
        'lff': 4,
        'rff': 5,
        'lbf': 6,
        'rbf': 7,
        'lfl': 0,
        'rfl': 1,
        'lbl': 2,
        'rbl': 3
    }
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

    min_joint_input = -1
    max_joint_input = 1
    min_joint_output = 0
    max_joint_output = 90

    # joint_angle_translate_fn = interp1d(
    #     [max_joint_input, max_joint_input],
    #     [min_joint_output, max_joint_output]
    # )

    def __init__(self):
        self.port = 1
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((addr, port))
        self.sock.settimeout(1.0)
        print('Bluetooth Connected')

        self.subs = {}

        self.joint_positions = {}
        for key in Allbot.JOINTS.keys():
            self.joint_positions[key] = 0

        # self.init_robot_subscriptions()


    def send_command(self, data):
        # print cmd.deserialize()
        # print dir(cmd)
        # print type(data.data)

        cmd = self.get_command_from_joint_angles()
        self.sock.send(cmd)

    # def command_robot(self, cmd_data, input_min=-1, input_max=1):
    #     #m = interp1d([input_min, input_max], [0, 90])
    #     cmd = ''
    #
    #     # for key in cmd_data.iterkeys():
    #     #     value = cmd_data[key]
    #     #     if value < -1:
    #     #         cmd_data[key] = -1
    #     #     elif value > 1:
    #     #         cmd_data[key] = 1
    #     #
    #     #     cmd_data[key] = int(m(cmd_data[key]))
    #
    #     #print(cmd_data)
    #
    #     # for key, value in sorted(Allbot.JOINTS.iteritems(), key=lambda (k, v): (v, k)):
    #     #     cmd += str(self.format_angle_for_cmd(cmd_data[key]))
    #
    #     s = [(key, Allbot.JOINTS[key]) for key in sorted(Allbot.JOINTS,
    #             key=Allbot.JOINTS.get)]
    #     for key, value in s:
    #         cmd += str(self.format_angle_for_cmd(cmd_data[key]))
    #         if value == 7:
    #             cmd += ';'
    #         else:
    #             cmd += ','
    #
    #     print (cmd)
    #     self.sock.send(cmd)

    def command_robot(self, cmd_data):

        cmd = ''
        for key, value in sorted(cmd_data.items()):
            cmd += str(cmd_data[key])
            if key == '7':
                cmd += ';'
            else:
                cmd += ','

        print (cmd)
        self.sock.send(cmd)

    def reverse(self,k,v):
        return (v,k)
    def shutdown(self):
        self.sock.close()

    def get_command_from_joint_angles(self):
        cmd = ''

        s = [(key, Allbot.JOINTS[key]) for key in sorted(Allbot.JOINTS,
                key=Allbot.JOINTS.get)]
        for key, value in s:
            cmd += self.format_angle_for_cmd(self.joint_positions[key])

        print (cmd)

        return cmd


    @staticmethod
    def format_angle_for_cmd(x):
        return '%03d' % x


if __name__ == '__main__':
    a = Allbot()
