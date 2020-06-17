from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk 
from tkinter import * 
import re
import threading

class Application:
    def __init__(self,root):
        self.root = root
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.config(bg="#ffdddd")
        self.top_label = Label(self.root, text="YOUTUBE DOWNLOAD MANAGER", fg="orange", font=("FC059", 50))
        self.top_label.grid(pady=(0, 10))
        self.linkLabel = Label(self.root, text="Past the YouTube Link Below", font=("Aerial", 30))
        self.linkLabel.grid(pady=(0, 20))
        self.youtubeEnteryVar = StringVar()
        self.youtubeEntery = Entry(self.root, width=70, textvariable=self.youtubeEnteryVar, font=("Aerial", 25), fg="green")
        self.youtubeEntery.grid(pady=(0, 15), ipady=2)

        self.youtubeEntryErr = Label(self.root, text="", font=("Aerial", 20))
        self.youtubeEntryErr.grid(pady=(0, 8))
        self.youtubeFileSaveLabel = Label(self.root, text="Chose Directory", font=("Aerial", 30))
        self.youtubeFileSaveLabel.grid()

        self.youtubeFileDirButton = Button(self.root, text="Directory", font=("Aerial", 15), command=self.openDir)
        self.youtubeFileDirButton.grid(pady=(10, 3 ))

        self.fileLocationLabel = Label(self.root, text="", font=("Aerial", 20))
        self.fileLocationLabel.grid(pady=(0,30))

        self.youtubeChoseLabel = Label(self.root, text="chose the Download type", font=("Aerial", 30))
        self.youtubeChoseLabel.grid()

        downloadChoises = [("Audio MP3", 1), ("Video MP4", 2)]
        self.choisesVar = StringVar()
        self.choisesVar.set(1)

        for text,mode in downloadChoises:
            self.youtubeChoises = Radiobutton(self.root, text=text, font=("Aerial", 15), variable = self.choisesVar, value = mode)
            self.youtubeChoises.grid()

        self.youtubeDownloadButton = Button(self.root, text="Download", width=10, command= self.checkYoutubeLink, font=("Aerial", 15))
        self.youtubeDownloadButton.grid(pady=(30, 5))



    def checkYoutubeLink(self):
        self.matchYoutubeLink = re.match("^https://www.youtube.com/.*", self.youtubeEnteryVar.get())

        if (not self.matchYoutubeLink):
            self.youtubeEntryErr.config(text="Invalid YouTube Link", fg="red")
        elif (not self.openDir()):
            self.fileLocationLabel.config(text="Please Choose the folder", fg="red")
        elif (self.matchYoutubeLink and self.openDir):
            self.downloadWindow()
    
    def downloadWindow(self):
        self.newWindow = Toplevel(self.root)
        self.root.withdraw()
        # self.app = SecondPage(self.newWindow, self.youtubeEnteryVar.get(), self.FolderName.get(), self.choisesVar.get())





    def openDir(self):
        self.FolderName = filedialog.askdirectory()
        if (len(self.FolderName)>1):
            self.fileLocationLabel.config(text=self.FolderName, fg="black", font=("Aerial", 15))
            return True
        else:
            self.fileLocationLabel.config(text="Please chose a folder", fg="red", font=("Aerial", 15))


if __name__ =='__main__':
    window = Tk()
    # window.state('-zoomed')
    window.attributes("-zoomed",True)
    app = Application(window)

    window.mainloop()
 