[OBJECT1]
ID=40
GROUP=1
NAME=Fast
MOS_ID=384      
ENABLED=rx
LENGTH=4
FREQ=100
ENDIAN=21436587
VALUES=2
  VALUE01    =       INTEGER16,    00, U100Hz    , %8d [LSB]
  VALUE02    =       INTEGER16,    16, I100Hz    , %8d [LSB]

[OBJECT2]
ID=35
GROUP=1
NAME=Lupa
MOS_ID=385      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=21436587
VALUES=4
  VALUE01    =       INTEGER16,    00, U1       , %8d [LSB]
  VALUE02    =       INTEGER16,    16, I1       , %8d [LSB]
  VALUE03    =       INTEGER16,    32, U2       , %8d [LSB]
  VALUE04    =       INTEGER16,    48, I2       , %8d [LSB]

[OBJECT3]
ID=45
GROUP=1
NAME=Slow
MOS_ID=386     
ENABLED=rx
LENGTH=4
FREQ=5
ENDIAN=21436587
VALUES=2
  VALUE01    =       INTEGER16,    00, Uef       , %8d [LSB]
  VALUE02    =       INTEGER16,    16, Ief       , %8d [LSB]

[OBJECT4]
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


[OBJECT5]
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

