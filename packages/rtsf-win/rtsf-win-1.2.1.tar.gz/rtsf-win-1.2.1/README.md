# rtsf-win
基于rtsf测试框架，关键字驱动Windows UI层面，进行自动化的控制及功能测试


## 环境准备

pip install rtsf-win


## 编写测试用例，模板基于rtsf

> 变量引用-> $var    关键字(函数)引用-> ${function}

- 常量的定义， glob_var 和  glob_regx
- 模板常用的关键字，参见 [rtsf](https://github.com/RockFeng0/rtsf)介绍

### 如何获取控件

运行 automation.py -h

![uiautomation-h.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-win-img/uiautomation-h.png)

automation中的参数示例如下:

automation.py -r -d 1 -t 0 ,# print desktop(the root of control tree) and it's children(top level windows) 

automation.py -t 0 -n -m ,# print current active window's controls, show fullname, show more properties

automation.py -t 3 ,# 延时3秒，打印当前激活窗口的树形结构，默认深度为1; 比如，此时打开notepad.exe,等待一会，automation.py会打印Notepad的所有控件树，并保存在 @AutomationLog.txt

```
# 一个简单的示例
import subprocess
import uiautomation as automation
 
print(automation.GetRootControl())
subprocess.Popen('notepad.exe')
notepadWindow = automation.WindowControl(searchDepth = 1, ClassName = 'Notepad')
print(notepadWindow.Name)
notepadWindow.SetTopmost(True)
edit = notepadWindow.EditControl()
edit.SetValue('Hello')
edit.SendKeys('{Ctrl}{End}{Enter}World')
notepadWindow.Close()
notepadWindow.ButtonControl(Name=u'保存(S)').Invoke()
notepadWindow.EditControl(Name="文件名:",AutomationId="1001").SetValue(r'c:\test dir')
notepadWindow.ButtonControl(Name="取消").Invoke()
notepadWindow.Close()
notepadWindow.ButtonControl(Name=u'不保存(N)').Invoke()
```

关于uiautomation的工作原理，参见[详细介绍](http://www.cnblogs.com/Yinkaisheng/p/3444132.html)

另外一个 UI工具, [Inspect.exe](https://docs.microsoft.com/zh-cn/windows/desktop/WinAuto/inspect-objects) 由 Microsoft支持,也能遍历windows UI元素。 不同的是，该工具有界面，而automation是个终端输出。不过，习惯了automation，你会发现更方便

![inspect-exe.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-win-img/inspect-exe.png)


### 基本用例

基本用例，是指没有分层的情况下，简单的测试用例

```
# test_case.yaml
# yaml测试用例，模型示例:
- project:
    name: xxx Window
    module: xxx模块-功能测试
    
- case:
    # id desc 选填，非约定字段
    id: ATP-1
    desc: 测试用例-模板格式的设计-模板（全字段）
    
    # name 必填，需确保唯一性
    name: windows_ui_auto_test_demo_1
    
    # responsible 选填
    responsible: rockfeng0
    
    # tester 选填
    tester: rockfeng0
    
    # 定义正则表达式, 定义的字符串不会解析,选填
    glob_regx:
        rex_open_file: '(文件名.*)'
        rex_hello: 'Hello'
    
    # 定义变量， 效果同 SetVar(name, value),选填
    glob_var:
        program: C:\Windows\System32\notepad.exe
        title: 无标题 - 记事本
        keys: '{Ctrl}{End}{Enter}World'
        text_hello: 'Hello'
        text_save: '保存(S)'
        text_file_path: 'c:\some test dir'
        text_unsave: '不保存(N)'
        
    # pre_command 选填
    pre_command:
        - ${StartApplication($program)}
        - ${TimeSleep(2)}
        - ${SwitchToRootControl()}
        
    # steps 必填
    steps:      
    
        # 在windows中，定位元素            
        - windriver:
            ControlType: WindowControl
            ClassName: Notepad
            Depth: 1
            index: 1
            timeout: 10
            action: ${ActivateWindow()}
            
        - windriver:
            action: ${MoveWindowPos(400, 400)}
            
        - windriver:
            action: ${VerifyProperty(Name, $title)}
        
        - windriver:
            action: ${TimeSleep(2)} 
            
        - windriver:
            action: ${SwitchToCurrentControl()}
                    
        - windriver:
            action: ${SetSearchProperty(ControlType=EditControl, ClassName=Edit)}
            
        - windriver:
            action: ${DyPropertyData(class_name, ClassName)}
        
        - windriver:
            action: ${VerifyVar(class_name, Edit)} 
        
        - windriver:
            action: ${SetValue(Hello)}
                
        - windriver:          
            action: ${SendKeys($keys)}
                           
    # post_command 选填
    post_command:
        - ${DyTextData(text, $rex_hello)}
    
    # verify 选填
    verify:
        - ${VerifyVar(text, $text_hello)} 

```

### 分层用例

- 分层用例，是指模块功能测试的时候，对测试用例进行分层，最小的单元为api，其次为suite，最后组成用例
- 其存放路径、编写规则等，详见 [rtsf](https://github.com/RockFeng0/rtsf)相关介绍
- 示例可以，参见[rtsf-http](https://github.com/RockFeng0/rtsf-http)相关介绍


## 执行测试用例

### windriver 命令

```
# 查看帮助 -h 
windriver -h

# 执行测试用例
windriver C:\f_disk\BaiduNetdiskDownload\rtsf-win\tests\data\test_case.yaml
```

## 测试报告及日志

> 执行结束后，测试用例所在路径，就是report生成的路径



## 封装的关键字(内置函数)

关键字的使用，在前面，有介绍，规则如下
> 变量引用-> $var    关键字(函数)引用-> ${function}

###  元素定位相关操作

<table>
    <tr>
        <th>WinElement methods</th>
        <th>参数</th>
        <th>参数类型</th>
        <th>描述</th>
    </tr>
    <tr>
        <td rowspan="7">SetSearchProperty(**kwargs)</td>
        <td>ControlType</td>
        <td>str or unicode</td>
        <td>always suggest to use, because some ControlType has special pattern functions</td>              
    </tr>
    <tr>
        <td>ClassName</td>
        <td>str or unicode</td>
        <td>控件ClassName</td>
    </tr>
    <tr>
       <td>AutomationId</td>
       <td>str or unicode</td>
       <td>控件AutomationId</td>
   </tr>
   <tr>
       <td>Name</td>
       <td>str or unicode</td>
       <td>控件Name</td>
   </tr>
   <tr>
       <td>SubName</td>
       <td>str or unicode</td>
       <td>控件SubName</td>
   </tr>
   <tr>
       <td>RegexName</td>
       <td>str or unicode, supports regex</td>
       <td>正则表达式，用于控件Name</td>
   </tr>
   <tr>
       <td>Depth</td>
       <td>integer</td>
       <td>控件搜索的深度，默认是最大值:260</td>
   </tr>
   <tr>
        <td>SwitchToCurrentControl()</td>
        <td colspan="2"></td>
        <td>切换到当前控件，以此作为搜索的根控件. **配合SetSearchProperty使用**</td>                
    </tr>
    <tr>
        <td>SwitchToRootControl()</td>
        <td colspan="2"></td>
        <td>切换到根控件(桌面)，以此作为搜索的根控件. **配合SetSearchProperty使用**</td>                
    </tr>   
</table>

                
### WinContext methods --> 用于上下文管理
```
DyPropertyData(var, attr)                   # -> 属性-动态存储变量，适用于，保存UI元素属性值。var-变量名称，attr为UI元素的属性名称，**配合SetSearchProperty使用**
DyTextData(var, regx, index)                # -> 字符串-动态存储变量，适用于，保存文本控件中指定的值。 var-变量名称，regx已编译的正则表达式，index指定索引，默认0

GetVar(name)                                # -> 获取指定变量的值
SetVar(name,value)                          # -> 设置指定变量的值
```

### WinWait methods --> 用于时间的控制
```
TimeSleep(seconds)                   # -> 指定等待时间(秒钟)
WaitForExist(timeout)                # -> 等待元素，timeout设置超时时间，单位秒，**配合SetSearchProperty使用**
WaitForDisappear(timeout)            # -> 等待元素消失，timeout设置超时时间，单位秒，**配合SetSearchProperty使用**
```

### WinVerify methods --> 用于验证
```
VerifyVar(name, expect_value)              # -> 验证变量值，变量name的值是expect_value
VerifyProperty(attr, expect_value)         # -> 验证元素属性attr的值，包含值expect_value,**配合SetSearchProperty使用**
VerifyKeyboardFocusable()                  # -> 验证该控件是否可被键盘聚焦，**配合SetSearchProperty使用**
VerifyKeyboardFocused()                    # -> 验证该控件已被键盘聚焦，**配合SetSearchProperty使用**
VerifyElemEnabled()                        # -> 验证该控件已启用，**配合SetSearchProperty使用**
VerifyNotExist()                           # -> 验证该控件不存在，**配合SetSearchProperty使用**
```

### WinActions methods --> 用于Windows UI（WPF or MFC）操作
```

StartApplication(app_path)                    # -> 运行指定路径（app_path）的应用程序
SetWinStat(state)                             # -> 设置window窗口状态，值：Normal、Maximize、Minimize。隶属WindowPattern，**配合SetSearchProperty使用**
ActivateWindow()                              # -> 激活window窗口并设置焦点。隶属WindowPattern，**配合SetSearchProperty使用**
SetTopmost(is_top_most)                       # -> 设置windows窗口是否置顶，is_top_most默认为True。隶属WindowPattern，**配合SetSearchProperty使用**
MoveWindowPos(x, y)                           # -> 移动windows窗口，默认(x=-1,y=-1)移动到屏幕中心。隶属WindowPattern，**配合SetSearchProperty使用**
CloseWin()                                    # -> 关闭windows窗口。隶属WindowPattern，**配合SetSearchProperty使用**
Invoke()                                      # -> 触发控件Invoke事件，类似于点击。隶属InvokePattern，**配合SetSearchProperty使用**
SetValue(value)                               # -> 触发控件SetValue事件，类似于设置文本值。隶属ValuePattern，**配合SetSearchProperty使用**
CurrentValue()                                # -> 触发控件CurrentValue事件，类似于获取文本值。隶属ValuePattern，**配合SetSearchProperty使用**
ScrollTo(horizontalPercent,verticalPercent)   # -> 触发控件ScrollTo事件，参数值为横纵百分比区间(0,100)，类似滚动滚动条。隶属ScrollPattern，**配合SetSearchProperty使用**      
CheckOn()                                     # -> 触发控件CheckOn事件，勾选复选框。隶属TogglePattern，**配合SetSearchProperty使用**  
CheckOff()                                    # -> 触发控件CheckOff事件，取消勾选复选框。隶属TogglePattern，**配合SetSearchProperty使用**
ExpandOn()                                    # -> 触发控件ExpandOn事件，展开下拉框。隶属ExpandCollapsePattern，**配合SetSearchProperty使用**
ExpandOff()                                   # -> 触发控件ExpandOff事件，收起下拉框。隶属ExpandCollapsePattern，**配合SetSearchProperty使用**  
SelectItem()                                  # -> 触发控件SelectItem事件，在组合框、 列表框、选项卡等展开操作后，选择条目。隶属SelectionItemPattern，**配合SetSearchProperty使用**
Click(ratioX,ratioY,simulateMove)             # -> 在指定控件中，鼠标左键单击，参数都有默认值。隶属Win32API，**配合SetSearchProperty使用**
    示例如：
    Click(): click center and move cursor to control smoothly
    Click(10, 10): click left+10, top+10
    Click(-10, -10): click right-10, bottom-10
    simulateMove: bool, if True, first move cursor to control smoothly

DoubleClick(ratioX,ratioY,simulateMove)       # -> 在指定控件中，鼠标左键双击，用法同Click。隶属Win32API，**配合SetSearchProperty使用**
WheelDown(times)                              # -> 在指定控件中，滚轮向下滑动几次，times参数为整数。隶属Win32API，**配合SetSearchProperty使用**
WheelUp(times)                                # -> 在指定控件中，滚轮向上滑动几次，times参数为整数。隶属Win32API，**配合SetSearchProperty使用**
SendKeys(text)                                # -> 在指定空间中，模拟发送keys,
    示例如：
    #press Ctrl+a, Delete, Ctrl+v, Ctrl+s, Ctrl+Shift+s, Win+e, PageDown
    SendKeys('{Ctrl}a{Delete}{Ctrl}v{Ctrl}s{Ctrl}{Shift}s{Win}e{PageDown}')
    
    #press Ctrl+A+B, type (, press Shift+1+2+3, type ), if () follows a hold key, hold key won't release util ) 
    SendKeys('{Ctrl}(AB)({Shift}(123))')
    
    #press Ctrl+a at the same time, release Ctrl+a, then type a 2 times 
    SendKeys('{Ctrl}{a 3}')
    
    #type a 3 times, type B 5 times 
    SendKeys('{a 3}{B 5}') 
    
    #type: {Hello}abc abc test}}}!a ()()
    SendKeys('{{}Hello{}}abc {a}{b}{c} test{} 3}{!}{a} (){(}{)}')
    SendKeys('0123456789{Enter}')
    SendKeys('ABCDEFGHIJKLMNOPQRSTUVWXYZ{Enter}')
    SendKeys('abcdefghijklmnopqrstuvwxyz{Enter}')
    SendKeys('`~!@#$%^&*()-_=+{Enter}')
    SendKeys('[]{{}{}}\\|;:\'\",<.>/?{Enter}')
        
```


## 自定义，关键字(函数、变量)
> 在case同级目录中，创建  preference.py, 该文件所定义的 变量、函数，可以被动态加载和引用

执行用例的时候，可以使用 变量引用 或者关键字引用的方法，调用，自定义的函数和变量

```
# preference.py 示例

test_var = "hello rtsf."
def test_func():
    return "nihao rtsf."
 
```
