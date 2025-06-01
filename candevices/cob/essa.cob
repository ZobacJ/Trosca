[OBJECT1]
NAME=rx1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=2
ENDIAN=21437856
VALUES=5
  VALUE01    =       UNSIGNED8,    00, reserved	, %8d [LSB]   
  VALUE02    =       UNSIGNED8,    08, status0	, %8d [LSB]
  VALUE03    =       UNSIGNED8,    16, status1	, %8d [LSB]
  VALUE04    =       UNSIGNED8,    24, status2	, %8d [LSB]	
  VALUE05    =       INTEGER32,    32, axis0   	, %8d [LSB]

[OBJECT2]
NAME=rx2
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=2
ENDIAN=34127856
VALUES=2
  VALUE01    =       INTEGER32,    00, axis1	, %8d [LSB]
  VALUE02    =       INTEGER32,    32, axis2	, %8d [LSB]
