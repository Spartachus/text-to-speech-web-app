# import os
# import openai

# openai.api_key = "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"
# audio_file = open("output.wav", "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)
# print(transcript.text)
# with open('transcript.txt', 'a') as f:
#         f.write(transcript.text)


import whisper
model = whisper.load_model("base")

result = model.transcribe("output.wav", verbose = True)
print(result["text"])
with open('transcript.txt', 'a') as f:
        f.write(result["text"])