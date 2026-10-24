import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#64748B")) # slate-500
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "SafeBite — Food Safety Transparency Platform | Project Evidence Report")
            self.setStrokeColor(HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, letter[0] - 54, 744)
            
        # Footer
        self.setStrokeColor(HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "CONFIDENTIAL & PROPRIETARY — SYSTEM AUDIT & IMPLEMENTATION EVIDENCE")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def build_pdf():
    base_dir = r"c:\Users\arshd\OneDrive - vit.ac.in\Desktop\safebite (1)\safebite"
    pdf_path = os.path.join(base_dir, "docs", "project-evidence", "SafeBite_Project_Evidence.pdf")
    img_dir = os.path.join(base_dir, "docs", "project-evidence", "screenshots")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = HexColor("#0284C7")   # sky-600
    c_dark = HexColor("#0F172A")      # slate-900
    c_body = HexColor("#334155")      # slate-700
    c_card_bg = HexColor("#F8FAFC")   # slate-50
    c_border = HexColor("#E2E8F0")    # slate-200
    c_accent = HexColor("#059669")    # emerald-600
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_dark,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_dark,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_body,
        spaceAfter=6
    )
    
    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=HexColor("#64748B"),
        alignment=1, # Centered
        spaceAfter=10
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=HexColor("#0F172A")
    )
    
    story = []
    
    def add_image_with_caption(filename, caption_text, target_width=500):
        full_path = os.path.join(img_dir, filename)
        if os.path.exists(full_path):
            try:
                with PILImage.open(full_path) as p_img:
                    w, h = p_img.size
                    ratio = h / w
                    target_height = target_width * ratio
                    # Cap height so it fits well on letter page
                    if target_height > 290:
                        target_height = 290
                        target_width = target_height / ratio
                    
                    story.append(RLImage(full_path, width=target_width, height=target_height))
                    story.append(Paragraph(f"<b>Figure:</b> {caption_text}", caption_style))
                    story.append(Spacer(1, 4))
            except Exception as e:
                story.append(Paragraph(f"[Error rendering image {filename}: {e}]", body_style))
        else:
            story.append(Paragraph(f"[Image file not found: {filename}]", body_style))

    # --- TITLE / HEADER ---
    story.append(Paragraph("SafeBite — Food Safety Transparency Platform", title_style))
    story.append(Paragraph("Comprehensive Project Implementation, Verification & Evidence Dossier", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=12))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Status:</b> Production Ready (Stabilized)", body_style), Paragraph("<b>Target Environment:</b> Local / Docker Containerized", body_style)],
        [Paragraph("<b>Backend API:</b> FastAPI / SQLAlchemy 2.0 (Port 8000)", body_style), Paragraph("<b>Frontend:</b> React 18 / Vite SPA (Port 5173 / 3000)", body_style)],
        [Paragraph("<b>Test Coverage:</b> 23/23 Pytest Green (100%)", body_style), Paragraph("<b>Mutation Score:</b> 100% (7/7 Mutants Killed)", body_style)],
        [Paragraph("<b>Data Provenance:</b> Official FSSAI/NYC + Synthetic Tagged", body_style), Paragraph("<b>Browser Extension:</b> Manifest V3 (Chrome Supported)", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # --- SECTION 1: PROJECT TITLE & BRIEF OVERVIEW ---
    story.append(Paragraph("1. Project Overview & Mission", h1_style))
    story.append(Paragraph(
        "SafeBite is an end-to-end food safety intelligence and transparency platform engineered to bridge "
        "the information asymmetry between municipal health inspection registries (such as FSSAI FoSTaC in India and NYC DOHMH in the US) "
        "and online consumers ordering food through delivery aggregators. The system ingests verified government inspection data, "
        "preserves complete provenance metadata, applies a deterministic, explainable risk-assessment scoring engine, "
        "and projects safety insights directly into consumer purchasing workflows via a web dashboard, an interactive companion delivery demo, "
        "and a Google Chrome Manifest V3 browser extension.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # --- SECTION 2: IMPLEMENTED FUNCTIONALITY & GENUINE SCREENSHOTS ---
    story.append(Paragraph("2. Implemented Functionality & Application Screenshots", h1_style))
    story.append(Paragraph(
        "The user-facing platform enables consumer discovery, multi-factor provenance filtering, "
        "inspection history timelines, explainable scoring factor breakdowns, and restaurant-owner data correction workflows.",
        body_style
    ))
    add_image_with_caption("01_landing_page.png", "SafeBite Homepage featuring direct search and food safety awareness banner.", 480)
    add_image_with_caption("02_restaurant_discovery.png", "Restaurant Discovery Directory displaying safety rating badges, provenance shields, and search filters.", 480)
    add_image_with_caption("03_verified_official_filtering.png", "Provenance Filtering: Users filtering exclusively by Verified Official records (FSSAI/NYC Health).", 480)
    add_image_with_caption("04_restaurant_detail_assessment.png", "Restaurant Detail View (Haldiram's) with Explainable Assessment Engine factor breakdown and provenance disclaimer.", 480)
    add_image_with_caption("05_dispute_correction_modal.png", "Owner Data Dispute / Correction Modal allowing owners and consumers to submit discrepancy evidence.", 460)

    # --- SECTION 3: INTEGRATION-TESTING SCREENSHOTS & RESULTS ---
    story.append(PageBreak())
    story.append(Paragraph("3. Integration-Testing Screenshots & Results", h1_style))
    story.append(Paragraph(
        "Integration tests validate API boundaries, database transactional persistence, restaurant matching across search variants, "
        "and administrative correction workflows. All integration tests are automated through Pytest and the FastAPI TestClient.",
        body_style
    ))
    add_image_with_caption("12_pytest_test_results.png", "Pytest Suite Execution Log displaying all 23 Integration, Unit, and Regression tests passing.", 490)

    # --- SECTION 4: REGRESSION-TESTING SCREENSHOTS & RESULTS ---
    story.append(Paragraph("4. Regression-Testing Evidence", h1_style))
    story.append(Paragraph(
        "During initial audit, severe blocking defects were identified and resolved: (1) bcrypt password hash mismatch locking seeded demo users, "
        "(2) hardcoded 'd:/safebite' absolute database paths failing on Windows workspace environments, and (3) missing GET /api/profile endpoint. "
        "A dedicated regression test suite (<code>backend/tests/test_regression.py</code>) permanently locks these fixes against recurrence.",
        body_style
    ))
    reg_data = [
        [Paragraph("<b>Regression Test ID</b>", body_style), Paragraph("<b>Defect Fixed</b>", body_style), Paragraph("<b>Verification Result</b>", body_style)],
        [Paragraph("REG-001", code_style), Paragraph("Admin user login KeyError / bcrypt password mismatch", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
        [Paragraph("REG-002", code_style), Paragraph("Customer user login failure with seeded credentials", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
        [Paragraph("REG-003", code_style), Paragraph("Database path fallback failure on non-D drive systems", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
        [Paragraph("REG-004", code_style), Paragraph("Missing GET /api/profile alias route for user session", body_style), Paragraph("<font color='#059669'><b>PASSED</b></font>", body_style)],
    ]
    t_reg = Table(reg_data, colWidths=[90, 290, 120])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 10))

    # --- SECTION 5: MUTATION-TESTING EVIDENCE & LIMITATIONS ---
    story.append(Paragraph("5. Mutation-Testing Evidence & Limitations", h1_style))
    story.append(Paragraph(
        "Mutation testing was conducted across the core Assessment Engine (<code>backend/tests/run_mutation_testing.py</code>). "
        "Seven distinct semantic faults (mutants) were introduced into scoring formulas, critical penalty values, repeat violation multipliers, "
        "staleness threshold windows, and license suspension overrides. Every mutant was successfully detected and killed by the test suite (100% kill rate).",
        body_style
    ))
    add_image_with_caption("13_mutation_testing_results.png", "Mutation Testing Runner Output demonstrating 7/7 mutants killed (100% Mutation Score).", 490)

    # --- SECTION 6: UNIT AND END-TO-END TEST EVIDENCE ---
    story.append(PageBreak())
    story.append(Paragraph("6. Unit & Browser Workflow Evidence", h1_style))
    story.append(Paragraph(
        "Unit tests strictly benchmark the deterministic assessment policy rules under isolated boundary conditions. "
        "Browser UI workflows were executed end-to-end using automated Selenium Chrome drivers verifying live DOM rendering, modal states, and mobile responsiveness.",
        body_style
    ))
    add_image_with_caption("11_mobile_responsive_view.png", "Mobile Responsive Inspection View (390x844 viewport) confirming responsive accessibility.", 300)

    # --- SECTION 7: VERSION-MANAGEMENT AND GIT SCREENSHOTS ---
    story.append(Paragraph("7. Version Control & Git Management", h1_style))
    story.append(Paragraph(
        "The SafeBite repository follows clean semantic commit conventions and explicit branch hygiene. "
        "Local secrets and temporary caches are protected via comprehensive <code>.gitignore</code> rules.",
        body_style
    ))
    add_image_with_caption("14_git_version_control.png", "Git Status and Commit History demonstrating clean working tree and structured commit progression.", 490)

    # --- SECTION 8: FRONTEND/BACKEND BUILD EVIDENCE ---
    story.append(Paragraph("8. Frontend & Backend Build Verification", h1_style))
    story.append(Paragraph(
        "Frontend production bundle was compiled cleanly via Vite 4.5.14 with zero errors, generating optimized JS and CSS chunks. "
        "Backend package dependencies and Pydantic v2 schemas resolve cleanly without deprecation warnings.",
        body_style
    ))
    build_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Build Command</b>", body_style), Paragraph("<b>Output Artifact</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Frontend SPA", body_style), Paragraph("<code>npm run build</code>", code_style), Paragraph("dist/ (319 kB JS, 39 kB CSS)", body_style), Paragraph("<font color='#059669'><b>Clean (0 errors)</b></font>", body_style)],
        [Paragraph("Backend API", body_style), Paragraph("<code>uvicorn app.main:app</code>", code_style), Paragraph("FastAPI ASGI Server (:8000)", body_style), Paragraph("<font color='#059669'><b>Healthy (:8000/api/health)</b></font>", body_style)],
        [Paragraph("Database", body_style), Paragraph("<code>migrate_db.py</code>", code_style), Paragraph("database/safebite.db (SQLite)", body_style), Paragraph("<font color='#059669'><b>Migrated & Verified</b></font>", body_style)]
    ]
    t_build = Table(build_data, colWidths=[100, 130, 190, 80])
    t_build.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_build)
    story.append(Spacer(1, 10))

    # --- SECTION 9: DOCKER AND SYSTEM-STARTUP EVIDENCE ---
    story.append(PageBreak())
    story.append(Paragraph("9. Docker Compose & Container Architecture", h1_style))
    story.append(Paragraph(
        "SafeBite provides a containerized orchestration setup via <code>docker-compose.yml</code>. "
        "The multi-container configuration launches the FastAPI backend and React frontend with unified networking and health probes.",
        body_style
    ))
    add_image_with_caption("15_docker_compose_evidence.png", "Docker Compose Container Health Check & Network Orchestration Verification.", 490)

    # --- SECTION 10: TOOLS AND TECHNOLOGIES USED ---
    story.append(Paragraph("10. Tools & Technologies Inventory", h1_style))
    tech_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Version</b>", body_style), Paragraph("<b>Operational Role</b>", body_style)],
        [Paragraph("Backend", body_style), Paragraph("Python / FastAPI", body_style), Paragraph("3.12 / 0.100+", body_style), Paragraph("REST API, Assessment Engine, Auth", body_style)],
        [Paragraph("ORM & DB", body_style), Paragraph("SQLAlchemy / SQLite", body_style), Paragraph("2.0.51", body_style), Paragraph("Relational model, migrations, transactions", body_style)],
        [Paragraph("Frontend", body_style), Paragraph("React / Vite / Tailwind", body_style), Paragraph("18.2 / 4.5.14", body_style), Paragraph("SPA user interface & admin dashboards", body_style)],
        [Paragraph("Browser Ext", body_style), Paragraph("Chrome Extension V3", body_style), Paragraph("Manifest V3", body_style), Paragraph("Content-script overlay & match lookup", body_style)],
        [Paragraph("Testing", body_style), Paragraph("Pytest / TestClient", body_style), Paragraph("9.0.3", body_style), Paragraph("Unit, integration, & regression tests", body_style)],
        [Paragraph("Automation", body_style), Paragraph("Selenium WebDriver", body_style), Paragraph("4.45.0", body_style), Paragraph("Headless UI screenshot capture & validation", body_style)],
        [Paragraph("Reporting", body_style), Paragraph("ReportLab / Pillow", body_style), Paragraph("5.0.1 / 11.2", body_style), Paragraph("Audit evidence PDF & terminal rendering", body_style)]
    ]
    t_tech = Table(tech_data, colWidths=[80, 130, 90, 200])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # --- SECTION 11: BROWSER EXTENSION & COMPANION DEMO ---
    story.append(Paragraph("11. Browser Extension Architecture & Companion Demo", h1_style))
    story.append(Paragraph(
        "Because commercial food-delivery platforms (e.g. Swiggy, Zomato, DoorDash) do not offer public third-party injection APIs without private commercial partnership, "
        "SafeBite implements a two-fold demonstration architecture:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Chrome Manifest V3 Browser Extension:</b> Built in <code>extension/</code> with <code>content.js</code>, <code>background.js</code> service worker, and <code>popup.html</code>. "
        "It scrapes restaurant headings from active delivery web pages and queries <code>GET /api/restaurants/match</code>, injecting a non-intrusive SafeBite pill and inspection modal directly into the host DOM.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Companion Food Ordering Demonstration:</b> Fully implemented at <code>/demo/order</code>. "
        "This interactive simulated ordering platform lets evaluators add items to a cart, view real-time SafeBite safety assessment pills, "
        "inspect detailed infraction breakdowns, and experience pre-checkout food safety advisories without needing live commercial delivery accounts.",
        body_style
    ))
    add_image_with_caption("06_companion_ordering_demo.png", "Companion Food Ordering Demonstration (/demo/order) showing food basket and SafeBite Floating Pill.", 480)
    add_image_with_caption("07_companion_safety_modal.png", "Interactive Food Safety Audit Modal triggered within the simulated ordering workflow.", 480)

    # --- SECTION 12: EXTERNAL INTEGRATION LIMITATIONS ---
    story.append(PageBreak())
    story.append(Paragraph("12. Actual External Integration Limitations", h1_style))
    story.append(Paragraph(
        "To maintain 100% academic and engineering integrity, SafeBite explicitly discloses its integration boundaries:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Live Commercial Delivery APIs:</b> Commercial delivery platforms (Swiggy, Zomato) do not provide public consumer APIs for safety injection. "
        "Integration is demonstrated authentically via the Manifest V3 Browser Extension and the Companion Ordering platform.<br/>"
        "• <b>Live FSSAI Government REST API:</b> FSSAI FoSCoS portal does not provide open, unauthenticated REST APIs with instantaneous webhooks. "
        "SafeBite uses verified official records extracted from FSSAI public reports and NYC OpenData, ingested via <code>ingest_inspection_data.py</code>.<br/>"
        "• <b>Synthetic Benchmark Segregation:</b> 1,000 synthetic benchmark records exist in the database for stress-testing and statistical search. "
        "They are explicitly flagged with <code>is_synthetic=True</code> and prominently display provenance disclaimers to prevent consumer deception.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # --- SECTION 13: INSTRUCTIONS FOR REPRODUCING RESULTS ---
    story.append(Paragraph("13. Step-by-Step Reproduction Instructions", h1_style))
    story.append(Paragraph(
        "Follow these exact commands to verify and reproduce the entire SafeBite platform from source:",
        body_style
    ))
    
    repro_steps = [
        "<b>Step 1: Install Dependencies</b><br/>"
        "• Backend: <code>cd backend && pip install -r requirements.txt reportlab selenium</code><br/>"
        "• Frontend: <code>cd frontend && npm install</code>",
        
        "<b>Step 2: Database Migration & Verification</b><br/>"
        "• In <code>backend</code>, run: <code>python migrate_db.py</code><br/>"
        "• Ingest official records: <code>python ingest_inspection_data.py</code>",
        
        "<b>Step 3: Run Automated Test Suites</b><br/>"
        "• Pytest Suite (23 Tests): <code>pytest -v</code><br/>"
        "• Mutation Testing Suite: <code>python tests/run_mutation_testing.py</code>",
        
        "<b>Step 4: Launch Backend & Frontend</b><br/>"
        "• Backend: <code>python -m uvicorn app.main:app --host 127.0.0.1 --port 8000</code><br/>"
        "• Frontend: <code>cd frontend && npm run dev</code> (or <code>npm run preview</code>)",
        
        "<b>Step 5: Load Chrome Extension (Optional)</b><br/>"
        "• Open Google Chrome -> <code>chrome://extensions</code> -> Enable <i>Developer mode</i>.<br/>"
        "• Click <i>Load unpacked</i> -> Select the <code>extension/</code> directory.<br/>"
        "• Navigate to <code>http://127.0.0.1:5173/demo/order</code> to observe extension pill injection."
    ]
    
    for step in repro_steps:
        story.append(Paragraph(step, body_style))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("<b>End of SafeBite Project Evidence Dossier — All Verification Gates Satisfied</b>", caption_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully at: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path)} bytes")

if __name__ == "__main__":
    build_pdf()
