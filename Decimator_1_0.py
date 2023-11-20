#v2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import soundfile as sf
from scipy.signal import decimate

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

def show_info(message):
    messagebox.showinfo("Decimator 1.0 - Information", message)

def downsample():
    folder_path = folder_path_entry.get()
    target_sample_rate_kHz = int(sample_rate_entry.get())
    target_sample_rate = int(target_sample_rate_kHz) * 1000
    # Filter files with both '.wav' and '.WAV' extensions
    wav_files = [f for f in os.listdir(folder_path) if f.endswith(".wav") or f.endswith(".WAV")]
    output_folder = os.path.join(folder_path, 'Decimated')
    os.makedirs(output_folder, exist_ok=True)
    
    show_info("Decimating audio files. This might take a while...")

    for wav_file in wav_files:
        try:
            wav_path = os.path.join(folder_path, wav_file)
            y, sr = librosa.load(wav_path, sr=None)
                        
            # Downsample using scipy.signal.decimate
            decimation_factor = int(sr / target_sample_rate)
            y = decimate(y, decimation_factor)
            
            filename = os.path.splitext(os.path.basename(wav_file))[0]
            output_filename = f"{filename}_{target_sample_rate_kHz}kHz.wav"
            output_path = os.path.join(output_folder, output_filename)
            sf.write(output_path, y, target_sample_rate)
            print(f"Saved to: {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    show_info("Process complete. Decimated files saved in a separate folder.")

app = tk.Tk()
app.title("Decimator 1.0")
app.geometry("400x280")

folder_label = tk.Label(app, text="Select a folder with .wav files:")
folder_label.pack(pady=10)

folder_path_entry = tk.Entry(app, width=40)
folder_path_entry.pack()

browse_button = tk.Button(app, text="Browse", command=browse_folder)
browse_button.pack()

sample_rate_label = tk.Label(app, text="Enter sample rate (in kHz):")
sample_rate_label.pack(pady=10)

sample_rate_entry = tk.Entry(app, width=10)
sample_rate_entry.pack()

downsample_button = tk.Button(app, text="Decimate", command=downsample)
downsample_button.pack(pady=10)

created_by_label = tk.Label(app, text=" ©GFrainer2023")
created_by_label.pack(side="bottom", padx=10, pady=10)

source_code_label = tk.Label(app, text="github.com/Gui-Frainer/Decimator-1.0")
source_code_label.pack(side="bottom", padx=10, pady=10)

#app.iconbitmap("D:/Postdoc/Decimator 1_0/logo_D.ico")

app.mainloop()