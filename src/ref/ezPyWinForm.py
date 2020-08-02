import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReferenceToFileAndPath("ScintillaNET.dll")

import System
from System import Uri
from System.Windows.Forms import *
'''(
    Application, Form, Padding, DockStyle, FlatStyle
    MenuStrip, StatusBar, AnchorStyles
    ToolStripContainer, TextImageRelation
    ToolStripMenuItem, ToolStripSeparator
    ToolStrip, ToolStripButton
    ToolStripLabel, ToolStripTextBox, ToolStripComboBox
    StatusStrip, ToolStripStatusLabel
    BorderStyle, ToolStripItemDisplayStyle
    ListView, View, SortOrder, SplitContainer
    Panel, ToolTip, Label, Button, TextBox, ScrollBars
    Orientation, TabControl, TabPage
    FlowLayoutPanel, FlowDirection,
    Shortcut, MainMenu, MenuItem 
)'''
from System.Drawing import *
'''
Size, Image, Point, Bitmap, Font
'''
import ScintillaNET
from ScintillaNET import WrapMode
from ScintillaNET import IndentView
from ScintillaNET import MarginType

_window__ctrl_table = {}

def GetControl(name):
    return _window__ctrl_table.get(name)

def GetWpfControl(name):
    if _window__ctrl_table.get(name): return _window__ctrl_table[name].ctrl;

def DumpControlTable():
    for k,v in _window__ctrl_table.items():
        print(k,v)
        
class WinControl():
    def Initialize(self,h):
        if h.get('width'): self.Width = h['width']
        if h.get('height'): self.Height = h['height']
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('menu'): self.SetContextMenu(h['menu'])
        if h.get('expand'): self.dockFill()
        self.ctrl.Anchor = AnchorStyles.None
    def SetSize(self,size): self.ctrl.Size = size
    def SetWidth(self,w): self.ctrl.Width = w;
    def SetHeight(self,h): self.ctrl.Height = h;
    def SetLocation(self,point): self.ctrl.Location = point
    def dockFill(self): self.ctrl.Dock = DockStyle.Fill
    def dockTop(self): self.ctrl.Dock = DockStyle.Top
    def dockBottom(self): self.ctrl.Dock = DockStyle.Bottom
    def dockLeft(self): self.ctrl.Dock = DockStyle.Left  
    def dockRight(self): self.ctrl.Dock = DockStyle.Right  
    def anchorAll(self): self.ctrl.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right     
    def Add(self,ctrl): self.ctrl.Controls.Add(ctrl)
    def SetBackColor(self,color): self.ctrl.BackColor = color
    def SetBackImage(self,filename): self.ctrl.BackgroundImage = Bitmap(filename)
    def SetBounds(self,bounds): self.ctrl.Bounds = bounds
    def SetBorderStyleLine(self): self.ctrl.BorderStyle = BorderStyle.FixedSingle;       
    def SetBorderStyle3D(self): self.ctrl.BorderStyle = BorderStyle.Fixed3D     
    def Invalidate(self): self.ctrl.Invalidate()
    def SetTabIndex(self,i): self.ctrl.TabIndex = i
    def SetFontSize(self,size): self.ctrl.Font = Font(self.ctrl.Font.Name,size,self.ctrl.Font.Style,self.ctrl.Font.Unit)  
    def GetFontSize(self,size): return ctrl.Font.Size
    def SetToolTip(self,tip):
        toolTip = ToolTip()
        toolTip.AutoPopDelay = 5000
        toolTip.InitialDelay = 500 #1000
        toolTip.ReshowDelay = 500
        toolTip.ShowAlways = True
        toolTip.IsBalloon = True
        toolTip.SetToolTip(self.ctrl, tip)
    def SetContextMenu__(self,menu_table):
        menu = ContextMenu()
        for m in menu_table:
            menu.MenuItems.Add(m['name']) 
        self.ContextMenu = menu
    def SetContextMenu(self,menu_table):
        menu = ContextMenuStrip()
        for m in menu_table:
            menu.Items.Add(WinMenu(m['name'],m['item'])) 
        self.ctrl.ContextMenuStrip = menu
    def OnMouseDown(self,sender,e):
        pos = Point(e.X, e.Y)
        if e.Button == MouseButtons.Right:
            self.ContextMenuStrip.Show()

