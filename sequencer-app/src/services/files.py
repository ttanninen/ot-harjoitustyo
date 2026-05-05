import base64
import json
import io
from scipy.io import wavfile

from services.audioengine import AudioEngine
from services.sequencer import Sequence, Track

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
        json.dump(sequence_payload, f)

def load_sequence(engine: AudioEngine, filename):


    with open(filename, "r", encoding="utf-8") as f:
        payload = json.load(f)

    sequence = Sequence(
        bpm = payload["bpm"],
        steps_per_beat = payload["steps_per_beat"],
        engine = engine,
        num_steps = payload["num_steps"],
    )

    for t in payload["tracks"]:
        audio_bytes = base64.b64decode(t["audio"])
        buffer = io.BytesIO(audio_bytes)
        samplerate, data = wavfile.read(buffer)

        track = Track.load_track_from_file(
            data=data,
            samplerate=samplerate,
            name=t["name"],
            pattern=t["pattern"],
        )
        track.volume = t["volume"]
        track.pan = t["pan"]
        sequence.tracks.append(track)
    return sequence
