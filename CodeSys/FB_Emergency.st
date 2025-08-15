FUNCTION_BLOCK FB_Emergency
VAR_INPUT
	ModeManual : BOOL; (* Current mode for information if needed *)
	ResetCmd : BOOL; (* HMI reset command *)
	(* VFD faults - individual inputs *)
	Fan1VfdFault : BOOL;
	Fan2VfdFault : BOOL;
	Fan3VfdFault : BOOL;
	Fan4VfdFault : BOOL;
	Fan5VfdFault : BOOL;
	TransportFanVfdFault : BOOL;
	ScrewVfdFault : BOOL;
	Vibrator1VfdFault : BOOL;
	Vibrator2VfdFault : BOOL;
	(* Circuit breaker trips *)
	Vibrator1CBTrip : BOOL;
	Vibrator2CBTrip : BOOL;
	HydraulicCBTrip : BOOL;
END_VAR
VAR_OUTPUT
	EmergencyActive : BOOL; (* Latch TRUE if any emergency condition present *)
	GlobalPermit : BOOL; (* TRUE when no emergency conditions and not latched *)
END_VAR
VAR
	anyFault : BOOL;
	anyTrip : BOOL;
	fanFaultAggregate : BOOL;
END_VAR

(* Aggregate all configured faults *)
fanFaultAggregate := Fan1VfdFault OR Fan2VfdFault OR Fan3VfdFault OR Fan4VfdFault OR Fan5VfdFault;
anyFault := fanFaultAggregate OR TransportFanVfdFault OR ScrewVfdFault OR Vibrator1VfdFault OR Vibrator2VfdFault;
anyTrip := Vibrator1CBTrip OR Vibrator2CBTrip OR HydraulicCBTrip;

(* Latch on any fault or trip; reset only when ResetCmd and all clear *)
IF EmergencyActive THEN
	IF ResetCmd AND NOT anyFault AND NOT anyTrip THEN
		EmergencyActive := FALSE;
	END_IF
ELSE
	IF anyFault OR anyTrip THEN
		EmergencyActive := TRUE;
	END_IF
END_IF;

GlobalPermit := NOT EmergencyActive;
END_FUNCTION_BLOCK