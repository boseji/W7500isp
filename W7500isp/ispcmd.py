'''
Created on 2019. 1. 10

@author: javakys
'''
# import unittest
import serial
import time
from xmodem import XMODEM
import os, sys
import filecmp

COM = 'COM10'
# BAUD = 115200
BAUD = 460800
comP = COM
baudR = BAUD
RET_SUCCESS     = '0'
RET_IVLD_SIZE   = '1'
RET_IVLD_ADDR   = '2'
RET_IVLD_CMD    = '3'
RET_NO_PRIV     = '4'
RET_IVLD_PARAM  = '5'
RET_READ_LOCK   = '6'
RET_WRITE_LOCK  = '7' 
RET_RESET       = '8'

class ispcmd(object):
    def __init__(self, comP):
        self.ser = comP
        self.srcbuf = None
        self.dumpbuf = None

    def serialClose(self):
        self.ser.close()

    def __del__(self):
        self.serialClose()
        
    def checkisp(self):
        while True:
            try:
                self.ser.write(str.encode('U'))
                recv = self.ser.read()
                # print (recv.decode("utf-8"))
                
                if recv.decode("utf-8") == 'U':  
                    # print (recv.decode("utf-8") + self.ser.readline().decode("utf-8"))
                    # print ('Boot Mode Entered')         
                    sys.stdout.write ("%s%s" % (recv.decode("utf-8"), self.ser.readline().decode("utf-8")))
                    sys.stdout.write ('Boot Mode Entered\r\n')         

                    self.ser.write('\r'.encode('utf-8'))
                    time.sleep(1)
                    self.ser.read_all()          
                    break
                else :  
                    # print(recv)
                    sys.stdout.write('.\r\n')
                time.sleep(1)
            except:
                pass

    def sendCmd(self, cmd, resp="0"):
        cmd = cmd + '\r'
        for i in cmd:
            self.ser.write(i.encode('utf-8'))
            time.sleep(0.01)

    def rcvResp(self, resp="0", paramLine=1, loopCnt=3, opt=0):
        resp = resp + '\r\n'
        # print(loopCnt)
        # print(opt)
        if opt is 0:
            for i in range(loopCnt):
                respData = self.ser.readline()
                respData = respData.decode('utf-8')
                if(i == paramLine - 1):
                    tempData = respData      
                sys.stdout.write("Resp : [%d]%s" % (i, respData))
                if(respData == resp):
                    sys.stdout.write("Success\r\n")
                    time.sleep(1)
                    self.ser.read_all()
                    break
                time.sleep(0.05)
            # print("")
            return respData
        elif opt == 1:
            for i in range(loopCnt-1):
                respData = self.ser.readline()
                respData = respData.decode('utf-8')
                addr, data = respData.split(':')
                sys.stdout.write('%s\r\n' % data)
            return self.ser.readline().decode('utf-8')

    def writeCmd(self,cmd,resp="0",paramLine=1,loopCnt=3,opt=0):
        self.sendCmd(cmd)
        return self.rcvResp(loopCnt=loopCnt, opt=0)


    def progLockFlag(self, FLOCK0, FLOCK1):
        resp = self.writeCmd("LOCK PROG" + " " + FLOCK0 + " " + FLOCK1) 
        return resp

    def readLockFlag(self):
        resp = self.writeCmd("LOCK READ")
        return resp

    def eraseFlashAll(self):
        resp = self.writeCmd("ERAS MASS")
        return resp

    def eraseDataFlash_0(self):
        resp = self.writeCmd("ERAS DAT0")
        return resp

    def eraseDataFlash_1(self):
        resp = self.writeCmd("ERAS DAT1")
        return resp
   
    def progDataFlash_0(self, sramaddr):
        resp = self.writeCmd("PROG DAT0 " + sramaddr)
        return resp

    def progDataFlash_1(self, sramaddr):
        resp = self.writeCmd("PROG DAT1 " + sramaddr)
        return resp

    def convertBytearray(self, file, data):
        tmpbuf = bytearray()
        tmpbuf.append(int(data[6:8], 16))
        tmpbuf.append(int(data[4:6], 16))
        tmpbuf.append(int(data[2:4], 16))
        tmpbuf.append(int(data[0:2], 16))
        file.write(tmpbuf)

    def printDumpData(self, index, addr, data):
        if (index % 8) == 0:
            sys.stdout.write('%s : %s %s %s %s' % (addr, data[6:8], data[4:6], data[2:4], data[0:2]))
            # print('%s : %s %s %s %s' % (addr, data[6:8], data[4:6], data[2:4], data[0:2]), end=' ')
        elif (index % 8) == 7:
            sys.stdout.write(' %s %s %s %s\r\n' % (data[6:8], data[4:6], data[2:4], data[0:2]))
            # print('%s %s %s %s' % (data[6:8], data[4:6], data[2:4], data[0:2]))
        else:
            sys.stdout.write(' %s %s %s %s' % (data[6:8], data[4:6], data[2:4], data[0:2]))
            # print('%s %s %s %s' % (data[6:8], data[4:6], data[2:4], data[0:2]), end=' ')
        
        
    def dumpDataFlash(self):
        # resp = self.writeCmd("DUMP 1003FE00 00000200", loopCnt=129)
        self.sendCmd("DUMP 1003FE00 00000200")
        for i in range(128):
            addr, data = self.ser.readline().decode('utf-8').split(':')
            self.printDumpData(i, addr, data)

        resp = self.ser.readline().decode('utf-8')
        if(resp == '0\r\n'):
            sys.stdout.write('Success\r\n')
            time.sleep(1)
        return resp

    def dumpCodeFlash(self, startAddr, Count, output=None, filename=None):
        # print(startAddr)
        int_startAddr = int(startAddr, 16)
        # print(int_startAddr)
        # print(Count)
        # loopCnt = Count / 4 + 1
        # print(loopCnt)
        if output is 'file':
            if filename is None:
                f = open('dumpfile.bin', 'wb')
            else:
                f = open(filename, 'wb')
        while Count > 0:
            if Count >= 2048:
                byte_count = bytearray.fromhex('{:08X}'.format(2048))
                Count -= 2048
                loopCnt = 512
            else:
                byte_count = bytearray.fromhex('{:08X}'.format(Count))
                loopCnt = int(Count / 4)
                Count = 0                
            # print("DUMP %s %s" % (startAddr, ''.join('{:02X}'.format(byte_count[i]) for i in range(0, 4))))
            # resp = self.writeCmd("DUMP " + startAddr + " " + ''.join('{:02X}'.format(byte_count[i]) for i in range(0, 4)), loopCnt=loopCnt)
            self.sendCmd("DUMP " + startAddr + " " + ''.join('{:02X}'.format(byte_count[i]) for i in range(0, 4)))
            for i in range(loopCnt):
                addr, data = self.ser.readline().decode('utf-8').split(':')
                if output is not 'file':
                    self.printDumpData(i, addr, data)
                else:
                    self.convertBytearray(f, data)

            resp = self.ser.readline().decode('utf-8')
            if(resp == '0\r\n'):
                sys.stdout.write('+')
                sys.stdout.flush()
                time.sleep(0.01)
                int_startAddr += 2048
                byte_addr = bytearray.fromhex('{:08X}'.format(int_startAddr))
                startAddr = ''.join('{:02X}'.format(byte_addr[i]) for i in range(0, 4))
            else:
                break
        if output is 'file':
            f.close()

        return resp
    
    def dumpSram(self):
        resp = self.writeCmd("DUMP 20000000 00004000", loopCnt=1025)
        return resp

    def downloadDatatoSRAM(self, filename):
        filesize = 0
        sentsize = 0
        f = open(filename, 'rb')
        # print(f)
        read_data = f.read()
        f.close()
        # print(read_data)
        filesize = len(read_data)
        print('filesize : %s' % str.format('{:08}', filesize))
        # send command
        self.writeCmd("DOWN 20000000 00000200", loopCnt=1)
        time.sleep(1)
        # if option is '0':
        #     tmp_data = read_data[0:256]
        # elif option is '1':
        #     tmp_data = read_data[256:512]

        self.ser.write(read_data[0:256])
        self.ser.write(read_data[256:512])

        resp = self.ser.readline()
        resp = resp.decode('utf-8')
        print(resp)
        time.sleep(1)
        self.ser.read_all()
    
        return resp

    def getc(self,size,timeout=1):
        return self.ser.read(size)

    def putc(self,data,timeout=1):
        return self.ser.write(data)

    def Xmodem_init(self):
        self.xmodem = XMODEM(self.getc, self.putc)

    def Xmodem_Send(self, filename, option):
        if option is 'code':
            cmd = "XPRG " + "10000000" + " " + "00020000" + "\r"
        elif option is 'sram':
            cmd = "XPRG " + "20000000" + " " + "00000200" + "\r"
        # print(cmd)
        self.ser.write(cmd.encode('utf-8'))
        sys.stdout.write("Start Send Binary using XMODEM\r\n")
        stream = open(filename, 'rb')
        # self.srcbuf = stream.read()
        sys.stdout.write("%s\r\n" % self.xmodem.send(stream))
        stream.close()

        sys.stdout.write("%s\r\n" % self.ser.readall())
        sys.stdout.write("End XMODEM\r\n")
        # print(len(self.srcbuf))

    def downloadDataByXModem(self, filename, option):
        self.Xmodem_init()
        self.Xmodem_Send(filename, option)
   
    def resetSystem(self):
        self.ser.write("REST\r".encode('utf-8')) 
        resp = self.ser.readline()
        sys.stdout.write(resp + "\r\n")
        return resp

    def readSerial(self):
        return self.ser.read_all()

    def diffFiles(self, file1, file2):
        f1 = open(file1, 'rb')
        f2 = open(file2, 'rb')
        f1_buf = f1.read()
        f2_buf = f2.read()
        f1.close()
        f2.close()
        bMismatched = False
        for i in range(len(f1_buf)):
            if f1_buf[i] != f2_buf[i]:
                sys.stdout.write("Mismatched at %s\r\n" % i)
                bMismatched = True
        if not bMismatched:
            sys.stdout.write("Both are the same\r\n")
            return True # Same
        return False # Different

        

        