import threading
from tkinter import *
from tkinter import colorchooser
import tkinter
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from service import Service

class App(Frame):
    def __init__(self, root:Tk):
        self.root = root
        root.title("PROJECT_NAME_HERE")
        # widget preparation
        self._threshold_value = DoubleVar()
        self._mode_status = StringVar(value='normal')
        self._secondary_mode_status = StringVar(value='img')
        self.__createThresholdWidget()
        self.__createModeWidget()
        self.__createSecondaryModeWidget(self._mode_status.get())
        # videostream service
        self.stopEvent = threading.Event()
        self.service = Service(self.stopEvent)
        self.thread = threading.Thread(target = self.service.run_service_loop,args=())
        self.thread.start()
        self.root.wm_protocol("WM_DELETE_WINDOW",self.__onClose)

    def __onClose(self):
        self.stopEvent.set()
        self.root.quit()

    def __createThresholdWidget(self):
        self.threshold_label = Label(root, text='Threshold')
        self.threshold_label.grid(row=0, column=0, sticky=W)

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
            root, text='Normal/Blur/Image:')
        self.mode_label.grid(row=1, column=0, sticky=W)
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
            self.__updateSecondaryModeWidget(self._mode_status.get())

    def __createSecondaryModeWidget(self, mode_str):
        self.secondary_mode_label = Label(root, text='Choose Background Color')
        self.secondary_mode_label.grid(row=3, column=1, sticky=W)

        self.secondary_mode_option = Button(
            root, text="Choose Image", command=lambda: _choose_color())
        self.secondary_mode_option.grid(row=4, column=1, sticky=W)

        def _choose_color():
            color_code = colorchooser.askcolor(title="Choose color")
            print(color_code)

    def __updateSecondaryModeWidget(self, mode_str):
        self.secondary_mode_label.destroy()
        self.secondary_mode_option.destroy()
        if mode_str == 'normal':
            self.secondary_mode_label = Label(
                root, text='Choose Background Color')
            self.secondary_mode_option = Button(
                root, text="Select color", command=lambda: _choose_color())

        elif mode_str == 'image':
            self.secondary_mode_label = Label(
                root, text='Choose Background Image')
            self.secondary_mode_option = Button(
                root, text="Choose Image", command=lambda: _choose_color())

        self.secondary_mode_label.grid(row=3, column=1, sticky=W)
        self.secondary_mode_option.grid(row=4, column=1, sticky=W)

        def _choose_color():
            color_code = colorchooser.askcolor(title="Choose color")
            print(color_code)


root = Tk()
root.geometry('360x360')
my_gui = App(root)
root.mainloop()
