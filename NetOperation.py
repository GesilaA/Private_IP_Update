import argparse
#import urllib2
import urllib.request
import requests
import re
import os
import time

class NetOperation():
    def __init__(self, username=None, password=None, index=0):
        self.userlist = ['98221925', '18839010', '118839010','18846501','17821907']
        self.pwdlist = ['820116', '19951122', '19951122','19940208','wanglifan']
        self.loginUrl = 'http://59.67.0.245/a70.htm'
        self.logstateUrl = 'http://59.67.0.245'
        self.logoutUrl = 'http://59.67.0.245/F.htm'
        self.username = username
        self.password = password
        self.ipv4 = '0.0.0.0'
        self.ipv6 = ''
        if username is None or password is None:
            self.username = self.userlist[index]
            self.password = self.pwdlist[index]
        
    def showList(self):
        print('\t' + '='*35)
        print('\t\tusername\tpassword')
        print('\t' + '-'*35)
        for i in range(len(self.userlist)):
            print('\t[%d]\t%s\t%s' % (i, self.userlist[i], self.pwdlist[i]))
        print('\t' + '='*35)
        
    def checkState(self):
        print('\t=======NET STATE=======')
        
        r = urllib.request.urlopen(self.logstateUrl).read()
        
        # f = open('t.txt', 'wb')
        # f.write(r)
        # f.close()
        
        r = str(r)
        if r.find('Drcom PC\\xd7\\xa2\\xcf\\xfa\\xd2\\xb3') >= 0:     #Drcom PC注销页      
            s = r.find('<script type="text/javascript">') + len('<script type="text/javascript">')
            e = r.find(';v6ip=\\\'0000:0000:0000:0000:0000:0000:0000:0000\\\'')
            r = r[s:e]
            regex = re.compile(r'\d+')
            ret = regex.findall(r)
            usageTime = ret[0]
            usageData = ret[1]
            
            s = r.find('uid')
            r = r[s:]
            regex = re.compile(r'\d+')
            uid = regex.search(r)
            print('\tCurrent user: %s' % uid[0])
            print('\tTotal usage time: %s minutes' % usageTime)
            print('\tTotal usage data: %d MBytes' % (int(usageData) / 1024))
            
            s = r.find('v4ip')
            r = r[s:]
            regex = re.compile(r'(\d+\.){3}\d*')
            v4ip = regex.search(r)
            if v4ip is not None:
                self.ipv4 = v4ip[0]
                print('\tCurrent IPv4 address: %s' % v4ip[0])
            s = r.find('v6ip')
            r = r[s:]
            regex = re.compile(r'((\d|[a-f])*\:){7}(\d|[a-f])*')
            v6ip = regex.search(r)
            if v6ip is not None:
                self.ipv6 = v6ip[0]
                print('\tCurrent IPv6 address: %s' % v6ip[0])

        else:
            print('\t unlogged')
        print('\t=======================')
    
    def login(self):
        if self.username == 'LOGOUT':
            print('\t=======LOGOUT INFO=======')
        else:
            print('\t=======LOGIN INFO=======')
        print('\tusername: ' + self.username)
        print('\t------------------------')
        postData = {
            'DDDDD': self.username, 
            'upass': self.password, 
            'R1': '0',
            'R2': None,
            'R6': '0',
            'para': '00',
            '0MKKey': '123456',
            #'v6ip': '2001:0da8:a005:0208:edba:15d6:a058:b78a',
            'v6ip': '0',
            'R7': '0'
        }
        r = requests.post(url=self.loginUrl, data=postData)
        if r.text.find('Drcom PC登陆成功页') >= 0:
            print('\tlogin SUCCESS')
            print('\t========================')
            self.checkState()
        else:
            if self.username == 'LOGOUT':
                print('\tlogout SUCCESS')
                print('\t=========================')
            else:
                print('\tlogin ERROR')
                print('\t========================')
        
    def logout(self):
        self.username = 'LOGOUT'
        self.password = ''
        self.login()

    def setUserIndex(self, index):
        self.username = self.userlist[int(index)]
        self.password = self.pwdlist[int(index)]
       
    def setUserInfo(self, username, password):
        self.username = username
        self.password = password

    def updateIP(self):
        file = 'IPv4: %s \nIPv6: %s' % (self.ipv4, self.ipv6)
        with open('readme.md', 'wt') as f:
            f.write(file)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        command_list = [
                'git add readme.md',
                'git commit -m "update time: %s"' % current_time,
                'git push -f origin master',
                ]
        for cmd in command_list:
            os.system(cmd)

def main():
    parser = argparse.ArgumentParser(
                prog='NetOperation', 
                usage='%(prog)s [options]',
                description='Login or Logout Network',
                epilog='--The End--',
                prefix_chars='-',
                fromfile_prefix_chars=None
    )
    parser.add_argument('--username', '-u', help='user for login')
    parser.add_argument('--password', '-p', help='password for user')
    parser.add_argument('--userindex', '-i', help='select user which in list')
    parser.add_argument('--showlist', '-s', help='show user list')
    parser.add_argument('--logout', '-o', help='logout network')
    parser.add_argument('--check', '-c', help='check network state')
    args = parser.parse_args()
    NetO = NetOperation()
    
    flag = True
    index = 0
    if args.showlist is not None:
        NetO.showList()
        flag = False
    if args.check is not None:
        NetO.checkState()
        flag = False
    if args.logout is not None:
        NetO.logout()
        flag = False
    if flag:
        if args.username is None or args.password is None:
            if args.userindex is None:
                print('\t**Login user: %s**' % NetO.userlist[0])
            else:
                print('\t**Login user: %s**' % NetO.userlist[int(args.userindex)])
                NetO.setUserIndex(int(args.userindex))
        else:
            NetO.setUserInfo(args.username, args.password)
        NetO.login()
    NetO.updateIP()
    
if __name__ == '__main__':
    main()
   

    
    
