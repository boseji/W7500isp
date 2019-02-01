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

**FLOCKR0**

|31|30|29 ~ 4|3|2|1|0|
|---|---|---|---|---|---|---|
|CRL|CBWLA|Reserved|DRL1|DRL0|DWL1|DWL0|


**FLOCKR1**

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
**이 함수를 수행하기 위해서는 SRAM에 program할 Data를 먼저 다운로드해 두어야한다.**
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

isp.progDataFlash_0('20000000')
```
### progDataFlash_1 ###
#### description ####
Data Flash 1번 Page를 SRAM 내의 Data를 가지고 program한다.
Parameter로 SRAM내 Data의 시작주소를 지정해야한다.
**이 함수를 수행하기 위해서는 SRAM에 program할 Data를 먼저 다운로드해 두어야한다.**
#### systax ####
progDataFlash_1( *startaddr* )
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.progDataFlash_1('20000000')
```
### dumpDataFlash ###
#### description ####
Data Flash내에 기록된 값을 읽어서 화면에 Hexadecimal 값으로 표시한다. 한줄에 32 바이트의 값을 표시하며 512 바이트 전체를 표시한다.
#### systax ####
dumpDataFlash()
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.dumpDataFlash()
```
### dumpCodeFlash ###
#### description ####
Code Flash내에 기록된 값을 읽어서 화면에 Hexadecimal 값으로 표시한다. Dump할 Flash의 시작주소와 byte counts를 Parameter로 지정해주어야 한다.
데이터 표시 방식은 다른 dump함수와 동일하게 한줄에 32바이트를 표시한다.
output은 dump한 값을 화면에 출력할지, file로 저장할지를 지정하는 옵션으로 default값은 'None"이고 화면으로 출력한다.
filename은 file에 저장하는 경우에 file의 이름을 지정하는 것이고, filename을 지정하지 않으면 'dumpfile.bin'이라는 이름으로 저장된다.
#### systax ####
dumpCodeFlash( *startaddr*, *count*, *output=None*, *filename=None* )
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.dumpCodeFlash( "10000000", 16*2048 )
```
### dumpSram ###
#### description ####
SRAM내에 기록된 값을 읽어서 화면에 Hexadecimal 값으로 표시한다. 
16K byte 전체 영역의 값을 dump하는데, 데이터 표시 방식은 다른 dump함수와 동일하게 한줄에 32바이트를 표시한다.
#### systax ####
dumpSram()
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.dumpSram()
```
### downloadDatatoSRAM ###
#### description ####
File내의 데이터를 SRAM으로 download 하는 함수이다.
파라미터로 다운로드할 file의 이름을 지정한다.
#### systax ####
downloadDatatoSRAM( *filename* )
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.downloadDatatoSRAM( 'a.bin' )
```
### downloadDataByXModem ###
#### description ####
Code Flash에 데이터를 다운로드할 때 XModem을 이용하는 함수이다.
파라미터로 filename과 option값을 지정해야한다.

#### systax ####
downloadDataByXModem( *filename*, *option* )
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

downlaodDataByXModem( 'a.bin', 'code' )
```
### resetSystem ###
#### description ####
ISP mode에서 빠져나오기 위해서 Software Reset을 하는 함수이다.
#### systax ####
resetSystem()
#### example ####
```python
from W7500isp import ispcmd
import serial
import xmodem

comport = serial.Serial('COM3', 460800)
isp = ispcmd.ispcmd(comport)
isp.checkisp()

isp.resetSystem()
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

diffFiles( 'a.bin', 'dump.bin' )
```
