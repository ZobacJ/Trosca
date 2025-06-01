[OBJECT1]
ID=25
GROUP=1
NAME=Data
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=21345678
VALUES=4
  VALUE01    =      INTEGER16,     00, Prutok     , %8d [LSB]
  VALUE02    =       INTEGER8,     16, Indikace   , %8d [LSB]
  VALUE03    =      INTEGER16,     32, Vccf       , %8d [LSB]
  VALUE04    =      INTEGER16,     48, Vflw       , %8d [LSB]


[OBJECT2]
ID=250
GROUP=1000
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


[OBJECT3]
ID=251
GROUP=1000
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

[OBJECT4]
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

[OBJECT5]
ID=25
GROUP=1
NAME=Data
MOS_ID=640      
ENABLED=tx
LENGTH=8
FREQ=5
ENDIAN=21345678
VALUES=4
  VALUE01    =      INTEGER16,     00, Prutok     , %8d [LSB]
  VALUE02    =       INTEGER8,     16, Indikace   , %8d [LSB]
  VALUE03    =      INTEGER16,     32, Vccf       , %8d [LSB]
  VALUE04    =      INTEGER16,     48, Vflw       , %8d [LSB]

