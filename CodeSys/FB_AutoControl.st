FUNCTION_BLOCK FB_AutoControl
VAR_INPUT
	AutoMode : BOOL; (* TRUE when selector is in automatic mode *)
	AutoStartRequest : BOOL; (* HMI request to enable automatic sequence *)
	GlobalPermit : BOOL; (* Permit from emergency handling; must be TRUE to run *)
END_VAR
VAR_OUTPUT
	AutoEnabled : BOOL; (* Auto mode active and permitted *)
	Fan1Start : BOOL; (* Auto start command for Local Fan 1 *)
	Fan2Start : BOOL; (* Auto start command for Local Fan 2 *)
	Fan3Start : BOOL; (* Auto start command for Local Fan 3 *)
	Fan4Start : BOOL; (* Auto start command for Local Fan 4 *)
	Fan5Start : BOOL; (* Auto start command for Local Fan 5 *)
	TransportFanStart : BOOL; (* Auto start command for Transport Fan *)
	ScrewStart : BOOL; (* Auto start command for Screw Conveyor *)
	Vibrator1Start : BOOL; (* Auto start command for Vibrator 1 *)
	Vibrator2Start : BOOL; (* Auto start command for Vibrator 2 *)
END_VAR
VAR
	tFan2 : TON;
	tFan3 : TON;
	tFan4 : TON;
	tFan5 : TON;
	tTransport : TON;
	tScrew : TON;
	tVibrators : TON;
	sequenceEnabled : BOOL;
END_VAR

(* Determine if automatic control is enabled *)
sequenceEnabled := AutoMode AND AutoStartRequest AND GlobalPermit;
AutoEnabled := sequenceEnabled;

(* Progressive start delays for fans 2..5 from AutoEnabled *)
tFan2(IN := sequenceEnabled, PT := T#1S);
tFan3(IN := sequenceEnabled, PT := T#2S);
tFan4(IN := sequenceEnabled, PT := T#3S);
tFan5(IN := sequenceEnabled, PT := T#4S);

Fan1Start := sequenceEnabled;
Fan2Start := sequenceEnabled AND tFan2.Q;
Fan3Start := sequenceEnabled AND tFan3.Q;
Fan4Start := sequenceEnabled AND tFan4.Q;
Fan5Start := sequenceEnabled AND tFan5.Q;

(* Transport fan after all local fans are on *)
tTransport(IN := sequenceEnabled AND tFan5.Q, PT := T#1S);
TransportFanStart := sequenceEnabled AND tTransport.Q;

(* Screw after transport fan is running *)
tScrew(IN := sequenceEnabled AND TransportFanStart, PT := T#1S);
ScrewStart := sequenceEnabled AND tScrew.Q;

(* Vibrators after screw is running; both start together *)
tVibrators(IN := sequenceEnabled AND ScrewStart, PT := T#2S);
Vibrator1Start := sequenceEnabled AND tVibrators.Q;
Vibrator2Start := sequenceEnabled AND tVibrators.Q;
END_FUNCTION_BLOCK