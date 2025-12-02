import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from opamp_physics import OpAmpSolver
# Force reload for physics update

st.set_page_config(
    layout="wide", 
    page_title="Op-Amp Deep Dive Lab",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Aesthetics ---
st.markdown("""
<style>
    .metric-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Page Navigation ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("", ["🏠 Home", "🔬 Lab Explorer", "📚 Tutorial"], label_visibility="collapsed")

if "🏠 Home" in page:
    st.session_state.page = 'Home'
elif "🔬 Lab" in page:
    st.session_state.page = 'Lab'
elif "📚 Tutorial" in page:
    st.session_state.page = 'Tutorial'

# ====================== HOME PAGE ======================
if st.session_state.page == 'Home':
    # Logo and Title side-by-side
    header_col1, header_col2 = st.columns([1, 3])
    with header_col1:
        st.image("images/opamp_lab_logo_1764687325820.png", width=180)
    with header_col2:
        st.markdown("""
        <div style="padding-top: 20px;">
            <h1 style="color: #2c3e50; margin: 0;">⚡ Op-Amp Deep Dive Lab</h1>
            <p style="font-size: 1.1rem; color: #7f8c8d; margin-top: 0.5rem;">Master the invisible physics of operational amplifiers through interactive visualization</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: white; margin: 0;">🎯 Interactive Learning Platform</h2>
        <p style="font-size: 1.1rem; color: #f0f0f0; margin-top: 0.5rem;">Explore circuits, visualize waveforms, and understand feedback in real-time</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3 style="color: #2c3e50;">🔬 Interactive Circuits</h3>
            <p style="color: #34495e;">Build and explore Inverting and Non-Inverting amplifier configurations in real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3 style="color: #2c3e50;">📊 Live Waveforms</h3>
            <p style="color: #34495e;">Visualize phase shifts, gain, and saturation with dynamic signal analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3 style="color: #2c3e50;">⚙️ Physics Engine</h3>
            <p style="color: #34495e;">Understand feedback, Virtual Ground, and Beta factor through accurate simulations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("What You'll Learn")
    
    learn_col1, learn_col2 = st.columns(2)
    
    with learn_col1:
        st.subheader("Core Concepts")
        st.markdown("""
        - **Inverting vs Non-Inverting** configurations
        - **Virtual Ground** - Why the (-) input stays at 0V
        - **Phase Shift** - The 180° inversion in action
        - **Feedback Factor (β)** - Control theory meets circuits
        - **Saturation & Clipping** - Output voltage limits
        """)
    
    with learn_col2:
        st.subheader("Advanced Topics")
        st.markdown("""
        - **Open Loop vs Closed Loop** Gain
        - **Kirchhoff's Current Law** at the summing junction
        - **Gain-Bandwidth Product** trade-offs
        - **Real-world resistor** selection (E24 series)
        - **Dynamic current** visualization
        """)
    
    st.markdown("---")
    st.info("👈 **Get Started:** Select 'Lab Explorer' from the sidebar to begin your journey!")
    
    # Quick Stats
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    with stats_col1:
        st.metric("Configurations", "2", help="Inverting & Non-Inverting")
    with stats_col2:
        st.metric("Interactive Tabs", "3", help="Explorer, Feedback, Summing Junction")
    with stats_col3:
        st.metric("Visualizations", "5+", help="Schematics, Waveforms, Graphs")
    with stats_col4:
        st.metric("Learning Modules", "3", help="Structured educational content")

# ====================== TUTORIAL PAGE ======================
elif st.session_state.page == 'Tutorial':
    st.title("📚 Step-by-Step Tutorial")
    
    tutorial_tab1, tutorial_tab2, tutorial_tab3 = st.tabs(["Basics", "Inverting Mode", "Non-Inverting Mode"])
    
    with tutorial_tab1:
        st.header("Op-Amp Fundamentals")
        st.markdown("""
        ### What is an Operational Amplifier?
        
        An **Op-Amp** is a high-gain differential amplifier with:
        - **Two inputs**: Inverting (-) and Non-Inverting (+)
        - **One output**: Vout
        - **Power rails**: +Vcc and -Vee (or GND)
        
        ### The Golden Rules (Ideal Op-Amp)
        1. **No current** flows into the input terminals (infinite input impedance)
        2. The voltage difference between the two inputs is **zero** when negative feedback is applied
        
        ### Why Feedback Matters
        - **Open Loop Gain** (Aol) is typically 100,000+ (very high, unstable)
        - **Negative Feedback** reduces gain but makes it **stable and predictable**
        - Closed Loop Gain depends on **resistor ratios**, not the op-amp itself
        """)
        
        st.info("💡 **Key Insight:** Negative feedback forces the op-amp to adjust its output so that the (-) input voltage matches the (+) input voltage!")
    
    with tutorial_tab2:
        st.header("Inverting Amplifier")
        st.markdown("""
        ### Circuit Configuration
        - **Input (Vin)** → Rin → Inverting terminal (-)
        - **Non-Inverting terminal (+)** → Ground symbol
        - **Feedback resistor (Rf)** from Output back to Inverting terminal
        
        ### The Math
        """)
        st.latex(r"A_{CL} = -\frac{R_f}{R_{in}}")
        st.markdown("""
        - **Negative sign** means 180° phase shift (output inverted)
        - If Rin = 1kΩ and Rf = 10kΩ, Gain = -10
        
        ### Virtual Ground Concept
        - The (-) terminal is held at **~0V** (hence "Virtual Ground")
        - This happens because the op-amp output adjusts to keep (-) = (+) = 0V
        - Current flowing in through Rin **must equal** current flowing out through Rf
        """)
        
        st.success("✅ **Try it:** Go to Lab Explorer, select Inverting mode, and watch the 180° phase shift in action!")
    
    with tutorial_tab3:
        st.header("Non-Inverting Amplifier")
        st.markdown("""
        ### Circuit Configuration
        - **Input (Vin)** → Non-Inverting terminal (+)  
        - **Inverting terminal (-)** → Rin → Ground symbol
        - **Feedback resistor (Rf)** from Output back to Inverting terminal
        
        ### The Math
        """)
        st.latex(r"A_{CL} = 1 + \frac{R_f}{R_{in}}")
        st.markdown("""
        - **No negative sign** means output is in-phase with input
        - Minimum gain is 1 (voltage follower when Rf = 0)
        - If Rin = 1kΩ and Rf = 10kΩ, Gain = 11
        
        ### Voltage Divider Action
        - The output voltage is divided by Rf and Rin
        - This divided voltage appears at the (-) terminal
        - Op-amp adjusts output until (-) = (+) = Vin
        """)
        
        st.success("✅ **Try it:** Switch to Non-Inverting mode and observe NO phase shift in the waveforms!")

# ====================== LAB EXPLORER PAGE ======================
elif st.session_state.page == 'Lab':
    st.title("🔬 Op-Amp Lab Explorer")
    
    # --- Sidebar Controls ---
    st.sidebar.header("Circuit Configuration")
    
    # Preset Configurations
    st.sidebar.subheader("⚡ Quick Presets")
    preset = st.sidebar.selectbox("Load Configuration", [
        "Custom",
        "Unity Gain (x1)",
        "Audio Preamp (x10)",
        "High Gain (x100)",
        "Precision Inverter (-5)",
        "Active Integrator",
        "Active Differentiator"
    ])
    
    # Apply preset values
    if preset == "Unity Gain (x1)":
        r_in, r_f, config_type = 10000.0, 0.0, "Non-Inverting"
    elif preset == "Audio Preamp (x10)":
        r_in, r_f, config_type = 1000.0, 10000.0, "Inverting"
    elif preset == "High Gain (x100)":
        r_in, r_f, config_type = 1000.0, 100000.0, "Inverting"
    elif preset == "Precision Inverter (-5)":
        r_in, r_f, config_type = 2000.0, 10000.0, "Inverting"
    elif preset == "Active Integrator":
        r_in, r_f, config_type = 10000.0, 10000.0, "Integrator" # Rf unused but kept for state
    elif preset == "Active Differentiator":
        r_in, r_f, config_type = 10000.0, 10000.0, "Differentiator" # Rin unused
    else:
        r_in, r_f, config_type = 1000.0, 10000.0, "Inverting"
    
    st.sidebar.markdown("---")
    
    # Extended Configuration List
    config_options = ["Inverting", "Non-Inverting", "Voltage Follower", "Integrator", "Differentiator", "Summing Amplifier", "Difference Amplifier"]
    
    # Determine index safely
    try:
        default_index = config_options.index(config_type)
    except ValueError:
        default_index = 0
        
    config_type = st.sidebar.selectbox("Configuration", config_options, index=default_index)

    st.sidebar.subheader("Components")
    
    # Dynamic Inputs based on Config
    cap_val = 1.0 # Default uF
    v_in2_amp = 0.0
    r_in2 = 10000.0
    
    if config_type == "Voltage Follower":
        r_in = 1e12
        r_f = 0.0
        st.sidebar.info("⚡ Voltage Follower: Unity Gain Buffer\n\nRf = 0Ω (direct connection)\nRin = ∞ (no load)\nGain = 1.0")
        
    elif config_type == "Integrator":
        r_in = st.sidebar.number_input("R_in (Ohms)", min_value=100.0, max_value=100000.0, value=r_in, step=100.0)
        cap_val = st.sidebar.number_input("Feedback Capacitor (uF)", min_value=0.01, max_value=100.0, value=1.0, step=0.1)
        st.sidebar.info(f"Time Constant τ = R*C = {(r_in * cap_val * 1e-6):.4f} s")
        
    elif config_type == "Differentiator":
        cap_val = st.sidebar.number_input("Input Capacitor (uF)", min_value=0.01, max_value=100.0, value=1.0, step=0.1)
        r_f = st.sidebar.number_input("Feedback Resistor (Ohms)", min_value=100.0, max_value=1000000.0, value=r_f, step=1000.0)
        st.sidebar.info(f"Time Constant τ = R*C = {(r_f * cap_val * 1e-6):.4f} s")
        
    elif config_type == "Summing Amplifier":
        st.sidebar.markdown("**Input 1**")
        r_in = st.sidebar.number_input("R1 (Ohms)", min_value=100.0, max_value=100000.0, value=r_in, step=100.0)
        st.sidebar.markdown("**Input 2**")
        v_in2_amp = st.sidebar.slider("Input 2 Amplitude (V)", 0.0, 10.0, 1.0)
        r_in2 = st.sidebar.number_input("R2 (Ohms)", min_value=100.0, max_value=100000.0, value=10000.0, step=100.0)
        st.sidebar.markdown("**Feedback**")
        r_f = st.sidebar.number_input("Rf (Ohms)", min_value=0.0, max_value=1000000.0, value=r_f, step=1000.0)
        
    elif config_type == "Difference Amplifier":
        st.sidebar.markdown("**Inputs**")
        st.sidebar.info("Vout = (Rf/Rin) * (V2 - V1)")
        v_in2_amp = st.sidebar.slider("Input 2 (Non-Inv) Amplitude (V)", 0.0, 10.0, 1.0)
        
        st.sidebar.markdown("**Resistors (Matched Pairs)**")
        r_in = st.sidebar.number_input("R1 = R2 (Ohms)", min_value=100.0, max_value=100000.0, value=r_in, step=100.0)
        r_f = st.sidebar.number_input("Rf = Rg (Ohms)", min_value=0.0, max_value=1000000.0, value=r_f, step=1000.0)
        
    else: # Inverting / Non-Inverting
        r_in = st.sidebar.number_input("R_in (Ohms)", min_value=100.0, max_value=100000.0, value=r_in, step=100.0)
        r_f = st.sidebar.number_input("R_f (Ohms)", min_value=0.0, max_value=1000000.0, value=r_f, step=1000.0)

    st.sidebar.subheader("Power & Signal")
    v_cc = st.sidebar.number_input("V_cc (+/- Volts)", value=15.0)
    
    # Waveform Selection
    wave_type = st.sidebar.selectbox("Waveform Type", ["Sine", "Square", "Triangle"])
    
    v_in_amp = st.sidebar.slider("Input Amplitude (V)", 0.1, 10.0, 1.0)
    v_in_dc = st.sidebar.slider("Input DC Offset (V)", -5.0, 5.0, 0.0)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Live Simulation")
    live_vin = st.sidebar.slider("Instantaneous Vin (for Schematic)", -v_in_amp, v_in_amp, v_in_dc)

    # Global Solver for Schematic
    solver = OpAmpSolver(config_type, r_in, r_f, live_vin, v_cc, C=cap_val*1e-6, V_in2=v_in2_amp if config_type in ["Summing Amplifier", "Difference Amplifier"] else 0, R_in2=r_in2)
    solver.calculate_parameters()
    state = solver.get_state()

    # Export Configuration
    st.sidebar.markdown("---")
    if st.sidebar.button("📥 Export Configuration"):
        config_data = {
            "config_type": config_type,
            "R_in": r_in,
            "R_f": r_f,
            "V_cc": v_cc,
            "V_in_amp": v_in_amp,
            "V_in_dc": v_in_dc,
            "Wave_Type": wave_type
        }
        st.sidebar.download_button(
            "Download JSON",
            data=json.dumps(config_data, indent=2),
            file_name="opamp_config.json",
            mime="application/json"
        )

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs(["1. Configuration Explorer", "2. The Feedback Loop", "3. The Summing Junction"])

    with tab1:
        st.header("Phase Shift & Gain")
        
        # Circuit Diagram on top
        st.subheader("Circuit Diagram")
        
        if config_type == "Inverting":
            st.image("images/schematic_inverting_amplifier_1764694375132.png", width=600)
        elif config_type == "Non-Inverting":
            st.image("images/schematic_non_inverting_amplifier_1764694394195.png", width=600)
        elif config_type == "Voltage Follower":
            st.image("images/schematic_voltage_follower_1764694412094.png", width=600)
        elif config_type == "Integrator":
            st.image("images/schematic_integrator_1764694633362.png", width=600)
        elif config_type == "Differentiator":
            st.image("images/schematic_differentiator_1764694650462.png", width=600)
        elif config_type == "Summing Amplifier":
            st.image("images/schematic_summing_amplifier_1764694666473.png", width=600)
        elif config_type == "Difference Amplifier":
            st.image("images/uploaded_image_1764694863206.png", width=600)
        
        # Status info
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.info(f"**Current State:** Vin = {live_vin:.2f}V, Vout = {state['V_out']:.2f}V")
        with info_col2:
            if config_type == "Inverting":
                st.markdown(f"**Gain:** -Rf/Rin = -{r_f}/{r_in} = **{state['Gain_Actual']:.2f}**")
            elif config_type == "Voltage Follower":
                st.success(f"**Gain:** 1.0 (Unity Gain Buffer)")
            elif config_type == "Integrator":
                st.markdown(f"**Gain:** Frequency Dependent (-1/jωRC)")
            elif config_type == "Differentiator":
                st.markdown(f"**Gain:** Frequency Dependent (-jωRC)")
            elif config_type == "Summing Amplifier":
                st.markdown(f"**Output:** Vout = -Rf * (V1/R1 + V2/R2)")
            elif config_type == "Difference Amplifier":
                st.markdown(f"**Output:** Vout = (Rf/Rin) * (V2 - V1)")
            else:
                st.markdown(f"**Gain:** 1 + Rf/Rin = 1 + {r_f}/{r_in} = **{state['Gain_Actual']:.2f}**")
        
        st.markdown("---")
        
        # Waveform Analysis below
        st.subheader("Waveform Analysis")
        phase_lock = st.checkbox("Phase Lock Visualization (Freeze & Show Shift)") if config_type == "Inverting" else False
            
        # Generate Waveforms
        wave_solver = OpAmpSolver(config_type, r_in, r_f, v_in_amp, v_cc, C=cap_val*1e-6, V_in2=v_in2_amp, R_in2=r_in2)
        wave_solver.calculate_parameters()
        t, vin_wave, vout_wave = wave_solver.generate_waveforms(freq=1.0, duration=2.0, wave_type=wave_type)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, vin_wave, label="Vin", color="blue", alpha=0.7, linewidth=2)
        ax.plot(t, vout_wave, label="Vout", color="red", alpha=0.7, linewidth=2)
        ax.set_xlabel("Time (s)", fontsize=12)
        ax.set_ylabel("Voltage (V)", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        ax.set_title(f"{config_type} - {wave_type} Wave Response", fontsize=13, fontweight='bold')
        
        if phase_lock and config_type == "Inverting" and wave_type == "Sine":
            peak_t = 0.25
            peak_vin = v_in_amp
            trough_vout = -v_in_amp * abs(wave_solver.actual_gain)
            if abs(trough_vout) > v_cc: trough_vout = -v_cc if trough_vout < 0 else v_cc
            
            ax.plot([peak_t, peak_t], [peak_vin, trough_vout], 'k--', linewidth=1.5)
            ax.scatter([peak_t], [peak_vin], color='blue', zorder=5)
            ax.scatter([peak_t], [trough_vout], color='red', zorder=5)
            ax.text(peak_t + 0.05, (peak_vin+trough_vout)/2, "180° Shift", rotation=90, verticalalignment='center')
            
            st.caption("Vertical line connects Input Peak to Output Trough, demonstrating inversion.")
        
        if config_type == "Voltage Follower":
            st.success("✅ **Perfect Unity Gain:** Output follows input with no phase shift and no attenuation!")

        st.pyplot(fig)

    with tab2:
        st.header("The Feedback Loop (Beta)")
        
        st.markdown(r"""
        The closed-loop gain $A_{CL}$ depends on the Open Loop Gain $A_{OL}$ and the Feedback Factor $\beta$:
        $$ A_{CL} = \frac{A_{OL}}{1 + A_{OL}\beta} $$
        """)
        
        col_beta1, col_beta2 = st.columns([1, 2])
        
        with col_beta1:
            a_ol_log = st.slider("Open Loop Gain ($A_{OL}$) (Log Scale)", 1.0, 6.0, 5.0)
            a_ol = 10**a_ol_log
            st.metric("Current A_OL", f"{int(a_ol):,}")
            
            beta = r_in / (r_in + r_f) if r_f > 0 else 0
            st.metric("Feedback Factor (Beta)", f"{beta:.4f}")
            st.caption(f"Beta = Rin / (Rin + Rf)")
            
        with col_beta2:
            beta_solver = OpAmpSolver(config_type, r_in, r_f, v_in_amp, v_cc, A_ol=a_ol)
            beta_solver.calculate_parameters()
            
            ideal_gain = beta_solver.ideal_gain
            actual_gain = beta_solver.actual_gain
            
            st.subheader("Gain Stability")
            
            aol_range = np.logspace(0, 6, 100)
            gains = []
            for a in aol_range:
                s = OpAmpSolver(config_type, r_in, r_f, v_in_amp, v_cc, A_ol=a)
                s.calculate_parameters()
                gains.append(abs(s.actual_gain))
                
            fig_beta, ax_beta = plt.subplots(figsize=(6, 3))
            ax_beta.semilogx(aol_range, gains, label="Actual Gain")
            ax_beta.axhline(abs(ideal_gain), color='g', linestyle='--', label="Ideal Gain")
            ax_beta.scatter([a_ol], [abs(actual_gain)], color='red', s=100, zorder=5, label="Current Point")
            ax_beta.set_xlabel("Open Loop Gain (A_OL)")
            ax_beta.set_ylabel("Closed Loop Gain")
            ax_beta.legend()
            ax_beta.grid(True, which="both", alpha=0.3)
            
            st.pyplot(fig_beta)
            
            error = abs(ideal_gain - actual_gain) / abs(ideal_gain) * 100 if ideal_gain != 0 else 0
            st.markdown(f"**Gain Error:** {error:.4f}%")
            if error > 10:
                st.warning("Low Open Loop Gain causes significant error!")

    with tab3:
        st.header("The Summing Junction (Virtual Ground)")
        
        st.markdown("Zooming in on the Inverting Input (-). According to KCL, currents must sum to zero.")
        
        kcl_col1, kcl_col2, kcl_col3 = st.columns(3)
        
        with kcl_col1:
            st.markdown("### I_in (Entering)")
            st.markdown(f"<h2 style='color:blue'>{state['I_in']*1000:.3f} mA</h2>", unsafe_allow_html=True)
            st.caption("From Input Source")
            
        with kcl_col2:
            st.markdown("### Summing Node")
            st.markdown(f"**Voltage:** {state['V_minus']*1000:.3f} mV")
            
        with kcl_col3:
            st.markdown("### I_f (Leaving)")
            st.markdown(f"<h2 style='color:red'>{state['I_f']*1000:.3f} mA</h2>", unsafe_allow_html=True)
            st.caption("To Output")

        kcl_error = state['I_in'] - state['I_f']
        st.metric("KCL Error (I_in - I_f)", f"{kcl_error*1e6:.3f} uA")
        
        st.markdown("---")
        st.subheader("Interactive Challenge: Match the Resistors")
        st.markdown("Target Gain: **-5.0**")
        
        e24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
        multipliers = [100, 1000, 10000, 100000]
        resistors = []
        for m in multipliers:
            resistors.extend([v * m for v in e24])
        resistors = sorted(list(set(resistors)))
        
        c1, c2 = st.columns(2)
        with c1:
            user_rin = st.selectbox("Pick Rin", resistors, index=resistors.index(1000.0) if 1000.0 in resistors else 0)
        with c2:
            user_rf = st.selectbox("Pick Rf", resistors, index=resistors.index(4700.0) if 4700.0 in resistors else 0)
            
        user_gain = -user_rf / user_rin
        st.markdown(f"**Your Gain:** {user_gain:.2f}")
        
        if abs(user_gain + 5.0) < 0.1:
            st.success("Correct! You matched the gain.")
        else:
            st.error("Try again. Remember Gain = -Rf/Rin")
