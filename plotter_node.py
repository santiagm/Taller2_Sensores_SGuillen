# plotter_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import re
import time
import matplotlib
matplotlib.use('Agg')  # backend no interactivo
import matplotlib.pyplot as plt
from collections import deque

class PlotterNode(Node):
    def __init__(self):
        super().__init__('plotter_node')
        self.data = deque(maxlen=300)   # ~5 min si llega 1 Hz
        self.times = deque(maxlen=300)
        self.start = time.time()
        self.create_subscription(String, 'sensor_data', self.cb, 10)
        # temporizador cada 5 s
        self.timer = self.create_timer(5.0, self.save_plot)
        self.out_path = '/root/ros2_ws/data/sensor_plot.png'

    def cb(self, msg):
        # Extrae número de "Temperatura: XX C"
        m = re.search(r'(-?\d+(\.\d+)?)', msg.data)
        if m:
            t = float(m.group(1))
            self.data.append(t)
            self.times.append(time.time() - self.start)
            self.get_logger().info(f'Plotter recibió: {t} C')

    def save_plot(self):
        if not self.data:
            return
        plt.figure(figsize=(8,4))
        plt.plot(list(self.times), list(self.data))
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (C)')
        plt.title('Temperatura vs Tiempo')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(self.out_path)
        plt.close()
        self.get_logger().info(f'Gráfico guardado en {self.out_path}')

def main(args=None):
    rclpy.init(args=args)
    node = PlotterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

