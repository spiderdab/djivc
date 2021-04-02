# djivc
A simple PyQt5 GUI to convert h264 (.mp4) 4k videos from a DJI drone like the Mini 2, to DNxHR (.mov), based on ffmpeg.

You can select one or more files to convert and put them in a queue.
You can select whether to use CPU or GPU (if available..) decoding. Unfortunately ffmpeg doesn't have AFAIK an hw-accelerated DNxHD encoder.
You can select one of 3 different encoding bitrate: LB, SQ, HQ, respectively 180, 577 and 873 Mbit/s.
You can choose the output folder.
Finally you press start and a progress bar will show you the queue convertion progress.

I know there are several project out there to give you a GUI for ffmpeg, but none of them gave me this specialized convertion, usefull if you want to edit your DJI Mini 2 4K videos into DaVinci Resolve (free linux version).

The only library needed is PyQt5. ..and of course python3..

![GitHub Logo](/images/DJIVC_Screenshot.png)
