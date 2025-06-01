[OBJECT1]
ID=65
GROUP=1
NAME=Data_A
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=12345678
VALUES=4
  VALUE01    =      INTEGER16,     00, Dist       , %8d [LSB]
  VALUE02    =      INTEGER16,     16, AIN4       , %8d [LSB]
  VALUE03    =      INTEGER16,     32, AIN5       , %8d [LSB]
  VALUE04    =      INTEGER16,     48, Zero       , %8d [LSB]

[OBJECT2]
ID=249
GROUP=1
NAME=Data_B
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=12345678
VALUES=4
  VALUE01    =      INTEGER16,     00, AIN0       , %8d [LSB]
  VALUE02    =      INTEGER16,     16, AIN1       , %8d [LSB]
  VALUE03    =      INTEGER16,     32, AIN2       , %8d [LSB]
  VALUE04    =      INTEGER16,     48, AIN3       , %8d [LSB]

[OBJECT3]
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


[OBJECT4]
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

