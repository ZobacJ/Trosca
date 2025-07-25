[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, D4QA_X   , %8d [LSB]
  VALUE02    =       INTEGER16,    16, D4QA_Y   , %8d [LSB]
  VALUE03    =       INTEGER16,    32, D4QA_Sum , %8d [LSB]
  VALUE04    =       INTEGER16,    48, Zero    , %8d [LSB]

[OBJECT2]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, D4QB_X   , %8d [LSB]
  VALUE02    =       INTEGER16,    16, D4QB_Y   , %8d [LSB]
  VALUE03    =       INTEGER16,    32, D4QB_Sum , %8d [LSB]
  VALUE04    =       INTEGER16,    48, Zero    , %8d [LSB]

[OBJECT3]
NAME=rx3
GROUP=1
MOS_ID=896      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, AD0     , %8d [LSB]
  VALUE02    =       INTEGER16,    16, AD1     , %8d [LSB]
  VALUE03    =       INTEGER16,    32, AD2     , %8d [LSB]
  VALUE04    =       INTEGER16,    48, AD3     , %8d [LSB]

[OBJECT4]
NAME=rx4
GROUP=1
MOS_ID=1152      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, AD4     , %8d [LSB]
  VALUE02    =       INTEGER16,    16, AD5     , %8d [LSB]
  VALUE03    =       INTEGER16,    32, AD6     , %8d [LSB]
  VALUE04    =       INTEGER16,    48, AD7     , %8d [LSB]

[OBJECT5]
NAME=tx1
GROUP=1
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, DA1       , %8d [LSB]
  VALUE02    =       INTEGER32,    32, DA2       , %8d [LSB]

[OBJECT6]
NAME=tx2
GROUP=1
MOS_ID=768      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=1
  VALUE01    =       INTEGER32,    00, DA3       , %8d [LSB]

[OBJECT7]
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


[OBJECT8]
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

