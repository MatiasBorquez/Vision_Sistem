import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import filedialog, messagebox

window = tkinter.Tk()
window.wm_withdraw()
window.wm_attributes("-topmost", True)

def selectFile():
    filename = ''
    try:
        filename = filedialog.askopenfilename(filetypes=[('Image Files', ('.png', '.jpg', '.jpeg', '.gif'))])
        if not filename:
            raise Exception('No se seleccionó ningún archivo')
    except Exception as e:
        messagebox.showerror('Error', str(e))
    print(f'{filename}')
    return filename