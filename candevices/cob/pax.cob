[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=1000
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, ST1    , %8d [LSB]
  VALUE02    =       INTEGER16,    16, ST2    , %8d [LSB]
  VALUE03    =       INTEGER16,    32, ST3    , %8d [LSB]
  VALUE04    =       UNSIGNED16,   48, lambda    , %8d [LSB]

[OBJECT2]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=1000
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, azimuth , %8d [LSB]
  VALUE02    =       INTEGER16,    16, ellipt  , %8d [LSB]
  VALUE03    =       UNSIGNED16,   32, dop     , %8d [LSB]
  VALUE04    =       INTEGER16,    48, pwr_dBm , %8d [LSB]


[OBJECT3]
ID=250
GROUP=1000
NAME=SDOrx
MOS_ID=1408      
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

