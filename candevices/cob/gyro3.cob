[OBJECT1]
ID=250
GROUP=1
NAME=DataA
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=125
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, VDD_2      , %8d [LSB]
  VALUE02    =       INTEGER32,    32, ACC_X      , %8d [LSB]

[OBJECT2]
ID=250
GROUP=1
NAME=DataB
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=125
VALUES=2
ENDIAN=12345678
  VALUE01    =       INTEGER32,    00, ACC_Y      , %8d [LSB]
  VALUE02    =       INTEGER32,    32, ACC_Z      , %8d [LSB]

[OBJECT3]
ID=250
GROUP=1
NAME=DataC
MOS_ID=896      
ENABLED=rx
LENGTH=8
FREQ=125
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, GYRO_X     , %8d [LSB]
  VALUE02    =       INTEGER32,    32, GYRO_Z     , %8d [LSB]

[OBJECT4]
ID=250
GROUP=1
NAME=DataD
MOS_ID=1152      
ENABLED=rx
LENGTH=8
FREQ=125
VALUES=2
ENDIAN=12345678
  VALUE01    =       INTEGER32,    00, TGYRO_X    , %8d [LSB]
  VALUE02    =       INTEGER32,    32, GYRO_Y     , %8d [LSB]

[OBJECT5]
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


[OBJECT6]
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
                      
