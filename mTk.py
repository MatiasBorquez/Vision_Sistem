import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

window = tkinter.Tk()
window.wm_withdraw()
window.wm_attributes("-topmost", True)

def selectFile():
    filename= askopenfilename()
    return filename