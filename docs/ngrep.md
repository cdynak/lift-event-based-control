
# CONTROLLER

## CONSOLE

```
14:49:31$ python graphics.py 
manual
```

## NGREP

```
14:49:21# ngrep -x tcp and port 8089 -d lo
interface: lo (127.0.0.0/255.0.0.0)
filter: (ip or ip6) and ( tcp and port 8089 )
###

silent after `python graphics.py`

now `python socket_control.py`

####
T 127.0.0.1:60536 -> 127.0.0.1:8089 [AP]
  31 3a 31                                              1:1             
##
T 127.0.0.1:60536 -> 127.0.0.1:8089 [AP]
  31 3a 32                                              1:2             
##
T 127.0.0.1:60536 -> 127.0.0.1:8089 [AP]
  31 3a 33                                              1:3             
##
T 127.0.0.1:60536 -> 127.0.0.1:8089 [AP]
  31 3a 34                                              1:4             
##
T 127.0.0.1:60536 -> 127.0.0.1:8089 [AP]
  31 3a 73                                              1:s             
#

after `python socket_control.py`

now "1:u" from simulator

after "1:u" from simulator

now "2:d" from simulator

after "2:d" from simulator

before automatic from simulator

after automatic from simulator 
```

# SIMULATOR

## CONSOLE

```
14:52:41$ python socket_control.py 
1:1
1:a
1:2
1:a
1:3
1:a
1:4
1:a
1:s
1:a
1:u
2:d
1:6
10:d
5:d
1:4
12:1
10:4
11:8
5:10
13:u
10:5
```

## NGREP

```
14:49:24# ngrep -x tcp and port 8090 -d lo
interface: lo (127.0.0.0/255.0.0.0)
filter: (ip or ip6) and ( tcp and port 8090 )
###

silent after `python graphics.py`

now `python socket_control.py`

####
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 61                                              1:a             
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 61                                              1:a             
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 61                                              1:a             
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 61                                              1:a             
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 61                                              1:a             
#

after `python socket_control.py`

now "1:u" from simulator#
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 75                                              1:u             
#

after "1:u" from simulator

now "2:d" from simulator

#
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  32 3a 64                                              2:d             
#

after "2:d" from simulator

before automatic from simulator

#
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 36                                              1:6             
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 30 3a 64                                           10:d            
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  35 3a 64                                              5:d             
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 3a 34                                              1:4             
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 32 3a 31                                           12:1            
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 30 3a 34                                           10:4            
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 31 3a 38                                           11:8            
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  35 3a 31 30                                           5:10            
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 33 3a 75                                           13:u            
##
T 127.0.0.1:8090 -> 127.0.0.1:60414 [AP]
  31 30 3a 35                                           10:5            
#

after automatic from simulator

```
