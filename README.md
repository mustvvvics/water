# 液位水温控制系统

## Instructions

系统程序放置在allnew.py

test文件放置各部分的测试程序

last文件放置温度传感器的C程序

## 运行说明

使用前应先运行startNetwork.sh

sudo bash startNetwork.sh

其后运行allnew.py

sudo python3 allnew.py

## 接线说明

### fan
ENB = 11                                        # site GPIO11 link ENB

IN3 = 29                                        # site GPIO29 link IN3

IN4 = 13                                        # site GPIO13 link IN4

### Peristaltic pump

ENA = 35                                        # site GPIO35 link ENA

IN1 = 31                                        # site GPIO31 link IN1

IN2 = 15                                        # site GPIO15 link IN2

### relay

RelayPin = 38                                   # Relay Control
