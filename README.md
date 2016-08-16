# VRL平台文档

VRL（Vulnerability Research Lab）的研究目的在于，在 Linux 平台下测试并验证已有漏洞，分析开启不同防御机制的情况下对攻击过程的影响，学习和熟悉漏洞利用原理与技巧，尝试研究出新的攻击或防御方法。

## 测试平台
Ubuntu 16.04 LTS (64 bits)    

## 实验环境
漏洞程序主要使用 C 或 C++ 编写，对应 exp 脚本主要使用 Python 2.7 编写。   

可能会用到的 Python 第三方库有:   

- [pwntools](https://github.com/Gallopsled/pwntools)
- [capstone](https://github.com/aquynh/capstone)
- [ropgadget](https://github.com/JonathanSalwan/ROPgadget)

## 平台架构
VRL平台大致分为五个部分。

- UI：用户交互，整合所有其他模块。所有的漏洞程序，攻击程序和设置、加工由VRL.py调用。
- Vulnerabilities：漏洞程序库，包括漏洞程序，漏洞程序调用脚本，程序源码，说明文档等。
- Exploits： Exploits库，包括利用程序，说明文档等。
- Payloads（待开发）： 供Exploits选用（如果支持）的Payload库。
- Misc（待开发）: 其他工具，加工paylaods等。

## 功能和使用方法

VRL平台可以分别载入Exploit，Vulnerability和Payload，并修改其设置。

+ 列出可用Exploits，Vulnerability和Payload：
    + `show exploits|vulnerability|payload`
        + *Tip: `可以缩写为show e|v|p`*
        - 当VRL载入时，会自动扫描目录下符合格式的Exploit等脚本，如果你不希望重启VRL并加入新的脚本，使用reload指令。

+ 选择Exploit或Vulnerability：
    + `useexp expname` 或`use e expname` `use exp expname`
    + `usevul vulname` 或`use v vulname` `use vul vulname`
    + `use name`将使用同一name尝试载入Exploit和Vulnerability。
        + *Tip：当载入的Exploit或Vulnerability有一个默认的Vulnerability或Exploit，VRL会提醒你是否载入对应脚本。*
        
+ 设置Exploit和Vulnerability的选项：
    + `show option` 或`show o` 显示所有选项（包括Exploit和Vulnerability）。
    + `set key value` 将改变key为value。这里`value`将作为字符串赋值，在脚本中注意这一属性。这里设计上认为Exploit和Vulnerability中相同名称的key应该保持相同值。在脚本中注意这一设计。
    + 不希望同时被更改option可以使用`setexp key value`和`setvul key value`，（更建议在设计时使用不同的属性名称）。
    
+ 运行Exploit或Vulnerability（使用当前设置）：
    + `runexp` 或`run e` `run exp`
    + `runvul` 或`run v` `run vul`
    + `run` 将先运行Vulnerability，再运行Exploit。
        + *Tip: 如果Vulnerability指定了默认的Exploit，可以使用`run vulname`来快速运行，甚至不需要use载入。*

+ 停止Exploit或Vulnerability（使用当前设置）：
    + 这一功能需要脚本中有stop()函数，用于在终止在后台运行的脚本。如果不需要，可以没有这一函数。
    + `stopexp` 或`stop e` `stop exp`
    + `stopvul` 或`stop v` `stop vul`
    + `stop` 将终止Exploit和Vulnerability。
    
+ 其他
    + `help`将列出所用命令，`help command`或`?command`将给出帮助。
    + `q`退出VRL
    + 如果你安装了cmd2包，将优先使用cmd2，这将带来如下便利：
        + 异常将不会导致退出VRL。
        + 一些默认的函数，例如`!command`执行bash指令等。


## 扩展方法

### 增加Vulnerability
增加新的漏洞程序需要在vulnerability文件夹中新建一个文件夹，以漏洞程序名命名，文件包括：
 
- `__init__.py` ： python package标识，你可以忽略这个文件，至少运行一次模板run.py将会自动生成这一文件。
- `run.py` ： 与平台交互的脚本，详见下面说明。
- 可执行文件（可选）：漏洞程序，如果你可以在run.py中完成漏洞程序，则不需要。
- 源码（可选）： 如果你希望你的漏洞程序可以跨平台，那么需要源码，否则不需要(可见的预期内并不会跨平台)。
- 说明文档（可选）： 说明这一漏洞程序原理的文档。

**注意：VRL平台只与你的run.py脚本交互**

一个简单的run.py如下：

```python
import..

class Vulnerability(vulnerability.VRL_Vulnerability):
    def __init__(self):
        #在这里添加你的漏洞程序信息
        self.name = 'stack_overflow'
        self.info = 'information'
        self.options={'dIP' : '127.0.0.1',
                      'dPort' : '12345'}
        self.exploit = 'stack_overflow'

    def run(self):
        #这一函数将被VRL启动以调用你的程序，确保你开启的时候按照options的参数
        print 'run your vulnerability here'
        
    def stop(self):
        #这一函数用于停止你的程序，如果你的程序无法，或不需要停止，可以没有这一函数

    def make(self):
        #重新编译你的程序，暂时没有这一功能
        
#这里默认检查你的脚本并以默认参数运行你的程序，无需更改
#这使得如果run.py运行通过了，就可以在VRL中使用了。
if __name__ == "__main__":
    ... 
```    

漏洞程序的属性(__init__中)如下：

+ name：字符串，脚本名称，建议与文件夹名一致。
+ info：脚本的简单信息。
+ options：必须（可以为空）。能够影响脚本运行的可设置选项和默认值。**注意：所有选项请统一为str类型，包括key和value**
+ exploit：默认的exploit脚本名称（以路径名为准，而非name属性）。

漏洞程序的方法如下：

+ run：必须。这一函数将被VRL启动以调用你的程序，确保以当前设置运行。
+ stop：非必须。用于终止你的程序。
+ make：非必须。用于重新编译。（暂时不会有这一功能）

### 增加Exploit

与增加Vulnerability基本相同，不同之处有：

```python
- from modules import vulnerability
+ from modules import exploit

- class Vulnerability(vulnerability.VRL_Vulnerability):
+ class Exploit(exploit.VRL_Exploit):
```

另外，如果你的Exploit支持更换payload，可以在属性中添加payload属性，默认值为默认的字节流。

---

## 待开发的功能：

+ payload替换 finish
+ payload加工
+ ROP/JOP构建
+ autoattach/autoDEBUG
+ 脚本名自动补全
+ make finish
+ info finish
