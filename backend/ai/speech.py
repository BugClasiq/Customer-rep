import os
import wave
import tempfile
import time
import contextlib
import pyaudio
from pywhispercpp.model import Model
import pyttsx3


@contextlib.contextmanager
def _suppress_stderr():
    """Redirect C-level stderr (fd 2) to devnull to silence whisper.cpp logs."""
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    old_stderr_fd = os.dup(2)
    try:
        os.dup2(devnull_fd, 2)
        yield
    finally:
        os.dup2(old_stderr_fd, 2)
        os.close(old_stderr_fd)
        os.close(devnull_fd)



class Speech:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            try:
                with _suppress_stderr():
                    cls._model = Model('tiny', n_threads=4)
            except Exception:
                import traceback
                traceback.print_exc()
                raise
        return cls._model

    @staticmethod
    def record_audio(output_path, silence_threshold=500, silence_duration=1.0, sample_rate=16000):
        audio = pyaudio.PyAudio()
        # Capture sample width BEFORE terminating PyAudio
        sample_width = audio.get_sample_size(pyaudio.paInt16)

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=1024,
        )

        frames = []
        silent_chunks = 0
        input("Press Enter to start recording...")

        while True:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            # Compute volume from the chunk
            volume = max(abs(int.from_bytes(data[i:i+2], "little", signed=True)) for i in range(0, len(data), 2))

            if volume < silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > int(silence_duration * (sample_rate / 1024)):
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(sample_width)  # use pre-captured value
            wf.setframerate(sample_rate)
            wf.writeframes(b"".join(frames))

        print("Recording saved to:", output_path)
        return output_path
    



    @staticmethod
    def convert_to_16k_wav(audio_path):
        """Converts any input audio file (WAV, WEBM, MP3, etc.) to 16kHz mono 16-bit WAV for whisper."""
        if not audio_path or not os.path.exists(audio_path):
            return audio_path

        # Quick check if it is already a 16kHz mono PCM 16-bit WAV file
        try:
            with wave.open(audio_path, 'rb') as wf:
                if wf.getframerate() == 16000 and wf.getnchannels() == 1 and wf.getsampwidth() == 2:
                    return audio_path
        except Exception:
            pass

        target_path = tempfile.mktemp(suffix="_16k.wav")

        # 1. Try PyAV (handles webm, ogg, wav, mp3 natively without external binaries)
        try:
            import av
            container = av.open(audio_path)
            stream = container.streams.audio[0]
            resampler = av.AudioResampler(format='s16', layout='mono', rate=16000)

            raw_frames = []
            for frame in container.decode(stream):
                resampled_frames = resampler.resample(frame)
                for rf in resampled_frames:
                    raw_frames.append(rf.to_ndarray().tobytes())

            flushed = resampler.resample(None)
            if flushed:
                for rf in flushed:
                    raw_frames.append(rf.to_ndarray().tobytes())

            audio_bytes = b"".join(raw_frames)
            with wave.open(target_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_bytes)
            container.close()
            return target_path
        except Exception as e:
            print("PyAV conversion failed, trying pydub:", e)

        # 2. Try pydub
        try:
            from pydub import AudioSegment
            sound = AudioSegment.from_file(audio_path)
            sound = sound.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            sound.export(target_path, format="wav")
            return target_path
        except Exception as e:
            print("Pydub conversion failed:", e)

        # 3. Try scipy fallback for WAV files
        try:
            import numpy as np
            from scipy.io import wavfile
            from scipy.signal import resample

            rate, data = wavfile.read(audio_path)
            if data.ndim > 1:
                data = data.mean(axis=1)
            if rate != 16000:
                num_samples = int(len(data) * 16000 / rate)
                data = resample(data, num_samples)

            data = np.int16(data)
            wavfile.write(target_path, 16000, data)
            return target_path
        except Exception as e:
            print("Scipy conversion failed:", e)

        return audio_path

    @staticmethod
    def stt(audio_path=None):
        if audio_path is None:
            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, "support_ai_voice.wav")
            Speech.record_audio(audio_path, silence_threshold=500, silence_duration=2.0, sample_rate=16000)

        converted_path = Speech.convert_to_16k_wav(audio_path)

        try:
            model = Speech.get_model()
            with _suppress_stderr():
                segments = model.transcribe(converted_path)
            text = " ".join(seg.text.strip() for seg in segments).strip()

            if converted_path != audio_path and os.path.exists(converted_path):
                try:
                    os.remove(converted_path)
                except Exception:
                    pass

            return text
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Transcription failed:", repr(e))
            return ""




    @staticmethod
    def speak_text(text):
        if not text:
            return

        if pyttsx3 is None:
            print("TTS:", text)
            return

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def speak_to_file(text, output_path=None):
        if not text:
            return None

        if pyttsx3 is None:
            return None

        if output_path is None:
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, "support_ai_response.wav")

        try:
            engine = pyttsx3.init()
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return output_path
        except Exception as e:
            print("TTS save_to_file failed:", e)
            return None



# def get_ai_reply(text):
#     try:
#         from engine import generate_response
#         result = generate_response(text, chat_history=[])
#         return result.get("response", text)
#     except Exception as exc:
#         print("AI engine unavailable:", exc)
#         return text


# def run_voice_chat(duration=5):
#     temp_dir = tempfile.gettempdir()
#     audio_path = os.path.join(temp_dir, "support_ai_voice.wav")

#     record_audio(audio_path, duration=duration)
#     transcript = transcribe_audio(audio_path)

#     print("You said:", transcript)

#     if not transcript:
#         print("No speech detected.")
#         return

#     reply = get_ai_reply(transcript)
#     print("Assistant:", reply)


#     speak_text(reply)


if __name__ == "__main__":
    # text = Speech.stt()
    # print("Transcript:", text)

    text = "Hello, I am fine, how are you?"
    Speech.speak_text(text)
