PROGRAM PLC_PRG
VAR
	(* Mode *)
	modeManual : BOOL; (* 1=Manual, 0=Automatic from I_ModeManual *)

	(* Emergency FB and adapter variables *)
	emg : FB_Emergency;
	emgFanFault1 : BOOL;
	emgFanFault2 : BOOL;
	emgFanFault3 : BOOL;
	emgFanFault4 : BOOL;
	emgFanFault5 : BOOL;

	(* Auto control FB *)
	autoCtl : FB_AutoControl;

	(* Fans FB instances *)
	fbFan1 : FB_Fan;
	fbFan2 : FB_Fan;
	fbFan3 : FB_Fan;
	fbFan4 : FB_Fan;
	fbFan5 : FB_Fan;

	(* Transport fan FB instance *)
	fbTransportFan : FB_Fan;

	(* Screw conveyor FB instance *)
	fbScrew : FB_ScrewConveyor;

	(* Vibrators FB instances *)
	fbVib1 : FB_Vibrator;
	fbVib2 : FB_Vibrator;

	(* Hydraulic hatch FB instance *)
	fbHatch : FB_HydraulicHatch;

	(* Internal wires for auto commands *)
	aFan1Start : BOOL;
	aFan2Start : BOOL;
	aFan3Start : BOOL;
	aFan4Start : BOOL;
	aFan5Start : BOOL;
	aTransportStart : BOOL;
	aScrewStart : BOOL;
	aVib1Start : BOOL;
	aVib2Start : BOOL;

	(* Global permit *)
	permitGlobal : BOOL;
END_VAR

(* Mode handling *)
modeManual := I_ModeManual;
Status_ModeManual := modeManual;

(* Emergency handling; map faults individually to avoid arrays in PLC_PRG *)
emgFanFault1 := I_Fan1_VFD_Fault;
emgFanFault2 := I_Fan2_VFD_Fault;
emgFanFault3 := I_Fan3_VFD_Fault;
emgFanFault4 := I_Fan4_VFD_Fault;
emgFanFault5 := I_Fan5_VFD_Fault;

emg(ModeManual := modeManual,
	ResetCmd := HMI_ResetFaults,
	Fan1VfdFault := emgFanFault1,
	Fan2VfdFault := emgFanFault2,
	Fan3VfdFault := emgFanFault3,
	Fan4VfdFault := emgFanFault4,
	Fan5VfdFault := emgFanFault5,
	TransportFanVfdFault := I_TransportFan_VFD_Fault,
	ScrewVfdFault := I_Screw_VFD_Fault,
	Vibrator1VfdFault := I_Vibrator1_VFD_Fault,
	Vibrator2VfdFault := I_Vibrator2_VFD_Fault,
	Vibrator1CBTrip := I_Vibrator1_CB_Trip,
	Vibrator2CBTrip := I_Vibrator2_CB_Trip,
	HydraulicCBTrip := I_Hydraulic_CB_Trip);

permitGlobal := emg.GlobalPermit;
Status_EmergencyActive := emg.EmergencyActive;

(* Automatic control *)
autoCtl(AutoMode := NOT modeManual,
	AutoStartRequest := HMI_Auto_Start,
	GlobalPermit := permitGlobal);

Status_AutoEnabled := autoCtl.AutoEnabled;

(* Cache auto commands for readability *)
aFan1Start := autoCtl.Fan1Start;
aFan2Start := autoCtl.Fan2Start;
aFan3Start := autoCtl.Fan3Start;
aFan4Start := autoCtl.Fan4Start;
aFan5Start := autoCtl.Fan5Start;
aTransportStart := autoCtl.TransportFanStart;
aScrewStart := autoCtl.ScrewStart;
aVib1Start := autoCtl.Vibrator1Start;
aVib2Start := autoCtl.Vibrator2Start;

(* Local Fans 1..5 *)
fbFan1(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Fan1_Start, AutoStartCmd := aFan1Start, DriveFault := I_Fan1_VFD_Fault);
Q_Fan1_Run := fbFan1.CmdRun;
Status_Fan1_Running := fbFan1.StatusRunning;

fbFan2(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Fan2_Start, AutoStartCmd := aFan2Start, DriveFault := I_Fan2_VFD_Fault);
Q_Fan2_Run := fbFan2.CmdRun;
Status_Fan2_Running := fbFan2.StatusRunning;

fbFan3(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Fan3_Start, AutoStartCmd := aFan3Start, DriveFault := I_Fan3_VFD_Fault);
Q_Fan3_Run := fbFan3.CmdRun;
Status_Fan3_Running := fbFan3.StatusRunning;

fbFan4(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Fan4_Start, AutoStartCmd := aFan4Start, DriveFault := I_Fan4_VFD_Fault);
Q_Fan4_Run := fbFan4.CmdRun;
Status_Fan4_Running := fbFan4.StatusRunning;

fbFan5(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Fan5_Start, AutoStartCmd := aFan5Start, DriveFault := I_Fan5_VFD_Fault);
Q_Fan5_Run := fbFan5.CmdRun;
Status_Fan5_Running := fbFan5.StatusRunning;

(* Transport Fan *)
fbTransportFan(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_TransportFan_Start, AutoStartCmd := aTransportStart, DriveFault := I_TransportFan_VFD_Fault);
Q_TransportFan_Run := fbTransportFan.CmdRun;
Status_TransportFan_Running := fbTransportFan.StatusRunning;

(* Screw Conveyor *)
fbScrew(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Screw_Start, AutoStartCmd := aScrewStart, DriveFault := I_Screw_VFD_Fault);
Q_Screw_Run := fbScrew.CmdRun;
Status_Screw_Running := fbScrew.StatusRunning;

(* Vibrators *)
fbVib1(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Vibrator1_Start, AutoStartCmd := aVib1Start, DriveFault := I_Vibrator1_VFD_Fault, CircuitBreakerTrip := I_Vibrator1_CB_Trip);
Q_Vibrator1_Run := fbVib1.CmdRun;
Status_Vibrator1_Running := fbVib1.StatusRunning;

fbVib2(Enable := permitGlobal, ManualMode := modeManual, ManualStartCmd := HMI_Vibrator2_Start, AutoStartCmd := aVib2Start, DriveFault := I_Vibrator2_VFD_Fault, CircuitBreakerTrip := I_Vibrator2_CB_Trip);
Q_Vibrator2_Run := fbVib2.CmdRun;
Status_Vibrator2_Running := fbVib2.StatusRunning;

(* Hydraulic Hatch - manual only with interlocks *)
fbHatch(Enable := permitGlobal, ManualMode := modeManual, ManualOpenCmd := HMI_Hydraulic_Open, ManualCloseCmd := HMI_Hydraulic_Close, LS_Open := I_Hatch_Open_LS, LS_Closed := I_Hatch_Closed_LS, CircuitBreakerTrip := I_Hydraulic_CB_Trip);
Q_Hydraulic_Open := fbHatch.CmdOpen;
Q_Hydraulic_Close := fbHatch.CmdClose;
Status_Hydraulic_Busy := fbHatch.Busy;
END_PROGRAM