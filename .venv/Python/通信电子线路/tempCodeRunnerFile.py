import numpy as np
import matplotlib.pyplot as plt

# Parameters
fc = 10e3  # Carrier frequency in Hz
fs = 100e3  # Sampling frequency in Hz
t = np.arange(0, 3e-3, 1/fs)  # Time vector for 3 ms

# Message signal (example: a 1 kHz sine wave)
fm = 1e3  # Message frequency in Hz
message = np.sin(2 * np.pi * fm * t)

# Carrier signal
carrier = np.cos(2 * np.pi * fc * t)

# DSB-SC signal
dsb = message * carrier

# Envelope of the DSB-SC signal
envelope = np.abs(message)

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
plt.plot(t, envelope, 'r--', label='Envelope')
plt.title('DSB-SC Signal with Envelope')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()
# Fourier Transform of the DSB-SC signal
dsb_fft = np.fft.fft(dsb)
frequencies = np.fft.fftfreq(len(dsb), 1/fs)

# Plotting the Fourier Transform
plt.figure(figsize=(10, 6))
plt.plot(frequencies, np.abs(dsb_fft))
plt.title('Fourier Transform of DSB-SC Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.xlim(0, 2*fc)  # Limit x-axis to show relevant frequencies
plt.grid()
plt.show()