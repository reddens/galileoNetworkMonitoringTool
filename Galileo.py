from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import psutil
import pandas as pd
import matplotlib.pyplot as plt


class NetworkGraphWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set up a figure and axis for the graph
        self.fig, self.ax = plt.subplots(figsize=(20, 20))
        self.ax.set_title('Network Usage')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Bytes')

        # Initialize variables for tracking time and network usage
        self.time = [0]
        self.bytes_sent_history = [0]
        self.bytes_recv_history = [0]
        self.upload_speed_history = [0]
        self.download_speed_history = [0]

        # Add the figure and labels to the widget
        self.cols = 1
        graph_widget = FigureCanvasKivyAgg(self.fig)
        graph_widget.size_hint = (15, 15)  # set the size_hint of the graph
        self.add_widget(graph_widget)
        self.interface_label = Label(text='Interface: ')
        self.ip_address_label = Label(text='IP Address: ')
        self.upload_speed_label = Label(text='Upload Speed: ')
        self.download_speed_label = Label(text='Download Speed: ')
        self.bytes_sent_label = Label(text='Bytes Sent: ')
        self.bytes_recv_label = Label(text='Bytes Received: ')
        self.add_widget(self.interface_label)
        self.add_widget(self.ip_address_label)
        self.add_widget(self.upload_speed_label)
        self.add_widget(self.download_speed_label)
        self.add_widget(self.bytes_sent_label)
        self.add_widget(self.bytes_recv_label)
        

    # Add start and stop buttons
        self.start_button = Button(text='Start', disabled=True)
        self.start_button.bind(on_press=self.start_update_graph)
        self.add_widget(self.start_button)
        self.stop_button = Button(text='Stop')
        self.stop_button.bind(on_press=self.stop_update_graph)
        self.add_widget(self.stop_button)

        # Start the update loop
        self.update_graph()

    # Define a function to start the update loop
    def start_update_graph(self, button):
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.update_graph()
        

    # Define a function to get the network usage
    def get_network_usage(self):
        net_io_counters = psutil.net_io_counters()
        bytes_sent = net_io_counters.bytes_sent
        bytes_recv = net_io_counters.bytes_recv
        interface = list(psutil.net_io_counters(pernic=True).keys())[0]
        ip_address = psutil.net_if_addrs()[interface][0].address
        return interface, ip_address, bytes_sent, bytes_recv

    # Define a function to update the network graph and labels
    def update_graph(self, dt=0.4):
        interface, ip_address, bytes_sent, bytes_recv = self.get_network_usage()
        prev_bytes_sent = self.bytes_sent_history[-1]
        prev_bytes_recv = self.bytes_recv_history[-1]
        prev_upload_speed = self.upload_speed_history[-1]
        prev_download_speed = self.download_speed_history[-1]
        upload_speed = (bytes_sent - prev_bytes_sent) / dt
        download_speed = (bytes_recv - prev_bytes_recv) / dt
        self.time.append(self.time[-1] + dt)
        self.bytes_sent_history.append(bytes_sent)
        self.bytes_recv_history.append(bytes_recv)
        self.upload_speed_history.append(upload_speed)
        self.download_speed_history.append(download_speed)
        data = pd.DataFrame(
        {
            'Time': self.time[-300:],
            'Upload': self.upload_speed_history[-300:],
            'Download': self.download_speed_history[-300:],
        }
        )
        self.ax.clear()
        self.ax.set_xlim(self.time[-1]-30, self.time[-1])
        self.ax.plot(data['Time'].values, data['Upload'].values, label='Upload')
        self.ax.plot(data['Time'].values, data['Download'].values, label='Download')
        self.ax.legend()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()



        # Update the labels with the network parameters
        self.interface_label.text = f'Interface: {interface}'
        self.ip_address_label.text = f'IP Address: {ip_address}'
        self.upload_speed_label.text = f'Upload Speed: {upload_speed/1024:.2f} KB/s'
        self.download_speed_label.text = f'Download Speed: {download_speed/1024:.2f} KB/s'
        self.bytes_sent_label.text = f'Bytes Sent: {bytes_sent//1024} KB'
        self.bytes_recv_label.text = f'Bytes Recieved: {bytes_recv//1024} KB'


        # Schedule the next update
        self._trigger_update_graph()

    def _trigger_update_graph(self):
        self.update_event = Clock.schedule_once(self.update_graph, 1)

    def stop_update_graph(self, button):
        self.start_button.disabled = False
        self.stop_button.disabled = True
        Clock.unschedule(self.update_event)

class GalileoNetworkMonitoringToolApp(App):
    def build(self):
        return NetworkGraphWidget()

if __name__ == '__main__':
    GalileoNetworkMonitoringToolApp().run()