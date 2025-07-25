[OBJECT1]
NAME=rx1
GROUP=1
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
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, AIN3    , %8d [LSB]
  VALUE02    =       INTEGER16,    16, AIN4    , %8d [LSB]
  VALUE03    =       INTEGER16,    32, AIN5    , %8d [LSB]
  VALUE04    =       INTEGER16,    48, AIN6    , %8d [LSB]

[OBJECT3]
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

[OBJECT4]
NAME=tx2
GROUP=1
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

[OBJECT5]
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


[OBJECT6]
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

[OBJECT7]
ID=252
GROUP=2000
NAME=NMTrx
MOS_ID=1792     
ENABLED=rx
LENGTH=1
FREQ=10
ENDIAN=12345678
VALUES=1
  VALUE01    =      UNSIGNED8,     00, Status    , %8d [LSB]