#
# Control
#

class WinLabel(WinControl):
    def __init__(self,h,tool=False):   
        if tool: self.ctrl = ToolStripLabel()
        else: 
            self.ctrl = Label()
            if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        self.ctrl.AutoSize = True
        self.Initialize(h)
        if h.get('label'): self.ctrl.Text = h['label']
        if h.get('icon'):  self.ctrl.Image = Image.FromFile(h['icon'])
        if h.get('handler'): self.ctrl.Click += h['handler']       
    def SetHandler(self,handler): self.ctrl.Click += handler
       
class WinSpacer(WinControl):
    def __init__(self,h,tool=False):   
        if tool: self.ctrl = ToolStripLabel()
        else: self.ctrl = Label()
        if not h.get('width'): h['expand'] = True
        self.ctrl.AutoSize = True
        self.Initialize(h)
                   
class WinButton(WinControl):
    def __init__(self,h,tool=False):   
        if tool: 
            self.ctrl = ToolStripButton()
            self.ctrl.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText
            self.ctrl.TextImageRelation = TextImageRelation.ImageAboveText
        else: 
            self.ctrl = Button()
            self.ctrl.FlatStyle = FlatStyle.Flat
            if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        self.Initialize(h)
        if h.get('label'): self.ctrl.Text = h['label']
        if h.get('icon'):  self.ctrl.Image = Image.FromFile(h['icon'])
        if h.get('handler'): self.ctrl.Click += h['handler']    
    def SetHandler(self,handler): self.ctrl.Click += handler

class WinToggleButton(WinControl):
    def __init__(self,h,tool=False):   
        if tool: 
            self.ctrl = ToolStripCheckBox()
        else: 
            self.ctrl = CheckBox()
            self.ctrl.FlatStyle = FlatStyle.Flat
            if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        self.Initialize(h)
        self.ctrl.Appearance = Appearance.Button
        if h.get('label'): self.ctrl.Text = h['label']
        if h.get('handler'): self.ctrl.Click += h['handler']    
    def SetHandler(self,handler): self.ctrl.Click += handler
    
class WinCheckBox(WinControl):
    def __init__(self,h,tool=False):   
        if tool: 
            self.ctrl = ToolStripCheckBox()
        else: 
            self.ctrl = CheckBox()
            self.ctrl.FlatStyle = FlatStyle.Flat
            if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        self.Initialize(h)
        if h.get('label'): self.ctrl.Text = h['label']
        if h.get('handler'): self.ctrl.Click += h['handler']    
    def SetHandler(self,handler): self.ctrl.Click += handler

class WinImageView(WinControl):
    def __init__(self,h): 
        self.ctrl = PictureBox()
        self.Initialize(h)
        self.ctrl.BorderStyle = BorderStyle.Fixed3D;
        self.ctrl.BorderStyle = BorderStyle.FixedSingle
        #StretchImage, CenterImage, Normal, AutoSize, Zoom
        self.ctrl.SizeMode = PictureBoxSizeMode.Zoom
        if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        if h.get('filename'): self.setImage(h['filename'])
        self.dockFill();    
        
    def setImage(self,filename):
        self.ctrl.Image = Bitmap(filename)

