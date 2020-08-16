import os
import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore");
clr.AddReference('WindowsBase')
clr.AddReference('System.Data')
clr.AddReference('System.ComponentModel')
clr.AddReference('System.Windows.Forms')

import System
from System import *
from System.Data import *
from System.Type import GetType
from System.Threading.Tasks import Task
from System.ComponentModel import SortDescription
from System.ComponentModel import ListSortDirection
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Controls.Primitives import *
from System.Windows.Media import *
from System.Windows.Media.Imaging import *
from System.Windows.Media.Effects import *
from System.Windows.Shapes import Rectangle
from System.Windows.Data import Binding
from System.Windows.Data import CollectionViewSource
from System.Windows.Ink import Stroke
from System.Windows.Forms import ( FolderBrowserDialog, DialogResult )
from Microsoft.Win32 import ( OpenFileDialog, SaveFileDialog )

'''
System:: 
    Data, Uri, UriKind, Timers, Threading, IO
System.Windows::
    Application, Window, Clipboard, DataFormats, Visibility, Thickness,
    TextWrapping, HorizontalAlignment, VerticalAlignment, MessageBox,
    MessageBoxButton, MessageBoxResult, GridUnitType, GridLength,
    TextAlignment
System.Windows.Controls::   
    GroupBox, Border, StackPanel, Orientation,
    Grid. RowDefinition. ColumnDefinition, TabControl, TabItem,
    ContextMenu, Menu, MenuItem, ToolTip, Separator, Image
    Label, TextBlock, Button, CheckBox, TextBox, ComboBox, ListBox
    ListView, ListViewItem, TreeView, TreeViewItem, GridView
    GridViewColumn, ProgressBar, DatePicker, Slider, ScrollViewer
    WebBrowser, ToolBarTray, ToolBar, ScrollBarVisibility, Canvas
System.Windows.Controls.Primitives
    ToggleButton, TickPlacement, StatusBar, StatusBarItem
System.Windows.Media    
    Brushes, Stretch, VisualTreeHelper
System.Windows.Media.Imaging
    BitmapImage, BitmapFrame
System.Data
    DataTable DataView DataColumn
System.Windows.Forms
    FolderBrowserDialog DialogResult
'''

#
# Control Table
#

_window__ctrl_table = {}

def GetControl(name):
    return _window__ctrl_table.get(name)

def GetWpfControl(name):
    if _window__ctrl_table.get(name): return _window__ctrl_table[name].ctrl;

def DumpControlTable():
    for k,v in _window__ctrl_table.items():
        print(k,v)
        

#
# Controls
#

class Class:
    def __init__(self,**kwargs): self.__dict__.update(kwargs)
    
def GetHandler(handler):
    return lambda sender,args: handler(Class(sender=sender,args=args))
    '''
    def Handler(sender,args):
        handler(Class(sender=sender,args=args))
    return Handler
    '''
class WpfControl():
    def Initialize(self,h):
        if h.get('key'): _window__ctrl_table[h['key']] = self
        if h.get('tooltip'): self.SetToolTip(h['tooltip'])
        if h.get('menu'): self.SetContextMenu(h['menu'])
        if h.get('width'): self.ctrl.Width = h['width']
        if h.get('height'): self.ctrl.Height = h['height']
        if h.get('drop'): self.SetFileDropHandler(h['drop'])
        if h.get('fontsize'): self.ctrl.FontSize = h['fontsize']
        if self.ctrl.Margin: self.ctrl.Margin  = Thickness(5)
        try:
            if self.ctrl.Padding: self.ctrl.Padding = Thickness(1)
        except:
            pass
    def SetMargin(self,l,t,r,b):
        self.ctrl.Margin = System.Windows.Thickness(l,t,r,b)
    def ShadowEffect(self):
        from System.Windows.Media.Effects import DropShadowBitmapEffect
        self.ctrl.BitmapEffect = DropShadowBitmapEffect()
    def SetFontSize(self,size):
        self.ctrl.FontSize = size
    def SetToolTip(self,tooltip):
        tip = ToolTip()
        tip.Content = tooltip
        self.ctrl.ToolTip = tip
    def SetContextMenu(self,menu_table):
        menu = ContextMenu()
        for m in menu_table:
            menu.Items.Add(WpfMenu(m['name'],m['item']).ctrl)         
        self.ctrl.ContextMenu = menu
    def SetFileDropHandler(self,handler):
        SetFileDropHandler(self.ctrl,handler)

class WpfSpacer(WpfControl):
    def __init__(self,h):
        self.ctrl = Label()
        if not h.get('width'): h['expand'] = True
        self.Initialize(h)
    def SetValue(self,text):
        self.ctrl.Content = text

class WpfLabel(WpfControl):
    def __init__(self,h):
        self.ctrl = Label()
        self.Initialize(h)
        if h.get('label'): self.SetValue(h['label'])
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
    def SetValue(self,text):
        self.ctrl.Content = text

