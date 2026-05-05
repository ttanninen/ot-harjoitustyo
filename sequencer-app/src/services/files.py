import base64
import json
import io
import numpy as np
from scipy.io import wavfile


import miniaudio


from config import MAX_SAMPLE_DURATION

def load_sound(filename: str):
    """Read waveform (numpy array) and samplerate from file

    Raises:
        ValueError: If wav-file length surpasses MAX_SAMPLE_DURATION

    Returns:
        _type_: tuple with audio data and sample rate
    """

    decoded = miniaudio.decode_file(
        filename,
        output_format=miniaudio.SampleFormat.FLOAT32,
        nchannels=1,
        sample_rate=44100,
    )
    data = np.frombuffer(decoded.samples, dtype=np.float32).copy()

    duration = len(data) / decoded.sample_rate
    if duration > MAX_SAMPLE_DURATION:
        raise ValueError(
            f"File duration is {duration:.1f}s."
            f"Maximum allowed is {MAX_SAMPLE_DURATION}"
        )

    return data, decoded.sample_rate

def save_sequence(sequence, filename: str):
    tracks = []

    for track in sequence.tracks:
        buffer =  io.BytesIO()
        wavfile.write(buffer, track.samplerate, track.data)
        audio_b64 = base64.b64encode(buffer.getvalue()).decode("ascii")

        tracks.append({
            "name": track.name,
            "volume": track.volume,
            "pan": track.pan,
            "pattern": track.pattern.tolist(),
            "audio": audio_b64,
        })

        sequence_payload = {
            "bpm": sequence.bpm,
            "steps_per_beat": sequence.steps_per_beat,
            "num_steps": sequence.num_steps,
            "tracks": tracks,
        }

    with open(filename, "w", encoding="utf-8") as f:
        try:
            json.dump(sequence_payload, f)
        except:
            raise TypeError("Track saving failed")

def load_sequence(filename):
    
    return