class WinTextBox(WinControl):
    def __init__(self,h,tool=False):
        multiline = False
        multiline = h.get('multiline')
        if tool: self.ctrl = ToolStripTextBox()
        else: 
            self.ctrl = TextBox()
            if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        self.ctrl.Multiline = multiline
        if multiline:
            self.ctrl.ScrollBars = ScrollBars.Both if multiline else ScrollBars.None
        self.ctrl.WordWrap = False
        self.ctrl.AcceptsReturn = True
        self.ctrl.AcceptsTab = True 
        self.ctrl.BorderStyle = BorderStyle.FixedSingle
        self.dockFill();     
        if h.get('handler'): self.ctrl.KeyDown += h['handler']
        if h.get('text'): self.ctrl.Text += h['text']        
    def ClearText(self): self.ctrl.Text = ""
    def AddText(self,text): self.ctrl.Text += text
    def SetMultiLine(v): self.ctrl.Multiline = v
    def SetWordWrap(v): self.ctrl.WordWrap = v
    def SetDrop(v): self.ctrl.AllowDrop = v

class WinStyledText(WinControl):
    def __init__(self,h):
        self.ctrl = ScintillaNET.Scintilla()
        self.Initialize(h)
        self.ctrl.Text = "StyledText"
        self.ctrl.Location = Point(0, 0)
        self.ctrl.Dock = DockStyle.Fill
        self.ctrl.BorderStyle = BorderStyle.FixedSingle
        self.ctrl.WrapMode = WrapMode.None;
        self.ctrl.IndentationGuides = IndentView.LookBoth
        
        nums = self.ctrl.Margins[0]
        nums.Width = 30
        nums.Type = MarginType.Number
        nums.Sensitive = True
        nums.Mask = 0
       
class WinComboBox(WinControl):
    def __init__(self,h,tool=False):   
        if tool: self.ctrl = ToolStripComboBox()
        else: 
            self.ctrl = ComboBox()
            if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        self.Initialize(h)
        self.ctrl.FlatStyle = FlatStyle.Flat
        if h.get('handler'): self.ctrl.SelectedIndexChanged += h['handler']
        if h.get('items'):
            for i in h['items']: self.ctrl.Items.Add(i)
            self.ctrl.SelectedIndex = 0; 
            
class WinTableView(WinControl):
    def __init__(self,h): #cols=None,check=False,grid=False,edit=False):
        self.ctrl = ListView()
        self.Initialize(h)
        self.ctrl.View = View.Details
        self.ctrl.FullRowSelect = True
        self.ctrl.AllowColumnReorder = True
        self.ctrl.Sorting = SortOrder.Ascending
        self.ctrl.BorderStyle = BorderStyle.FixedSingle
        self.dockFill()
        if h.get('grid'): self.ctrl.GridLines = True
        else: self.ctrl.GridLines = False
        if h.get('check'): self.ctrl.CheckBoxes = True
        else: self.ctrl.CheckBoxes = False
        if h.get('edit'):  self.ctrl.LabelEdit = True
        else: self.ctrl.LabelEdit = False
        if h.get('cols'):  self.AddColumns(h['cols'])        

    def getColumnCount(self):
        return self.ctrl.Columns.Count
    def getCount(self):
        return self.ctrl.Items.Count
    def AddColumn(self,text,size=0):
        if size: self.ctrl.Columns.Add(text, size)
        else:    self.ctrl.Columns.Add(text)
    def AddColumns(self,cols):
        if cols:
            for col in cols:
                self.ctrl.Columns.Add(col, -2, HorizontalAlignment.Left )
    def InsertColumn(self,index,text):
        self.ctrl.Columns.Insert(index, text)
    def RemoveColumn(self,col):
        self.ctrl.Columns.RemoveAt(col)
    def AddItems(self,items=None,imgIdx=None, fg=None, bg=None, font=None, grp=None): #Color,Font,ListViewGroup
        if grp: return self.ctrl.Items.Add(ListViewItem(items,imgIdx, fg, bg, font, grp))
        elif font: return self.ctrl.Items.Add(ListViewItem(items,imgIdx, fg, bg, font))
        elif imgIdx: return self.ctrl.Items.Add(ListViewItem(items, imgIdx));
        elif items: return self.ctrl.Items.Add(ListViewItem(items));
    def AddItem(self,text,imgIdx):
        if imgIdx: return self.ctrl.Items.Add(ListViewItem(text, imgIdx))
        else: return self.ctrl.Items.Add(ListViewItem(text))
    def AddSubItem(self,item,text):
        return item.SubItems.Add(text)
    def SelectFirstItem():
        if self.ctrl.Items.Count > 0:
            self.ctrl.Items[0].Selected = True
            self.ctrl.Select()
    def GetItem(self, row, col):
        return self.ctrl.Items[row].SubItems[col].Text
    def getSelectedItems(self):
        itemIndices = []
        for i in range(self.ctrl.SelectedIndices.Count): 
            itemIndices.append(self.ctrl.SelectedIndices[i])
        return itemIndices
    def GetSelectedItemCount(self):
        return self.ctrl.SelectedIndices.Count
    def removeSelectedItems(self):
        for item in self.ctrl.SelectedItems:
            self.ctrl.Items.Remove(item);
    def getCheckedItems(self):
        itemIndices = []
        for i in range(self.ctrl.CheckedIndices.Count): 
            itemIndices.append(self.ctrl.CheckedIndices[i])
        return itemIndices;
    def removeSelectedItems(self):
        for item in self.ctrl.CheckedItems:
            self.ctrl.Items.Remove(item);

