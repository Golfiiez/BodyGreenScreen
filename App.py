from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile


class App(Frame):
    def __init__(self, root):
        self.root = root
        root.title("PROJECT_NAME_HERE")

        self._threshold_value = DoubleVar()
        self._mode_status = StringVar(value='normal')
        self._secondary_mode_status = StringVar(value='img')
        self.__createThresholdWidget()
        self.__createModeWidget()
        

    def __createThresholdWidget(self):
        self.threshold_label = Label(root, text='Threshold').grid(
            row=0, column=0, sticky=W)

        self.threshold = Scale(root, variable=self._threshold_value, from_=0, to=1,
                               orient=HORIZONTAL, command=lambda *a: _slider_select(*a))
        self.threshold.grid(row=0, column=1, sticky=W)
        # update treshold

        def _slider_select(*args):
            print(self._threshold_value.get())

    def __createModeWidget(self):
        # update select radio button (nornal/ blur)
        # Normal/Blur/Image
        self.mode_label = Label(
            root, text='Normal/Blur/Image:').grid(row=1, column=0, sticky=W)
        self.radio_normal = Radiobutton(
            root, text='Normal', variable=self._mode_status, value='normal', command=lambda: _radio_mode_select())
        self.radio_normal.grid(row=2, column=0, sticky=W)
        self.radio_blur = Radiobutton(root, text='Gaussian blur', variable=self._mode_status,
                                      value='blur', command=lambda: _radio_mode_select())
        self.radio_blur.grid(row=2, column=1, sticky=W)
        self.radio_image = Radiobutton(root, text='Custom Image', variable=self._mode_status,
                                       value='image', command=lambda: _radio_mode_select())
        self.radio_image.grid(row=2, column=2, sticky=W)

        def _radio_mode_select(*args):
            print(self._mode_status.get())
            self.__createSecondaryModeWidget(self._mode_status.get())

    #TODO: create event based image upload or color changing frame using given radio choice
    def __createSecondaryModeWidget(self,mode_str):
        pass


root = Tk()
root.geometry('360x200')
my_gui = App(root)
root.mainloop()
