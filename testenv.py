import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 100)
line, = ax.plot([], [])

# Function to get network throughput data using psutil
def get_network_data():
    io_counters = psutil.net_io_counters()
    return io_counters.bytes_sent, io_counters.bytes_recv

# Function to update the plot
def update(frame):
    xdata, ydata = line.get_data()
    xdata = list(xdata)
    ydata = list(ydata)
    xdata.append(frame)
    bytes_sent, bytes_recv = get_network_data()
    ydata.append((bytes_sent + bytes_recv) / 1000000)  # Convert bytes to MB
    if xdata[-1] > 10:
        xdata = xdata[-10:]
        ydata = ydata[-10:]
    line.set_data(xdata, ydata)
    return line,

# Create and start the animation
ani = FuncAnimation(fig, update, frames=100, interval=1000)
plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mbps)')
plt.title('Network Throughput')
plt.show()
