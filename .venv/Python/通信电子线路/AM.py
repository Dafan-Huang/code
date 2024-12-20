import numpy as np
import matplotlib.pyplot as plt

# Parameters
carrier_freq = 10e3  # Carrier frequency in Hz (10 kHz) (载波频率)
modulation_freq = 1e3  # Modulation frequency in Hz (1 kHz) (调制频率)
amplitude = 1  # Amplitude in Volts (1 V) (幅度)
modulation_index = 1  # Modulation index (x%) (调制指数)
sampling_rate = 1e6  # Sampling rate in Hz (1 MHz) (采样率)
duration = 0.275 * 1e-2  # Duration in seconds (持续时间 0.2s)

# Time array
t = np.arange(0, duration, 1/sampling_rate)

# Carrier signal
carrier = amplitude * np.sin(2 * np.pi * carrier_freq * t)

# Modulation signal
modulation = modulation_index * np.sin(2 * np.pi * modulation_freq * t)

# Modulated signal (Amplitude Modulation)
modulated_signal = (1 + modulation) * carrier

# Plotting the signals
plt.figure(figsize=(10, 8))

# Plot carrier signal
plt.subplot(3, 1, 1)
plt.plot(t, carrier)
plt.title('Carrier Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# Plot modulation signal
plt.subplot(3, 1, 2)
plt.plot(t, modulation)
plt.title('Modulation Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# Plot modulated signal
plt.subplot(3, 1, 3)
plt.plot(t, modulated_signal)
plt.title('Modulated Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

# Plot modulation and modulated signals together
plt.figure(figsize=(10, 4))
plt.plot(t, modulation, label='Modulation Signal')
plt.plot(t, modulated_signal, label='Modulated Signal')
plt.title('Modulation and Modulated Signals')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.tight_layout()
plt.show()

# Fourier Transform of the modulated signal
modulated_signal_fft = np.fft.fft(modulated_signal)
frequencies = np.fft.fftfreq(len(modulated_signal), 1/sampling_rate)

# Plot the Fourier Transform
plt.figure(figsize=(10, 4))
plt.plot(frequencies, np.abs(modulated_signal_fft))
plt.title('Fourier Transform of Modulated Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.xlim(0, 2*carrier_freq)  # Limit x-axis to twice the carrier frequency for better visualization
plt.tight_layout()
plt.show()
