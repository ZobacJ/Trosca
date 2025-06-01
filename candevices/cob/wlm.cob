[OBJECT1]
NAME=rx1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=100
ENDIAN=12345678
VALUES=2
  VALUE01    =       UNSIGNED32,    00, frequency_GHz, %8d [LSB]
  VALUE02    =       UNSIGNED32,    32, frequency_Hz_fraction, %8d [LSB]

[OBJECT2]
NAME=rx2
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=100
ENDIAN=12345678
VALUES=2
  VALUE01    =       UNSIGNED32,    00, lambda_fm, %8d [LSB]   
  VALUE02    =       UNSIGNED32,    32, lambda_am, %8d [LSB] 

[OBJECT3]
NAME=rx3
MOS_ID=896      
ENABLED=rx
LENGTH=8
FREQ=100
ENDIAN=12345678
VALUES=2
  VALUE01    =       REAL32,    00, fwhm_MHz, %8d [LSB]
  VALUE02    =       REAL32,    32, fwhm_pm, %8d [LSB]

[OBJECT4]
NAME=rx4
MOS_ID=1152
ENABLED=rx
LENGTH=8
FREQ=100
ENDIAN=12345678
VALUES=4
  VALUE01    =       UNSIGNED8,    00, node_online, %8d [LSB]
  VALUE02    =       UNSIGNED8,    08, wlm_online, %8d [LSB]
  VALUE03    =       UNSIGNED8,    16, measurement_running, %8d [LSB]
  VALUE04    =       UNSIGNED8,    24, signal_ok, %8d [LSB]


[OBJECT5]
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

[OBJECT6]
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



	
  
