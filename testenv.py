import psutil
from kivy.app import App
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GraphLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize the plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 1)
        self.line, = self.ax.plot([], [])

        # Initialize the ydata with zeros
        self.ydata = [0] * 10

        # Create and start the animation
        self.ani = FuncAnimation(self.fig, self.update, frames=100, interval=1000)

        # Add the plot to the layout
        self.add_widget(FigureCanvasKivyAgg(self.fig))

    # Function to get network throughput data using psutil
    def get_network_data(self):
        io_counters = psutil.net_io_counters()
        return io_counters.bytes_sent, io_counters.bytes_recv

    # Function to update the plot
    def update(self, frame):
        xdata, ydata = self.line.get_data()
        xdata = list(xdata)
        ydata = list(ydata)
        xdata.append(frame)
        bytes_sent, bytes_recv = self.get_network_data()
        mbps = (bytes_sent + bytes_recv) / 1000000  # Convert bytes to MB
        ydata.append(mbps)
        if xdata[-1] > 10:
            xdata = xdata[-10:]
            ydata = ydata[-10:]
        # Set the y-axis limits based on the maximum throughput observed so far
        max_y = max(ydata)
        self.ax.set_ylim(0, max_y + 0.1)
        self.line.set_data(xdata, ydata)
        return self.line,

class NetworkGraphApp(App):
    def build(self):
        return GraphLayout()

if __name__ == '__main__':
    NetworkGraphApp().run()
