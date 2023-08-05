# rtsf-web
 基于rtsf测试框架和selenium程序框架，关键字驱动Web UI层面，进行自动化的功能测试
 
## 环境准备

### 安装浏览器驱动和下载selenium-server.jar
1. 安装浏览器
2. 下载浏览器官方驱动
3. 设置环境变量，确保驱动可被调用
4. 下载 selenium-server

经过多年的发展WebDriver已经成为了事实上的标准，现在每种浏览器都有独立的官方驱动文件了

Browser | Component
--------|----------
Chrome              |[chromedriver(.exe)](http://chromedriver.storage.googleapis.com/index.html)
Internet Explorer   |[IEDriverServer.exe](http://selenium-release.storage.googleapis.com/index.html)
Edge                |[MicrosoftWebDriver.msi](http://go.microsoft.com/fwlink/?LinkId=619687)
Firefox 47+         |[geckodriver(.exe)](https://github.com/mozilla/geckodriver/releases/)
PhantomJS           |[phantomjs(.exe)](http://phantomjs.org/)
Opera               |[operadriver(.exe)](https://github.com/operasoftware/operachromiumdriver/releases)
Safari              |[SafariDriver.safariextz](http://selenium-release.storage.googleapis.com/index.html)
**selenium-server** |[selenium-server-standalone.jar](http://selenium-release.storage.googleapis.com/index.html)


### 安装rtsf-web
pip install rtsf-web

## 编写测试用例，模板基于rtsf

> 变量引用-> $var    关键字(函数)引用-> ${function}

- 常量的定义， glob_var 和  glob_regx
- 模板常用的关键字，参见 [rtsf](https://github.com/RockFeng0/rtsf)介绍

### 如何获取控件
web控件元素的获取，遵循selenium的规则，可以通过下述方式来定位元素控件:  id、xpath、link text、partial link text、name、tag name、class name、css selector

推荐常用的工具，一般是 Firefox 或者 Chrome 等浏览器的开发者工具。如下图，使用chrome开发模式，采用css和xpath两种方式定位输入框:
![chrome-deployment-tools.gif](https://github.com/RockFeng0/img-folder/blob/master/rtsf-web-img/chrome-deployment-tools.gif)

另一个工具，selenium IDE，官方推出的带有界面的工具
![selenium-ide.png](https://github.com/RockFeng0/img-folder/blob/master/rtsf-web-img/selenium-ide.png)

那么，我为什么不推荐使用，Selenium IDE? 从selenium1.0开始，selenium ide曾经给我惊艳，可以录制、定位、生成脚本等，很优秀，但是selenium2.0后，再也没有用了。一方面由于是基于旧技术实现，在火狐55及之后的新版本上不再支持了，虽然很好用，但是退出历史舞台了； 另一方面，firefox和chrome等浏览器，web开发工具功能强大，安装简单，对元素的定位和调试提供了非常便捷的方式。


### 基本用例

基本用例，是指没有分层的情况下，简单的测试用例

```
# test_case.yaml
- project:
    name: xxx系统
    module: 登陆模块-功能测试
    
- case:
    # id desc 选填，非约定字段
    id: ATP-1    
    desc: 测试用例-模板格式的设计-模板（全字段）
    
    # name 必填，需确保唯一性
    name: web_auto_test_demo
    
    # responsible 选填
    responsible: rockfeng0
    
    # tester 选填
    tester: rockfeng0
    
    # 定义正则表达式, 定义的字符串不会解析
    glob_regx:
        rex_title: '百度一下，你就知道'
    
    # 定义变量， 效果同 SetVar(name, value)
    glob_var:
        url1: https://www.baidu.com
        url2: https://www.sina.com
        
    # pre_command 选填
    pre_command:
        - ${NavigateTo($url1)}
        # - ${DyStrData("title", re.compile(rex_title))}
        # - ${VerifyTitle($title)}
        
    # steps 必填
    steps:        
        # webdriver 测试web ui 时使用
        
        - webdriver:
            action: ${NavigateTo($url2)}
            
        - webdriver:
            action: ${ScrollTo(0, 1000)}
        
        - webdriver:
            action: ${TimeSleep(1)}
        
        - webdriver:
            action: ${Refresh()}
        
        - webdriver:
            action: ${NewTab($url1)}
                
        # 在webdriver中，设置 SetControl参数，定位元素
        - webdriver:
            by: css selector
            value: '#kw'
            index: 0
            timeout: 10
            action: ${SendKeys(123)}
        
        - webdriver:
            action: ${TimeSleep(1)}
            
        # 直接使用 SetControl关键字，定位元素
        - webdriver:
            action: ${SetControl(by=css selector, value=#kw)}
        
        - webdriver:
            action: ${SendKeys(456)}
        
        - webdriver:
            action: ${SetControl(by=id, value=su)}
        
        - webdriver:
            action: ${DyAttrData(id_su_value, value)}
            
        - webdriver:
            action: ${TimeSleep(1)}
        
        - webdriver:
            action: ${WebClose()} 
                   
    # post_command 选填
    post_command:
        - ${WebQuit()}

```

### 分层用例

- 分层用例，是指模块功能测试的时候，对测试用例进行分层，最小的单元为api，其次为suite，最后组成用例
- 其存放路径、编写规则等，详见 [rtsf](https://github.com/RockFeng0/rtsf)相关介绍
- 示例可以，参见[rtsf-http](https://github.com/RockFeng0/rtsf-http)相关介绍


## 执行测试用例

1. 执行前，注意下selenium的执行环境， rtsf-web限定了两中浏览器(chrome和firefox)
2. 谷歌浏览器，按照selenium的文档介绍，自行下载chromedriver.exe并配置
3. 火狐浏览器，按照selenium的文档介绍，版本高的，自行下载geckodriver.exe并配置

> 执行测试用例，有个命令：  wldriver 和 wrdriver

### wldriver(web local driver)本地执行
本地执行测试用例，是指直接使用webdriver中各个浏览器的驱动，比如webdriver.Chrome等

![wldriver-h.png](https://github.com/RockFeng0/img-folder/blob/master/rtsf-web-img/wldriver-h.png)

查看帮助: wldriver -h
选填：
- 设置浏览器(chrome、firefox),默认是谷歌浏览器:      --browser chrome
- 设置浏览器下载文件的路径，默认值是浏览器的设置:    --download-path c:\downloads
- 设置火狐是否使用geckodriver.exe,默认值是False:     --marionette False

```
# run web local case
wldriver --browser chrome C:\f_disk\BaiduNetdiskDownload\rtsf-web\tests\data\test_case.yaml
```

![wldriver-case.png](https://github.com/RockFeng0/img-folder/blob/master/rtsf-web-img/wldriver-case.png)


### wrdriver(web remote driver)远程执行，即selnium grid分布式模式
该模式，遵循selnium grid要求，需要开启hub和node, rtsf-web提供两个命令: wrhub和wrnode

#### 开启hub
简单理解下hub, 玩局域网游戏，我们先要建立主机，那么hub可以理解为主机的概念

![wrhub-command.png](https://github.com/RockFeng0/img-folder/blob/master/rtsf-web-img/wrhub-command.png)

查看帮助: wrhub -h
选填：
- 设置HUB监听端口,默认是4444:       --port 4444
- 指定java.exe路径,默认(已配置java环境变量):    --java-path java

```
# start hub A: 192.168.0.1
wrhub c:\selenium-server-standalone-3.14.0.jar --port 4444 --java-path C:\tmp\Java\jdk1.8.0_161\bin\java.exe
```

#### 开启node
简单理解下node, 游戏主机创建好，玩家需要加入，那么node可以理解为加入主机的玩家

![wrnode-command.png](https://github.com/RockFeng0/img-folder/blob/master/rtsf-web-img/wrnode-command.png)

查看帮助: wrnode -h
选填：
- 设置NODE监听端口,默认是5555:       --port 5555
- 执行连接hub的ip,默认是localhost:   --hub-ip 127.0.0.1
- 执行连接hub的,默认是4444:          --hub-port 4444
- 指定java.exe路径,默认(已配置java环境变量):    --java-path java
  
```
# start node B: 192.168.0.1     这个node机器的ip跟hub A一样，主机也可以是玩家
wrnode c:\selenium-server-standalone-3.14.0.jar --port 5555 --hub-ip 192.168.0.1 --hub-port 4444 --java-path C:\tmp\Java\jdk1.8.0_161\bin\java.exe

# start node C: 192.168.0.2
wrnode c:\selenium-server-standalone-3.14.0.jar --port 5555 --hub-ip 192.168.0.1 --hub-port 4444 --java-path C:\tmp\Java\jdk1.8.0_161\bin\java.exe
```

#### 执行分布式测试
远程执行测试用例，也就是selnium grid分布式执行测试用例，是指使用webdriver.Remote驱动各个浏览器进行测试

简单理解下，创建了主机，玩家也上线了，wrdriver将指定的游戏异步发送给这些玩家

![wrdriver-command.png](https://github.com/RockFeng0/img-folder/blob/master/rtsf-web-img/wrdriver-command.png)

查看帮助: wrdriver -h
选填：
- 设置浏览器(chrome、firefox),默认是谷歌浏览器:      --browser chrome
- 设置浏览器下载文件的路径，默认值是浏览器的设置:    --download-path c:\downloads
- 设置火狐是否使用geckodriver.exe,默认值是False:     --marionette False
- 设置HUB IP,默认是localhost:    --ip 127.0.0.1
- 设置HUB PORT,默认是4444:       --port 4444

```
# run web remote case.  简单理解， 已连接上主机的玩家，会接收到test_case游戏
wrdriver C:\f_disk\BaiduNetdiskDownload\rtsf-web\tests\data\test_case.yaml --browser chrome --ip 192.168.0.1 --port 4444
```

## 测试报告及日志

> 执行结束后，测试用例所在路径，就是report生成的路径


## 封装的关键字(内置函数)

关键字的使用，在前面，有介绍，规则如下
> 变量引用-> $var    关键字(函数)引用-> ${function}

### 浏览器相关操作

Web functions | 参数介绍 | 描述
--------------|----------|-----
AlertAccept()        | |点击alert弹窗的Accept(确定)
AlertDismiss()       | |点击alert弹窗的Dismiss(取消)
AlertSendKeys(value) | |向alert弹窗中输入信息
Back()               | |浏览器后退
Forward()            | |浏览器前进
IESkipCertError()    | |IE Skip SSL Cert Error
Js(script)           | |浏览器执行js脚本
Maximize()           | |浏览器最大化
NavigateTo(url)      | |浏览器打开url
NewTab()             | |浏览器新开标签页，并将所有焦点指向该标签页
PageSource()         | |当前页面源码
Refresh()            | |浏览器刷新当前页面
ScreenShoot(pic_path)| |截图当前页面，并为pic_path
ScrollTo(x,y)        | |移动滚动条至(x,y),如下，X-Y-top :  ScrollTo(、,"0"); X-bottom:  ScrollTo("10000","0");Y-bottom:  ScrollTo("0","10000")
SetWindowSize(width, height)| |设置浏览器窗口大小
SwitchToAlert()             | |切换浏览器焦点至alert弹窗
SwitchToDefaultFrame()      | |切换浏览器焦点至默认frame框, 比如打开的页面有多个iframe的情况
SwitchToDefaultWindow()     | |切换浏览器焦点至默认window窗,比如多个标签页窗的情况
SwitchToNewFrame(frame_name)| |切换浏览器焦点至frame_name框
SwitchToNewWindow()         | |切换浏览器焦点至新window窗
WebClose()                  | |关闭浏览器当前窗口
WebQuit()                   | |Quits the driver and closes every associated window.

###  元素定位相关操作

<table>
    <tr>
        <th>WebElement methods</th>
        <th>参数介绍</th>
        <th>描述</th>
    </tr>
    <tr>
        <td>GetControl()</td>
        <td> </td>
        <td>获取element controls,返回字典，如：{"by":None,"value":None,"index":0,"timeout":10}</td>
    </tr>
    <tr>
        <td rowspan="4">SetControl(by,value,index,timeout)</td>
        <td>by: 指selenium的寻找元素的方式("id", "xpath", "link text","partial link text","name", "tag name", "class name", "css selector")，默认为None</td>
        <td rowspan="4">设置取element controls</td>
    </tr>
    <tr>
        <td>value: 与by配对使用，相应by的值</td>
    </tr>
    <tr>
        <td>index: 索引值，默认为0，即第一个， 如果by,value组合找到很多元素，通过索引index指定一个</td>
    </tr>
    <tr>
       <td>timeout: 超时时间，默认10，即10秒，如果by,value组合寻找元素超过10秒，超时报错</td>
   </tr>    
</table>
                                                   

### WebContext methods --> 用于上下文管理
```
DyAttrData(name,attr)                       # -> 属性-动态存储变量，适用于，保存UI元素属性值。name-变量名称，attr为UI元素的属性名称，**配合SetControl使用**
DyJsonData(name,sequence)                   # -> json-动态存储变量，适用于，保存页面返回json中的指定值。 name-变量名称，sequence是指访问json的序列串
                                                    示例,页面返回 {"a":1,
                                                            "b":[1,2,3,4],
                                                            "c":{"d":5,"e":6},
                                                            "f":{"g":[7,8,9]},
                                                            "h":[{"i":10,"j":11},{"k":12}]
                                                            }
                                                        DyJsonData("var1","a")      #var1值为 1
                                                        DyJsonData("var2","b.3")    #var2值为 4
                                                        DyJsonData("var3","f.g.2")  #var3值为 9
                                                        DyJsonData("var4","h.0.j")  #var4值为 11
DyStrData(name, regx, index)                # -> 字符串-动态存储变量，适用于，保存页面html中指定的值。 name-变量名称，regx已编译的正则表达式，index指定索引，默认0
GetAttribute(attr)                          # -> 获取元素指定属性的值， **配合SetControl使用**
GetText()                                   # -> 获取元素text值，**配合SetControl使用**
GetVar(name)                                # -> 获取指定变量的值
SetVar(name,value)                          # -> 设置指定变量的值
```

### WebWait methods --> 用于时间的控制
```
TimeSleep(seconds)                   # -> 指定等待时间(秒钟)
WaitForAppearing()                   # -> 等待元素出现(可能是隐藏，不可见的)，**配合SetControl使用**
WaitForDisappearing()                # -> 等待元素消失，**配合SetControl使用**
WaitForVisible()                     # -> 等待元素可见，**配合SetControl使用**
```

### WebVerify methods --> 用于验证
```
VerifyAlertText(text)                        # -> 验证alert弹窗，包含文本text
VerifyElemAttr(attr_name,expect_value)       # -> 验证元素属性attr_name的值，包含值expect_value,**配合SetControl使用**
VerifyElemCounts(num)                        # -> 验证元素数量为num,**配合SetControl使用**
VerifyElemEnabled()                          # -> 验证元素是enabled，**配合SetControl使用**
VerifyElemInnerHtml(expect_text)             # -> 验证元素innerHtml中，包含期望文本， **配合SetControl使用**
VerifyElemNotEnabled()                       # -> 验证元素是Not Enabled, **配合SetControl使用**
VerifyElemNotVisible()                       # -> 验证元素是不可见的，**配合SetControl使用**
VerifyElemVisible()                          # -> 验证元素是可见的， **配合SetControl使用**
VerifyTitle(title)                           # -> 验证浏览器标题为title
VerifyURL(url)                               # -> 验证浏览器当前url为期望值
```

### WebActions methods --> 用于浏览器操作
```
Alt(key)                     # -> 在指定元素上执行alt组合事件，**配合SetControl使用**
Backspace()                  # -> 在指定输入框发送回退键，**配合SetControl使用**
Click()                      # -> 在指定元素上，左键点击 1次，**配合SetControl使用**
ClickAndHold()               # -> 在指定元素上， 按压press住，**配合SetControl使用**
Ctrl(key)                    # ->  在指定元素上执行ctrl组合键事件，**配合SetControl使用**
DeSelectByIndex(index)       # -> 通过索引，取消选择下拉框选项，**配合SetControl使用**
DeSelectByText(text)         # -> 通过文本值，取消选择下拉框选项，**配合SetControl使用**
DeSelectByValue(value)       # -> 通过value值，取消选择下拉框选项，**配合SetControl使用**
DoubleClick()                # -> 鼠标左键点击2次，**配合SetControl使用**
Enter()                      # -> 在指定输入框发送回回车键,**配合SetControl使用**
Escape()                     # -> 在指定输入框发送回退出键,**配合SetControl使用**
Focus()                      # -> 在指定输入框发送 Null,用于设置焦点，**配合SetControl使用**
MouseOver()                  # -> 指定元素上，鼠标悬浮，**配合SetControl使用**
MoveAndDropTo()              # -> 暂不支持
ReleaseClick()               # -> 在指定元素上，释放按压操作，**配合SetControl使用**
RightClick()                 # -> 在指定元素上，鼠标右键点击1次，**配合SetControl使用**
SelectByIndex(index)         # -> 通过索引，选择下拉框选项，**配合SetControl使用**
SelectByText(text)           # -> 通过文本值，选择下拉框选项，**配合SetControl使用**
SelectByValue(value)         # -> 通过value值，选择下拉框选项，**配合SetControl使用**
SendKeys(value)              # -> 在指定元素上，输入文本，**配合SetControl使用**
Space()                      # -> 在指定元素上,发送空格，**配合SetControl使用**
Tab()                        # -> 在指定元素上,发送回制表键，**配合SetControl使用**
Upload(filename)             # -> 暂不支持。非原生，需要第三方工具
UploadType(file_path)        # -> 上传文件，仅原生file文件框, 如： <input type="file" ...>, **配合SetControl使用**
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








 