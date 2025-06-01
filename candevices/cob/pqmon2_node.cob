[OBJECT1]
NAME=rx1
MOS_ID=384      
ENABLED=tx
LENGTH=8
FREQ=100
ENDIAN=12345678
VALUES=3
  VALUE01    =       UNSIGNED16,         00, seqcnt, %8d [LSB] 
  VALUE02    =       UNSIGNED16,         16, active, %8d [LSB] 
  VALUE03    =       UNSIGNED8,         32, ptid, %8d [LSB]

[OBJECT2]
NAME=rx2
MOS_ID=640
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       UNSIGNED16,         0, ratio0, %8d [LSB] 
  VALUE02    =       UNSIGNED16,        16, ratio1, %8d [LSB] 
  VALUE03    =       UNSIGNED16,        32, ratio2, %8d [LSB] 
  VALUE04    =       UNSIGNED16,        48, ratio3, %8d [LSB] 

[OBJECT3]
NAME=rx3
MOS_ID=896
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=8
  VALUE01    =       UNSIGNED8,         0, ratio0, %8d [LSB] 
  VALUE02    =       UNSIGNED8,         8, ratio1, %8d [LSB] 
  VALUE03    =       UNSIGNED8,        16, ratio2, %8d [LSB] 
  VALUE04    =       UNSIGNED8,        24, ratio3, %8d [LSB] 
  VALUE05    =       UNSIGNED8,        32, ratio4, %8d [LSB] 
  VALUE06    =       UNSIGNED8,        40, ratio5, %8d [LSB] 
  VALUE07    =       UNSIGNED8,        48, ratio6, %8d [LSB] 
  VALUE08    =       UNSIGNED8,        56, ratio7, %8d [LSB] 


[OBJECT4]
ID=250
GROUP=1000
NAME=SDOrx
MOS_ID=1408      
ENABLED=tx
LENGTH=8
FREQ=50
;ENDIAN=21436587
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
ENABLED=rx
LENGTH=8
FREQ=50
;ENDIAN=21436587
ENDIAN=12345678
VALUES=4
  VALUE01    =      UNSIGNED8,     00, Command    , %8d [LSB]
  VALUE02    =     UNSIGNED16,     08, Index      , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, SubIndex   , %8d [LSB]
  VALUE04    =     UNSIGNED32,     32, Data       , %8d [LSB]

[OBJECT6]  
NAME=nmt
GROUP=2000
MOS_ID=1792
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=1
  VALUE01    =       INTEGER8,      00, devState    , %8d [LSB] 

