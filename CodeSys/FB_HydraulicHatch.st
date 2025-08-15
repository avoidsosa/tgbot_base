FUNCTION_BLOCK FB_HydraulicHatch
VAR_INPUT
	Enable : BOOL; (* Permit from emergency & interlocks *)
	ManualMode : BOOL; (* TRUE = Manual, FALSE = Automatic; automatic is not allowed *)
	ManualOpenCmd : BOOL; (* HMI open command *)
	ManualCloseCmd : BOOL; (* HMI close command *)
	LS_Open : BOOL; (* Limit switch: hatch at OPEN position *)
	LS_Closed : BOOL; (* Limit switch: hatch at CLOSED position *)
	CircuitBreakerTrip : BOOL; (* Circuit breaker trip for hydraulic motor *)
END_VAR
VAR_OUTPUT
	CmdOpen : BOOL; (* Command to open the hatch *)
	CmdClose : BOOL; (* Command to close the hatch *)
	Busy : BOOL; (* TRUE when either open or close command is active *)
	InterlockActive : BOOL; (* TRUE if inhibited due to limits, mode, CB trip or no permit *)
END_VAR

VAR
	localPermit : BOOL;
END_VAR

(* Only manual mode is allowed; apply permits and interlocks *)
localPermit := Enable AND ManualMode AND NOT CircuitBreakerTrip;

CmdOpen := FALSE;
CmdClose := FALSE;

IF localPermit THEN
	IF ManualOpenCmd AND NOT LS_Open THEN
		CmdOpen := TRUE;
	ELSIF ManualCloseCmd AND NOT LS_Closed THEN
		CmdClose := TRUE;
	END_IF
END_IF;

Busy := CmdOpen OR CmdClose;
InterlockActive := NOT localPermit OR (ManualOpenCmd AND LS_Open) OR (ManualCloseCmd AND LS_Closed);
END_FUNCTION_BLOCK