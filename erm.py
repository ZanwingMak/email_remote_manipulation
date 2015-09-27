#coding:utf-8
__author__ = 'm9Kun'

import msvcrt
from ctypes import *
import poplib
from email.parser import Parser
from email.header import decode_header
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib
import time
import os

def pwd_input():
        chars = []
        while True:
            try:
                newChar = msvcrt.getch().decode(encoding="utf-8")
            except:
                print
                print u"你很可能不是在cmd命令行下运行，密码输入将不能隐藏:",
                return raw_input()
            if newChar in '\r\n': # 如果是换行，则输入结束
                 print
                 break
            elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号
                 if chars:
                     del chars[-1]
                     msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格
                     msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号
                     msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入
            else:
                chars.append(newChar)
                msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号
        return (''.join(chars) )


def check_email(pc_address,password,smtp_server,pop_server,ifuserssl):

    def guess_charset(msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        # 如果获取不到，再从Content-Type字段获取:
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    #邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode
    def decode_str(s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def get_info(msg):
            for header in ['From','Subject']:
                    value = msg.get(header, '')
                    if value:
                        if header=='Subject':
                            subject = decode_str(value)
                        else:
                            hdr, from_email = parseaddr(value)
            return from_email,subject

    def reply(text,zhilingduan_email,pc_address):
            def format_address(s):
                name,address = parseaddr(s)
                return formataddr((Header(name,'utf-8').encode(),\
                           address.encode('utf-8') if isinstance(address,unicode) else address))

            msg = MIMEText(text,'plain','utf-8')
            msg['From'] = format_address(u'电脑端 <%s>'% pc_address)
            msg['To'] = format_address(u'指令发送端 <%s>' % zhilingduan_email)
            msg['Subject'] = Header(u'电脑端发来信息','utf-8').encode()

            serve_smtp = smtplib.SMTP(smtp_server,25)
            serve_smtp.set_debuglevel(1)
            serve_smtp.login(pc_address,password)
            serve_smtp.sendmail(pc_address,[zhilingduan_email],msg.as_string())
            serve_smtp.quit()

    def play(from_email,subject,pc_address):
        if subject == 'suoping':
                server.dele(1) #删除最新一封邮件
                text = u'已收到远程指令：锁屏'
                reply(text,from_email,pc_address)
                print text
                time.sleep(2)
                try:
                        text = u'正在执行远程锁屏指令'
                        reply(text,from_email,pc_address)
                        print text
                        time.sleep(2)
                        user32 = windll.LoadLibrary('user32.dll')
                        user32.LockWorkStation()
                except:
                        text = u'远程指令执行失败，请重试'                        
                        reply(text,from_email,pc_address)
                        print text
                        time.sleep(2)
        elif subject == 'guanji':
                 server.dele(1) #删除最新一封邮件
                 text = u'已收到远程指令：关机'
                 reply(text,from_email,pc_address)
                 print text
                 time.sleep(2)
                 try:
                        text = u'正在执行远程关机指令'
                        reply(text,from_email,pc_address)
                        print text
                        time.sleep(2)
                        os.system('shutdown -f -s -t 10 -c Closing...')
                 except:
                        text = u'远程指令执行失败，请重试'
                        reply(text,from_email,pc_address)
                        print text
                        time.sleep(2)
        elif subject == 'chongqi':
                server.dele(1) #删除最新一封邮件
                text = u'已收到远程指令：重启'
                reply(text,from_email,pc_address)
                print text
                time.sleep(2)
                try:
                        text = u'正在执行远程重启指令'
                        reply(text,from_email,pc_address)
                        print text
                        time.sleep(2)
                        os.system('shutdown -f -r -t 10 -c Rstarting...')
                except:
                        text = u'远程指令执行失败，请重试'
                        print text
                        reply(text,from_email,pc_address)
                        time.sleep(2)

    while True:
        try:
            # 连接到POP3服务器:
            if ifuserssl == 'y' or ifchange == 'Y':
                server = poplib.POP3_SSL(pop_server)
            else:
                server = poplib.POP3(pop_server)
            # 身份认证:
            server.user(pc_address)
            server.pass_(password)          
            
            # list()返回所有邮件的编号:
            resp, mails, octets = server.list()
            #print resp,mails,octets
            
            # 获取最新一封邮件, 注意索引号从1开始:
            resp, lines, octets = server.retr(len(mails))

            # 解析邮件:
            msg = Parser().parsestr('\r\n'.join(lines))

            # 获取邮件信息:
            from_email,subject = get_info(msg)

            #执行远程命令
            play(from_email,subject,pc_address)

            # 关闭连接:
            server.quit()
            break
        except Exception as e:
                if 'Syntax' not in str(e) and 'EOF' not in str(e):
                        print e
                time.sleep(100) #100秒检测一次，最好设置成5分钟！
                break


if __name__ == '__main__':
    print u'请先设置好参数...'
    print u'请输入电脑端邮箱：',
    pc_address = raw_input().strip()
    print u'请输入密码：',
    password = pwd_input()

    #SMTP服务器
    mail_check = (pc_address.split('@'))[-1].split('.')[0]

    smtp_check = 'smtp.%s.com' % mail_check
    print u'【已检测到您使用的是%s邮箱】\n已为您自动填写SMTP服务器地址:[%s]\n是否需要修改?[y/n]' % (mail_check,smtp_check),
    ifchange = raw_input()
    if ifchange == 'y' or ifchange == 'Y':
        print u'好的,请修改SMTP服务器地址'
        print u'请输入SMTP服务器地址：',
        smtp_server = raw_input().strip()
    else:
        smtp_server = smtp_check

    #POP3服务器
    pop_check = 'pop.%s.com' % mail_check
    print u'已为您自动填写POP服务器地址:[%s]\n是否需要修改?[y/n]' % (pop_check),
    ifchange = raw_input()
    if ifchange == 'y' or ifchange == 'Y':
        print u'好的,请修改POP服务器地址'
        print u'请输入POP服务器地址：',
        pop_server = raw_input().strip()
    else:
        pop_server = pop_check

    print u'是否使用SSL加密传输方式?[y/n]',
    ifuserssl = raw_input()
    if ifuserssl == 'y' or ifuserssl == 'Y':
        print u'好的,正在使用SSL加密服务...'
    else:
        print u'好的,不使用SSL加密服务...'

    print u'邮件远程指令功能开始待命...'
    while True:
            check_email(pc_address,password,smtp_server,pop_server,ifuserssl)

