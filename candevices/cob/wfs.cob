[OBJECT1]
ID=56
GROUP=1
NAME=Data
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=100
ENDIAN=12345678
VALUES=2
  VALUE01    =     UNSIGNED32,     00, Rychlost1  , %8d [LSB]
  VALUE02    =     UNSIGNED32,     32, Spotreba1  , %8d [LSB]

[OBJECT2]
ID=61
GROUP=1
NAME=Data
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=100
ENDIAN=12345678
VALUES=2
  VALUE01    =     UNSIGNED32,     00, Rychlost2  , %8d [LSB]
  VALUE02    =     UNSIGNED32,     32, Spotreba2  , %8d [LSB]

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