class WinWebView(WinControl):
    def __init__(self,h):
        self.ctrl = WebBrowser()
        self.Initialize(h)
        self.dockFill()
        if h.get('url'): self.Go(h['url'])
    def Go(self,url):
        if not url.StartsWith("http://") and not url.StartsWith("https://"):
            url = "http://" + url;
        self.ctrl.Navigate(Uri(url))
    def GetUrl(self): return self.ctrl.Url.ToString()
    def GoHome(self): self.ctrl.GoHome()
    def GoBack(self): self.ctrl.GoBack()
    def GoForward(self): self.ctrl.GoForward()
    def GoSearch(self): self.ctrl.GoSearch()
    def Refresh(self): self.ctrl.Refresh()
    def Stop(self): self.ctrl.Stop()
    def Print(self): self.ctrl.Print()
        
class WinProgressBar(WinControl):
    def __init__(self,h,tool=False):
        if tool: self.ctrl = ToolStripProgressBar()
        else: self.ctrl = ProgressBar()
        self.Initialize(h)
        self.ctrl.Style = ProgressBarStyle.Continuous
        self.ctrl.Minimum = 0
        self.ctrl.Maximum = 100
        self.ctrl.Step = 1
        self.ctrl.Value = 0
        if h.get('value'): self.SetValue(h['value'])
    def SetValue(self,value):
        self.ctrl.Value = value
               
#
# Container
#

class WinGridPanel():
    def __init__(self):
        self.ctrl = TableLayoutPanel()
    def AddRow(self,height=1,expand=False,span=1):
        if expand: self.ctrl.RowStyles.Add(RowStyle(SizeType.StarSize))
        else: self.ctrl.RowStyles.Add(RowStyle(SizeType.AutoSize))
        self.ctrl.RowCount += 1
    def AddColumn(self,width=1,expand=False,span=1):
        if expand: self.ctrl.ColumnStyles.Add(ColumnStyle(SizeType.StarSize))
        else: self.ctrl.ColumnStyles.Add(ColumnStyle(SizeType.AutoSize))
        self.ctrl.ColumnCount += 1
    def AddItem(self,item,row,col,rowspan=1,colspan=1):
        self.ctrl.Controls.Add(item, col, row);
        
class WinVBox():
    def __init__(self):
        self.ctrl = TableLayoutPanel()
        self.ctrl.Dock = DockStyle.Fill
        self.rows = 0
    def AddItem(self,item,attr=None,height=1):
        self.ctrl.RowCount += 1
        self.ctrl.Controls.Add(item, 0, self.ctrl.RowCount-1);
        expand = True if attr and attr.get('expand') else False
        if expand: 
            style = RowStyle()
            style.SizeType = SizeType.Percent
            style.Height = 100
            self.ctrl.RowStyles.Add(style)
        else: 
            #style = RowStyle()
            #style.SizeType = SizeType.Absolute
            #style.Height = 30
            #self.ctrl.RowStyles.Add(style)
            self.ctrl.RowStyles.Add(RowStyle(SizeType.AutoSize))
        
