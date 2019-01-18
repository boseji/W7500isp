# W7500x isp tool package #

## Overview ##

## Getting Started ##

### ISP 객체 생성 ###
### ISP 객체의 functions ###
* checkisp()
* progLockFlag()
* readLockFlag()
* eraseFlashAll()
* eraseDataFlash_0()
* eraseDataFlash_1()
* progDataFlash_0()
* progDataFlash_1()
* dumpDataFlash()
* dumpCodeFlash()
* dumpSram()
* downloadDatatoSRAM()
* downloadDataByXModem()
* resetSystem()
* diffFiles()
------------------
### checkisp ###
#### description ####
W7500(P)가 ISP 모드에 진입했는지를 확인하는 함수이다.
W7500(P)는 ISP로 진입하면 ISP 포트로 'U'를 수신했을 때, 'U'를 전송한다. 최초 'U'를 수신한 후에는 그 다음 'U' 신호에 반응하지 않는다.
#### systax ####
checkisp()
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### progLockFlag ###
#### description ####
Code Flash와 Data Flash에 Read/Write Lock을 설정하거나 해제하는 함수이다.
W7500(P)는 Flash Lock과 관련해서 FLOCK0와 FLOCK1 두개의 register를 가지고 있는데, 각 bit별로 관련된 Page가 다르다.

FLOCKR0

|31|30|29 ~ 4|3|2|1|0|
|---|---|---|---|---|---|---|
|CRL|CBWLA|Reserved|DRL1|DRL0|DWL1|DWL0|


FLOCKR1
|31|30|29 ~ 4|3|2|1|0|
|---|---|---|---|---|---|---|
|CWL31|CWL30|...|CWL3|CWL2|CWL1|CWL0|

#### systax ####
progLockFlag( *FLOCKR0_Cmd*, *FLOCKR1_Cmd* )

#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.progLockFlag("00000000", "00000000")
```
### readLockFlag ###
Code Flash와 Data Flash의 Read/Write Lock 상태를 읽는다.
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### eraseFlashAll ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### eraseDataFlash_0 ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### eraseDataFlash_1 ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### progDataFlash_0 ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### progDataFlash_1 ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### dumpDataFlash ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### dumpCodeFlash ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### dumpSram ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### downloadDatatoSRAM ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### downloadDataByXModem ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### resetSystem ###
#### description ####
#### systax ####
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
### diffFiles ###
#### description ####
Binary 파일을 Flash에 다운로드한 후, verify하기 위해서 사용하는 함수이다.
파일로드한 Binary 파일의 file명과 Flash 메모리를 dump해서 저장한 파일의 file명을 parameter로 지정하면 두 파일의 내용을 읽어서 byte 단위로 비교해서 두 파일이 동일한지 여부를 reture한다.
#### systax ####
diffFiles(filename1, filename2)
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()
```
