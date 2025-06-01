[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=8
  VALUE01    =       UNSIGNED8,    00, B00, %8d [LSB]
  VALUE02    =       UNSIGNED8,    08, B00, %8d [LSB]
  VALUE03    =       UNSIGNED8,    16, B00, %8d [LSB]
  VALUE04    =       UNSIGNED8,    24, B00, %8d [LSB]
  VALUE05    =       UNSIGNED8,    32, B00, %8d [LSB]
  VALUE06    =       UNSIGNED8,    40, B00, %8d [LSB]
  VALUE07    =       UNSIGNED8,    48, B00, %8d [LSB]
  VALUE08    =       UNSIGNED8,    56, B00, %8d [LSB]

[OBJECT2]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=8
  VALUE01    =       UNSIGNED8,    00, B00, %8d [LSB]
  VALUE02    =       UNSIGNED8,    08, B00, %8d [LSB]
  VALUE03    =       UNSIGNED8,    16, B00, %8d [LSB]
  VALUE04    =       UNSIGNED8,    24, B00, %8d [LSB]
  VALUE05    =       UNSIGNED8,    32, B00, %8d [LSB]
  VALUE06    =       UNSIGNED8,    40, B00, %8d [LSB]
  VALUE07    =       UNSIGNED8,    48, B00, %8d [LSB]
  VALUE08    =       UNSIGNED8,    56, B00, %8d [LSB]


[OBJECT3]
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


[OBJECT4]
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