class WpfImageView(WpfControl):
    def __init__(self,h):
        self.ctrl = Label()
        self.Initialize(h)
        self.image = Image()
        self.image.HorizontalAlignment = HorizontalAlignment.Center
        self.image.VerticalAlignment = VerticalAlignment.Center
        if h.get('file'): self.image.Source = BitmapImage(System.Uri(h['file'],System.UriKind.Relative))
        if h.get('stretch'): self.Stretch(h['stretch'])
        else: self.StretchUniform()
        if h.get('size'): self.image.Height = float(h['size']); self.image.Width = float(h['size'])
        if h.get('scroll') and h['scroll']:
            scroll = ScrollViewer()
            scroll.HorizontalScrollBarVisibility = ScrollBarVisibility.Auto;
            scroll.Content = self.image;
            self.ctrl.Content = scroll
        elif h.get('multiple') and h['multiple']:
            stack = StackPanel()
            stack.Orientation = Orientation.Horizontal
            stack.Children.Add(self.image)
            self.ctrl.Content = stack 
        else:
            self.ctrl.Content = self.image       
    def StretchNone(self): self.image.Stretch = Stretch.None
    def StretchFill(self): self.image.Stretch = Stretch.Fill
    def StretchUniform(self): self.image.Stretch = Stretch.Uniform
    def StretchUniformToFill(self): self.image.Stretch = Stretch.UniformToFill
    def Stretch(self,stretch):
        if stretch == 'none': self.StretchNone()
        elif stretch == 'fill': self.StretchFill()
        elif stretch == 'uniform': self.StretchUniform()
        elif stretch == 'uniformfill': self.StretchUniformToFill()

class WpfButton(WpfControl):
    def __init__(self,h):
        self.ctrl = Button()
        self.Initialize(h)
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.Click += GetHandler(h['handler'])
        stack = StackPanel()
        if h.get('orientation') and h['orientation'] == 'vertical': 
            stack.Orientation = Orientation.Vertical
        else:
            stack.Orientation = Orientation.Horizontal
        self.ctrl.Content = stack
        if h.get('image'):
            image = Image()
            image.Source = BitmapImage(System.Uri(h['image'],System.UriKind.Relative))
            image.VerticalAlignment = VerticalAlignment.Center
            image.Stretch = Stretch.Fill #Stretch.None
            if h.get('size'): image.Height = float(h['size']);  image.Width = float(h['size'])
            stack.Children.Add(image)
        if h.get('label'): 
            text = TextBlock()
            text.Text = h['label']
            text.TextAlignment = TextAlignment.Center
            stack.Children.Add(text);            

class WpfToggleButton(WpfControl):
    def __init__(self,h):
        self.ctrl = ToggleButton()
        self.Initialize(h)
        if h.get('label'): self.ctrl.Content = h.get('label')
        if h.get('handler'): self.ctrl.Click += GetHandler(h['handler'] )
    def IsSelected(self):
        return self.ctrl.IsChecked
     
class WpfCheckBox(WpfControl):
    def __init__(self,h):
        self.ctrl = CheckBox()
        self.ctrl.VerticalAlignment = VerticalAlignment.Center
        self.ctrl.VerticalContentAlignment = VerticalAlignment.Center
        self.Initialize(h)
        if h.get('label'): self.ctrl.Content = h['label']
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.Click += GetHandler(h['handler'] )
    def GetValue(self): return self.ctrl.IsChecked

class WpfTextBox(WpfControl):
    def __init__(self,h):
        self.text = TextBox()
        self.ctrl = self.text
        self.Initialize(h)
        if h.get('width'): self.SetWidth(h['width'])
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('multiline'): 
            self.ctrl.AcceptsReturn = True
            self.ctrl.AcceptsTab = True
            self.ctrl.TextWrapping = TextWrapping.NoWrap
            self.ctrl.HorizontalScrollBarVisibility = ScrollBarVisibility.Auto
            self.ctrl.VerticalScrollBarVisibility   = ScrollBarVisibility.Auto
        if h.get('toolbar') and h['toolbar']:
            self.vbox = WpfVBox()
            self.hbox = WpfHBox()
            self.hbox.AddItem(self.Button("Clear", self.ClearHandler))
            self.hbox.AddItem(self.Button("Copy", self.CopyHandler))
            self.hbox.AddItem(self.Button("CopyAll", self.CopyAllHandler))
            self.hbox.AddItem(self.Button("Paste", self.PasteHandler))
            self.hbox.AddItem(self.Button("PasteHtml", self.PasteHtmlHandler))
            self.vbox.AddItem(self.hbox.ctrl)
            self.vbox.AddItem(self.text,{'expand':True})
            self.ctrl = self.vbox.ctrl
    def Button(self,label,handler):
        button = Button()
        button.Content = label
        button.Click += handler
        return button
    def ClearHandler(self,sender,args):
        self.text.Clear()
    def CopyHandler(self,sender,args):
        self.text.Copy()
    def CopyAllHandler(self,sender,args):
        self.text.SelectAll()
        self.text.Copy()
    def PasteHandler(self,sender,args):
        self.text.Paste()
    def PasteHtmlHandler(self,sender,args):
        self.text.Text = ClipboardGetHtmlData()
    def Clear(self):
        self.text.Text = ""
    def GetValue(self):
        return self.text.Text
    def SetValue(self,text):
        self.text.Text = text
    def AppendText(self,text):
        self.text.Text += text
    def SetWidth(self,width):
        self.text.Width = width
    def ScrollToEnd(self):
        self.text.ScrollToEnd()
    def SetWrap(self,wrap):
        self.text.TextWrapping = TextWrapping.Wrap if wrap else TextWrapping.NoWrap
        
