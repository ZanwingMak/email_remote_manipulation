# email_remote_manipulation
remote manipulation through the e-mail

邮件远程指令

![image](http://i11.tietuku.com/ecf3d5cb5d14274a.jpg)

这个程序的灵感是来自开源中国网站上一位网友，因为现在手机那么普及，微信、QQ也可以发送邮件，那么我们可以把收发邮件的功能用来当作远程指令不就好了吗。
首先，程序会登录所填写的邮箱，然后读取最新一条邮件，如果邮件的标题是suoping、chongqi、guanji，那么就会执行指定的系统命令，并会发送反馈邮件到指令来源的邮箱里，让用户清楚电脑是否接收到指令，随后会删除带有指令标题的邮件，避免重复执行命令。

主要使用库：poplib、smtplib、ctypes、thread、email

【EXE打包】链接: http://pan.baidu.com/s/1nto08aP 密码: a7dr

![image](http://i5.tietuku.com/63f1f7186319580e.png)

![image](http://i11.tietuku.com/1afe6d52c6d9da49.jpg)
