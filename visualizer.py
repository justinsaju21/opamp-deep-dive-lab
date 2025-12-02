import numpy as np

def render_dynamic_schematic(state):
    """
    Generates a high-quality, publication-ready IEEE schematic.
    Style: Black & White, Thick Lines, Standard Symbols.
    """
    config = state["config"]
    vin = state["V_in"]
    vout = state["V_out"]
    v_cc = state["V_cc"]
    
    # Canvas
    width, height = 800, 450
    svg = [f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" style="max-height: 450px;">']
    
    # Background
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF" stroke="none"/>')
    
    # Styles
    STYLE_WIRE = 'stroke="#000000" stroke-width="3" stroke-linecap="round" fill="none"'
    STYLE_COMP = 'stroke="#000000" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    STYLE_TEXT = 'font-family="Arial, sans-serif" font-size="16" fill="#000000" font-weight="bold"'
    STYLE_LABEL = 'font-family="Arial, sans-serif" font-size="14" fill="#444444"'
    
    # --- Primitives ---
    def line(x1, y1, x2, y2):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {STYLE_WIRE}/>'
        
    def dot(x, y):
        return f'<circle cx="{x}" cy="{y}" r="5" fill="#000000"/>'
        
    def terminal(x, y, label=""):
        s = f'<circle cx="{x}" cy="{y}" r="6" stroke="#000000" stroke-width="3" fill="#FFFFFF"/>'
        if label:
            s += f'<text x="{x-15}" y="{y+5}" {STYLE_TEXT} text-anchor="end">{label}</text>'
        return s

    def resistor(x1, y1, x2, y2, label=""):
        # IEEE Zig-Zag Resistor
        dx, dy = x2 - x1, y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        angle = np.degrees(np.arctan2(dy, dx))
        
        # Resistor body is 60 units long
        body_len = 60
        if length < body_len: body_len = length # Should not happen in good layout
        
        lead_len = (length - body_len) / 2
        
        # Transform group
        mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
        g = f'<g transform="translate({mid_x},{mid_y}) rotate({angle})">'
        
        # Leads
        g += f'<line x1="{-length/2}" y1="0" x2="{-body_len/2}" y2="0" {STYLE_WIRE}/>'
        g += f'<line x1="{body_len/2}" y1="0" x2="{length/2}" y2="0" {STYLE_WIRE}/>'
        
        # Zig-Zag (6 segments)
        # -30 to +30
        pts = [
            (-30, 0), (-25, -10), (-15, 10), (-5, -10), 
            (5, 10), (15, -10), (25, 10), (30, 0)
        ]
        d = "M " + " L ".join([f"{px},{py}" for px, py in pts])
        g += f'<path d="{d}" {STYLE_COMP}/>'
        g += '</g>'
        
        # Label
        if label:
            # Offset based on angle (simplified for horiz/vert)
            if abs(dx) > abs(dy): # Horizontal
                lx, ly = mid_x, mid_y - 25
            else: # Vertical
                lx, ly = mid_x + 35, mid_y
            g += f'<text x="{lx}" y="{ly}" {STYLE_TEXT} text-anchor="middle">{label}</text>'
            
        return g

    def opamp(x, y):
        # Standard Triangle
        w, h = 100, 100
        g = f'<g transform="translate({x},{y})">'
        g += f'<path d="M {-w/2} {-h/2} L {w/2} 0 L {-w/2} {h/2} Z" {STYLE_COMP}/>'
        # Inputs
        g += f'<text x="{-w/2 + 10}" y="{-h/4 + 8}" {STYLE_TEXT}>-</text>'
        g += f'<text x="{-w/2 + 10}" y="{h/4 + 8}" {STYLE_TEXT}>+</text>'
        # Leads
        lead = 20
        g += f'<line x1="{-w/2}" y1="{-h/4}" x2="{-w/2-lead}" y2="{-h/4}" {STYLE_WIRE}/>' # Inverting
        g += f'<line x1="{-w/2}" y1="{h/4}" x2="{-w/2-lead}" y2="{h/4}" {STYLE_WIRE}/>' # Non-Inverting
        g += f'<line x1="{w/2}" y1="0" x2="{w/2+lead}" y2="0" {STYLE_WIRE}/>' # Output
        g += '</g>'
        return g

    def ground(x, y):
        g = f'<g transform="translate({x},{y})">'
        g += f'<line x1="0" y1="0" x2="0" y2="15" {STYLE_WIRE}/>'
        g += f'<line x1="-15" y1="15" x2="15" y2="15" {STYLE_WIRE}/>'
        g += f'<line x1="-10" y1="22" x2="10" y2="22" {STYLE_WIRE}/>'
        g += f'<line x1="-5" y1="29" x2="5" y2="29" {STYLE_WIRE}/>'
        g += '</g>'
        return g

    # --- Layout Logic ---
    cx, cy = 400, 225 # Center of OpAmp
    
    # OpAmp
    svg.append(opamp(cx, cy))
    
    # Power Rails
    svg.append(line(cx, cy-50, cx, cy-90))
    svg.append(f'<text x="{cx}" y="{cy-95}" {STYLE_LABEL} text-anchor="middle">+Vcc</text>')
    svg.append(line(cx, cy+50, cx, cy+90))
    svg.append(f'<text x="{cx}" y="{cy+105}" {STYLE_LABEL} text-anchor="middle">-Vee</text>')
    
    # Terminals
    t_minus = (cx - 70, cy - 25)
    t_plus = (cx - 70, cy + 25)
    t_out = (cx + 70, cy)
    
    # Output Wire
    p_out_end = (t_out[0] + 100, t_out[1])
    svg.append(line(t_out[0], t_out[1], p_out_end[0], p_out_end[1]))
    svg.append(terminal(p_out_end[0], p_out_end[1], f"Vout={vout:.2f}V"))
    
    # Feedback Network
    # Up from (-), Right, Down to Output
    fb_y = t_minus[1] - 100
    fb_node_out = t_out[0] + 50 # Connection point on output wire
    
    svg.append(line(t_minus[0], t_minus[1], t_minus[0], fb_y)) # Up
    
    if config == "Voltage Follower":
        # Wire only
        svg.append(line(t_minus[0], fb_y, fb_node_out, fb_y))
    else:
        # Resistor
        svg.append(resistor(t_minus[0], fb_y, fb_node_out, fb_y, "Rf"))
        
    svg.append(line(fb_node_out, fb_y, fb_node_out, t_out[1])) # Down
    svg.append(dot(fb_node_out, t_out[1])) # Junction
    
    # Input Network
    if config == "Inverting":
        # Vin -> Rin -> (-)
        p_in = (t_minus[0] - 150, t_minus[1])
        svg.append(terminal(p_in[0], p_in[1], f"Vin={vin:.2f}V"))
        svg.append(resistor(p_in[0], t_minus[1], t_minus[0], t_minus[1], "Rin"))
        
        # (+) -> Ground
        svg.append(line(t_plus[0], t_plus[1], t_plus[0], t_plus[1] + 40))
        svg.append(ground(t_plus[0], t_plus[1] + 40))
        
        # Virtual Ground Label (Simple text)
        svg.append(f'<text x="{t_minus[0]}" y="{t_minus[1]+25}" {STYLE_LABEL} text-anchor="end" font-style="italic">Virtual GND →</text>')
        
    elif config == "Non-Inverting":
        # Vin -> (+)
        p_in = (t_plus[0] - 100, t_plus[1])
        svg.append(terminal(p_in[0], p_in[1], f"Vin={vin:.2f}V"))
        svg.append(line(p_in[0], t_plus[1], t_plus[0], t_plus[1]))
        
        # (-) -> Rin -> Ground
        # Down from (-) then Left? Or Left then Down?
        # Standard: (-) -> Left -> Down -> Resistor -> Ground
        p_rin_top = (t_minus[0] - 50, t_minus[1])
        p_rin_bot = (p_rin_top[0], t_plus[1] + 80)
        
        svg.append(line(t_minus[0], t_minus[1], p_rin_top[0], t_minus[1]))
        svg.append(line(p_rin_top[0], t_minus[1], p_rin_top[0], p_rin_top[1] + 20)) # Stub down
        svg.append(resistor(p_rin_top[0], p_rin_top[1] + 20, p_rin_bot[0], p_rin_bot[1], "Rin"))
        svg.append(ground(p_rin_bot[0], p_rin_bot[1]))
        
    elif config == "Voltage Follower":
        # Vin -> (+)
        p_in = (t_plus[0] - 100, t_plus[1])
        svg.append(terminal(p_in[0], p_in[1], f"Vin={vin:.2f}V"))
        svg.append(line(p_in[0], t_plus[1], t_plus[0], t_plus[1]))
        
        # (-) is connected to feedback loop (already drawn)
        # No other connections
        pass

    svg.append('</svg>')
    return "".join(svg)
