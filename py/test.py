import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.callback)
        self.count = 0

    def callback(self):
        cmd_msg = Twist()

        if self.count == 0 or self.count == 2:
            # 直行3秒
            cmd_msg.linear.x = 0.2
        else:
            # 左转2秒
            cmd_msg.angular.z = 0.2

        self.pub.publish(cmd_msg)

        self.count += 1
        if self.count > 3:
            self.count = 0

def main(args=None):
    rclpy.init(args=args)

    robot_controller = RobotController()

    rclpy.spin(robot_controller)

    robot_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
