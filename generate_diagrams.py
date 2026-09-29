"""
Diagram Generator for EduGenie Phase 3 Design Documentation
Generates 6 clean, professional, high-resolution architectural and workflow diagrams.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arrow

DIAGRAMS_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "Phase_Wise_Submission", "03_Project_Design", "diagrams"
))
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def draw_box(ax, x, y, width, height, text, subtext="", bg_color="#eef2ff", border_color="#4f46e5", text_color="#1e1b4b", fontsize=10):
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        facecolor=bg_color, edgecolor=border_color, linewidth=1.5,
        zorder=3
    )
    ax.add_patch(box)
    if subtext:
        ax.text(x + width/2, y + height*0.62, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=text_color, zorder=4)
        ax.text(x + width/2, y + height*0.32, subtext, ha='center', va='center', fontsize=fontsize-2.5, color="#475569", zorder=4)
    else:
        ax.text(x + width/2, y + height/2, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=text_color, zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#475569", label_pos=0.5):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, lw=1.8, shrinkA=5, shrinkB=5),
        zorder=2
    )
    if label:
        mx = x1 + (x2 - x1) * label_pos
        my = y1 + (y2 - y1) * label_pos + 0.02
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=8, color="#334155", fontweight='semibold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.85), zorder=5)

# Diagram 1: System Architecture
def create_system_architecture():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, "EduGenie: Comprehensive System Architecture", ha='center', fontsize=14, fontweight='bold', color="#1e1b4b")
    ax.text(0.5, 0.91, "Three-Tier Client-Server Architecture with Hybrid AI Inference & Deterministic Fallbacks", ha='center', fontsize=9.5, color="#64748b")

    # Layer 1: Client Layer (Frontend)
    rect_client = FancyBboxPatch((0.04, 0.68), 0.92, 0.18, boxstyle="round,pad=0.02", facecolor="#f8fafc", edgecolor="#cbd5e1", linestyle="--", linewidth=1.2)
    ax.add_patch(rect_client)
    ax.text(0.06, 0.83, "PRESENTATION TIER (Web Client)", fontsize=9, fontweight='bold', color="#475569")
    draw_box(ax, 0.07, 0.70, 0.25, 0.11, "Responsive Web Dashboard", "HTML5 • Vanilla JS • Modern CSS", "#e0e7ff", "#4f46e5")
    draw_box(ax, 0.37, 0.70, 0.26, 0.11, "Interactive UI Components", "5 Cards • Live Grader • Score Banner", "#e0e7ff", "#4f46e5")
    draw_box(ax, 0.68, 0.70, 0.25, 0.11, "Status & Health Badges", "Demo Mode • System Liveness", "#e0e7ff", "#4f46e5")

    # Layer 2: Application Layer (FastAPI Backend)
    rect_app = FancyBboxPatch((0.04, 0.34), 0.92, 0.28, boxstyle="round,pad=0.02", facecolor="#f8fafc", edgecolor="#cbd5e1", linestyle="--", linewidth=1.2)
    ax.add_patch(rect_app)
    ax.text(0.06, 0.59, "APPLICATION TIER (FastAPI ASGI Server :8000)", fontsize=9, fontweight='bold', color="#475569")
    draw_box(ax, 0.07, 0.46, 0.19, 0.10, "FastAPI App Router", "Pydantic Input Validation", "#dbeafe", "#2563eb")
    draw_box(ax, 0.29, 0.46, 0.18, 0.10, "QnA Module", "Concise Fact Retrieval", "#fef3c7", "#d97706")
    draw_box(ax, 0.50, 0.46, 0.18, 0.10, "Concept Explainer", "Student Analogies", "#f3e8ff", "#9333ea")
    draw_box(ax, 0.71, 0.46, 0.22, 0.10, "Quiz & Summary Engine", "JSON Validation & Retries", "#d1fae5", "#059669")
    draw_box(ax, 0.29, 0.35, 0.39, 0.09, "Learning Path Generator", "Beginner -> Advanced Roadmaps", "#e0e7ff", "#4f46e5")
    draw_box(ax, 0.71, 0.35, 0.22, 0.09, "Health Monitor (/health)", "Mode Resolution & Models", "#f1f5f9", "#475569")

    # Layer 3: AI Inference & Data Tier
    rect_ai = FancyBboxPatch((0.04, 0.04), 0.92, 0.24, boxstyle="round,pad=0.02", facecolor="#f8fafc", edgecolor="#cbd5e1", linestyle="--", linewidth=1.2)
    ax.add_patch(rect_ai)
    ax.text(0.06, 0.25, "AI INFERENCE & FALLBACK TIER", fontsize=9, fontweight='bold', color="#475569")
    draw_box(ax, 0.07, 0.07, 0.26, 0.14, "Google Gemini API", "Cloud Foundation Model\ngemini-1.5-flash / pro", "#ecfdf5", "#10b981")
    draw_box(ax, 0.37, 0.07, 0.26, 0.14, "Local HuggingFace Model", "LaMini-Flan-T5-783M\nTransformers + PyTorch", "#fdf2f8", "#db2777")
    draw_box(ax, 0.68, 0.07, 0.25, 0.14, "Deterministic Generator", "Zero-Downtime Fallback\nOffline Educational Corpus", "#fffbeb", "#f59e0b")

    # Connecting Arrows
    draw_arrow(ax, 0.20, 0.70, 0.17, 0.56, "HTTP / REST API")
    draw_arrow(ax, 0.50, 0.70, 0.50, 0.56, "JSON Payloads")
    draw_arrow(ax, 0.80, 0.70, 0.80, 0.56, "Async Responses")

    draw_arrow(ax, 0.20, 0.46, 0.20, 0.21, "API Requests")
    draw_arrow(ax, 0.50, 0.46, 0.50, 0.21, "Local Pipeline")
    draw_arrow(ax, 0.80, 0.46, 0.80, 0.21, "Deterministic Fallback")

    plt.tight_layout()
    out_path = os.path.join(DIAGRAMS_DIR, "01_system_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

# Diagram 2: Workflow Flowchart
def create_workflow_flowchart():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.96, "EduGenie: End-to-End System Workflow Flowchart", ha='center', fontsize=13, fontweight='bold', color="#1e1b4b")

    draw_box(ax, 0.35, 0.86, 0.30, 0.07, "Start / User Interaction", "User enters query/topic on Web Dashboard", "#e0e7ff", "#4f46e5")
    draw_box(ax, 0.35, 0.73, 0.30, 0.07, "Input Validation", "Pydantic Schema & Length Sanitization", "#dbeafe", "#2563eb")
    draw_box(ax, 0.35, 0.60, 0.30, 0.07, "Backend & Mode Decision", "Check GEMINI_API_KEY & EXPLAIN_BACKEND", "#fef3c7", "#d97706")

    draw_box(ax, 0.08, 0.44, 0.26, 0.09, "Execute Gemini API", "Send Structured Prompt to Google Cloud", "#ecfdf5", "#10b981")
    draw_box(ax, 0.37, 0.44, 0.26, 0.09, "Local Model Pipeline", "Execute LaMini-Flan-T5 Locally", "#fdf2f8", "#db2777")
    draw_box(ax, 0.66, 0.44, 0.26, 0.09, "Deterministic Generator", "Fetch Verified Offline Educational Data", "#fffbeb", "#f59e0b")

    draw_box(ax, 0.35, 0.28, 0.30, 0.08, "Response Post-Processing", "Strip Markdown Code Fences & Validate JSON", "#f3e8ff", "#9333ea")
    draw_box(ax, 0.35, 0.15, 0.30, 0.07, "Render Result in UI", "Formatted Markdown / Interactive Grader", "#d1fae5", "#059669")
    draw_box(ax, 0.35, 0.03, 0.30, 0.06, "End / Ready for Next Query", "Update Health & Score Banners", "#e0e7ff", "#4f46e5")

    # Arrows
    draw_arrow(ax, 0.50, 0.86, 0.50, 0.80)
    draw_arrow(ax, 0.50, 0.73, 0.50, 0.67)
    draw_arrow(ax, 0.40, 0.60, 0.21, 0.53, "Live Cloud")
    draw_arrow(ax, 0.50, 0.60, 0.50, 0.53, "Local Backend")
    draw_arrow(ax, 0.60, 0.60, 0.79, 0.53, "Demo / Key Missing")

    draw_arrow(ax, 0.21, 0.44, 0.40, 0.36)
    draw_arrow(ax, 0.50, 0.44, 0.50, 0.36)
    draw_arrow(ax, 0.79, 0.44, 0.60, 0.36)

    draw_arrow(ax, 0.50, 0.28, 0.50, 0.22)
    draw_arrow(ax, 0.50, 0.15, 0.50, 0.09)

    plt.tight_layout()
    out_path = os.path.join(DIAGRAMS_DIR, "02_workflow_flowchart.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

# Diagram 3: Data Flow Diagram (Level 0 & Level 1)
def create_data_flow_diagram():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5), dpi=300)
    
    for ax in [ax1, ax2]:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # DFD Level 0
    ax1.text(0.5, 0.93, "Data Flow Diagram — Level 0 (Context Diagram)", ha='center', fontsize=12, fontweight='bold', color="#1e1b4b")
    draw_box(ax1, 0.06, 0.40, 0.22, 0.30, "Student / Learner", "External Entity", "#f1f5f9", "#475569")
    draw_box(ax1, 0.38, 0.35, 0.24, 0.40, "0.0\nEduGenie System", "Central Learning Process", "#e0e7ff", "#4f46e5")
    draw_box(ax1, 0.72, 0.40, 0.22, 0.30, "Google Gemini AI", "External Cloud Service", "#ecfdf5", "#10b981")

    draw_arrow(ax1, 0.28, 0.60, 0.38, 0.60, "Learning Request")
    draw_arrow(ax1, 0.38, 0.45, 0.28, 0.45, "Formatted Answer / Quiz")
    draw_arrow(ax1, 0.62, 0.60, 0.72, 0.60, "API Prompt")
    draw_arrow(ax1, 0.72, 0.45, 0.62, 0.45, "Raw AI Response")

    # DFD Level 1
    ax2.text(0.5, 0.95, "Data Flow Diagram — Level 1 (Functional Decomposition)", ha='center', fontsize=12, fontweight='bold', color="#1e1b4b")
    draw_box(ax2, 0.04, 0.45, 0.16, 0.35, "Learner\n(Web UI)", "User Input", "#f1f5f9", "#475569")
    
    draw_box(ax2, 0.25, 0.70, 0.18, 0.18, "1.0 Validate Input", "Pydantic Schema", "#dbeafe", "#2563eb")
    draw_box(ax2, 0.25, 0.42, 0.18, 0.18, "2.0 Route Request", "Select Feature Module", "#fef3c7", "#d97706")
    draw_box(ax2, 0.25, 0.14, 0.18, 0.18, "3.0 Format Response", "Markdown / JSON Grader", "#d1fae5", "#059669")

    draw_box(ax2, 0.52, 0.56, 0.20, 0.25, "4.0 AI Generation\n(Gemini / Local)", "Prompt Execution", "#ecfdf5", "#10b981")
    draw_box(ax2, 0.52, 0.16, 0.20, 0.25, "5.0 Fallback Manager", "Deterministic Corpus", "#fffbeb", "#f59e0b")

    draw_box(ax2, 0.80, 0.35, 0.16, 0.40, "Offline Corpus\n& Rules Store", "Data Store D1", "#ede9fe", "#7c3aed")

    # Connect Level 1
    draw_arrow(ax2, 0.20, 0.62, 0.25, 0.75, "Raw Query")
    draw_arrow(ax2, 0.34, 0.70, 0.34, 0.60)
    draw_arrow(ax2, 0.43, 0.51, 0.52, 0.65, "Valid Topic")
    draw_arrow(ax2, 0.43, 0.45, 0.52, 0.30, "On API Error")
    draw_arrow(ax2, 0.72, 0.28, 0.80, 0.45, "Lookup")
    draw_arrow(ax2, 0.62, 0.56, 0.43, 0.24, "Model Output")
    draw_arrow(ax2, 0.62, 0.20, 0.43, 0.20, "Fallback Content")
    draw_arrow(ax2, 0.25, 0.23, 0.12, 0.45, "Rendered UI View")

    plt.tight_layout()
    out_path = os.path.join(DIAGRAMS_DIR, "03_data_flow_diagram.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

# Diagram 4: Use Case Diagram
def create_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "EduGenie: System Use Case Diagram", ha='center', fontsize=13, fontweight='bold', color="#1e1b4b")

    # System boundary box
    sys_box = FancyBboxPatch((0.26, 0.05), 0.68, 0.85, boxstyle="round,pad=0.02", facecolor="#ffffff", edgecolor="#4f46e5", linewidth=2)
    ax.add_patch(sys_box)
    ax.text(0.60, 0.87, "EduGenie Learning Assistant Boundary", ha='center', fontsize=11, fontweight='bold', color="#4f46e5")

    # Actor on the left
    ax.plot([0.12, 0.12], [0.55, 0.45], color="#1e1b4b", lw=3) # body
    circle = plt.Circle((0.12, 0.60), 0.035, facecolor="#e0e7ff", edgecolor="#1e1b4b", lw=2, zorder=5) # head
    ax.add_patch(circle)
    ax.plot([0.07, 0.17], [0.52, 0.52], color="#1e1b4b", lw=3) # arms
    ax.plot([0.12, 0.07], [0.45, 0.35], color="#1e1b4b", lw=3) # left leg
    ax.plot([0.12, 0.17], [0.45, 0.35], color="#1e1b4b", lw=3) # right leg
    ax.text(0.12, 0.29, "Student / Learner\n(Actor)", ha='center', fontsize=10, fontweight='bold', color="#1e1b4b")

    # Use Cases inside boundary
    use_cases = [
        ("UC-01: Ask Academic Question (/qa)", 0.77),
        ("UC-02: Simplify Complex Concept (/explain)", 0.64),
        ("UC-03: Summarize Study Passage (/summarize)", 0.51),
        ("UC-04: Take Interactive 3-MCQ Quiz (/quiz)", 0.38),
        ("UC-05: Generate Personalized Roadmap (/learn)", 0.25),
        ("UC-06: Monitor System Liveness & Health (/health)", 0.12)
    ]

    for title, y_pos in use_cases:
        ellipse = FancyBboxPatch((0.34, y_pos-0.04), 0.52, 0.08, boxstyle="round,pad=0.02,rounding_size=0.04", facecolor="#eef2ff", edgecolor="#6366f1", lw=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(0.60, y_pos, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color="#1e1b4b", zorder=4)
        # Line from actor to use case
        ax.plot([0.16, 0.34], [0.50, y_pos], color="#94a3b8", linestyle="--", lw=1.5, zorder=2)

    plt.tight_layout()
    out_path = os.path.join(DIAGRAMS_DIR, "04_use_case_diagram.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

# Diagram 5: AI Generation Flow
def create_ai_generation_flow():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "EduGenie: AI Prompt Generation & Validation Pipeline", ha='center', fontsize=13, fontweight='bold', color="#1e1b4b")

    draw_box(ax, 0.05, 0.65, 0.24, 0.18, "1. User Input Ingestion", "Topic, Query or Passage\nSanitized & Trimmed", "#e0e7ff", "#4f46e5")
    draw_box(ax, 0.38, 0.65, 0.24, 0.18, "2. Prompt Engineering", "Role Definition • Few-shot Format\nStrict Output Constraints", "#dbeafe", "#2563eb")
    draw_box(ax, 0.71, 0.65, 0.24, 0.18, "3. Model Inference", "Google GenAI SDK Call\nModel: gemini-1.5-flash/pro", "#ecfdf5", "#10b981")

    draw_box(ax, 0.71, 0.25, 0.24, 0.18, "4. Raw Output Cleaning", "clean_json_block()\nStrip Markdown ```json fences", "#fef3c7", "#d97706")
    draw_box(ax, 0.38, 0.25, 0.24, 0.18, "5. Schema Validation", "validate_quiz_data()\n3 MCQs, 4 Options, Answer match", "#f3e8ff", "#9333ea")
    draw_box(ax, 0.05, 0.25, 0.24, 0.18, "6. Client Response", "HTTP 200 OK + Payload\nInteractive UI Rendering", "#d1fae5", "#059669")

    # Connect Pipeline
    draw_arrow(ax, 0.29, 0.74, 0.38, 0.74, "Clean Input")
    draw_arrow(ax, 0.62, 0.74, 0.71, 0.74, "Constructed Prompt")
    draw_arrow(ax, 0.83, 0.65, 0.83, 0.43, "Raw Text / Stream")
    draw_arrow(ax, 0.71, 0.34, 0.62, 0.34, "Stripped JSON")
    draw_arrow(ax, 0.38, 0.34, 0.29, 0.34, "Validated Object")

    # Retry loop arrow on validation fail
    ax.annotate("On Schema Fail (Retry 1x)", xy=(0.83, 0.65), xytext=(0.50, 0.45),
                arrowprops=dict(arrowstyle="->", color="#ef4444", lw=1.5, linestyle=":", connectionstyle="arc3,rad=-0.3"),
                fontsize=8, color="#b91c1c", fontweight='bold')

    plt.tight_layout()
    out_path = os.path.join(DIAGRAMS_DIR, "05_ai_generation_flow.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

# Diagram 6: Fallback Flow
def create_fallback_flow():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "EduGenie: Fault-Tolerant Fallback & Graceful Degradation Architecture", ha='center', fontsize=13, fontweight='bold', color="#1e1b4b")

    draw_box(ax, 0.38, 0.82, 0.24, 0.08, "Incoming Request", "Endpoint (/qa, /quiz, etc.)", "#e0e7ff", "#4f46e5")
    draw_box(ax, 0.38, 0.68, 0.24, 0.08, "Is Demo Mode?", "API Key Empty or Placeholder", "#fef3c7", "#d97706")

    draw_box(ax, 0.06, 0.50, 0.26, 0.10, "Attempt Live Gemini API", "Call Google GenAI SDK", "#ecfdf5", "#10b981")
    draw_box(ax, 0.06, 0.32, 0.26, 0.10, "Did API Succeed & Validate?", "Status 200 & Schema Valid", "#dbeafe", "#2563eb")
    draw_box(ax, 0.06, 0.12, 0.26, 0.10, "Return Live Response", "Mode: LIVE • Gemini Model", "#d1fae5", "#059669")

    draw_box(ax, 0.68, 0.40, 0.26, 0.14, "Deterministic Fallback Engine", "Generate Verified Offline Response\nZero-Downtime Guarantee", "#fffbeb", "#f59e0b")
    draw_box(ax, 0.68, 0.12, 0.26, 0.10, "Return Fallback Response", "Mode: DEMO/FALLBACK\nVisible Badge & Notice", "#fee2e2", "#ef4444")

    # Arrows
    draw_arrow(ax, 0.50, 0.82, 0.50, 0.76)
    draw_arrow(ax, 0.38, 0.72, 0.19, 0.60, "No (Key Present)")
    draw_arrow(ax, 0.62, 0.72, 0.81, 0.54, "Yes (Demo Mode)")

    draw_arrow(ax, 0.19, 0.50, 0.19, 0.42)
    draw_arrow(ax, 0.19, 0.32, 0.19, 0.22, "Yes (Valid)")
    draw_arrow(ax, 0.32, 0.37, 0.68, 0.45, "No (Timeout/Quota/Invalid)", color="#ef4444")
    draw_arrow(ax, 0.81, 0.40, 0.81, 0.22)

    plt.tight_layout()
    out_path = os.path.join(DIAGRAMS_DIR, "06_fallback_flow.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    create_system_architecture()
    create_workflow_flowchart()
    create_data_flow_diagram()
    create_use_case_diagram()
    create_ai_generation_flow()
    create_fallback_flow()
    print("All 6 design diagrams generated successfully!")
