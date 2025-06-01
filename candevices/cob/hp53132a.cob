[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, F_Counter1, %8d [LSB]
  VALUE02    =       INTEGER32,    32, F_Counter2, %8d [LSB]


[OBJECT2]
ID=250
GROUP=1
NAME=DataB
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
VALUES=5
ENDIAN=12345678
  VALUE01    =       INTEGER32,    00, MUX_Temp_Curr  , %8d [LSB]
  VALUE02    =       UNSIGNED8,    32, SW_Temperature , %8d [LSB]
  VALUE03    =       UNSIGNED8,    40, SW_Current     , %8d [LSB]
  VALUE04    =       UNSIGNED8,    48, SW_Drive       , %8d [LSB]
  VALUE05    =       UNSIGNED8,    56, SW_Lock        , %8d [LSB]
