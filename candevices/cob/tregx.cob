[OBJECT1]
ID=250
GROUP=1
NAME=DataA
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=2
  VALUE01    =       INTEGER32,    00, Temperature, %8d [LSB]
  VALUE02    =       INTEGER32,    32, TEC_Current, %8d [LSB]

[OBJECT2]
ID=250
GROUP=1
NAME=DataB
MOS_ID=512      
ENABLED=tx
LENGTH=8
FREQ=500
VALUES=5
ENDIAN=12345678
  VALUE01    =       INTEGER32,    00, MUX_Temp_Curr  , %8d [LSB]
  VALUE02    =       UNSIGNED8,    32, SW_Temperature , %8d [LSB]
  VALUE03    =       UNSIGNED8,    40, SW_Current     , %8d [LSB]
  VALUE04    =       UNSIGNED8,    48, SW_Drive       , %8d [LSB]
  VALUE05    =       UNSIGNED8,    56, SW_Lock        , %8d [LSB]

[OBJECT3]
ID=250
GROUP=1
NAME=DataC
MOS_ID=640      
ENABLED=rx
LENGTH=8
FREQ=50
ENDIAN=12345678
VALUES=6
  VALUE01    =       BOOLEAN  ,    48, F_Drive       , %8d [LSB]
  VALUE02    =       BOOLEAN  ,    51, F_ZN_Process  , %8d [LSB] 
  VALUE03    =       BOOLEAN  ,    52, F_ZN_Ready    , %8d [LSB] 
  VALUE04    =       BOOLEAN  ,    54, F_Lock_Status , %8d [LSB] 
  VALUE05    =       BOOLEAN  ,    55, F_Loop_Closed , %8d [LSB] 
  VALUE06    =       UNSIGNED8,    56, ZN_Process    , %8d [LSB]


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
                      
