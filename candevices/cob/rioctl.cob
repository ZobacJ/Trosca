[OBJECT1]
NAME=DataTEC
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=3
  VALUE01    =       UNSIGNED16,    00, R_LSB, %8d [LSB]
  VALUE02    =       UNSIGNED16,    16, R_Ohms, %8d [LSB]
  VALUE03    =       UNSIGNED16,    32, RsetPt_Ohms, %8d [LSB]

[OBJECT2]
NAME=DataI
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=3
  VALUE01    =       UNSIGNED16,    00, PD_LSB, %8d [LSB]
  VALUE02    =       UNSIGNED16,    16, PD_mA_x_1000, %8d [LSB]
  VALUE03    =       UNSIGNED16,    32, SetPt_mA_x_10, %8d [LSB]

[OBJECT3]
GROUP=1
NAME=Ctl
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
VALUES=4
ENDIAN=12345678
  VALUE01    =       INTEGER32,    00, MUX_DataIn    , %8d [LSB]
  VALUE02    =       UNSIGNED8,    32, TEC_Temperature , %8d [LSB]
  VALUE03    =       UNSIGNED8,    40, TEC_Resistance  , %8d [LSB]
  VALUE04    =       UNSIGNED8,    48, Ild_Current  , %8d [LSB]


[OBJECT4]
NAME=Mon
MOS_ID=896
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=22
   VALUE01 =       UNSIGNED8,    0, FSM_state  , %8d [LSB]
   VALUE02 =       UNSIGNED8,    8, DebugVal  , %8d [LSB]
   VALUE03 =       BOOLEAN  ,    32, RS232_comm_OK  , %8d [LSB]
   VALUE04 =       BOOLEAN  ,    33, TurnKey_on       , %8d [LSB]
   VALUE05 =       BOOLEAN  ,    34, LD_ready        , %8d [LSB]
   VALUE06 =       BOOLEAN  ,    35, LD_on            , %8d [LSB]
   VALUE07 =       BOOLEAN  ,    48, LD_stable        , %8d [LSB]
   VALUE08 =       BOOLEAN  ,    49, Vcc_range , %8d [LSB]
   VALUE09 =       BOOLEAN  ,    50, Vld_range , %8d [LSB]
   VALUE10 =       BOOLEAN  ,    51, Vtec_range , %8d [LSB]
   VALUE11 =       BOOLEAN  ,    52, Itec_max_warn , %8d [LSB]
   VALUE12 =       BOOLEAN  ,    53, TEC_drv_warn , %8d [LSB]
   VALUE13 =       BOOLEAN  ,    54, Brd_temp_warn , %8d [LSB]
   VALUE14 =       BOOLEAN  ,    55, LD_temp_warn , %8d [LSB]
   VALUE15 =       BOOLEAN  ,    56, I_mon_warn , %8d [LSB]
   VALUE16 =       BOOLEAN  ,    57, TEC_Tset_warn , %8d [LSB]
   VALUE17 =       BOOLEAN  ,    58, TEC_status_warn , %8d [LSB]
   VALUE18 =       BOOLEAN  ,    59, reserved1 , %8d [LSB]
   VALUE19 =       BOOLEAN  ,    60, reserved2 , %8d [LSB]
   VALUE20 =       BOOLEAN  ,    61, Firmware_OK , %8d [LSB]
   VALUE21 =       BOOLEAN  ,    62, Brd_temp_fault , %8d [LSB]
   VALUE22 =       BOOLEAN  ,    63, LD_temp_fault , %8d [LSB]


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
ENDIAN=12345678
VALUES=4
  VALUE01    =      UNSIGNED8,     00, Command    , %8d [LSB]
  VALUE02    =     UNSIGNED16,     08, Index      , %8d [LSB]
  VALUE03    =      UNSIGNED8,     24, SubIndex   , %8d [LSB]
  VALUE04    =     UNSIGNED32,     32, Data       , %8d [LSB]

[OBJECT7]  
NAME=nmt
GROUP=2000
MOS_ID=1792
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=1
  VALUE01    =       INTEGER8,      00, devState    , %8d [LSB] 

