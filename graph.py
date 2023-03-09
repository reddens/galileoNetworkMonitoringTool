import psutil
import pandas as pd
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class NetworkThroughputGraph(App):

    def build(self):
        # Create a box layout to hold the graph and labels
        layout = BoxLayout(orientation='vertical')

        # Create a figure and axis for the graph
        fig, ax = plt.subplots()
        ax.set_title('Network Throughput')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Throughput (kB/s)')

        # Initialize variables for tracking time and network usage
        self.time = [0]
        self.throughput_history = [0]

        # Add the figure to the layout
        graph_widget = FigureCanvasKivyAgg(fig)
        layout.add_widget(graph_widget)

        # Start the update loop
        Clock.schedule_interval(lambda dt: self.update_graph(ax), 1)

        return layout

    def get_network_throughput(self):
        # Get the network usage statistics
        net_io_counters = psutil.net_io_counters()
        bytes_sent = net_io_counters.bytes_sent
        bytes_recv = net_io_counters.bytes_recv

        # Calculate the throughput (kB/s)
        throughput = (bytes_sent + bytes_recv - sum(self.throughput_history[-2:])) / 1024

        return throughput

    def update_graph(self, ax):
        # Get the current time and network throughput
        current_time = self.time[-1] + 1
        throughput = self.get_network_throughput()

        # Update the graph data
        self.time.append(current_time)
        self.throughput_history.append(throughput)
        data = pd.DataFrame({'Time': self.time, 'Throughput': self.throughput_history})
        ax.clear()
        ax.plot(data['Time'], data['Throughput'])
        ax.set_xlim(min(self.time), max(self.time))
        ax.set_ylim(min(self.throughput_history), max(self.throughput_history))
        ax.set_title('Network Throughput')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Throughput (kB/s)')

if __name__ == '__main__':
    NetworkThroughputGraph().run()
