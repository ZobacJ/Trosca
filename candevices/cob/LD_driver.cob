[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12347856
VALUES=3
  VALUE01    =       INTEGER16,    00, I_LD, %8d [LSB]
  VALUE02    =       INTEGER16,    16, I_PD, %8d [LSB]
  VALUE03    =       INTEGER32,    32, DAC_Value, %8d [LSB]
  

[OBJECT2]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, Vss    , %8d [LSB]
  VALUE02    =       INTEGER16,    16, Vdd    , %8d [LSB]
  VALUE03    =       INTEGER16,    32, LDStatus    , %8d [LSB]
  VALUE04    =       INTEGER16,    48, rsvd   , %8d [LSB]
  
[OBJECT3]
NAME=tx1
GROUP=1
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, LD_DAC_Target       , %8d [LSB]
  VALUE02    =       UNSIGNED16,    32, LD_ON       , %8d [LSB]


[OBJECT4]
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


[OBJECT5]
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

