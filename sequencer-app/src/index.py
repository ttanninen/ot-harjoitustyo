import sequencer
import os
from audioengine import AudioEngine
import clock

# Clear terminal screen:
os.system("cls" if os.name == "nt" else "clear")

# Resolve program directory name
dirname = os.path.dirname(__file__)

# Create new track
test_sample = os.path.join(dirname, "samples", "bd01.wav")
track1 = sequencer.Track(test_sample, "BD")

# Create 16-step pattern
track1.set_length(16)

# Write some notes
track1.write_step(0)
track1.write_step(4)
track1.write_step(8)
track1.write_step(12)
track1.write_step(5)
track1.write_step(7)

# Initialize master clock:
clock.start()

# Initialize audioengine:
engine = AudioEngine()
engine.start()

# Create new sequence
sequence = sequencer.Sequence(128, 4, engine)


# Load track 1 to sequence
sequence.add_track(track1)

while True:
    # Print instructions
    current_pattern_str = "Current pattern: " + str(sequence.tracks[0].pattern)
    commands_str = "Test commands:\np play\nh pause\ns stop\ne edit pattern\nx exit"
    print(commands_str)
    print(current_pattern_str)

    command = input("Enter command: ")
    if command == "p":
        sequence.play()
    elif command == "h":
        sequence.pause()
    elif command == "s":
        sequence.stop()
    elif command == "e":
        while True:
            print(current_pattern_str)
            print("w write step\nd delete step\nOther cancel")
            edit_command = input("What do you wish to do? ")
            if edit_command == "w":
                step_number = input("Insert step number to write in range 1-16: ")
                sequence.tracks[0].write_step(int(step_number) - 1)
                print(current_pattern_str, commands_str)
                break
            elif edit_command == "d":
                step_number = input("Insert step number to delete from range 1-16: ")
                sequence.tracks[0].erase_step(int(step_number) - 1)
                print(current_pattern_str, commands_str)
                break
            else:
                break
    elif command == "x":
        sequence.engine.stop()
        clock.stop()
        break
