from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.loop as lp
import moviepy.video.fx.fadeout as fdout
import os

print (os.path.realpath(__file__))
videoFile = './assets/input/video_output.mp4'
audioFile = './assets/input/audio_output.mp3'

videoClip = VideoFileClip(filename=videoFile, audio=False)
audioClip = AudioFileClip(filename=audioFile)

print(f'duration of the video is {videoClip.duration}')
print(f'duration of the audio clip is {audioClip.duration}')
audioClip.close()

newClip = videoClip.fx(lp.loop, duration=audioClip.duration).fx(fdout.fadeout, duration= 1)
newClip.write_videofile(filename='./assets/output/final_output.mp4', audio=audioFile)
videoClip.close()