class WinHBox():
    def __init__(self):
        self.ctrl = TableLayoutPanel()
        self.ctrl.Dock = DockStyle.Fill
        self.rows = 0
    def AddItem(self,item,attr=None,height=1):
        self.ctrl.ColumnCount += 1
        self.ctrl.Controls.Add(item, self.ctrl.ColumnCount-1, 0);
        expand = True if attr and attr.get('expand') else False
        if expand: 
            style = ColumnStyle()
            style.SizeType = SizeType.Percent
            style.Width = 100
            self.ctrl.ColumnStyles.Add(style)
        else: 
            self.ctrl.ColumnStyles.Add(ColumnStyle(SizeType.AutoSize))

class WinSplit(WinControl):
    def __init__(self,h):
        self.ctrl = SplitContainer()
        self.Initialize(h)
        self.dockFill();   
        items = h.get('items')
        first = h.get('first')
        vert  = h.get('vertical')
        fixed = h.get('fixed')
        self.items = [ self.ctrl.Panel1, self.ctrl.Panel2 ]
        if items and len(items) >= 2:
            self.AddItem(WinLayout(self.ctrl,items[0]),0)
            self.AddItem(WinLayout(self.ctrl,items[1]),1)
        if first: self.ctrl.SplitterDistance = self.ctrl.ClientSize.Width * first
        if fixed: self.ctrl.IsSplitterFixed = True
        if vert: self.ctrl.Orientation = Orientation.Vertical
        else: self.ctrl.Orientation = Orientation.Horizontal
    def AddItem(self,ctrl,index): 
        self.items[index].Controls.Add(ctrl)

def WinHSplitPane(h):
    h['vertical'] = True
    return WinSplit(h)

def WinVSplitPane(h):
    h['vertical'] = False
    return WinSplit(h)

class WinTabPane(WinControl):
    def __init__(self,h):
        self.ctrl = TabControl()
        self.Initialize(h)
        self.dockFill(); 
        #self.ctrl.Margin =  System.Windows.Thickness(15)
        
        labels = h.get('labels')
        items = h.get('items')
        if labels and items:
            for i in range(0,len(items)):
                self.AddItem( WinLayout(self.ctrl,items[i]), labels[i] )  
    def AddItem(self,layout,label): 
        tab = TabPage()
        tab.Text = label;
        tab.Padding = Padding(10);
        tab.Controls.Add(layout);
        self.ctrl.Controls.Add(tab);


#
# Form
#

def StartThread(handler):
    import threading
    thread = threading.Thread(target=handler)
    thread.daemon = True
    thread.start()

def RunLater(ctrl,handler):
    ctrl.BeginInvoke(System.Action(handler))
     
def WinMenu(name,menu_table):
    ctrl = ToolStripMenuItem(name)
    for m in menu_table:
        if not m.get('name') or m['name'] == '-':
            ctrl.DropDownItems.Add(ToolStripSeparator())
            continue
        if not m.get('item'): continue # Disabled
        if type(m['item']) == list:
            ctrl.DropDownItems.Add(EzMenu(m['name'],m['item']))
        else:
            item = ToolStripMenuItem(m['name'],None,m['item'])
            if m.get('icon'): item.Image = Image.FromFile(m['icon'])
            if m.get('check'): item.Checked = True
            ctrl.DropDownItems.Add(item)
    return ctrl
    
def WinMenuBar(parent,menubar_table):
    ctrl = MenuStrip()
    ctrl.Parent = parent         
    for m in menubar_table:
        ctrl.Items.Add(WinMenu(m['name'],m['item'])) 
    return ctrl
    
