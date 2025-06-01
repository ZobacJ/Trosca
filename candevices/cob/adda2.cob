[OBJECT1]
NAME=rx1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, SyncD_Re, %8d [LSB]
  VALUE02    =       INTEGER16,    16, SyncD_Im, %8d [LSB]
  VALUE03    =       INTEGER16,    32, AIN1    , %8d [LSB]
  VALUE04    =       INTEGER16,    48, AIN2    , %8d [LSB]

[OBJECT2]
NAME=tx1
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, DA1       , %8d [LSB]
  VALUE02    =       INTEGER32,    32, DA2       , %8d [LSB]

[OBJECT3]
NAME=tx2
MOS_ID=768      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=5
  VALUE01    =       INTEGER32,    00, DA3       , %8d [LSB]
  VALUE02    =        INTEGER8,    32, Modulatn  , %8d [LSB]
  VALUE03    =        INTEGER8,    40, Phase     , %8d [LSB]
  VALUE04    =        INTEGER8,    48, Output    , %8d [LSB]
  VALUE05    =        INTEGER8,    56, Input     , %8d [LSB]

[OBJECT4]
ID=250
GROUP=1
NAME=SDOrx
MOS_ID=1408      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=12345678
VALUES=4
  VALUE01    =      UNSIGNED8,     00, Command    , %8d [LSB]
  VALUE02    =     UNSIGNED16,     08, Index      , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, SubIndex   , %8d [LSB]
  VALUE04    =     UNSIGNED32,     32, Data       , %8d [LSB]


[OBJECT5]
ID=251
GROUP=1
NAME=SDOtx
MOS_ID=1536     
ENABLED=tx
LENGTH=8
FREQ=5
ENDIAN=12345678
VALUES=4
  VALUE01    =      UNSIGNED8,     00, Command    , %8d [LSB]
  VALUE02    =     UNSIGNED16,     08, Index      , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, SubIndex   , %8d [LSB]
  VALUE04    =     UNSIGNED32,     32, Data       , %8d [LSB]

