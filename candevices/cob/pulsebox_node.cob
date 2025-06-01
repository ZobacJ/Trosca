[OBJECT1]
NAME=tx1
GROUP=1
MOS_ID=384      
ENABLED=tx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
   VALUE01    =	      INTEGER16,  00, reserved1, 	%8d [LSB]	
   VALUE02    =	      INTEGER16,  16, reserved2, 	%8d [LSB]
   VALUE03    =	      INTEGER16,  32, reserved3, 	%8d [LSB]
   VALUE04    =       BOOLEAN, 	  48, b_seq_running, 	%8d [LSB]
   


[OBJECT2]
NAME=rx1
GROUP=1
MOS_ID=512      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=4
  VALUE01    =       INTEGER16,    00, rsvd_rx1       , %8d [LSB]
  VALUE02    =       INTEGER16,    16, rsvd_rx2       , %8d [LSB]
  VALUE03    =       INTEGER16,    32, rsvd_rx3       , %8d [LSB]
  VALUE04    =       INTEGER16,    48, rsvd_rx4       , %8d [LSB]






