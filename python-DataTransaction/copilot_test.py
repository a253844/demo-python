#write a program to download youtube video using python

import pytube

link = input("Enter the link of the video: ")

url = input("Enter the url of the video: ")
video = pytube.YouTube(url)

stream = video.streams.get_highest_resolution()

stream.download()

print("Download Completed!!")