class WpfChoiceBox(WpfControl):
    def __init__(self,h):
        self.ctrl = ComboBox()
        self.Initialize(h)
        self.init_ComboBox(h)
    def init_ComboBox(self,h):
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.SelectionChanged += GetHandler(h['handler'] )
        if h.get('items'):
            self.ctrl.ItemsSource = h['items']
            self.ctrl.SelectedIndex = 0     
    def GetValue(self): return self.ctrl.Text
    def GetSelectedItem(self): return self.ctrl.SelectedItem
    def GetAddedItem(self,args): return args.AddedItems[0]

class WpfComboBox(WpfChoiceBox):
    def __init__(self,h):
        self.ctrl = ComboBox()
        self.Initialize(h)
        self.init_ComboBox(h)
        self.ctrl.IsEditable=True
        self.ctrl.IsReadOnly=False

class WpfListBox(WpfControl):
    def __init__(self,h):
        self.ctrl = ListBox()
        self.Initialize(h)
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.SelectionChanged += GetHandler(h['handler'] )
        if h.get('items'):
            self.ctrl.ItemsSource = h['items']
            self.ctrl.SelectedIndex = 0
    def GetValue(self): return self.ctrl.SelectedItem.ToString()
    def GetSelectedItem(self): return self.ctrl.SelectedItem

class WpfTableView(WpfControl):
    def __init__(self,h):
        self.ctrl = ListView()
        self.table = DataTable('table')
        self.cols = []
        self.Initialize(h)
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        #if h.get('handler'): self.ctrl.SelectionChanged += h['handler']
        if h.get('handler'): self.ctrl.SelectionChanged += GetHandler(h['handler'])
        self.grid = GridView()
        self.grid.AllowsColumnReorder = True; 
        self.grid.ColumnHeaderToolTip = "ListView Column Info";   
        if h.get('columns'): 
            items = h['columns']
            widths = None
            labels = None
            if h.get('widths'): widths = h['widths']
            if h.get('labels'): labels = h['labels']
            for i in range(0,len(items)):
                width = widths[i] if widths else None
                label = labels[i] if labels else None
                self.AddColumn(items[i],width,label)     
        self.ctrl.View = self.grid
        self.ctrl.ItemsSource = self.table.DefaultView
        self.ctrl.AddHandler(GridViewColumnHeader.ClickEvent, RoutedEventHandler(self.OnColumnHeaderClick))
        self.sort_dir = ListSortDirection.Ascending
    def Clear(self):
        self.table.Clear()
    def Select(self):
        return self.table.Select()
    def AddColumn(self,name,width=None,label=None):
        col = GridViewColumn()
        if width: col.Width = width
        col.Header = label if label else name
        col.DisplayMemberBinding = Binding(name)
        self.grid.Columns.Add(col); 
        item = DataColumn(name, GetType("System.String"))
        self.table.Columns.Add(item)
        self.cols.append(name)
        '''
        item = DataColumn()
        item.DataType = System.Type.GetType("System.String");
        item.ColumnName = name
        item.AutoIncrement = False
        item.Header = label #if label else name
        item.ReadOnly = False
        item.Unique = False       
        self.table.Columns.Add(item)
        '''
    def AddRow(self,row):
        if len(self.cols) == len(row):
            item = self.table.NewRow()
            for index in range(len(row)):
                item[self.cols[index]] = row[index]
            self.table.Rows.Add(item)
    def AddItem(self,items):
        item = self.table.NewRow()
        for key, value in items.items():
            item[key] = value;
        self.table.Rows.Add(item);
    def GetValue(self): return self.ctrl.SelectedItem
    def GetSelectedItems_org(self): return self.ctrl.SelectedItems
    def GetSelectedItems(self): 
        items = []
        for row in self.ctrl.SelectedItems:
            item = []
            for col in self.cols:
                item.append(row[col])
            items.append(item)
        return items
    def AddSortColumnName(self,col_name,ascending=True):
        view = CollectionViewSource.GetDefaultView(self.ctrl.ItemsSource)
        if ascending:
            view.SortDescriptions.Add(SortDescription(col_name, ListSortDirection.Ascending))
        else:
            view.SortDescriptions.Add(SortDescription(col_name, ListSortDirection.Descending))
    def ColumnSort(self,col_name,direction):
        view = CollectionViewSource.GetDefaultView(self.ctrl.ItemsSource)
        view.SortDescriptions.Clear()
        view.SortDescriptions.Add(SortDescription(col_name, direction))
        view.Refresh()
    def OnColumnHeaderClick(self,sedner,event):
        headerClicked = event.OriginalSource
        columnBinding = headerClicked.Column.DisplayMemberBinding
        if self.sort_dir == ListSortDirection.Descending:
            self.sort_dir = ListSortDirection.Ascending 
            headerClicked.Column.Header = columnBinding.Path.Path + " (+)"
        else: 
            self.sort_dir = ListSortDirection.Descending
            headerClicked.Column.Header = columnBinding.Path.Path + " (-)"
        self.ColumnSort( columnBinding.Path.Path, self.sort_dir ) #headerClicked.Column.Header

        
