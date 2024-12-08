import numpy as np
import matplotlib.pyplot as plt

# Parameters
fc = 10e3  # Carrier frequency in Hz
fs = 100e3  # Sampling frequency in Hz
t = np.arange(0, 3e-3, 1/fs)  # Time vector for 3 ms

# Message signal (example: a 1 kHz sine wave)
fm = 1e3  # Message frequency in Hz
message = np.sin(2 * np.pi * fm * t)  # 100 mV peak-to-peak

# Carrier signal
carrier = np.sin(2 * np.pi * fc * t)

# DSB-SC signal
dsb = message * carrier

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(t, message)
plt.title('Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(3, 1, 2)
plt.plot(t, carrier)
plt.title('Carrier Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(3, 1, 3)
plt.plot(t, dsb, label='DSB-SC Signal')
plt.plot(t, message, label='Message Signal', linestyle='--')
plt.title('DSB-SC Signal with Message Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()
