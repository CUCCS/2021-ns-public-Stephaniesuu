# EXP3-HTTP代理服务器实验

## 实验目的

- Kali Linux中安装```tinyproxy```
- 用主机设置浏览器代理指向tinyproxy建立的HTTP正向代理
- 在Kali中用wireshark抓包
- 分析抓包过程，理解HTTP正向代理HTTPS流量的特点

## 实验步骤

1. ### 搭建实验所需的网络拓扑图

   ![](img/topology.png)

   * 攻击者Attacker-kali

     * 可ping通网关gateway
     * 不能ping通靶机
     * 可上网

     ![](img/attacjer-net.png)

   * 网关gateway

     * 攻击者、靶机、互联网都可以ping通

       ![](img/gateway-net.png)

   * 靶机Victim-kali

     * 攻击者、靶机、互联网都可以ping通

       ![](img/victim-net.png)

2. ### 配置tinyproxy代理

   

   1. 在网关Gateway中进行tinyproxy配置

      ```shell
      #安装
      apt-get update & apt-get install tinyproxy
      
      # 备份tinyproxy配置文件
      cp /etc/tinyproxy/tinyproxy.conf /etc/tinyproxy/tinyproxy.conf.bak
      
      # 编辑tinyproxy配置文件
      vim /etc/tinyproxy/tinyproxy.conf
      #————————————————————配置开始————————————
      # 注释掉下面这一行
      # Allow 127.0.0.1 #仅限当前主机访问代理服务
      
      # 取消掉下面这一行的注释
      Allow 10.0.0.0/8
      # Allow 是允许访问的主机IP，不写就是允许所有主机访问
      #————————————————————配置完毕————————————
      
      #启动/停止/查看状态/重启命令
      systemctl start tinyproxy.service
      systemctl stop tinyproxy.service
      systemctl status tinyproxy.service
      systemctl restart tinyproxy.service
      
      ```

      ![image-20210929193940511](img/tinyproxy-config.png)

   2. 在攻击者里`打开浏览器->preference->搜索'network settings'->手动配置代理->点击'ok'`

      ![image-20210929195654886](img/tinyproxy-config-2.png)

   3. 开启靶机Apache服务

      ```shell
      #查看Apache进程
      ps aux |grep apache
      
      #开启服务
      service apache2 start
      ```

      ![image-20210929211001477](img/apche2-start.png)

3. ### 使用tinyproxy访问靶机并抓包

   * 攻击者

     * 下载wireshark。

     * 使用浏览器访问靶机`172.16.111.111`和`172.16.111.111/hack`，分别显示Apache默认页面和404页面，没有直接给出代理服务器信息。![image-20210929213854848](img/web2victim.png)![image-20210929213929026](img/web2victim-hack.png)

     * 打开wireshark抓包并分析。设置过滤器fliter，发现HTTP响应头中有`Via: 1.1 tinyproxy (tinyproxy/1.10.0)`字段。即攻击者访问靶机需要通过代理。

       ![image-20210929215335713](img/attacker-wireshark.png)

   * 网关

       同上，也可看到`tinyproxy`的字段。

       ![image-20211004212141383](img/gw-wireshark.png)

       - 若在网关设置防火墙规则过滤攻击者主机（客户端）发出的的请求，则攻击者主机依然无法访问靶机端的HTTP服务

       - 网关作为代理层可以理解HTTP报文

   * 靶机

     * 使用wireshark抓包，可发现HTTP 响应头里含有`Via: 1.1 tinyproxy (tinyproxy/1.10.0)`字段。![image-20210930104343702](img/victim-wireshark.png)
       * 攻击者（访问者）IP地址、以太网接口被隐藏。
       * via字段说明网关（代理服务器）正在提供代理服务。

4. ### 使用tinyproxy访问靶机并抓包

   1. 攻击者主机访问www.baidu.com

      ![image-20211007162549128](img/attacker-baidu.png)
   
   2. 在网关上抓包
   
      * 通过tinyproxy代理，代理服务器可看到用户访问的网址。
   
        ![image-20211007163421044](img/gw-wireshark-url)
   
      * 但是对应网址传输的数据会被加密，代理服务器无法观测。
   
        ![image-20211007163150210](img/gw-wireshark-encrypt.png)

## 问题与解决方法

1. 问题：配置NAT网络后网关与攻击者虚拟机IP冲突

   1. 在`管理->全局设定->网络`中添加新的NAT网络![image-20210929120151539](img/ip-conflit-setNAT.png)

   2. 分别在网关和攻击者的`设置->网络`中将`连接方式`里的`网络地址转换（NAT）`改为`NAT网络`

      ![image-20210929191620049](img/change-NAT.png)

   3. 手动刷新MAC地址![image-20210929191824455](img/reflesh-MACaddress.png)

2. 配置Debian允许root用户SSH登录

   * 一直报错无法解析HOST:debian
   
     解决：在vscode中修改ssh配置文件出错，更改正确即可。![image-20211007162213248](img/config-error.png)

## 课后习题

1. 代理技术在网络攻防中的意义？
   1. 对攻方的意义？
      * 能访问本无法访问的机器（如本实验中攻击者访问靶机）。
      * 被攻击者无法判断攻方身份（如本实验中靶机无法确定攻击者的身份），攻击无法溯源。
   2. 对守方的意义？
      * 攻方也无法辨认守方身份，无法确定攻击的对象。

2. 常规代理技术和高级代理技术的设计思想区别与联系？
   - 区别：高级代理技术的匿名通信技术放大了网络安全对抗的复杂性。
   - 联系：可以通过常用代理技术实现高级代理。

## 参考

* [virtualbox自定义nat模式解决多个虚拟机IP冲突](https://blog.csdn.net/qq_41631806/article/details/103892858)
* [CUCCS/2018-NS-Public-jckling](https://github.com/CUCCS/2018-NS-Public-jckling/blob/master/ns-0x03/3.md)

