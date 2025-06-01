[OBJECT1]
NAME=rx1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=3
   VALUE01    =       INTEGER16,    00, PID_INPUT(AD3), %8d [LSB]
   VALUE02    =       INTEGER16,    16, PID_OutputDisabled, %8d [LSB]
   VALUE03    =       INTEGER32,    32, PID_OUTPUT(DA1), %8d [LSB]

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
NAME=tx1
GROUP=1
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
   VALUE01    =       INTEGER32,    00, DA1_offst, %8d [LSB]
   VALUE02    =       INTEGER32,    32, DA2_offst, %8d [LSB]

[OBJECT5]
NAME=rx2
GROUP=1
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
   VALUE01    =       INTEGER16,    00, AD2, %8d [LSB]
   VALUE02    =       INTEGER16,    16, AD4, %8d [LSB]
   VALUE03    =       INTEGER16,    32, AD5, %8d [LSB]
   VALUE04    =       INTEGER16,    48, AD6, %8d [LSB]

[OBJECT6]
NAME=tx2
GROUP=1
MOS_ID=768      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=8
   VALUE01    =       UNSIGNED16,    	00, PID_OutputDisable, %8d [LSB]
   VALUE02    =       INTEGER16,    	16, PID_Setpoint0, %8d [LSB]
   VALUE03    =       BOOLEAN,    	32, b_output_SW1, %8d [LSB]
   VALUE04    =       BOOLEAN,    	33, b_output_SW2, %8d [LSB]
   VALUE05    =       BOOLEAN,    	34, b_output_SW3, %8d [LSB]
   VALUE06    =       BOOLEAN,    	35, b_output_SW4, %8d [LSB]
   VALUE07    =       BOOLEAN,    	36, b_SW_write_enable, %8d [LSB]   
   VALUE08    =       INTEGER16,    	48, PID_Setpoint1, %8d [LSB]


