[OBJECT1]
ID=250
GROUP=1
NAME=DataA
MOS_ID=384      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, F_Rep, %8d [LSB]
  VALUE02    =       INTEGER32,    32, F_Ofs, %8d [LSB]

[OBJECT2]
NAME=DataB
GROUP=1
MOS_ID=640      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       BOOLEAN,      00, Bool_Out01, %1d [LSB]
  VALUE02    =       BOOLEAN,      01, Bool_Out01, %1d [LSB]
  VALUE03    =       BOOLEAN,      02, Bool_Out01, %1d [LSB]
  VALUE04    =       BOOLEAN,      03, Bool_Out01, %1d [LSB]


[OBJECT3]
NAME=DataB
GROUP=1
MOS_ID=896      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=6
  VALUE01    =       INTEGER32,    00, F_beat_req, %8d [LSB]
  VALUE02    =       INTEGER16,    32, Int16_reserved, %8d [LSB]
  VALUE03    =       BOOLEAN,      48, B_PLL2ndOffReq, %1d [LSB]
  VALUE04    =       BOOLEAN,      49, B_AutoLockReq, %1d [LSB]
  VALUE05    =       BOOLEAN,      50, B_F_Beat_pol, %1d [LSB]
  VALUE06    =       BOOLEAN,      51, B_rsv4, %1d [LSB]

