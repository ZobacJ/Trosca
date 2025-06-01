[OBJECT1]
ID=45
GROUP=1
NAME=TrueRMS
MOS_ID=384     
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=21438765
VALUES=3
  VALUE01    =      UNSIGNED16,    00, U_ef      , %8d [LSB]
  VALUE02    =      UNSIGNED16,    16, I_ef      , %8d [LSB]
  VALUE03    =      UNSIGNED32,    32, Power     , %8d [LSB]

[OBJECT2]
ID=46
GROUP=1
NAME=DcAc50
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=21436587
VALUES=4
  VALUE01    =       INTEGER16,    00, U_dc      , %8d [LSB]
  VALUE02    =       INTEGER16,    16, I_dc      , %8d [LSB]
  VALUE03    =      UNSIGNED16,    32, U_ac50    , %8d [LSB]
  VALUE04    =      UNSIGNED16,    48, I_ac50    , %8d [LSB]

[OBJECT3]
ID=47
GROUP=1
NAME=Envelope
MOS_ID=896      
ENABLED=rx
LENGTH=8
FREQ=20
ENDIAN=21436587
VALUES=4
  VALUE01    =       INTEGER16,    00, U_min    , %8d [LSB]
  VALUE02    =       INTEGER16,    16, I_min    , %8d [LSB]
  VALUE03    =       INTEGER16,    32, U_max    , %8d [LSB]
  VALUE04    =       INTEGER16,    48, I_max    , %8d [LSB]

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

