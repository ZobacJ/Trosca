[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4   
   VALUE01    =       INTEGER16,    00, AD1, %8d [LSB]
   VALUE02    =       INTEGER16,    16, AD2, %8d [LSB]
   VALUE03    =       INTEGER16,    32, AD3, %8d [LSB]
   VALUE04    =       INTEGER16,    48, AD4, %8d [LSB]

[OBJECT2]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=6   
   VALUE01    =       INTEGER16,    0, AD5, %8d [LSB]
   VALUE02    =       INTEGER16,    16, AD6, %8d [LSB]
   VALUE03    =       BOOLEAN,      32, PID1_ENABLED, %8d [LSB]
   VALUE04    =       BOOLEAN,      33, PID2_ENABLED, %8d [LSB]
   VALUE05    =       BOOLEAN,      34, PID1_LOCKED, %8d [LSB]
   VALUE06    =       BOOLEAN,      35, PID2_LOCKED, %8d [LSB]

[OBJECT3]
NAME=rx3
MOS_ID=896      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
   VALUE01    =       INTEGER32,    00, PID1_OUT, %8d [LSB]
   VALUE02    =       INTEGER32,    32, PID2_OUT, %8d [LSB]


[OBJECT4]
NAME=tx1
GROUP=1
MOS_ID=512     
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=9
   VALUE01    =       BOOLEAN,    	00, PID1_Enable, %8d [LSB]
   VALUE02    =       BOOLEAN,    	01, PID2_Enable, %8d [LSB]
   VALUE03    =       INTEGER16,    	16, PID1_RAM_Setpoint, %8d [LSB]
   VALUE04    =       INTEGER16,    	32, PID2_RAM_Setpoint, %8d [LSB]
   VALUE05    =       BOOLEAN,    	48, b_output_SW1, %8d [LSB]
   VALUE06    =       BOOLEAN,    	49, b_output_SW2, %8d [LSB]
   VALUE07    =       BOOLEAN,    	50, b_output_SW3, %8d [LSB]
   VALUE08    =       BOOLEAN,    	51, b_output_SW4, %8d [LSB]
   VALUE09    =       BOOLEAN,    	52, b_SW_write_enable, %8d [LSB]  

   
[OBJECT5]
NAME=tx2
GROUP=1
MOS_ID=768      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
   VALUE01    =       INTEGER32,    00, DA1, %8d [LSB]
   VALUE02    =       INTEGER32,    32, DA2, %8d [LSB]

[OBJECT6]
NAME=tx3
GROUP=1
MOS_ID=1024      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=1
   VALUE01    =       INTEGER32,    00, DA3, %8d [LSB]



[OBJECT7]
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


[OBJECT8]
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









