[OBJECT1]
NAME=rx1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=200
ENDIAN=12345678
VALUES=3
  VALUE01    =       UNSIGNED32,   00, F_peak0*10	, %8d [LSB]   
  VALUE02    =       INTEGER16,    32, Re_peak0	, %8d [LSB]
  VALUE03    = 	     INTEGER16,	   48, Im_peak0	, %8d [LSB]


[OBJECT2]
NAME=rx2
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=200
ENDIAN=12345678
VALUES=3
  VALUE01    =       UNSIGNED32,   00, F_peak1*10	, %8d [LSB]   
  VALUE02    =       INTEGER16,    32, Re_peak1	, %8d [LSB]
  VALUE03    = 	     INTEGER16,	   48, Im_peak1	, %8d [LSB]


[OBJECT3]
ID=250
GROUP=1000
NAME=SDOrx
MOS_ID=1408      
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


[OBJECT4]
ID=251
GROUP=1000
NAME=SDOtx
MOS_ID=1536     
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



	
  