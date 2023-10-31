import os
import time
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

class VideoTrimmerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Trimmer")
        self.root.geometry("400x250")
        self.input_folder = ""
        self.output_folder = ""
        self.duration_per_video = 3600

        self.create_ui()

    def create_ui(self):
        # Input folder selection
        input_folder_label = Label(self.root, text="Select Input Folder:")
        input_folder_label.grid(row=0, column=0, padx=10, pady=10)
        self.input_folder_entry = Entry(self.root, width=40)
        self.input_folder_entry.grid(row=0, column=1, padx=10, pady=10)
        browse_input_button = Button(self.root, text="Browse", command=self.browse_input_folder)
        browse_input_button.grid(row=0, column=2, padx=10, pady=10)

        # Output folder selection
        output_folder_label = Label(self.root, text="Select Output Folder:")
        output_folder_label.grid(row=1, column=0, padx=10, pady=10)
        self.output_folder_entry = Entry(self.root, width=40)
        self.output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
        browse_output_button = Button(self.root, text="Browse", command=self.browse_output_folder)
        browse_output_button.grid(row=1, column=2, padx=10, pady=10)

        # Duration per video
        duration_label = Label(self.root, text="Duration per Video (seconds):")
        duration_label.grid(row=2, column=0, padx=10, pady=10)
        self.duration_per_video_entry = Entry(self.root, width=10)
        self.duration_per_video_entry.insert(0, "3600")
        self.duration_per_video_entry.grid(row=2, column=1, padx=10, pady=10)

        # Trim button
        trim_button = Button(self.root, text="Trim Videos", command=self.process_videos)
        trim_button.grid(row=3, column=1, padx=10, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=4, column=1, padx=10, pady=10)

    def browse_input_folder(self):
        self.input_folder = filedialog.askdirectory()
        self.input_folder_entry.delete(0, END)
        self.input_folder_entry.insert(0, self.input_folder)

    def browse_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        self.output_folder_entry.delete(0, END)
        self.output_folder_entry.insert(0, self.output_folder)

    def trim_video(self, input_file, output_dir, duration_per_video=3600):
        video = VideoFileClip(input_file)
        total_duration = video.duration
        num_parts = int(total_duration // duration_per_video)

        for i in range(num_parts):
            start_time = i * duration_per_video
            end_time = (i + 1) * duration_per_video
            output_file = os.path.join(output_dir, f"trim_{i + 1}.mp4")

            ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)
            self.progress["value"] = (i + 1) * 100 / num_parts
            self.root.update()

        if total_duration % duration_per_video > 0:
            start_time = num_parts * duration_per_video
            end_time = total_duration
            output_file = os.path.join(output_dir, f"trim_{num_parts + 1}.mp4")

            ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)

    def process_videos(self):
        self.input_folder = self.input_folder_entry.get()
        self.output_folder = self.output_folder_entry.get()
        self.duration_per_video = int(self.duration_per_video_entry.get())

        self.progress["value"] = 0

        threading.Thread(target=self.trim_videos_thread).start()

    def trim_videos_thread(self):
        for video_file in os.listdir(self.input_folder):
            if video_file.endswith('.mp4'):
                video_name = os.path.splitext(video_file)[0]
                video_input_path = os.path.join(self.input_folder, video_file)
                video_output_path = os.path.join(self.output_folder, video_name)
                os.makedirs(video_output_path, exist_ok=True)
                self.trim_video(video_input_path, video_output_path, self.duration_per_video)

        self.progress["value"] = 100
        self.root.update()
        time.sleep(1)
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = VideoTrimmerApp(root)
    root.mainloop()
