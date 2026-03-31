import sequencer
import os

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

# Create new sequence
sequence = sequencer.Sequence(128, 4)

# Load track 1 to sequence
sequence.add_track(track1)

while True:
    # Print instructions
    current_pattern_str = "Current pattern: " + str(sequence.tracks[0].pattern)
    commands_str = "Test commands:\nP play\nS stop\nE edit pattern\nOther exit"
    print(commands_str)
    print(current_pattern_str)

    command = input("Enter command: ")
    if command == "P":
        sequence.play()
    elif command == "S":
        sequence.stop()
    elif command == "E":
        while True:
            print(current_pattern_str)
            print("W write step\nD delete step\nOther cancel")
            edit_command = input("What do you wish to do? ")
            if edit_command == "W":
                step_number = input("Insert step number to write in range 1-16: ")
                sequence.tracks[0].write_step(int(step_number) - 1)
                print(current_pattern_str, commands_str)
                break
            elif edit_command == "D":
                step_number = input("Insert step number to delete from range 1-16: ")
                sequence.tracks[0].erase_step(int(step_number) - 1)
                print(current_pattern_str, commands_str)
                break
            else:
                break
    else:
        break
