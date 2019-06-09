#coding=utf-8
import wx
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import load_meta_cnn as detect

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,parent=None,title="人脸表情识别系统",size=(1400,1200))
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        self.grid_sizer=wx.GridBagSizer(0,0)

        self.filename='../other/default.png'

        self.panel_top=wx.Panel(self)
        self.panel_top.SetMinSize((700,200))
        self.grid_sizer.Add(self.panel_top,pos=(0,0),span=(1,2),flag=wx.EXPAND)
        self.img_top=wx.Image('../other/title.jpg',wx.BITMAP_TYPE_ANY).Scale(1400, 200)
        wx.StaticBitmap(self.panel_top,pos=(0,0),bitmap=wx.Bitmap(self.img_top))

        self.panel_img=wx.Panel(self)
        self.panel_img.SetMinSize((700,350))
        self.grid_sizer.Add(self.panel_img,pos=(1,0),span=(1,1),flag=wx.EXPAND)
        self.setImage(self.filename,'0')
##        self.img_default=wx.Image('../temp/default.png',wx.BITMAP_TYPE_ANY)
##        wx.StaticBitmap(self.panel_left,pos=(100,50),bitmap=wx.Bitmap(self.img_default))

        self.panel_btn=wx.Panel(self)
        self.panel_btn.SetMinSize((700,150))
        self.grid_sizer.Add(self.panel_btn,pos=(2,0),span=(1,1),flag=wx.EXPAND)
        
        self.up=wx.Image('../other/up.png',wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.upBtn=wx.BitmapButton(self.panel_btn,-1,self.up,pos=(150,50))
        self.upBtn.Bind(wx.EVT_BUTTON,self.upBtnEvent)
        self.start=wx.Image('../other/start.png',wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.startBtn=wx.BitmapButton(self.panel_btn,-1,self.start,pos=(400,50))
        self.startBtn.Bind(wx.EVT_BUTTON,self.startBtnEvent)
        
        self.panel_right=wx.Panel(self)
        self.panel_right.SetMinSize((700,500))
        self.grid_sizer.Add(self.panel_right,pos=(1,1),span=(2,1),flag=wx.EXPAND)

        self.setPlot()

        self.SetSizer(self.grid_sizer)
        self.Fit()

    def setImage(self,path,flag):
        self.img_default=wx.Image(path,wx.BITMAP_TYPE_ANY).Rescale(500,300).ConvertToBitmap()

##        source = cv2.imread(path, cv2.IMREAD_COLOR)    
##        img = cv2.cvtColor(source, cv2.COLOR_BGR2RGB) 
##        h, w = img.shape[:2]
##        wxbmp = wx.BitmapFromBuffer(w, h, img)
##        size = wxbmp.GetWidth(),wxbmp.GetHeight()
        if flag=='0':
            self.img=wx.StaticBitmap(self.panel_img,pos=(100,50),bitmap=self.img_default)
        else:
            self.img.SetBitmap(wx.Bitmap(self.img_default))

    def upBtnEvent(self,event):
        dlg=wx.FileDialog(self, message="Choose a file", defaultDir='../other',defaultFile='',style=wx.FD_OPEN, wildcard="*.*",pos=wx.DefaultPosition)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetPath()
            self.setImage(self.filename,'1')
            print(self.filename)
        
    def startBtnEvent(self,event):
        if detect.main(self.filename):
            #wx.ProgressDialog(title='检测中', message='waiting...', maximum=100, parent=self,style=wx.PD_CAN_ABORT)
            f=open('../other/cv/1.txt')
            line=f.readline()
            d=eval(line)
            self.y=[d['angry'],d['disgust'],d['fear'],d['happy'],d['sad'],d['surprise'],d['neutral']]
            self.setPlot(self.y)
            self.setImage('../other/cv/pic/test.jpg','1')


    def setPlot(self,y=[1,1,1,1,1,1,1]):
        self.fig,self.axe=plt.subplots()
        self.canvas=FigureCanvasWxAgg(self.panel_right,-1,self.fig)
        self.x=np.arange(7)
        self.y=y
        plt.bar(self.x,self.y,facecolor='#ffd07e')
        for x_, y_ in zip(self.x, self.y):
            plt.text(x_, y_, '{:.2f}'.format(y_), ha='center', va='bottom',color='#ff8776',fontsize=11)
        plt.xticks([0,1,2,3,4,5,6],[r'$angry$',r'$disgust$',r'$fear$',r'$happy$',r'$sad$',r'$surprise$',r'$neutral$'])


app=wx.App()
frame=Frame()
frame.Show()
app.MainLoop()
