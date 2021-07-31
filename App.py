import threading
from tkinter import *
from tkinter import colorchooser, messagebox
import tkinter
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from service import Service
from PIL import ImageColor


class App(Frame):
    def __init__(self, root: Tk):
        self.root = root
        root.title("Green Screen Me Config")

        # widget preparation
        self._threshold_value = DoubleVar()
        self._mode_status = StringVar(value='normal')
        self._secondary_mode_status = StringVar(value='img')
        self._away_from_screen_status = IntVar(value=0)
        self.__createThresholdWidget()
        self.__createModeWidget()
        self.__createOrUpdateSecondaryModeWidget(self._mode_status.get(), create=True)
        self.__createAwayFromScreenWidget()

        # virtualcamera service

        # thread's events
        self.stopEvent = threading.Event()

        self.service = Service(self.stopEvent)
        self.thread = threading.Thread(
            target=self.service.run_service_loop, args=())
        self.root.wm_protocol("WM_DELETE_WINDOW", self.__onClose)
        self.__initVCamService()

    def __initVCamService(self):
        try:
            self.thread.start()
        except Exception as e:
            messagebox.showerror(
                "Error starting virtual camera service", str(e))
            self.__onClose()

    def __onClose(self):
        self.stopEvent.set()
        self.root.quit()

    def __createThresholdWidget(self):
        self.threshold_label = Label(root, text='Threshold')
        self.threshold_label.grid(row=0, column=0, sticky=W)

        self.threshold = Scale(root, variable=self._threshold_value, from_=1, to=0,
                               orient=HORIZONTAL, command=lambda *a: _sliderSelect(*a))
        self.threshold.grid(row=0, column=1, sticky=W)
        # update treshold

        def _sliderSelect(*args):
            threshold_value = self._threshold_value.get()
            self.service.segment_utils.update_threshold(threshold_value)

    def __createModeWidget(self):
        # update select radio button (normal/ blur)
        # Normal/Blur/Image
        self.mode_label = Label(
            root, text='Normal/Blur/Image:')
        self.mode_label.grid(row=1, column=0, sticky=W)
        self.radio_normal = Radiobutton(
            root, text='Normal', variable=self._mode_status, value='normal', command=lambda: _radioModeSelect())
        self.radio_normal.grid(row=2, column=0, sticky=W)
        self.radio_blur = Radiobutton(root, text='Gaussian blur', variable=self._mode_status,
                                      value='blur', command=lambda: _radioModeSelect())
        self.radio_blur.grid(row=2, column=1, sticky=W)
        self.radio_image = Radiobutton(root, text='Custom Image', variable=self._mode_status,
                                       value='image', command=lambda: _radioModeSelect())
        self.radio_image.grid(row=2, column=2, sticky=W)

        def _radioModeSelect(*args):
            self.service.segment_utils.update_mode_selected(
                self._mode_status.get())
            self.__createOrUpdateSecondaryModeWidget(self._mode_status.get())

    def __createOrUpdateSecondaryModeWidget(self, mode_str, create=False):
        if mode_str != 'blur':
            if not create:
                self.secondary_mode_label.destroy() 
                self.secondary_mode_option.destroy()

            if mode_str == 'normal':
                self.secondary_mode_label = Label(
                    root, text='Choose Background Color')
                self.secondary_mode_option = Button(
                    root, text="Select Color", command=lambda: _chooseColor())

            elif mode_str == 'image':
                self.secondary_mode_label = Label(
                    root, text='Choose Background Image')
                self.secondary_mode_option = Button(
                    root, text="Choose Image", command=lambda: _chooseImage())

            self.secondary_mode_label.grid(row=3, column=1, sticky=W)
            self.secondary_mode_option.grid(row=4, column=1, sticky=W)

        def _chooseColor():
            color_code = colorchooser.askcolor(title="Choose color")
            # convert from rgb to bgr
            self.service.segment_utils._MASK_COLOR = ( color_code[0][2], color_code[0][1], color_code[0][0] )
        
        def _chooseImage():
            file_path = askopenfile(mode='r', filetypes=[('Image Files', ['.jpeg', '.jpg', '.png',
                                                       '.tiff', '.tif', '.bmp'])])
            if file_path is not None:
                self.service.segment_utils.set_bg_image(file_path.name)
    
    def __createAwayFromScreenWidget(self):
        self.away_from_screen_checkbutton = Checkbutton(
            root, variable=self._away_from_screen_status, text='Enable away from screen mode', command=lambda: _toggleAwayFromScreen())
        self.away_from_screen_checkbutton.grid(row=5, column=0, sticky=W)

        self.away_from_screen_uploadbutton = Button(
            root, text=f"update your away pic", command=lambda: _updateDefaultPicture())

        def _toggleAwayFromScreen():
            self.service.away_from_screen_flag = bool(self._away_from_screen_status.get())
            if self.service.away_from_screen_flag:
                self.away_from_screen_uploadbutton.grid(
                    row=6, column=1, sticky=W)
                self.service.segment_utils.AWAY_FLAG = True
            else:
                self.service.segment_utils.AWAY_FLAG = False
                self.away_from_screen_uploadbutton.grid_remove()

        def _updateDefaultPicture():
            file_path = askopenfile(mode='r', filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', '.gif',
                                                                          '.tiff', '.tif', '.bmp'])])
            if file_path is not None:
                self.service.segment_utils.set_default_img(file_path.name)

root = Tk()
root.geometry('720x720')
my_gui = App(root)
root.mainloop()
