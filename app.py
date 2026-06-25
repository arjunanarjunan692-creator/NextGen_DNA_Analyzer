import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os
import io

# ReportLab Imports for PDF Generation Pipeline
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Append root path to python path to resolve database and module imports safely
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from database.db_manager import init_db, get_connection
from auth.login import show_login_page
from auth.register import show_register_page
from modules.dna_analyzer_logic import (
    validate_dna_sequence, 
    calculate_sequence_metrics, 
    generate_molecular_utilities,
    clean_sequence,
    track_snps,
    generate_3d_helix_coordinates
)

def generate_pdf_report(user_name, sequence_name, metrics, utilities, snp_logs):
    """Generates a clean biological PDF report using ReportLab memory buffer."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E3A8A'), spaceAfter=15)
    section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#10B981'), spaceBefore=10, spaceAfter=10)
    body_style = ParagraphStyle('BodyStyle', parent=styles['BodyText'], fontSize=11, leading=14)
    
    story.append(Paragraph("🧬 NextGen DNA Analyzer - Sequence Analysis Report", title_style))
    story.append(Paragraph(f"<b>Prepared For:</b> {user_name}", body_style))
    story.append(Paragraph(f"<b>Sequence Identifier:</b> {sequence_name}", body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("📊 Core Sequence Metrics Summary", section_style))
    metrics_data = [
        ["Biological Metric Parameter", "Calculated Structural Value"],
        ["Sequence Base Length", f"{metrics['length']} bp"],
        ["GC Content Ratio", f"{metrics['gc_percentage']}%"],
        ["AT Content Ratio", f"{metrics['at_percentage']}%"]
    ]
    t1 = Table(metrics_data, colWidths=[200, 250])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F3F4F6')),
    ]))
    story.append(t1)
    story.append(Spacer(1, 15))
    
    if snp_logs:
        story.append(Paragraph("🎯 Identified Genomic Variants (SNP Audit Trail)", section_style))
        snp_table_data = [["Position", "Ref", "Variant", "dbSNP rsID", "Reported Clinical Impact"]]
        for row in snp_logs:
            snp_table_data.append([row["Position"], row["Reference Base"], row["Observed Variant"], row["dbSNP rsID"], row["Reported Clinical Impact / Association"]])
        t_snp = Table(snp_table_data, colWidths=[65, 35, 50, 80, 220])
        t_snp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (1,0), colors.HexColor('#EF4444')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        story.append(t_snp)
        story.append(Spacer(1, 15))
    
    story.append(Paragraph("🧬 Downstream Molecular Biology Utilities Output", section_style))
    utilities_data = [
        [Paragraph("<b>Reverse Complement:</b>", body_style), Paragraph(utilities['reverse_complement'], body_style)],
        [Paragraph("<b>mRNA Transcription:</b>", body_style), Paragraph(utilities['mrna'], body_style)],
        [Paragraph("<b>Protein Translation:</b>", body_style), Paragraph(utilities['protein'], body_style)]
    ]
    t2 = Table(utilities_data, colWidths=[150, 300])
    t2.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t2)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def show_founder_footer():
    """Renders a unified modern branding and contact footer for Arjunan G."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 0.5px solid #3b82f6;'>", unsafe_allow_html=True)
    prof_col1, prof_col2 = st.columns([1, 3])
    with prof_col1:
        st.markdown("<h3 style='color:#10b981; margin-top:0;'>🛠️ Workspace Crew</h3>", unsafe_allow_html=True)
    with prof_col2:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1);'>
            <h4 style='color:#ffffff; margin:0 0 5px 0;'><b>Arjunan G</b></h4>
            <p style='color:#3b82f6; margin:0 0 5px 0;'>🚀 <i>Founder & Lead System Developer</i></p>
            <p style='color:#9ca3af; margin:0;'>📫 <b>Contact:</b> <a href='mailto:arjunanarjunan692@gmail.com' style='color:#10b981;'>arjunanarjunan692@gmail.com</a></p>
            <p style='color:#9ca3af; margin:5px 0 0 0;'>💬 <i>NextGen DNA Analyzer Platform Engineering Lead</i></p>
        </div>
        """, unsafe_allow_html=True)

# Global Streamlit Page Configuration
st.set_page_config(page_title="NextGen DNA Analyzer", page_icon="🧬", layout="wide")

# --- INJECTING MODERN CUSTOM UI CSS THEME MATRIX ---
st.markdown("""
    <style>
        /* Base Background Canvas Gradient */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }
        /* Custom Modern Typography */
        h1, h2, h3, h4, label, .stMarkdown {
            color: #ffffff !important;
            font-family: 'Inter', system-ui, sans-serif;
        }
        /* Glassmorphic KPI Cards Styling */
        div[data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #10b981 !important;
        }
        div[data-testid="stMetricLabel"] p {
            color: #9ca3af !important;
            font-size: 0.95rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 15px 20px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        /* Neon Glow Submit Buttons Custom Architecture */
        div.stButton > button {
            background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 25px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.4) !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px 0 rgba(59, 130, 246, 0.6) !important;
        }
        /* Sidebar Glassmorphic Overlay Override */
        section[data-testid="stSidebar"] {
            background-color: #0b0f19 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        /* Info/Warning/Success Modern Alerts Box Styling Override */
        .stAlert {
            background-color: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

init_db()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- ROUTING SYSTEM ---
if not st.session_state['logged_in']:
    st.sidebar.title("🧬 NextGen Gateway")
    auth_choice = st.sidebar.radio("Navigation Menu", ["Sign-In Terminal", "Create Workspace Account"])
    
    if auth_choice == "Sign-In Terminal":
        show_login_page()
    else:
        show_register_page()
        
    show_founder_footer()
else:
    st.sidebar.markdown("<h2 style='color:#3b82f6; font-size:1.4rem;'>🧬 NextGen Core</h2>", unsafe_allow_html=True)
    st.sidebar.write(f"🌐 Core Active Node: **{st.session_state['user_name']}**")
    menu = st.sidebar.radio("Control Panel Modules", ["Dashboard Operational Node", "DNA Deep Analysis Engine", "Terminate Session"])
    
    if menu == "Dashboard Operational Node":
        st.markdown("<h1 style='color: #ffffff; margin-bottom: 5px;'>📊 Cloud Workspace Dashboard</h1>", unsafe_allow_html=True)
        st.write("Real-time telemetry and summary matrices of your cloud genomic computing environment.")
        st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total_runs, AVG(sequence_length) as avg_len, AVG(gc_content) as avg_gc FROM analysis_history WHERE user_id = ?", (st.session_state['user_id'],))
            summary_stats = cursor.fetchone()
            
            cursor.execute("SELECT sequence_name, sequence_length, gc_content, timestamp FROM analysis_history WHERE user_id = ? ORDER BY timestamp DESC", (st.session_state['user_id'],))
            history_rows = cursor.fetchall()
            conn.close()
            
            total_runs = summary_stats['total_runs'] if summary_stats['total_runs'] else 0
            avg_len = round(summary_stats['avg_len'], 1) if summary_stats['avg_len'] else 0
            avg_gc = round(summary_stats['avg_gc'], 1) if summary_stats['avg_gc'] else 0
            
            card_col1, card_col2, card_col3 = st.columns(3)
            card_col1.metric("Total Computations Run", f"{total_runs} Batches")
            card_col2.metric("Mean Core Sequence Length", f"{avg_len} bp")
            card_col3.metric("Average GC Structural Weight", f"{avg_gc}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📋 Core Audit Logs & Computation History")
            
            if total_runs > 0:
                history_df = pd.DataFrame([dict(row) for row in history_rows])
                history_df.columns = ["Sequence Identifier", "Length (bp)", "GC Weight (%)", "Timestamp Logged"]
                st.dataframe(history_df, use_container_width=True)
            else:
                st.info("No compute pipelines found. Start a run inside the 'DNA Deep Analysis Engine'!")
                
        except Exception as e:
            st.error(f"Workspace Telemetry Stack Failed: {e}")
            
        show_founder_footer()
        
    elif menu == "DNA Deep Analysis Engine":
        st.markdown("<h1 style='color: #ffffff; margin-bottom: 5px;'>🧬 DNA Deep Analysis Engine</h1>", unsafe_allow_html=True)
        st.write("Process algorithmic matrices, track structural mutations, and map 3D macromolecule coordinates.")
        st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        input_type = st.radio("Choose Input Matrix Target Array:", ["Manual Character Entry Sequence", "Standard FASTA File Asset Upload"])
        raw_sequence = ""
        
        if input_type == "Manual Character Entry Sequence":
            raw_sequence = st.text_area("Paste Raw DNA Array Base String (Case-Insensitive A, T, C, G only):", height=150)
        else:
            uploaded_file = st.file_uploader("Upload Biological Asset FASTA File (.fasta, .fa):", type=["fasta", "fa"])
            if uploaded_file is not None:
                file_contents = uploaded_file.read().decode("utf-8")
                lines = file_contents.splitlines()
                raw_sequence = "".join([line.strip() for line in lines if not line.startswith(">")])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Execute Pipeline Vector"):
            if not raw_sequence:
                st.warning("Computational pipeline rejected: Vector payload empty.")
            elif not validate_dna_sequence(raw_sequence):
                st.error("Validation Error! Character string contains non-nucleotide sequences.")
            else:
                cleaned_seq = clean_sequence(raw_sequence)
                
                metrics = calculate_sequence_metrics(cleaned_seq)
                utilities = generate_molecular_utilities(cleaned_seq)
                snp_results = track_snps(cleaned_seq)
                
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO analysis_history (user_id, sequence_name, sequence_length, gc_content) VALUES (?, ?, ?, ?)",
                        (st.session_state['user_id'], f"DNA_Strand_{metrics['length']}bp", metrics['length'], metrics['gc_percentage'])
                    )
                    conn.commit()
                    conn.close()
                    st.success("Telemetry payload synced with relational database node!")
                except Exception as e:
                    st.error(f"Database logging failure: {e}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Processed Base Array Length", f"{metrics['length']} bp")
                col2.metric("GC Ratio Mass Distribution", f"{metrics['gc_percentage']}%")
                col3.metric("AT Ratio Mass Distribution", f"{metrics['at_percentage']}%")
                
                st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
                
                st.subheader("🔮 Predicted Dynamic 3D Molecular Double Helix Configuration View")
                st.info("💡 Interactive Model Loaded: Use mouse click-and-drag matrix to rotate helix space parameters offline.")
                
                helix_df = generate_3d_helix_coordinates(cleaned_seq)
                if not helix_df.empty:
                    fig_3d = px.scatter_3d(
                        helix_df, x='X', y='Y', z='Z', 
                        color='Base', symbol='Strand',
                        color_discrete_sequence=px.colors.qualitative.G10
                    )
                    fig_3d.update_traces(marker=dict(size=7, opacity=0.9, line=dict(width=1, color='#ffffff')))
                    fig_3d.update_layout(
                        scene=dict(
                            bgcolor='#0b0f19',
                            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
                            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
                            zaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)')
                        ),
                        margin=dict(l=0, r=0, b=0, t=0),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_3d, use_container_width=True)
                
                st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
                
                st.subheader("🎯 Genomic Polymorphism Variant Audit Log (Reference Assembly v3)")
                if snp_results:
                    st.warning("Alert: Variant audit mismatch coordinates logged against reference strain!")
                    snp_df = pd.DataFrame(snp_results)
                    st.dataframe(snp_df, use_container_width=True)
                else:
                    st.success("Relational Identity 100% Core Match: No mutations logged in this sequence array.")
                
                st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
                
                st.subheader("📊 Dynamic Nucleotide Density Distribution Diagrams")
                freq_data = pd.DataFrame({'Nucleotide Structural Block': list(metrics['frequencies'].keys()), 'Total Population Base Count': list(metrics['frequencies'].values())})
                
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    fig_bar = px.bar(freq_data, x='Nucleotide Structural Block', y='Total Population Base Count', color='Nucleotide Structural Block', color_discrete_sequence=px.colors.qualitative.Pastel)
                    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', scene=dict(bgcolor='#0b0f19'))
                    st.plotly_chart(fig_bar, use_container_width=True)
                with chart_col2:
                    fig_pie = px.pie(freq_data, names='Nucleotide Structural Block', values='Total Population Base Count', color_discrete_sequence=px.colors.qualitative.Safe)
                    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
                
                st.subheader("🧬 Downstream Expression Mapping & Translation Outputs")
                st.text_area("Calculated DNA Reverse Complement Strand:", utilities['reverse_complement'], height=70)
                st.text_area("Transcribed Messenger RNA (mRNA) Chain Variant:", utilities['mrna'], height=70)
                st.text_area("Translated Amino Acid Protein Structural String Vector:", utilities['protein'], height=70)
                
                st.markdown("<br>", unsafe_allow_html=True)
                pdf_data = generate_pdf_report(st.session_state['user_name'], f"DNA_Strand_{metrics['length']}bp", metrics, utilities, snp_results)
                
                st.download_button(
                    label="📥 Export Certified Clinical Genomic Analysis Dossier (PDF)",
                    data=pdf_data,
                    file_name=f"Genomic_Dossier_Report_{metrics['length']}bp.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
    elif menu == "Terminate Session":
        st.session_state['logged_in'] = False
        st.session_state.clear()
        st.success("Secure node access handshake terminated successfully.")
        st.rerun()