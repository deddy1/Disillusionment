import cv2
import wx
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure


class mainFrame(wx.Frame):
    def __init__(self, img):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title='Click the pixel you want to match color', size=(800,600))
        
        # Values that get passed back to the main script
        self.lower_bound = np.array([0, 0, 0])
        self.upper_bound = np.array([255, 255, 255])
        
        # min, max coords
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        
        self.img = img
        self.inv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        self.dimensions = self.img.shape
        
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        
        self.axes.imshow(self.inv_img)
        self.canvas.draw()
        
        self.canvas.mpl_connect('button_press_event', self.get_range)
    
    def get_range(self, event):
        self.xmin,self.ymin = int(event.xdata), int(event.ydata)
        self.yeet = self.canvas.mpl_connect('motion_notify_event', self.on_drag)
    
    def on_drag(self, event):
        self.xmax,self.ymax = int(event.xdata), int(event.ydata)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        del self.axes.lines[:]
        self.draw_box()
    
    def draw_box(self):
        self.axes.axvline(self.xmin, ymin=(self.dimensions[0] - self.ymin)/self.dimensions[0], ymax=(self.dimensions[0] - self.ymax)/self.dimensions[0], c='r')
        self.axes.axhline(self.ymin, xmin=self.xmin/self.dimensions[1], xmax=self.xmax/self.dimensions[1], c='r')
        self.axes.axvline(self.xmax, ymin=(self.dimensions[0] - self.ymin)/self.dimensions[0], ymax=(self.dimensions[0] - self.ymax)/self.dimensions[0], c='r')
        self.axes.axhline(self.ymax, xmin=self.xmin/self.dimensions[1], xmax=self.xmax/self.dimensions[1], c='r')
        self.canvas.draw()
    
    def on_release(self, event):
        self.xmax,self.ymax = int(event.xdata), int(event.ydata)
        self.canvas.mpl_disconnect(self.yeet)
        self.draw_box()
        self.do_the_math()
        self.Close()
    
    def do_the_math(self):
        mini_img = self.img[self.ymin:self.ymax, self.xmin:self.xmax, :]
        list_of_maxes = [np.max(mini_img[:,:,0]), np.max(mini_img[:,:,1]), np.max(mini_img[:,:,2])]
        max_color = max(list_of_maxes)
        if max_color == list_of_maxes[0]:
            # Blue is dominant
            self.lower_bound[0] = np.min(mini_img[:,:,0])
            self.upper_bound[1] = np.max(mini_img[:,:,1])
            self.upper_bound[2] = np.max(mini_img[:,:,2])
            print('Blocking the color BLUE')
        
        elif max_color == list_of_maxes[1]:
            # Green is dominant
            self.lower_bound[1] = np.min(mini_img[:,:,1])
            self.upper_bound[0] = np.max(mini_img[:,:,0])
            self.upper_bound[2] = np.max(mini_img[:,:,2])
            print('Blocking the color GREEN')
        
        elif max_color == list_of_maxes[2]:
            # Red is dominant
            self.lower_bound[2] = np.min(mini_img[:,:,2])
            self.upper_bound[0] = np.max(mini_img[:,:,0])
            self.upper_bound[1] = np.max(mini_img[:,:,1])
            print('Blocking the color RED')
        
        print('\tLower color bound is: {}'.format(self.lower_bound))
        print('\tUpper color bound is: {}'.format(self.upper_bound))

if __name__ == '__main__':
    app = wx.App()
    frame = mainFrame(cv2.imread('opencv_color_frame.png'))
    frame.Show()
    app.MainLoop()
