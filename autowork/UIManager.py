#-*- coding: utf-8 -*-
import wx 
import win32api
import os,sys
import time


from . import mysendmail
from . import autoconfig
from . import autotelnet
from . import autobianyi

APP_TITLE=u'状态监控'
APP_ICON ='res/app.bmp'

class mainFrame(wx.Frame):
	def __init__(self,parent):
		super(mainFrame, self).__init__(parent, -1, APP_TITLE);
		self.SetBackgroundColour(wx.Colour(224, 224, 224));
		self.SetSize((400, 700));
		self.Center();
		
		#创建控件控制器
		self.panel = wx.Panel(self);
		box = wx.BoxSizer(wx.VERTICAL);
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		#设置图标
		if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
			exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None));
			icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO);
		else:
			icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO);
		self.SetIcon(icon);
		
		#设置背景图片
		#image_file = 'res/test.jpg';
		#to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap();
		#panel.bitmap = wx.StaticBitmap(panel, -1, to_bmp_image, (0, 0))
		
		
		#输入框。
		#wx.StaticText(self, -1, u'输入命令：', pos=(0, 300), size=(400, -1), style=wx.ALIGN_RIGHT);
		#self.tip = wx.StaticText(self, -1, u'', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)
		#必须加多Line的参数，要不然不能触发事件。
		self.tc1 = wx.TextCtrl(self.panel,pos=(0, 230), size=(400, 30), name='INPUT', style=wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_RICH);
		
		#显示框
		self.tc2 = wx.TextCtrl(self.panel, -1, '', pos=(0, 0), size=(400, 630), name='OUTPUT', style=wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2);
		self.tc2.SetDefaultStyle(wx.TextAttr(wx.WHITE,wx.BLACK));
		self.tc2.SetBackgroundColour('Black');
		
		#调整输入框和显示框的位置
		#self.SetTransparent(200)
		box.Add(self.tc2,0,wx.ALIGN_CENTER|wx.EXPAND);
		box.Add(self.tc1,0,wx.ALIGN_CENTER|wx.EXPAND);
		
		#bind event
		self.tc1.Bind(wx.EVT_TEXT_ENTER,self.on_enter_pressed,self.tc1);
		self.panel.Bind(wx.EVT_ERASE_BACKGROUND,self.on_erase_back);
		#self.tc1.Bind(wx.EVT_TEXT, self.EvtText);
		self.Bind(wx.EVT_CLOSE, self.on_close);
		self.Bind(wx.EVT_SIZE, self.on_size);
		
		self.panel.SetSizer(box)
		#self.Fit() 
		self.Centre()
		
	#input treat
	def on_enter_pressed(self, evt):
		text = evt.GetString();
		arg=text.replace('\n','');
		self.tc1.ChangeValue("");
		self.tc1.Update();
		args = arg.split(' ');
		print(args[0]);
		if args[0] == "发送邮件":
			mysendmail.send_mail();
		elif args[0] == "配置":
			autoconfig.config(args[1],args[2]);
		elif args[0] == "切换":
			autotelnet.auto_telnet_change_ip();
		elif args[0] == "编译":
			autobianyi.auto_bianyi("D:/test");
		
	
	def on_size(self, evt):
		self.Refresh();
		evt.Skip();
		
	def on_close(self, evt):
		self.Destroy()
		
	def on_erase_back(self, evt):
		dc = evt.GetDC();
		if not dc:
			dc = wx.ClientDC(self);
			rect = self.GetUpdateRegion().GetBox();
			dc.SetClippingRect(rect);
		dc.Clear();
		bmp = wx.Bitmap("res/test.jpg");
		dc.DrawBitmap(bmp,0,0);
	
	def show_str(self,text):
		self.tc2.AppendText(text);
		self.tc2.Update();


class mainApp(wx.App):
	def OnInit(self):
		self.SetAppName(APP_TITLE);
		self.Frame=mainFrame(None);
		self.Frame.Show(True);
		return True;

showApp=mainApp();
showFrame=showApp.Frame;

		
	
