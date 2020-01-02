import skvideo.io
import skvideo.datasets

video = skvideo.io.FFmpegWriter("out.mp4")

for i in range(91):
    name = str(i)
    if len(name)==1:
        name = "0"+name
    name = "out/"+name+".png"
    vid = skvideo.io.vread(name)
    video.writeFrame(vid)
