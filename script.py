import serial
import pygame
from time import sleep

# Set up serial communication with Arduino
ser = serial.Serial('COM4', 9600)

# Initialize pygame mixer
pygame.mixer.init()

def play_sound(file_path):
    sound = pygame.mixer.Sound(file=file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))  # Convert seconds to milliseconds

while True:
    # Read data from serial port
    data = ser.readline().strip().decode('utf-8')
    print(data)
    
    # Check if Arduino sent 'pressed'
    if data == 'pressed':
        # Play the sound file
        play_sound('sound.wav')
        
        # Wait 3 seconds
        sleep(3)
        
        # Play the sound file again
        play_sound('sound.wav')
