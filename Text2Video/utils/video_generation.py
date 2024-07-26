from moviepy.editor import *
from PIL import Image 
import glob
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from scipy.io import wavfile

def video_generation():
    audio_path=os.path.join(os.getcwd(), 'audio//audio.wav')
    image_folder_path=os.path.join(os.getcwd(),'enhanced_images')
    output_video_path = os.path.join(os.getcwd(),'video//video.mp4')
    
    Fs, data = wavfile.read(audio_path)

    total_audio_duration=(len(data)/Fs)

    frame_rate = 24  
    image_files = [os.path.join(image_folder_path, filename) for filename in os.listdir(image_folder_path) if filename.endswith(('.jpg', '.png', '.jpeg'))]
    image_duration = total_audio_duration/len(image_files)
    image_clips = []

    save_directory='video'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    for image_path in image_files:
        image_pil = Image.open(image_path).convert('RGB')
        # Create an ImageClip from the RGB image
        image_clip = ImageClip(np.array(image_pil))
        image_clip = image_clip.set_duration(image_duration)
        image_clips.append(image_clip)

    final_video = concatenate_videoclips(image_clips, method="compose")
    audio_clip = AudioFileClip(audio_path)

    final_video = final_video.set_audio(audio_clip)
    final_video.write_videofile(output_video_path, fps=24)

    return output_video_path

