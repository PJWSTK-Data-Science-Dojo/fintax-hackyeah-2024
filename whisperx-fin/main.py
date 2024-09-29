from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import whisperx
# import gc
import os
import pathlib
import shutil
import uvicorn
app = FastAPI()

# Global configurations
device = "cpu"
batch_size = 16
compute_type = "int8"  # Adjust depending on resources

# Ensure a temporary directory for saving uploaded audio files
TEMP_AUDIO_DIR = pathlib.Path("./temp_audio")
TEMP_AUDIO_DIR.mkdir(exist_ok=True)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Step 1: Save the uploaded file to the temporary directory
        audio_file_path = TEMP_AUDIO_DIR / file.filename
        with open(audio_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 2: Load and transcribe with WhisperX
        audio_file = str(audio_file_path)
        
        # Load the WhisperX model
        model = whisperx.load_model("tiny", device, compute_type=compute_type, asr_options={"initial_prompt": "Now, umm.. watch uhh.. this video"})

        # Load the audio
        audio = whisperx.load_audio(audio_file)

        # Transcribe the audio
        result = model.transcribe(audio, batch_size=batch_size)
        transcription_segments = result["segments"]

        # Clean up WhisperX model to save memory
        # gc.collect()

        # Step 3: Align the transcription
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        aligned_result = whisperx.align(transcription_segments, model_a, metadata, audio, device, return_char_alignments=False)

        # Clean up alignment model
        # gc.collect()

        # Step 4: Diarization for speaker labels
        diarize_model = whisperx.DiarizationPipeline(use_auth_token="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", device=device)
        diarize_segments = diarize_model(audio)

        # Assign speakers to words
        final_result = whisperx.assign_word_speakers(diarize_segments, aligned_result)

        # Clean up diarization model
        # gc.collect()

        # Return the final result with speaker labels
        return JSONResponse(content={
            "transcription_segments": final_result["segments"],
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Clean up the temporary audio file after processing
        if audio_file_path.exists():
            os.remove(audio_file_path)

# Optional: Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Run the FastAPI application on port 5000
if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=False, access_log=False)