class WpfTreeView(WpfControl):
    def __init__(self,h):
        self.root = TreeViewItem()
        self.root.Header = h['label']
        self.root.IsExpanded = True
        self.ctrl = TreeView()
        self.ctrl.Items.Add(self.root)
        self.Initialize(h)
        if h.get('handler'): self.ctrl.SelectedItemChanged  += GetHandler(h['handler'] )
    def AddRootItem(self,label):
        return self.AddItem(label)
    def AddItem(self,label,parent=None):
        item = TreeViewItem()
        item.Header = label
        item.IsExpanded = True
        if parent: parent.Items.Add(item)
        else: self.root.Items.Add(item)
        return item
    def GetSelectedIndex(self):
        pass
    def GetSelectedItem(self):
        return self.ctrl.SelectedItem
    def GetSelectedItemText(self):
        return self.ctrl.SelectedItem.Header.ToString()
    def GetSelectedItemPath(self,delim="/"):
        item = self.ctrl.SelectedItem
        return self.GetItemPath(item,delim)
    def GetItemPath(self,item,delim="/"):
        path = item.Header.ToString()
        while type(item.Parent) == TreeViewItem:
            item = item.Parent
            path = item.Header.ToString() + delim + path
        return path
    def GetParentItem(self,item):
        return item.Parent
    def GetItemValue(self,item):
        return item.ToString()
    def IsRootItem(self,item):
        return type(item.Parent) == TreeView

class WpfWebView(WpfControl):
    def __init__(self,h):
        self.web = WebBrowser()
        self.ctrl = self.web
        self.web.Navigated += self.LoadedHandler
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        self.Initialize(h)
        if h.get('toolbar') and h['toolbar']:
            self.vbox = WpfVBox()
            self.hbox = WpfHBox()
            self.text = TextBox()
            self.hbox.AddItem(self.Button("<-", self.BackHandler))
            self.hbox.AddItem(self.Button("->", self.ForwardHandler))
            self.hbox.AddItem(self.Button("<>", self.RefreshHandler))
            self.hbox.AddItem(self.text, {'expand':True})
            self.hbox.AddItem(self.Button("Go", self.GoHandler))
            self.vbox.AddItem(self.hbox.ctrl)
            self.vbox.AddItem(self.web,{'expand':True})
            self.ctrl = self.vbox.ctrl
        if h.get('uri'): self.Go(h['uri'])
        
    def Button(self,label,handler):
        button = Button()
        button.Content = label
        button.Click += handler
        return button
    def LoadedHandler(self,sender,args):
        self.text.Text = self.web.Source.ToString()
    def GoHandler(self,sender,args):
        uri = self.text.Text
        if not uri.startswith('http'):
            uri = "http://" + uri
            self.text.Text = uri
        self.Go(uri)
    def BackHandler(self,sender,args): self.Back()
    def ForwardHandler(self,sender,args): self.Forward()
    def RefreshHandler(self,sender,args): self.Refresh()
    def Load(self,html): self.web.NavigateToString(html);
    def Go(self,uri): self.web.Navigate(System.Uri(uri, System.UriKind.RelativeOrAbsolute));
    def Back(self):
        if self.web.CanGoBack: self.web.GoBack()
    def Forward(self):
        if self.web.CanGoForward: self.web.GoForward()
    def Refresh(self):
        self.web.Refresh()
    def Html(self): return self.web.Document.documentElement.InnerHtml
           
class WpfProgressBar(WpfControl):
    def __init__(self,h):   
        self.ctrl = ProgressBar()
        #self.ctrl.IsIndeterminate = True
        #self.ctrl.Margin = new Thickness(10,0,10,10);
        self.ctrl.Visibility = Visibility.Visible;
        self.ctrl.Width = 100;
        self.ctrl.Height = 16;
        #self.ctrl.Foreground = System.Windows.Media.Brushes.Green;
        #self.ctrl.Background = System.Windows.Media.Brushes.Red;
        #self.ctrl.Style = ProgressBarStyle.Continuous #Marquee
        self.ctrl.Maximum = 100
        self.ctrl.Value = 0
        #self.ctrl.FlowDirection = FlowDirection.LeftToRight
        self.Initialize(h)
    def GetValue(self):
        return self.ctrl.Value
    def SetValue(self,v):
        self.ctrl.Value = v


class WpfDatePicker(WpfControl):
    def __init__(self,h):   
        self.ctrl = DatePicker()
        self.Initialize(h)
        if h.get('handler'): self.ctrl.SelectedDateChanged += GetHandler(h['handler'] )
    def GetValue(self):
        return self.ctrl.Text
    def SetValue(self,v):
        self.ctrl.Text = v

