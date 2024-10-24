import numpy as np

import matplotlib.pyplot as plt

# Parameters
carrier_freq = 10e3  # Carrier frequency in Hz
modulating_freq = 1e3  # Modulating frequency in Hz
freq_deviation = 500  # Frequency deviation in Hz
sampling_rate = 100e3  # Sampling rate in Hz
duration = 1e-1  # Duration in seconds

# Time array
t = np.arange(0, duration, 1/sampling_rate)

# Modulating signal (1 kHz sine wave)
modulating_signal = np.sin(2 * np.pi * modulating_freq * t)

# Instantaneous frequency
instantaneous_freq = carrier_freq + freq_deviation * modulating_signal

# FM signal
fm_signal = np.cos(2 * np.pi * np.cumsum(instantaneous_freq) / sampling_rate)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t, fm_signal)
plt.title('FM Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()