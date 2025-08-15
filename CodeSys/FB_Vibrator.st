FUNCTION_BLOCK FB_Vibrator
VAR_INPUT
	Enable : BOOL; (* Permit from emergency & interlocks *)
	ManualMode : BOOL; (* TRUE = Manual, FALSE = Automatic *)
	ManualStartCmd : BOOL; (* Manual start command from HMI *)
	AutoStartCmd : BOOL; (* Automatic start command from FB_AutoControl *)
	DriveFault : BOOL; (* VFD fault input if vibrator uses VFD; otherwise tie FALSE *)
	CircuitBreakerTrip : BOOL; (* Circuit breaker trip input (required) *)
END_VAR
VAR_OUTPUT
	CmdRun : BOOL; (* Command to the physical output *)
	StatusRunning : BOOL; (* Mirrors CmdRun for HMI/debug *)
	Inhibited : BOOL; (* TRUE if disabled due to fault or no permit *)
END_VAR

IF Enable AND NOT DriveFault AND NOT CircuitBreakerTrip THEN
	IF ManualMode THEN
		CmdRun := ManualStartCmd;
	ELSE
		CmdRun := AutoStartCmd;
	END_IF
ELSE
	CmdRun := FALSE;
END_IF;

StatusRunning := CmdRun;
Inhibited := NOT Enable OR DriveFault OR CircuitBreakerTrip;
END_FUNCTION_BLOCK