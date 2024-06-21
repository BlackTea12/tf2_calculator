import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import tf2_ros

class TfListener(Node):

  def __init__(self):
    super().__init__('tf_listener_node')
    self.publisher_ = self.create_publisher(PoseStamped, 'base_link_pose', 10)
    self.tf_buffer = tf2_ros.Buffer()
    self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
    self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz

  def timer_callback(self):
    try:
      # Lookup transform from 'map' to 'base_link'
      transform = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
      self.get_logger().info('Transform: {}'.format(transform))

      # Create Pose message from transform
      pose_stamped = PoseStamped()
      pose_stamped.header.stamp = transform.header.stamp
      pose_stamped.header.frame_id = transform.header.frame_id
      pose_stamped.pose.position.x = transform.transform.translation.x
      pose_stamped.pose.position.y = transform.transform.translation.y
      pose_stamped.pose.position.z = transform.transform.translation.z
      pose_stamped.pose.orientation = transform.transform.rotation

      # Publish the PoseStamped message
      self.publisher_.publish(pose_stamped)

    except tf2_ros.LookupException as ex:
      self.get_logger().info(f'Could not transform: {ex}')
    except tf2_ros.ExtrapolationException as ex:
      self.get_logger().info(f'Extrapolation exception: {ex}')
    except tf2_ros.ConnectivityException as ex:
      self.get_logger().info(f'Connectivity exception: {ex}')

def main(args=None):
  rclpy.init(args=args)
  node = TfListener()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  node.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()