def WinToolStatusBar(ctrl,ctrl_table):
    for m in ctrl_table:
        if not m.get('name') or m['name'] == '-':
            ctrl.Items.Add(ToolStripSeparator())
            continue;
        elif m['name'] == "Label" and m.get('label'): tool = WinLabel(m,tool=True)
        elif m['name'] == "Button": tool = WinButton(m,tool=True)
        elif m['name'] == 'TextBox': tool = WinTextBox(m,tool=True)
        elif m['name'] == 'ComboBox': tool = WinComboBox(m,tool=True)
        elif m['name'] == 'ProgressBar': tool = WinProgressBar(m,tool=True)
        else: continue      
        if m.get('key'): _window__ctrl_table[m['key']] = tool
        ctrl.Items.Add(tool.ctrl)
    return ctrl
    
def WinToolBar(parent,tool_table):
    return WinToolStatusBar(ToolStrip(),tool_table)

def WinStatusBar(parent,status_table):
    return WinToolStatusBar(StatusStrip(),status_table)

def WinLayout(parent,content):
    vbox = WinVBox()
    for v in content:
        hbox = WinHBox()
        attr = None
        height = 30
        for h in v:
            name = h.get('name')
            if not name:
                attr = h
                if h.get('height'): height = h['height']
                if h.get('expand'): height = 0
            else:
                f = None
                if   name == 'Label': f = WinLabel(h)
                elif name == 'Spacer': f = WinSpacer(h)
                elif name == 'Button': f = WinButton(h)
                elif name == 'ToggleButton': f = WinToggleButton(h)
                elif name == 'CheckBox': f = WinCheckBox(h)
                elif name == 'ComboBox': f = WinComboBox(h)
                elif name == 'ImageView': f = WinImageView(h)
                elif name == 'TextArea': f = WinTextBox(h)
                elif name == 'TextField': f = WinTextBox(h)
                elif name == 'StyledText': f = WinStyledText(h)
                elif name == 'TableView': f = WinTableView(h)
                elif name == 'WebView': f = WinWebView(h)
                elif name == 'TabPane': f = WinTabPane(h)
                elif name == 'HSplit': f = WinHSplitPane(h)
                elif name == 'VSplit': f = WinVSplitPane(h)
                elif name == 'ProgressBar': f = WinProgressBar(h)
                else: continue
                if h.get('key'): _window__ctrl_table[h['key']] = f
                hbox.AddItem(f.ctrl,h) 
        hbox.ctrl.Height = height       
        vbox.AddItem(hbox.ctrl,attr)
    return vbox.ctrl
    
class WinForm(Form):
    def __init__(self):
        self.Text = 'StyledText Demo'        
        self.Size = Size(640,480)
        self.CenterToScreen()
        self.layout = ToolStripContainer()
        self.layout.TopToolStripPanelVisible = False
        self.layout.RightToolStripPanelVisible = False
        self.layout.BottomToolStripPanelVisible = False
        self.layout.LeftToolStripPanelVisible = False
        self.layout.Dock = DockStyle.Fill
        self.menu = None
        self.tool = None
        self.body = None
        self.status = None
        
    def AddMenu(self,child): self.menu = child
    def AddTool(self,child): self.tool = child        
    def AddBody(self,child): self.body = child
    def AddStatus(self,child): self.status = child
    def SetCreatedHandler(self,handler): self.created = handler
    def Run(self):
        self.Controls.Add(self.layout)
        if self.tool:
            for m in self.tool: 
                self.layout.TopToolStripPanel.Controls.Add(WinToolBar(self,m))
            self.layout.TopToolStripPanelVisible = True
        if self.menu:
            self.layout.TopToolStripPanel.Controls.Add(WinMenuBar(self,self.menu))
            self.layout.TopToolStripPanelVisible = True
        if self.status:
            self.layout.BottomToolStripPanel.Controls.Add(WinStatusBar(self,self.status))
            self.layout.BottomToolStripPanelVisible = True
        if self.body:
            self.layout.ContentPanel.Controls.Add(WinLayout(self,self.body))
            self.layout.ContentPanel.Padding = Padding(10)
        if self.created: self.created(None,None)
        Application.Run(self)

#
# Application
#

