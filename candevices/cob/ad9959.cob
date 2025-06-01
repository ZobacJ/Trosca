[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=3
   VALUE01    =       INTEGER16,    00, AD3_In, %8d [LSB]
   VALUE02    =       INTEGER16,    16, PID_OutputDisabled, %8d [LSB]
   VALUE03    =       INTEGER32,    32, DA1_Out  , %8d [LSB]

[OBJECT2]
ID=250
GROUP=1000
NAME=SDOrx
MOS_ID=1408      
ENABLED=rx
LENGTH=8
FREQ=50
ENDIAN=12345678
VALUES=4
  VALUE01    =      UNSIGNED8,     00, Command    , %8d [LSB]
  VALUE02    =     UNSIGNED16,     08, Index      , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, SubIndex   , %8d [LSB]
  VALUE04    =     UNSIGNED32,     32, Data       , %8d [LSB]


[OBJECT3]
ID=251
GROUP=1000
NAME=SDOtx
MOS_ID=1536     
ENABLED=tx
LENGTH=8
FREQ=50
ENDIAN=12345678
VALUES=4
  VALUE01    =      UNSIGNED8,     00, Command    , %8d [LSB]
  VALUE02    =     UNSIGNED16,     08, Index      , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, SubIndex   , %8d [LSB]
  VALUE04    =     UNSIGNED32,     32, Data       , %8d [LSB]

[OBJECT4]
NAME=tx1
GROUP=1
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=34125678
VALUES=2
   VALUE01    =       UNSIGNED32,    00, Frequency*10, %8d [LSB]
   VALUE02    =       UNSIGNED8,    32, Channel, %8d [LSB]


