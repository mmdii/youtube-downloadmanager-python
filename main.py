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
        elif (not self.openDir):
            self.fileLocationLabel.config(text="Please Choose the folder", fg="red")
        elif (self.matchYoutubeLink and self.openDir):
            self.downloadWindow()
    
    def downloadWindow(self):
        self.newWindow = Toplevel(self.root)
        self.root.withdraw()
        self.app = SecondPage(self.newWindow, self.youtubeEnteryVar.get(), self.FolderName, self.choisesVar.get())

    def openDir(self):
        self.FolderName = filedialog.askdirectory()
        if (len(self.FolderName)>1):
            self.fileLocationLabel.config(text=self.FolderName, fg="black", font=("Aerial", 15))
            return True
        else:
            self.fileLocationLabel.config(text="Please chose a folder", fg="red", font=("Aerial", 15))

class SecondPage:
    def __init__(self, downloadwindow, youtubeEntery, FolderName, Choises):
        self.downloadwindow = downloadwindow
        self.downloadwindow.attributes("-zoomed", True)
        self.downloadwindow.grid_rowconfigure(0, weight=0)
        self.downloadwindow.grid_columnconfigure(0, weight=1)

        self.youtubeChoseLabel = Label(self.downloadwindow, text="test label", font=("Aerial", 30))
        self.youtubeChoseLabel.grid()

        self.youtubeEntery = youtubeEntery
        self.FolderName = FolderName
        self.Choises = Choises

        self.yt = YouTube(self.youtubeEntery)

        if (self.Choises=="1"):
            self.video_type = self.yt.streams.filter(only_audio=True).first()
            self.Maxfilesize = self.video_type.filesize
        if (self.Choises=="2"):
            self.video_type = self.yt.streams.first()
            self.Maxfilesize = self.video_type.filesize

        self.loadingLabel = Label(self.downloadwindow, text="Downloading in Progress", font=("Aerial", 40))
        self.loadingLabel.grid(pady=(100, 0))

        self.loadingPersent = Label(self.downloadwindow, text="0", fg="green", font=("Aerial", 40))
        self.loadingPersent.grid(pady=(50, 0))

        self.progressBar = ttk.Progressbar(self.downloadwindow, length=500, orient="horizontal", mode="indeterminate")
        self.progressBar.grid(pady=(50, 0))
        self.progressBar.start()

        threading.Thread(target=self.yt.register_on_progress_callback(self.show_progressbar)).start()
        threading.Thread(target=self.DownloadFile).start()

    def DownloadFile(self):
        if (self.Choises == "1"):
            self.yt.streams.filter(only_audio=True).first().download(self.FolderName)
        elif (self.Choises == "2"):
            self.yt.streams.first().download(self.FolderName)

    def show_progressbar(self, streams = None, chunk = None, filehandle = None, bytes_remaining = None):
        self.percentCount = float("%0.2f" % (100-(100*(bytes_remaining/self.Maxfilesize))))

        if (self.percentCount < 100):
            self.loadingPersent.config(text=str(self.percentCount))
        else:
            self.progressBar.stop()
            self.loadingLabel.grid_forget()
            self.progressBar.grid_forget()
            self.downloadFinishedLabel = Label (self.downloadwindow, text="Download completed", font=("Aerial", 40))
            self.downloadFinishedLabel.grid(pady=(150, 0))

            self.downloadLocation = Label(self.downloadwindow, text= self.yt.title, font=("Aerial", 40))
            self.downloadLocation.grid(pady=(50, 0))

            MB = float("%0.2f" % (self.Maxfilesize/1000000))
            self.downloadedFilesize = Label(self.downloadwindow, text=str(MB)+"MB", font=("Aerial", 40))
            self.downloadedFilesize.grid(pady=(50, 0))



if __name__ =='__main__':
    window = Tk()
    # window.state('-zoomed')
    window.attributes("-zoomed",True)
    app = Application(window)

    window.mainloop()
 