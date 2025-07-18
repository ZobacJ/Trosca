[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, U1_Re, %8d [LSB]
  VALUE02    =       INTEGER16,    16, U1_Im, %8d [LSB]
  VALUE03    =       INTEGER16,    32, U2_Re, %8d [LSB]
  VALUE04    =       INTEGER16,    48, U2_Im, %8d [LSB]

[OBJECT2]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, AIN2    , %8d [LSB]
  VALUE02    =       INTEGER16,    16, AIN3    , %8d [LSB]
  VALUE03    =       INTEGER16,    32, AIN4    , %8d [LSB]
  VALUE04    =       INTEGER16,    48, AIN5    , %8d [LSB]

[OBJECT3]
NAME=rx3
GROUP=1
MOS_ID=896      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, AIN6    , %8d [LSB]
  VALUE02    =       INTEGER16,    16, U3_Re    , %8d [LSB]
  VALUE03    =       INTEGER16,    32, U3_Im    , %8d [LSB]
  VALUE04    =       INTEGER16,    48, N/A    , %8d [LSB]

[OBJECT4]
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

[OBJECT5]
NAME=tx2
GROUP=1
MOS_ID=768      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=3
  VALUE01    =       INTEGER32,    00, DA3       , %8d [LSB]
  VALUE02    =       INTEGER16,    32, DA1_magnitude, %8d [LSB]
  VALUE03    =       INTEGER16,    48, DA2_magnitude, %8d [LSB]
  

[OBJECT6]
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


[OBJECT7]
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

