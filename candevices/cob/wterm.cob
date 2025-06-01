[OBJECT1]
ID=10
GROUP=1
NAME=Data
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=21436578
VALUES=4
  VALUE01    =      INTEGER16,     00, TAtm   , %8d [LSB]
  VALUE02    =      INTEGER16,     16, RH     , %8d [LSB]
  VALUE03    =      INTEGER16,     32, TInt   , %8d [LSB]
  VALUE04    =      UNSIGNED8,     48, Key    , %8d [LSB]

[OBJECT2]
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


[OBJECT3]
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
ID=252
GROUP=3000
NAME=EMCYrx
MOS_ID=128     
ENABLED=rx
LENGTH=8
FREQ=10
ENDIAN=12345678
VALUES=7
  VALUE01    =     UNSIGNED16,     00, ErrCode   , %8d [LSB]
  VALUE02    =      UNSIGNED8,     16, ErrReg    , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, MfcErr1   , %8d [LSB]
  VALUE04    =      UNSIGNED8,     32, MfcErr2   , %8d [LSB]
  VALUE05    =      UNSIGNED8,     40, MfcErr3   , %8d [LSB]
  VALUE06    =      UNSIGNED8,     48, MfcErr4   , %8d [LSB]
  VALUE07    =      UNSIGNED8,     56, MfcErr5   , %8d [LSB]
