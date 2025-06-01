[OBJECT1]
NAME=RPDO2
GROUP=1
MOS_ID=640      
ENABLED=tx
LENGTH=8
FREQ=5
ENDIAN=12345678
VALUES=6
  VALUE01    =       UNSIGNED16,    00, req_dist,    %8d [LSB]
  VALUE02    =       UNSIGNED16,    16, req_angle,   %8d [LSB]
  VALUE03    =        UNSIGNED8,    32, t1_space,    %8d [LSB]
  VALUE04    =        UNSIGNED8,    40, t2_space,    %8d [LSB]
  VALUE05    =        UNSIGNED8,    48, code_seq,    %8d [LSB]
  VALUE06    =        UNSIGNED8,    56, t3_space,    %8d [LSB]

[OBJECT2]
NAME=TPDO2_ZB
GROUP=1
MOS_ID=768      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=12345678
VALUES=6
  VALUE01    =       UNSIGNED16,    00, distance,   %8d [LSB]
  VALUE02    =       UNSIGNED16,    16, angle,      %8d [LSB]
  VALUE03    =        UNSIGNED8,    32, dist_seq,   %8d [LSB]
  VALUE04    =        UNSIGNED8,    40, angle_seq,  %8d [LSB]
  VALUE05    =        UNSIGNED8,    48, voltage,    %8d [LSB]
  VALUE06    =        UNSIGNED8,    56, current,    %8d [LSB]

[OBJECT3]
NAME=TPDO4
GROUP=1
MOS_ID=1152      
ENABLED=rx
LENGTH=8
FREQ=5
ENDIAN=12345678
VALUES=7
  VALUE01    =      UNSIGNED16,    00, TgtCurDist, %8d [LSB]
  VALUE02    =       UNSIGNED8,    16, TgtCurAngle,%8d [LSB]
  VALUE03    =       UNSIGNED8,    24, TgtBat,     %8d [LSB]
  VALUE04    =       UNSIGNED8,    32, distStst,   %8d [LSB]
  VALUE05    =       UNSIGNED8,    40, turnSts,    %8d [LSB]
  VALUE06    =       UNSIGNED8,    48, TermSts,    %8d [LSB]
  VALUE07    =       UNSIGNED8,    56, TermIn,     %8d [LSB]

[OBJECT4]
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


[OBJECT5]
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

