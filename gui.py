import tkinter as tk
from tkinter import filedialog, ttk
import collector
import threading
import time
import main


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("600x300")
        self.grid()
        self.create_widgets()
        self.filenames = "C:/Users/Public/Videos"

    def create_widgets(self):
        self.meme_count = tk.IntVar(root, value=0)
        print(self.meme_count.get())
        self.collection = tk.Frame(self)
        self.collection.grid(row=1, column=2)

        self.title = tk.Label(self.collection, text="Collect Memes", pady=10)
        self.title.grid(row=1, column=1, columnspan=2)

        self.count = tk.Entry(self.collection, textvariable=self.meme_count)
        self.count.grid(row=2, column=2)

        self.count_label = tk.Label(self.collection, text="# of memes to collect ")
        self.count_label.grid(row=2, column=1)

        self.collect_button = tk.Button(self.collection, text="Begin Collecting\nMemes", command=self.get_vids)
        self.collect_button.grid(row=4, column=1, columnspan=2, pady=10)
        self.progress = ttk.Progressbar(self.collection)
        self.select_output_button = tk.Button(self.collection, text="Select Output Folder", command=self.browse_files)
        self.select_output_button.grid(row=3, column=1, columnspan=2, pady=10)

    def get_vids(self):
        self.progress.grid(row=5, column=1, columnspan=2)
        print(self.progress.winfo_viewable())
        self.master.update()
        self.master.update_idletasks()
        self.progress["value"] = 0
        collection = threading.Thread(target=collector.get_reddit_videos,
                                      args=("dankvideos", self.meme_count.get(), self.filenames))
        collection.start()
        while collection.is_alive():
            time.sleep(6)
            self.progress["value"] += 100 / self.meme_count.get()
            self.master.update_idletasks()
            print("LOOPED")
        main.clean_files(self.filenames)
        self.progress.grid_forget()

    def browse_files(self):
        self.filenames = filedialog.askdirectory(initialdir=self.filenames,
                                                 title="Select the output folder")
        print(self.filenames)


# print(os.listdir("meme storage"))
root = tk.Tk()
app = Application(master=root)
app.mainloop()