class WpfSlider(WpfControl):
    def __init__(self,h):   
        self.ctrl = Slider()
        self.Initialize(h)
        if h.get('handler'): self.ctrl.ValueChanged += GetHandler(h['handler'] )
        self.ctrl.Width = 100;
        self.ctrl.Height = 16;        
        self.ctrl.Minimum = h['min'] if h.get('min') else 0
        self.ctrl.Maximum = h['max'] if h.get('max') else 100     
        self.ctrl.Value = h['value'] if h.get('value') else 0
        self.ctrl.SmallChange = 1
        self.ctrl.LargeChange = 10
        self.ctrl.TickPlacement = TickPlacement.BottomRight
        self.ctrl.TickFrequency = 10
    def GetValue(self):
        return self.ctrl.Value
    def SetValue(self,v):
        self.ctrl.Value = v
              
#
# Containers
#

class WpfBorderGrid():
    def __init__(self):
        self.grid = Grid()
        self.ctrl = Border()
        self.ctrl.HorizontalAlignment = HorizontalAlignment.Left
        self.ctrl.VerticalAlignment = VerticalAlignment.Top
        #border.BorderBrush = BorderBrush.Black
        self.ctrl.BorderThickness = 2
        self.ctrl.Content = self.grid
    def AddRow(self,height=1,expand=False,span=1):
        if expand: length = GridLength(height, GridUnitType.Star)
        else:      length = GridLength(height, GridUnitType.Auto)
        self.grid.RowDefinitions.Add(RowDefinition(Height = length))
    def AddColumn(self,width=1,expand=False,span=1):
        if expand: length = GridLength(width, GridUnitType.Star)
        else:      length = GridLength(width, GridUnitType.Auto)
        self.grid.ColumnDefinitions.Add(ColumnDefinition(Width = length))
    def AddItem(self,item,row,col,rowspan=1,colspan=1):
        Grid.SetRow(item, row);
        Grid.SetColumn(item, col);
        self.grid.Children.Add(item)
        if rowspan > 1: item.SetValue(Grid.RowSpanProperty, rowspan);
        if colspan > 1: item.SetValue(Grid.ColumnSpanProperty, colspan);
        
class WpfGrid():
    def __init__(self):
        self.ctrl = Grid()
    def AddRow(self,height=1,expand=False,span=1):
        if expand: length = GridLength(height, GridUnitType.Star)
        else:      length = GridLength(height, GridUnitType.Auto)
        self.ctrl.RowDefinitions.Add(RowDefinition(Height = length))
    def AddColumn(self,width=1,expand=False,span=1):
        if expand: length = GridLength(width, GridUnitType.Star)
        else:      length = GridLength(width, GridUnitType.Auto)
        self.ctrl.ColumnDefinitions.Add(ColumnDefinition(Width = length))
    def AddItem(self,item,row,col,rowspan=1,colspan=1):
        Grid.SetRow(item, row);
        Grid.SetColumn(item, col);
        self.ctrl.Children.Add(item)
        if rowspan > 1: item.SetValue(Grid.RowSpanProperty, rowspan);
        if colspan > 1: item.SetValue(Grid.ColumnSpanProperty, colspan);
        
class WpfVBox():
    def __init__(self):
        self.ctrl = Grid()
        self.ctrl.Margin = Thickness(1)
        self.rows = 0
    def AddItem(self,item,attr=None,height=1):
        if attr and attr.get('expand'): length = GridLength(height, GridUnitType.Star)
        else: length = GridLength(height, GridUnitType.Auto)
        self.ctrl.RowDefinitions.Add(RowDefinition(Height = length))
        Grid.SetRow(item, self.rows);
        if attr and attr.get('group'):
            group = GroupBox()
            group.Header = attr['group']
            group.AddChild(item)
            Grid.SetRow(group, self.rows);
            self.ctrl.Children.Add(group)
        else:
            if attr and attr.get('border') and attr['border']:
                rect = Rectangle()
                rect.Stroke = Brushes.Gray
                rect.Fill = Brushes.Transparent
                Grid.SetRow(rect, self.rows);
                self.ctrl.Children.Add(rect)
            self.ctrl.Children.Add(item)
        self.rows = self.rows + 1
    def AddSplitter(self,width=1):
        from System.Windows.Controls import GridSplitter
        item = GridSplitter()
        item.HorizontalAlignment = HorizontalAlignment.Stretch
        item.VerticalAlignment = VerticalAlignment.Center
        item.ShowsPreview = True
        item.Height = 5
        length = GridLength(width, GridUnitType.Auto)
        self.ctrl.RowDefinitions.Add(RowDefinition(Height = length))
        Grid.SetRow(item, self.rows);
        self.ctrl.Children.Add(item)
        self.rows = self.rows + 1
                 
