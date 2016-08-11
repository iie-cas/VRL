# VRL
**Under Refacting**

VRL(Vulnerability Research Lab)的研究目的在于，在 Linux 平台下测试并验证已有漏洞，分析开启不同防御机制的情况下对攻击过程的影响，学习和熟悉漏洞利用原理与技巧，尝试研究出新的攻击或防御方法。

## 测试平台
Ubuntu 12.04 LTS (32 bits)    
Kali 2.0 (64 bits) 

## 项目规划
- vulnerabilities: 存放不同类别的漏洞程序，其源码存放于 code 目录中
- test: 存放漏洞利用测试框架，模仿 MetaSploit 的形式，可以不断扩展添加 exp
- slides: 存放组会时分享的相关资料  

## 实验环境
漏洞程序主要使用 C 或 C++ 编写，对应 exp 脚本主要使用 Python 2.7 编写。   

可能会用到的 Python 第三方库有:   

- [pwntools](https://github.com/Gallopsled/pwntools)
- [capstone](https://github.com/aquynh/capstone)
- [ropgadget](https://github.com/JonathanSalwan/ROPgadget)

## 基本用法

```
$ cd test
$ python test.py
test >> help
    help: 帮助信息
    quit: 退出
    reload: 重新加载exploits和payloads模块
    show exploits|payloads|options: 显示相应的信息
         exploits: 显示所有的exploits模块
         payloads: 显示所有的payloads模块
         options: 显示test所需要设置的参数
    set dIP|dPort|exploit|payload arg: 设置test所需要设置的参数
        dIP: 设置目标IP
        dPort: 设置目标端口
        exploit: 所选用的exploit模块
        payload: 所选用的payload模块
    test: 设置完参数后进行测试
test >>
```

将 vulnerabilities 内的漏洞程序绑定到某个端口运行，使用`set dIP`和`set dPort`将其设定为攻击目标，然后`set exploit`和`set payload`（有时不需要 payload)设定攻击方式，最后`test`执行