def threadHandler():     
    import time
    prog = GetControl('progress')
    for i in range(100):
        print(i)
        RunLater(winApp, lambda : prog.SetValue(i))
        time.sleep(0.1)        
def OnCreated(sender,event):
    print('OnCreated')
    ctrl = GetControl('table')
    ctrl.SetFontSize(12)
    ctrl.AddColumns(("Name","Age"))
    ctrl.AddItems(('Tom',"20"))
    ctrl.AddItems(('Jane',"18"))
    StartThread(threadHandler)    
def onExit(sender, event):
    winApp.Close()
def onCombo(sender, event):
    pass

MainMenu = [
    { 'name' : "File",
      'item' : [
            { 'name' : "Exit" , 'item' : onExit, 'icon' : 'icon/exit.png' },
            { 'name' : "-" ,  },
            { 'name' : "Exit" , 'item' : onExit, 'icon' : 'icon/exit.png' } ]
    }, { 'name' : "Help",
      'item' : [
            { 'name' : "About", 'item' : onExit, 'icon' : 'icon/new.png' } ]
    }]
                    
MainTool = [[
        { "name" : "Label",   "label" : "File:",  },
        { "name" : "TextBox", "handler" : onExit, 'key' : 'text'   },
        { 'name' : "-" ,  },
        { "name" : "Button",  "label" : "Exit", 'icon' : 'icon/exit.png', "handler" : onExit, "tooltip" : "Quit"  },
    ],[
        { "name" : "ComboBox", 'items' : [ 'orange', 'apple' ], 'key' : 'combo', 'handler' : onCombo  },
    ]]

MainStatus = [
        { "name" : "ProgressBar", 'value' : 0, 'key' : 'progress'  },
        { "name" : "ComboBox", 'items' : [ 'orange', 'apple' ], 'key' : 'status', 'handler' : onCombo  },
    ]

tab1 = [[ { "name" : "TextArea", 'multiline' : True, "menu" : MainMenu } ]]
tab2 = [[ { "name" : "TableView", 'key' : 'table', "menu" : MainMenu } ]]
tab3 = [[ { "name" : "ImageView", "filename" : "Lenna.png", "menu" : MainMenu } ]]
tab4 = [[ { "name" : "WebView", "url" : "http://google.co.kr", "menu" : MainMenu } ]]
split1 = [[ 
        { "name" : "StyledText" , "menu" : MainMenu, 'expand' : True},
        { 'expand' : True }
    ]]
split2 = [ [ 
            { "name" : "TabPane", 'fontsize' : 12,
                "items" : [ tab1, tab2, tab3, tab4 ],
                "labels" : [ "Text", "List", "Image", "Web" ],
                'expand' : True },
            { 'expand' : True }
        ] ]

MainBody = [ 
        [
            { "name" : "Label", "label" : "Address", 'width' : 32 },
            { "name" : "TextField", 'expand' : True },
            { "name" : "Button", "label" : "Click", 'tooltip' : "Test Action" },
        ],
        [
            { "name" : "HSplit", "items" : [ split1, split2 ], "first" : 0.5, 'expand' : True },
            { 'expand' : True },
        ],
        [
            { "name" : "Spacer", },
            { "name" : "Button", "label" : "Click", 'tooltip' : "Test Action" },
            { "name" : "ToggleButton", "label" : "Toggle", 'tooltip' : "Test Toggle" },
            { "name" : "CheckBox", "label" : "Check", 'tooltip' : "Test Check" },
            { "name" : "ComboBox", 'items' : [ 'orange', 'apple' ], 'key' : 'status', 'handler' : onCombo  },
            { "name" : "Spacer", 'width' : 16},
        ],
    ]
    
if __name__ == "__main__":     
    winApp = WinForm()
    winApp.AddMenu(MainMenu)
    winApp.AddTool(MainTool)
    winApp.AddStatus(MainStatus)
    winApp.AddBody(MainBody)
    winApp.SetCreatedHandler(OnCreated)
    winApp.Run()
