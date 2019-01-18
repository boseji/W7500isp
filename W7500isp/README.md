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
|CWL31|CWL30|~|CWL3|CWL2|CWL1|CWL0|

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
#### description ####
Code Flash와 Data Flash의 Read/Write Lock 상태를 읽는다.
표시되는 문자열은 Hexa Format으로 표현된 것으로 "80000000 00000000"이 반환된다면 FLOCKR0의 첫번째 bit만 1이라는 것인데
Code Block 전체가 Read Lock이 되었다는 의미이다.
#### systax ####
readLockFlag()
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

print(isp.readLockFlag())
```
### eraseFlashAll ###
#### description ####
Code Flash와 Data Flash 전체 영역을 Erase 하는 함수이다.
이 명령을 수행하기 위해서는 Code Flash와 Data Flash가 Write Lock이 해제되어 있어야한다.

#### systax ####
eraseFlashAll()

#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.progLockFlag('00000000', '00000000')

isp.eraseFlashAll()
```
### eraseDataFlash_0 ###
#### description ####
2개 page로 구성된 Data Flash의 0번 Page를 Erase하는 함수이다.
이 명령을 수행하기 위해서는 최소한 Data Flash 0의 Write Lock이 해제되어 있어야 한다.

#### systax ####
eraseDataFlash_0()

#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.progLockFlag('xxxxxxx2', 'xxxxxxxx')
isp.eraseDataFlash_0()
```
### eraseDataFlash_1 ###
#### description ####
Data Flash의 1번 Page를 Erase하는 함수이다.
이 명령을 수행하기 위해서는 최소한 Data Flash 1의 Write Lock이 해제되어 있어야 한다.
#### systax ####
eraseDataFlash_1()

#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.progLockFlag('xxxxxxx1', 'xxxxxxxx')
isp.eraseDataFlash_1()

```
### progDataFlash_0 ###
#### description ####
Data Flash 0번 Page를 SRAM 내의 Data를 가지고 program한다.
Parameter로 SRAM내 Data의 시작주소를 지정해야한다.
이 함수를 수행하기 위해서는 SRAM에 program할 Data를 먼저 다운로드해 두어야한다.
#### systax ####
progDataFlash_0( *startaddr* )
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