class WpfHBox():
    def __init__(self):
        self.ctrl = Grid()
        self.ctrl.Margin = Thickness(1)
        self.cols = 0
    def AddItem(self,item,attr=None,width=1):
        if attr and attr.get('expand'): length = GridLength(width, GridUnitType.Star)
        else: length = GridLength(width, GridUnitType.Auto)
        self.ctrl.ColumnDefinitions.Add(ColumnDefinition(Width = length))
        Grid.SetColumn(item, self.cols);
        if attr and attr.get('group'):
            group = GroupBox()
            group.Header = attr['group']
            group.AddChild(item)
            Grid.SetColumn(group, self.cols);
            self.ctrl.Children.Add(group)
        else:
            if attr and attr.get('border') and attr['border']:
                rect = Rectangle()
                rect.Stroke = Brushes.Gray
                rect.Fill = Brushes.Transparent
                Grid.SetColumn(rect, self.cols);
                self.ctrl.Children.Add(rect)
            self.ctrl.Children.Add(item)
        self.cols = self.cols + 1
    def AddSplitter(self,width=1):
        from System.Windows.Controls import GridSplitter
        item = GridSplitter()
        item.HorizontalAlignment = HorizontalAlignment.Center
        item.VerticalAlignment = VerticalAlignment.Stretch
        item.ShowsPreview = True
        item.Width = 5
        length = GridLength(width, GridUnitType.Auto)
        self.ctrl.ColumnDefinitions.Add(ColumnDefinition(Width = length))
        Grid.SetColumn(item, self.cols);
        self.ctrl.Children.Add(item)
        self.cols = self.cols + 1

class WpfBorder():
    def __init__(self):
        self.ctrl = Border()
        self.ctrl.HorizontalAlignment = HorizontalAlignment.Left
        self.ctrl.VerticalAlignment = VerticalAlignment.Top
        self.ctrl.Background = Brushes.SkyBlue
        self.ctrl.BorderBrush = Brushes.Black
        self.ctrl.BorderThickness = Thickness(1)
    def SetChild(self,ctrl):
        self.ctrl.Child = ctrl
        
class WpfStackBox():
    def __init__(self):
        self.ctrl = StackPanel()
        self.ctrl.Margin = Thickness(1)
    def Add(self,item):
        self.ctrl.Children.Add(item)

class WpfGroupBox():
    def __init__(self,h):
        self.ctrl = GroupBox()
        if h.get('label'): self.ctrl.Header = h['label']
        if h.get('item'):
            self.AddItem(WpfLayout(h['item']))   
    def AddItem(self,item):
        self.ctrl.AddChild(item)
        
class WpfTabPane():
    def __init__(self,h):
        self.ctrl = TabControl()
        self.ctrl.Margin =  System.Windows.Thickness(15)
        labels = h.get('labels')
        items = h.get('items')
        if labels and items:
            for i in range(0,len(items)):
                self.AddItem( labels[i], WpfLayout(items[i]))  
    def AddItem(self,label,layout):
        tab = TabItem()
        tab.Header = label
        tab.Content = layout
        self.ctrl.Items.Add(tab)

class WpfHSplitPane():
    def __init__(self,h):
        self.box = WpfHBox()
        self.ctrl = self.box.ctrl
        self.ctrl.Margin = Thickness(1)
        items = h.get('items')
        width = [ 1, 1 ]
        if h.get('first'):
            width[0] = float(h['first']) * 10
            width[1] = 10 - width[0] 
        self.box.AddItem(WpfLayout(items[0]),{'expand':True},width[0])
        self.box.AddSplitter()
        self.box.AddItem(WpfLayout(items[1]),{'expand':True},width[1])  

class WpfVSplitPane():
    def __init__(self,h):
        self.box = WpfVBox()
        self.ctrl = self.box.ctrl
        self.ctrl.Margin =  System.Windows.Thickness(1)
        items = h.get('items')
        height = [ 1, 1 ]
        if h.get('first'):
            height[0] = float(h['first']) * 10
            height[1] = 10 - height[0] 
        self.box.AddItem(WpfLayout(items[0]),{'expand':True},height[0])
        self.box.AddSplitter()
        self.box.AddItem(WpfLayout(items[1]),{'expand':True},height[1])  

class WpfMenu():
    def __init__(self,name,menu_table):
        self.ctrl = MenuItem()
        self.ctrl.Header = name;        
        for m in menu_table:
            if not m.get('name') or m['name'] == '-':
                self.ctrl.Items.Add(Separator())
                continue
            if not m.get('item'): continue # Disabled
            if type(m['item']) == list:
                self.ctrl.Items.Add(WpfMenu(m['name'],m['item']).ctrl)
            else:
                item = MenuItem()
                if m.get('name'): item.Header = m['name']
                if m.get('image'):
                    image = Image()
                    image.Source = BitmapImage(System.Uri(m['image'],System.UriKind.Relative))
                    item.Icon = image
                if m.get('item'): item.Click += m['item']
                if m.get('tooltip'): 
                    tooltip =  ToolTip()
                    tooltip.Content = m['tooltip']
                    item.ToolTip = tooltip
                self.ctrl.Items.Add(item)

def WpfMenuBar(menu_table):
    ctrl = Menu()
    ctrl.HorizontalAlignment = System.Windows.HorizontalAlignment.Stretch;
    ctrl.VerticalAlignment = System.Windows.VerticalAlignment.Top;
    for m in menu_table:
        ctrl.Items.Add(WpfMenu(m['name'],m['item']).ctrl) 
    return ctrl

