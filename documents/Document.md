# VRL平台文档（编辑中）

VRL（Vulnerability Research Lab）的研究目的在于，在 Linux 平台下测试并验证已有漏洞，分析开启不同防御机制的情况下对攻击过程的影响，学习和熟悉漏洞利用原理与技巧，尝试研究出新的攻击或防御方法。

## 平台架构
VRL平台大致分为五个部分。

- UI：用户交互，整合所有其他模块。所有的漏洞程序，攻击程序和设置、加工由VRL.py调用。
- Vulnerabilities：漏洞程序库，包括漏洞程序，漏洞程序调用脚本，程序源码，说明文档等。
- Exploits： Exploits库，包括利用程序，说明文档等。
- Payloads（待开发）： 供Exploits选用（如果支持）的Payload库。
- Misc（待开发）: 其他工具，加工paylaods等。

## 功能和使用方法

## 扩展方法

### 增加Vulnerability
增加新的漏洞程序需要在vulnerability文件夹中新建一个文件夹，以漏洞程序名命名，文件包括：
 
- __init__.py ： python package标识，你可以忽略这个文件，模板run.py将会自动生成这一文件。[^1]
- run.py ： 与平台交互的脚本，详见下面说明。
- 可执行文件（可选）：漏洞程序，如果你可以在run.py中完成漏洞程序，则不需要。
- 源码（可选）： 如果你希望你的漏洞程序可以跨平台，那么需要源码，否则不需要(可见的预期内并不会跨平台)。
- 说明文档（可选）： 说明这一漏洞程序原理的文档。

**VRL平台只与你的run.py脚本交互**

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
        
    def make(self):
        #重新编译你的程序，暂时没有这一功能
        
#这里默认检查你的脚本并以默认参数运行你的程序，无需更改
#这使得如果run.py运行通过了，就可以在VRL中使用了。
if __name__ == "__main__":
    ... 
```    

漏洞程序的参数如下：




[^1]: 未实现的功能