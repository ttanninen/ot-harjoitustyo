import miniaudio
import numpy as np
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