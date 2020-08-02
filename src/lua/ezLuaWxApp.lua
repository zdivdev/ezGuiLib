require ("ezLuaWxLib")

function fnExit()
    --appWin.frame.Close()
    os.exit(0)
end

function fnAbout()
    Message( appWin.frame, "About ezWxLua", "ezWxLua V0.0.1" )
end

function fnOpen() 
    local path = OpenFileDialog( appWin.frame )
    print(path)
    if path ~= nil then
        appWin.ctrl.text.Clear()
        appWin.ctrl.text.AppendText(path)
    end
end

function fnToggle() 
    local ctrl = GetControl('toggle')
    if ctrl.GetValue() then
        ctrl.SetLabel('On')
    else
        ctrl.SetLabel('Off')
    end
end

function fnCheckBox() 
    local wxCtrl = GetControl('checkbox')
    if wxCtrl.GetValue() then
        wxCtrl.SetLabel('CheckOn')
    else
        wxCtrl.SetLabel('CheckOff')
    end
end


function fnStart() 
    appWin.StartTimer(0)
end

fnTimer_index = 0
function fnTimer()
    appWin.ctrl.list.AddRow( {
        string.format("Time:%d", fnTimer_index),
        string.format("Diff:%d", fnTimer_index),
    } )
    
    appWin.SetStatusText( string.format("Timer: %d", fnTimer_index), 0 )
    fnTimer_index = fnTimer_index + 1
    if fnTimer_index > 300 then
        appWin.StopTimer()
    end
end

function fnChoice()
    Message( appWin.frame, "About Choice", GetControl('choice').GetText() )
end

function fnComboBox()
    Message( appWin.frame, "About ComboBox", GetControl('combobox').GetText())
end

function fnListBox()
    local ctrl = GetControl('listbox')
    local count = ctrl.GetCount()
    local value = ""
    for i = 1, count do
        if ctrl.IsSelected(i-1) then
            value = value .. " " .. ctrl.GetString(i-1)
        end
    end
    Message( appWin.frame, "About ListBox", value)
end

function fnListCtrl()
    local ctrl = GetControl('list')
    local items = ctrl.GetSelectedItems()
    local value = ""
    for i = 1, #items do
        value = value .. " " .. items[i]
    end
    Message( appWin.frame, "About ListCtrl", value)
end

function fnCheckListBox()
    local ctrl = GetControl('checklist')
    local count = ctrl.GetCount()
    local value = ""
    for i = 1, count do
        if ctrl.IsChecked(i-1) then
            value = value .. " " .. ctrl.GetString(i-1)
        end
    end
    Message( appWin.frame, "About ListBox", value)
end

function fnRadioBox()
    local ctrl = GetControl('radiobox')
    Message( appWin.frame, "About RadioBox", tostring(ctrl.GetSelection()) .. " " .. ctrl.GetText())
end

function fnFileDrop(filenames)
    local ctrl = GetControl('text')
    ctrl.SetValue(filenames[1]) 
end

function fnCopyFilePath()
    local fpick = GetControl('filepick')
    local stc = GetControl('stc')
    stc.AppendText( fpick.GetValue() )
end

function fnCopyDirPath()
    local fpick = GetControl('dirpick')
    local stc = GetControl('stc')
    stc.AppendText( fpick.GetValue() )
end

function main()
    local menu = { 
        { Name = "File", Value = {
                { Name = "Exit" , Value = fnExit, Icon='exit' } 
            }
        },
        { Name = "Help", Value = {
                { Name = "About", Value = fnAbout, Icon='help' }
            }
        } 
    }    
    local tool = {
        { Name = "Exit", Value = fnExit, Icon='exit', ToolTip="Quit Program" },
        { Name = "-" },
        { Name = nil, Value = fnAbout, Icon='help', ToolTip="About this Program" },
    }
    local main_layout = { expand=1, border=1 } 
    local list_menu = {
        { Name = "Exit" , Value = fnExit, Icon='exit' }
    }
    local listctrl_menu = {
        { Name = "Show Selected Items" , Value = fnListCtrl }
    }    
    local left = { -- vbox
            { -- hbox
                { name="Table", key="list", menu=listctrl_menu, layout=main_layout },
                { expand=1}
            },
            { expand=1 }
        }
    local right = { --vbox
            { -- hbox
                { name="StyledText", key="stc", layout=main_layout },
                { expand=1 }
            },
            { expand=1}
        }
    local content = { -- vbox
        { -- hbox
            { name="StaticText", label="  File  ",  },
            { name="TextField", key="text", label="Text", layout=main_layout, bgcolor={140,240,140}, filedrop=fnFileDrop },
            { name="Button", label="Open", handler=fnOpen,   },
            { name="ToggleButton", key='toggle', label="On", handler=fnToggle,   },
            { name="CheckBox", key='checkbox', label="CheckOn", handler=fnCheckBox,   },
        },
        { -- hbox
            { name="StaticText", label="  File  ",  },
            { name='FilePicker', key='filepick', label="C:\\a.txt", layout=main_layout },
            { name="Button", label="Copy", handler=fnCopyFilePath,   },
        },        
        { -- hbox
            { name="StaticText", label="  Folder  ",  },
            { name='DirPicker', key='dirpick', label="", layout=main_layout },
            { name="Button", label="Copy", handler=fnCopyDirPath,   },
        },        
        { -- hbox
            { name='Choice', key='choice', items={'apple','grape'}, value=1, handler=fnChoice },
            { name='ComboBox', key='combobox', items={'apple','grape'}, value="apple", handler=fnComboBox },
        },        
        { -- hbox
            { name='ListBox', key='listbox', items={'apple','grape'}, menu=list_menu, handler=fnListBox },
            { name='CheckListBox', key='checklist', items={'apple','grape'}, menu=list_menu, handler=fnCheckListBox },
            { name='RadioBox', key='radiobox', label='RadioBox', items={'apple','grape'}, value=1, menu=list_menu, handler=fnRadioBox },
        },
        { -- hbox
            { name="HSplit", key="split", children={left, right}, layout=main_layout },
            { expand=1 }
        },
        { -- hbox
            { name="Spacer",  },
            { name="Button", label="Start", tooltip="Make dummy list data", handler=fnStart,   },
        },
    }
    local layout = {
        menubar = menu,
        toolbar = tool,
        statusbar = 2,
        content = content,
    }

    appWin = Window("ezWxLua",exit_xpm,layout,800,600,10)
    appWin.SetTimer(fnTimer)
    appWin.ctrl.list.AddColumns( { "Time", "Diff" }, { 150, 150 } )
    appWin.Show()
    appWin.Run()
end

main() 
