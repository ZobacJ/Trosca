[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=1000
ENDIAN=12345678
VALUES=4
  VALUE01    =       UNSIGNED16,    00, AIN1    , %8d [LSB]
  VALUE02    =       UNSIGNED16,    16, AIN2    , %8d [LSB]
  VALUE03    =       UNSIGNED16,    32, AIN3    , %8d [LSB]
  VALUE04    =       UNSIGNED16,    48, AIN4    , %8d [LSB]

[OBJECT2]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=1000
ENDIAN=12345678
VALUES=2
  VALUE01    =       REAL32,    00, DATA1    , %8d [LSB]
  VALUE02    =       REAL32,    32, DATA2    , %8d [LSB]

[OBJECT3]
NAME=tx1
GROUP=1
MOS_ID=512      
ENABLED=rx
LENGTH=8
FREQ=1000
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, AOUT1       , %8d [LSB]
  VALUE02    =       INTEGER32,    32, AOUT2       , %8d [LSB]

[OBJECT4]
NAME=tx2
GROUP=1
MOS_ID=768      
ENABLED=rx
LENGTH=8
FREQ=1000
ENDIAN=12345678
VALUES=5
  VALUE01    =       INTEGER32,    00, DataOut1  , %8d [LSB]
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
ENABLED=rx
LENGTH=8
FREQ=50
ENDIAN=12345678
VALUES=4
  VALUE01    =      UNSIGNED8,     00, Command    , %8d [LSB]
  VALUE02    =     UNSIGNED16,     08, Index      , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, SubIndex   , %8d [LSB]
  VALUE04    =     UNSIGNED32,     32, Data       , %8d [LSB]