def WpfToolBar(tool_table):
    tray = ToolBarTray()
    for v in tool_table:
        ctrl = ToolBar()
        ctrl.HorizontalAlignment = System.Windows.HorizontalAlignment.Stretch;
        ctrl.VerticalAlignment = System.Windows.VerticalAlignment.Bottom;
        for h in v:
            name  = h['name']
            f = None
            if   name == 'Label': f = WpfLabel(h)
            elif name == 'Button': f = WpfButton(h)     
            elif name == 'ToggleButton': f = WpfToggleButton(h)
            elif name == 'CheckBox': f = WpfCheckBox(h)
            elif name == 'TextField': f = WpfTextBox(h)
            elif name == 'ChoiceBox': f = WpfChoiceBox(h)
            elif name == 'ComboBox': f = WpfComboBox(h)
            elif name == 'ProgressBar': f = WpfProgressBar(h)
            elif name == 'DatePicker': f = WpfDatePicker(h)
            elif name == 'Slider': f = WpfSlider(h)
            if f: ctrl.Items.Add(f.ctrl)
        tray.AddChild(ctrl)
    return tray

def WpfStatusBar(status_table):
    ctrl = StatusBar()
    ctrl.HorizontalAlignment = System.Windows.HorizontalAlignment.Stretch;
    ctrl.VerticalAlignment = System.Windows.VerticalAlignment.Bottom;
    for h in status_table:
        if h.get('name'):
            name  = h['name']
            if   name == 'Label': f = WpfLabel(h)
            elif name == 'Button': f = WpfButton(h)
            elif name == 'ToggleButton': f = WpfToggleButton(h)
            elif name == 'CheckBox': f = WpfCheckBox(h)
            elif name == 'TextField': f = WpfTextBox(h)
            elif name == 'ChoiceBox': f = WpfChoiceBox(h)
            elif name == 'ComboBox': f = WpfComboBox(h)
            elif name == 'ProgressBar': f = WpfProgressBar(h)
            elif name == 'DatePicker': f = WpfDatePicker(h)
            elif name == 'Slider': f = WpfSlider(h)
            item = StatusBarItem()
            item.Content = f.ctrl        
            ctrl.Items.Add(item)
    return ctrl

def WpfLayout(content):
    vbox = WpfVBox()
    for v in content:
        hbox = WpfHBox()
        attr = None
        for h in v:
            name = h.get('name')
            if not name:
                attr = h
            else:
                if   name == 'Spacer': f = WpfSpacer(h)
                elif name == 'Label': f = WpfLabel(h)
                elif name == 'ImageView': f = WpfImageView(h)
                elif name == 'Button': f = WpfButton(h)
                elif name == 'ToggleButton': f = WpfToggleButton(h)
                elif name == 'CheckBox': f = WpfCheckBox(h)
                elif name == 'TextField': f = WpfTextBox(h)
                elif name == 'ChoiceBox': f = WpfChoiceBox(h)
                elif name == 'ComboBox': f = WpfComboBox(h)
                elif name == 'ProgressBar': f = WpfProgressBar(h)
                elif name == 'DatePicker': f = WpfDatePicker(h)
                elif name == 'Slider': f = WpfSlider(h)
                elif name == 'TextArea': h['multiline'] = True; f = WpfTextBox(h)
                elif name == 'ListBox': f = WpfListBox(h)
                elif name == 'TreeView': f = WpfTreeView(h)
                elif name == 'TableView': f = WpfTableView(h)
                elif name == 'WebView': f = WpfWebView(h)
                elif name == 'GroupBox': f = WpfGroupBox(h)
                elif name == 'TabPane': f = WpfTabPane(h)
                elif name == 'HSplit': f = WpfHSplitPane(h)
                elif name == 'VSplit': f = WpfVSplitPane(h)
                else: continue
                hbox.AddItem(f.ctrl,h)
            '''
            elif name == 'ScrollImageView': f = WpfScrollImageView(h,parent)
            elif name == 'ProgressBar': f = WpfProgressBar(h)
            '''            
        vbox.AddItem(hbox.ctrl,attr)
    return vbox.ctrl

#
# API
#

#
# Thread, Execute
#

def RunLater(ctrl,handler):
    ctrl.Dispatcher.BeginInvoke(System.Action(handler))

def Execute(cmd):
    import subprocess
    try:
        out = subprocess.check_output(cmd)
        return 0,out
    except:
        return -1,""
                
def StartTimer(handler,msec):
    aTimer = System.Timers.Timer(msec)
    aTimer.Elapsed += GetHandler(handler)
    aTimer.AutoReset = True
    #aTimer.Enabled = True
    aTimer.Start()
    #aTimer.Stop();
    #aTimer.Dispose();
           
def StartThread(handler,args=()):
    import threading
    thread = threading.Thread(target=handler,args=args)
    thread.daemon = True
    thread.start()

def StartTask(handler):
    Task.Factory.StartNew(handler) 

#
# Drag and Drop
#

