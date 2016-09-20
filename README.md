# VRL使用文档

VRL（Vulnerability Research Lab）的研究目的在于，在 Linux 平台下测试并验证已有漏洞，分析开启不同防御机制的情况下对攻击过程的影响，学习和熟悉漏洞利用原理与技巧，尝试研究出新的攻击或防御方法。

## 测试环境
Ubuntu 16.04 LTS (64 bits)    

漏洞程序主要使用 C 或 C++ 编写，对应脚本主要使用 Python 2.7 编写。   

可能会用到的 Python 第三方库有:

- [cmd2](https://pythonhosted.org/cmd2/)
- [pwntools](https://github.com/Gallopsled/pwntools)等

环境配置参见[环境配置向导](documents/环境配置向导.md)

## 平台架构
VRL平台大致分为五个部分。

- UI：用户交互，整合所有其他模块。所有的漏洞程序，攻击程序和设置、加工由VRL.py调用。
- Vulnerabilities：漏洞程序库，包括漏洞程序，漏洞程序调用脚本，程序源码，说明文档等。
- Exploits： Exploits库，包括利用程序，说明文档等。
- Payloads： 供Exploits选用（如果支持）的Payload库。
- Misc: 其他工具，加工paylaods等。

## 常用功能和使用方法

VRL平台可以分别载入Exploit，Vulnerability和Payload，并修改其设置。

*命令行支持多种自动补全，在输入较长的命令/参数/脚本名称时可以尝试自动补全。*

###主要功能

+ 状态显示：
    + 在命令行左端，会显示当前状态。![prompt.jpg](documents/pic/prompt.jpg)
    + V表示Vulnerability，E表示Exploit，P表示Payload
    + 灰色表示没有选择，绿色表示已经选择，蓝色表示当前不可用。

+ 列出可用Exploits，Vulnerability，Payload和Tools：
    + `show exploits|vulnerabilities|payloads|tools`
        - 所有参数你可以简写至前几个字母
        - 当VRL载入时，会自动扫描目录下符合格式的Exploit等脚本，如果你不希望重启VRL并加入新的模块，使用reload指令。

+ 选择Exploit或Vulnerability：
    + `useexp expname` 或`use e expname` `use exp expname`
    + `usevul vulname` 或`use v vulname` `use vul vulname`
    + `use name`将使用同一name尝试载入Exploit和Vulnerability。
        + *Tip：当更换Exploit或Vulnerability时，VRL会将Exploit的默认设置同步到Vulnerability中。*
        
+ 设置Exploit和Vulnerability的选项：
    + `show options` 显示所有选项（包括Exploit和Vulnerability）。
    + `set key value` 将改变key为value。这里`value`将作为字符串赋值，在脚本中注意这一属性。这里设计上认为Exploit和Vulnerability中相同名称的key应该保持相同值。在脚本中注意这一设计。
    + 不希望同时被更改option可以使用`setexp key value`和`setvul key value`，（更建议在设计时使用不同的属性名称）。

+ 选择payload：
    + `usepay payname` 或 `use p payname` `use pay payname` 选择payload，在这之前要确定你使用的Exploit支持更换Payload。
    + 这一命令将列出Exploit对于Payload的要求和当前Payload的信息供对比，询问是否使用。所以你并不需要单独的命令查看payload信息，如果不符合，就输入`n`放弃。
        + 目前仅支持一个Exploit中只包含一个Payload块，多个Payload连用请使用工具连接，但分离的多个Payload并不支持。因为暂时没有遇到需要的情况。

+ 运行Exploit或Vulnerability：
    + `runexp` 或`run e` `run exp`
    + `runvul` 或`run v` `run vul`
    + `run` 将尝试先运行Vulnerability，再运行Exploit。

###其他功能

+ 调试程序
    + `attach` 将自动查找正在运行的Vulnerability进程并用GDB调试。
    + `attach` 默认调试Vulnerability，你可以使用`attach e|v|exp|vul`来选择调试哪一个程序。
    + 查找到多个可能进程时，默认调试PID最大的，并输出警告。

+ 调用工具
    + `tool toolname` 将调用工具，例如连接payload等。

+ 查询和改变ASLR状态
    + `aslr check` 或`aslr status`：查询当前ASLR状态
    + `aslr on`， `aslr off`， `aslr conservative`：改变ASLR状态

+ 停止Exploit或Vulnerability：
    + 这一功能需要脚本中有stop()函数，用于在终止在后台运行的脚本。如果不需要，可以没有这一函数。
    + `stopexp` 或`stop e` `stop exp`
    + `stopvul` 或`stop v` `stop vul`
    + `stop` 将终止Exploit和Vulnerability。

+ 显示Exploit和Vulnerability信息：
    + `info` 系列指令与`stop`结构完全相同，显示脚本内info属性中记录的文字。
    + 显示payload信息参见选择payload。
    
+ 重新编译Exploit和Vulnerability：
    + `make` 系列指令与`stop`结构完全相同，将调用脚本内的make方法。如果不需要，可以没有这一函数。

+ 其他
    + `help`将列出所用命令，`help command`或`?command`将给出帮助。
    + `q`退出VRL
    + `gdb`将调出GDB，这将不会像使用`!gdb`这样让当前终端陷入GDB。
    + `coloron``coloroff`用于开关命令行颜色
    + 命令不区分大小写，但脚本名区分。
    + 强烈建议安装cmd2，如果你安装了cmd2包，将优先使用cmd2，这将带来如下便利：
        + 可以方便地使用脚本，bash命令和python命令。
        + 异常将不会导致退出VRL。
        + 一些默认的函数，例如`exit`, `!command`执行bash指令等。


## 扩展方法和其他

添加新的Exploit，Vulnerability，Payload和工具，请参考[扩展向导](documents/扩展向导.md)

已知bug请参考[bugs](documents/bugs.md)

FAQ:[FAQ](documents/FAQ.md)

---

