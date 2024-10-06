import tkinter as tk
import speedtest

# Create the main window
window = tk.Tk()
window.title("Internet Speed Test")
window.geometry('400x300')

# Function to check internet speed
def speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    
    # Get the download and upload speed
    download_speed = round(st.download() / 10**6, 2)  # Convert to Mbps
    upload_speed = round(st.upload() / 10**6, 2)      # Convert to Mbps
    
    # Update the labels with the results
    lab_down.config(text=f"Download: {download_speed} Mbps")
    lab_up.config(text=f"Upload: {upload_speed} Mbps")

# Title label
lab_title = tk.Label(window, text="Internet Speed Test", font="Courier 20 bold")
lab_title.pack(pady=20)

# Labels to display download and upload speed
lab_down = tk.Label(window, text="Download: 00.00 Mbps", font="Courier 15")
lab_down.pack(pady=10)

lab_up = tk.Label(window, text="Upload: 00.00 Mbps", font="Courier 15")
lab_up.pack(pady=10)

# Button to start the speed test
btn = tk.Button(window, text="Start Test", command=speed, font="Courier 12", relief=tk.RAISED)
btn.pack(pady=20)

# Run the application
window.mainloop()