def DragEnter(sender, event):
    if event.Data.GetDataPresent(DataFormats.FileDrop):
        event.Effect = DragDropEffects.All
    else:
        event.Effect = DragDropEffects.None

def DragOver(sender, event):
    if event.Data.GetDataPresent(DataFormats.FileDrop):
        event.Effect = DragDropEffects.Copy
    
def DragDropped(handler):
    def DropHandler(sender, event):
        if event.Data.GetDataPresent(DataFormats.FileDrop):
            files = event.Data.GetData(DataFormats.FileDrop)
            handler(files)
    return DropHandler
    
def SetFileDropHandler(ctrl,handler):
    ctrl.AllowDrop = True 
    #ctrl.DragEnter += DragEnter
    #ctrl.DragOver += DragOver
    ctrl.Drop += DragDropped(handler)

#
# Clipboard
#

def ClipboardGetTextData():
    return Clipboard.GetData(DataFormats.Text)

def ClipboardSetTextData(text):
    Clipboard.SetData(DataFormats.Text, text)

def ClipboardGetHtmlData():
    return Clipboard.GetData(DataFormats.Html)

def ClipboardSetHtmlData(text):
    Clipboard.SetData(DataFormats.Html, text)

def ClipboardGetText():
    return Clipboard.GetText()

def ClipboardSetText(text):
    Clipboard.SetText(text)
       

#
# Dialog
#

def AlertDialog(message,title=None):
    if title: MessageBox.Show(message,title)
    else: MessageBox.Show(message)

def YesNoDialog(message,title,icon=System.Windows.MessageBoxImage.Information):
    rv = MessageBox.Show(message,title,MessageBoxButton.YesNo,icon)
    if rv == MessageBoxResult.Yes: return True
    else: return False

def YesNoCancelDialog(message,title,icon=System.Windows.MessageBoxImage.Information):
    rv = MessageBox.Show(message,title,MessageBoxButton.YesNoCancel,icon)
    if rv == MessageBoxResult.Yes: return True
    elif rv == MessageBoxResult.No: return False
    else: return None
    
def FileOpenDialog(initialFile=None,multiselect=False):
    dlg = OpenFileDialog()
    dlg.Multiselect = multiselect
    dlg.DefaultExt = ".txt"; # Default file extension
    dlg.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
    if initialFile:
        dlg.InitialDirectory = System.IO.Path.GetDirectoryName(initialFile)
        dlg.FileName = System.IO.Path.GetFileName(initialFile)
        #Directory.GetParent(initialFile) #Path.GetFileName(initialFile)
    if dlg.ShowDialog() == True:
        return dlg.FileNames 

def FileSaveDialog(initialFile=None):
    dlg = SaveFileDialog()
    dlg.DefaultExt = ".txt"; # Default file extension
    dlg.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
    if initialFile:
        dlg.InitialDirectory = System.IO.Path.GetDirectoryName(initialFile)
        dlg.FileName = System.IO.Path.GetFileName(initialFile)
    if dlg.ShowDialog() == True:
        return dlg.FileNames 

def DirectoryOpenDialog(initialDirectory=None):
    dlg = FolderBrowserDialog()
    dlg.ShowNewFolderButton = True
    if initialDirectory:
        dlg.SelectedPath = initialDirectory #Path.GetFileName(initialFile)
    if dlg.ShowDialog() != DialogResult.Cancel:
        return dlg.SelectedPath 

#
# Window
#

class Window(System.Windows.Window):  
    def __init__(self,title="",width=800,height=600):
        print('WpfWindow.__init__()')
        self.ctrl = None
        self.stage = None
        self.createdHandler = None
        self.closeHandler = None
        self.title = None
        self.icon = None
        self.width = 800
        self.height = 600
        self.menu = None
        self.tool = None
        self.status = None
        self.content = None
    def Popup(self):
        self.box = WpfVBox()
        if self.menu: self.box.AddItem(WpfMenuBar(self.menu),{'expand':False})
        if self.tool: self.box.AddItem(WpfToolBar(self.tool),{'expand':False})
        if self.content: self.box.AddItem(WpfLayout(self.content),{'expand':True})
        if self.status: self.box.AddItem(WpfStatusBar(self.status),{'expand':False})
        self.Content = self.box.ctrl
        if self.createdHandler: self.createdHandler()
        self.Show()
    def Run(self):
        self.Popup()
        Application().Run(self) 
    def SetTitle(self,title): self.Title = title
    def SetSize(self,width,height): self.Width = width; self.Height = height
    def SetIcon(self,icon): self.Icon = BitmapFrame.Create(System.Uri(icon, System.UriKind.RelativeOrAbsolute)) if os.path.exists(icon) else None
    def SetMenuBar(self,menu): self.menu = menu
    def SetToolBar(self,tool): self.tool = tool
    def SetStatusBar(self,status): self.status = status
    def SetContent(self,content): self.content = content
    def SetCreatedHandler(self,handler): self.createdHandler = handler
    def SetCloseHandler(self,handler): self.Closing += GetHandler(handler)
    def SetFileDropHandler(self,handler): SetFileDropHandler(self,handler)
