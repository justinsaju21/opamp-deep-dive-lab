import numpy as np

class OpAmpSolver:
    def __init__(self, config_type, R_in, R_f, V_in, V_cc, A_ol=100000, C=1e-6, V_in2=0, R_in2=10000):
        self.config_type = config_type
        self.R_in = R_in
        self.R_f = R_f
        self.V_in = V_in
        self.V_cc = V_cc
        self.A_ol = A_ol
        self.C = C
        self.V_in2 = V_in2
        self.R_in2 = R_in2
        
        # Default values
        self.ideal_gain = 0
        self.actual_gain = 0
        self.beta = 0
        self.V_out = 0
        self.V_minus = 0
        self.V_plus = 0
        self.I_in = 0
        self.I_f = 0
        self.I_Rin = 0

    def calculate_parameters(self):
        # Feedback Factor (Beta)
        if self.config_type == "Non-Inverting":
            self.beta = self.R_in / (self.R_in + self.R_f)
        elif self.config_type == "Voltage Follower":
            self.beta = 1.0
        elif self.config_type in ["Inverting", "Summing Amplifier"]:
            self.beta = self.R_in / (self.R_in + self.R_f) # Simplified for summing
        else:
            # Integrator/Differentiator frequency dependent, use DC approximation for static state
            self.beta = 1.0 # Approximation

        # Ideal Closed Loop Gain (DC / Static)
        if self.config_type == "Inverting":
            self.ideal_gain = -self.R_f / self.R_in
        elif self.config_type == "Non-Inverting":
            self.ideal_gain = 1 + (self.R_f / self.R_in)
        elif self.config_type == "Voltage Follower":
            self.ideal_gain = 1.0
        elif self.config_type == "Summing Amplifier":
            # Vout = -Rf * (V1/R1 + V2/R2)
            # Gain isn't a single number relative to V1, but let's store the factor -Rf/Rin
            self.ideal_gain = -self.R_f / self.R_in 
        
        # Static Output Calculation
        if self.config_type == "Summing Amplifier":
            raw_vout = -self.R_f * (self.V_in/self.R_in + self.V_in2/self.R_in2)
        elif self.config_type == "Difference Amplifier":
            # Vout = (Rf/Rin) * (V2 - V1)
            # V1 = V_in (Inverting), V2 = V_in2 (Non-Inverting)
            raw_vout = (self.R_f / self.R_in) * (self.V_in2 - self.V_in)
        elif self.config_type == "Integrator":
            # DC Gain is infinite (capacitor open), practically limited by A_ol
            raw_vout = -self.A_ol * (self.V_in - 0) # Saturation likely
        elif self.config_type == "Differentiator":
            # DC Gain is 0 (capacitor open blocks DC)
            raw_vout = 0
        else:
            raw_vout = self.V_in * self.ideal_gain # Using ideal for simplicity in static view

        self.V_out = np.clip(raw_vout, -self.V_cc, self.V_cc)
        self.actual_gain = self.ideal_gain # Placeholder for complex types

        # Node Voltages (Simplified for new modes)
        if self.config_type in ["Inverting", "Integrator", "Differentiator", "Summing Amplifier"]:
            self.V_plus = 0
            self.V_minus = 0 # Virtual Ground approximation
        elif self.config_type == "Difference Amplifier":
            # V_plus = V2 * (Rf / (Rin + Rf))
            self.V_plus = self.V_in2 * (self.R_f / (self.R_in + self.R_f))
            self.V_minus = self.V_plus # Virtual Short
        else:
            self.V_plus = self.V_in
            self.V_minus = self.V_in # Virtual Short

        # Currents
        if self.config_type == "Inverting":
            self.I_in = (self.V_in - self.V_minus) / self.R_in
            self.I_f = (self.V_minus - self.V_out) / self.R_f
            self.I_Rin = self.I_in
        elif self.config_type == "Voltage Follower":
            self.I_in = 0
            self.I_f = 0
            self.I_Rin = 0
        elif self.config_type == "Summing Amplifier":
            self.I_in = (self.V_in - self.V_minus) / self.R_in # I1
            # I2 would be (V_in2 - V_minus) / R_in2
            self.I_f = (self.V_minus - self.V_out) / self.R_f
        elif self.config_type == "Difference Amplifier":
            self.I_in = (self.V_in - self.V_minus) / self.R_in
            self.I_f = (self.V_minus - self.V_out) / self.R_f
        else:
            self.I_in = 0 
            self.I_f = (self.V_minus - self.V_out) / self.R_f
            self.I_Rin = self.V_minus / self.R_in

    def generate_waveforms(self, freq=1.0, duration=2.0, points=1000, wave_type="Sine"):
        t = np.linspace(0, duration, points)
        
        # Generate Input Waveform
        if wave_type == "Sine":
            vin_ac = self.V_in * np.sin(2 * np.pi * freq * t)
            vin_ac2 = self.V_in2 * np.sin(2 * np.pi * freq * t) # For adder/subtractor
        elif wave_type == "Square":
            vin_ac = self.V_in * np.sign(np.sin(2 * np.pi * freq * t))
            vin_ac2 = self.V_in2 * np.sign(np.sin(2 * np.pi * freq * t))
        elif wave_type == "Triangle":
            vin_ac = self.V_in * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1)
            vin_ac2 = self.V_in2 * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1)
        
        # Calculate Output Waveform
        if self.config_type == "Integrator":
            # Vout = -1/(RC) * integral(Vin)
            # Numerical integration
            dt = t[1] - t[0]
            vout_ideal = -1 / (self.R_in * self.C) * np.cumsum(vin_ac) * dt
            # Center it (remove integration constant drift for display)
            vout_ideal -= np.mean(vout_ideal)
            
        elif self.config_type == "Differentiator":
            # Vout = -RC * dVin/dt
            # Numerical differentiation
            dt = t[1] - t[0]
            vout_ideal = -self.R_f * self.C * np.gradient(vin_ac, dt)
            
        elif self.config_type == "Summing Amplifier":
            vout_ideal = -self.R_f * (vin_ac/self.R_in + vin_ac2/self.R_in2)
            
        elif self.config_type == "Difference Amplifier":
             # Vout = (Rf/Rin) * (V2 - V1)
             vout_ideal = (self.R_f / self.R_in) * (vin_ac2 - vin_ac)
            
        elif self.config_type == "Inverting":
            vout_ideal = vin_ac * (-self.R_f / self.R_in)
            
        elif self.config_type == "Non-Inverting":
            vout_ideal = vin_ac * (1 + self.R_f / self.R_in)
            
        elif self.config_type == "Voltage Follower":
            vout_ideal = vin_ac
            
        else:
            vout_ideal = np.zeros_like(t)

        vout_ac = np.clip(vout_ideal, -self.V_cc, self.V_cc)
        
        return t, vin_ac, vout_ac

    def get_state(self):
        return {
            "config": self.config_type,
            "V_in": self.V_in,
            "V_out": self.V_out,
            "V_cc": self.V_cc,
            "Gain_Actual": self.actual_gain,
            "I_in": self.I_in,
            "I_f": self.I_f,
            "V_minus": self.V_minus
        }
