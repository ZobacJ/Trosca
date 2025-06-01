[OBJECT1]
NAME=Intf1
GROUP=1
MOS_ID=384      
ENABLED=rx
LENGTH=8
FREQ=500
ENDIAN=12345678
VALUES=3
  VALUE01    =       INTEGER32,    00, Length, %8d [LSB]
;  VALUE02    =        INTEGER8,    32, Dummy1, %8d [LSB]
;  VALUE03    =        INTEGER8,    40, Dummy2, %8d [LSB]
  VALUE02    =        UNSIGNED8,    48, X_axis, %8d [LSB]
  VALUE03    =        UNSIGNED8,    56, Y_axis, %8d [LSB]

;[OBJECT2]
;NAME=Intf2
;GROUP=1
;MOS_ID=640      
;ENABLED=rx
;LENGTH=8
;ENDIAN=12345678
;VALUES=5
;  VALUE01    =       INTEGER32,    00, Length, %8d [LSB]
;  VALUE02    =        INTEGER8,    32, Dummy1, %8d [LSB]
;  VALUE03    =        INTEGER8,    40, Dummy2, %8d [LSB]
;  VALUE04    =       UNSIGNED8,    48, X_axis, %8d [LSB]
;  VALUE05    =       UNSIGNED8,    56, Y_axis, %8d [LSB]
