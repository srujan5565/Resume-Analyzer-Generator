import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import streamlit as st
import tempfile
import os
from PIL import Image as PILImage
from io import BytesIO


# Function to generate the resume as a PDF (Template 1 - Classic Layout)
def generate_resume_pdf_template1(data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdf_file = temp_pdf.name

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=24,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    # Styles
    name_style = ParagraphStyle(
        "name_style",
        parent=styles["Heading1"],
        fontName="Times-Roman",
        fontSize=18,  # Larger font size for name
        textColor=colors.black,
        spaceAfter=6,
    )
    contact_style = ParagraphStyle(
        "contact_style",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
    )
    section_title_style = ParagraphStyle(
        "section_title_style",
        parent=styles["Heading2"],
        fontName="Times-Roman",  # Set to Times New Roman
        fontSize=14,  # Increased font size for section titles
        alignment=1,  # Center alignment
        textColor=colors.black,
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "bullet_style",
        parent=styles["BodyText"],
        bulletText="• ",  # Add bullet before text
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.black,
        spaceAfter=3,
    )
    normal_style = ParagraphStyle(
        "normal_style",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.black,
    )

    elements = []

    # Header Section: Name, Contact, and Photo
    header_table_data = [
        [
            Paragraph(f"<b>{data['name']}</b>", name_style),
            # Image(data["photo"], width=100, height=100) if data["photo"] else "",
        ]
    ]
    header_table = Table(header_table_data, colWidths=[400, 150])
    elements.append(header_table)
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(data["contact"], contact_style))
    elements.append(Spacer(1, 8))

    # Career Objective
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Career Objective</b>", section_title_style))
    elements.append(Paragraph(data["career_objective"], normal_style))
    elements.append(Spacer(1, 8))

    # Education
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Education</b>", section_title_style))
    for edu in data["education"]:
        elements.append(Paragraph(edu, bullet_style))
    elements.append(Spacer(1, 8))

    # Technical Skills and Experience
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    if data["experience"]:
        # Display both Technical Skills and Experience side by side
        tech_exp_table_data = [
            [
                Paragraph("<b>Technical Skills</b>", section_title_style),
                Paragraph("<b>Experience</b>", section_title_style),
            ]
        ]
        max_rows = max(len(data["skills"]), len(data["experience"]))
        for i in range(max_rows):
            tech_exp_table_data.append([
                Paragraph(data["skills"][i], bullet_style) if i < len(data["skills"]) else "",
                Paragraph(data["experience"][i], bullet_style) if i < len(data["experience"]) else "",
            ])
        tech_exp_table = Table(tech_exp_table_data, colWidths=[250, 250])
        tech_exp_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        elements.append(tech_exp_table)
    else:
        # Display only Technical Skills in the center
        elements.append(Paragraph("<b>Technical Skills</b>", section_title_style))
        for skill in data["skills"]:
            elements.append(Paragraph(skill, bullet_style))
    elements.append(Spacer(1, 8))

    # Projects
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Projects</b>", section_title_style))
    for proj in data["projects"]:
        elements.append(Paragraph(f"<b>{proj['title']}</b>", normal_style))
        for line in proj["description"]:
            elements.append(Paragraph(line, bullet_style))
    elements.append(Spacer(1, 8))

    # Achievements and Certifications (Side by Side)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    ach_cert_table_data = [
        [
            Paragraph("<b>Achievements</b>", section_title_style),
            Paragraph("<b>Certifications</b>", section_title_style),
        ]
    ]
    max_rows = max(len(data["achievements"]), len(data["certifications"]))
    for i in range(max_rows):
        ach_cert_table_data.append([
            Paragraph(data["achievements"][i], bullet_style) if i < len(data["achievements"]) else "",
            Paragraph(data["certifications"][i], bullet_style) if i < len(data["certifications"]) else "",
        ])
    ach_cert_table = Table(ach_cert_table_data, colWidths=[250, 250])
    ach_cert_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(ach_cert_table)

    # Build PDF
    doc.build(elements)
    return pdf_file


# Function to generate the resume as a PDF (Template 2 - Modern Two-Column Layout)
def generate_resume_pdf_template2(data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdf_file = temp_pdf.name

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=24,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    # Styles
    name_style = ParagraphStyle(
        "name_style",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,  # Larger font size for name
        textColor=colors.black,
        spaceAfter=6,
    )
    contact_style = ParagraphStyle(
        "contact_style",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
    )
    section_title_style = ParagraphStyle(
        "section_title_style",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,  # Increased font size for section titles
        alignment=0,  # Left alignment
        textColor=colors.black,
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "bullet_style",
        parent=styles["BodyText"],
        bulletText="• ",  # Add bullet before text
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.black,
        spaceAfter=3,
    )
    normal_style = ParagraphStyle(
        "normal_style",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.black,
    )

    elements = []

    # Header Section: Name, Contact, and Photo
    header_table_data = [
        [
            Paragraph(f"<b>{data['name']}</b>", name_style),
            # Image(data["photo"], width=100, height=100) if data["photo"] else "",
        ]
    ]
    header_table = Table(header_table_data, colWidths=[400, 150])
    elements.append(header_table)
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(data["contact"], contact_style))
    elements.append(Spacer(1, 8))

    # Career Objective
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Career Objective</b>", section_title_style))
    elements.append(Paragraph(data["career_objective"], normal_style))
    elements.append(Spacer(1, 8))

    # Education (Two Columns)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Education</b>", section_title_style))
    edu_table_data = []
    for edu in data["education"]:
        edu_table_data.append([Paragraph(edu, bullet_style)])
    edu_table = Table(edu_table_data, colWidths=[500])
    edu_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(edu_table)
    elements.append(Spacer(1, 8))

    # Technical Skills and Experience (Two Columns)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    tech_exp_table_data = [
        [
            Paragraph("<b>Technical Skills</b>", section_title_style),
            Paragraph("<b>Experience</b>", section_title_style),
        ]
    ]
    max_rows = max(len(data["skills"]), len(data["experience"]))
    for i in range(max_rows):
        tech_exp_table_data.append([
            Paragraph(data["skills"][i], bullet_style) if i < len(data["skills"]) else "",
            Paragraph(data["experience"][i], bullet_style) if i < len(data["experience"]) else "",
        ])
    tech_exp_table = Table(tech_exp_table_data, colWidths=[250, 250])
    tech_exp_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(tech_exp_table)
    elements.append(Spacer(1, 8))

    # Projects (Two Columns)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Projects</b>", section_title_style))
    for proj in data["projects"]:
        elements.append(Paragraph(f"<b>{proj['title']}</b>", normal_style))
        for line in proj["description"]:
            elements.append(Paragraph(line, bullet_style))
    elements.append(Spacer(1, 8))

    # Achievements and Certifications (Two Columns)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 4))
    ach_cert_table_data = [
        [
            Paragraph("<b>Achievements</b>", section_title_style),
            Paragraph("<b>Certifications</b>", section_title_style),
        ]
    ]
    max_rows = max(len(data["achievements"]), len(data["certifications"]))
    for i in range(max_rows):
        ach_cert_table_data.append([
            Paragraph(data["achievements"][i], bullet_style) if i < len(data["achievements"]) else "",
            Paragraph(data["certifications"][i], bullet_style) if i < len(data["certifications"]) else "",
        ])
    ach_cert_table = Table(ach_cert_table_data, colWidths=[250, 250])
    ach_cert_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(ach_cert_table)

    # Build PDF
    doc.build(elements)
    return pdf_file


# Streamlit app
st.title("Resume Generator ⬇️")

# Template Selection
template = st.radio("Select Template", ["Template 1 - Classic", "Template 2 - Modern"])

# User inputs
# Section for User Inputs
st.markdown("## Personal Information")
data = {
    "name": st.text_input("Full Name", placeholder="Enter your full name (e.g., John Doe)"),
    "contact": st.text_area("Contact Info", placeholder="Add email, phone number, and address"),
    "career_objective": st.text_area("Career Objective", placeholder="Write a brief statement about your career goals"),
    # "photo": st.file_uploader("Upload Profile Photo (Optional)", type=["jpg", "jpeg", "png"]),
}

# Section for Education
st.markdown("---")
st.markdown("## Educational Background")
num_edu_entries = st.number_input("Number of Education Entries", min_value=1, step=1, value=1)
data["education"] = [
    f"{st.text_input(f'Degree {i+1}', placeholder='Type of Degree (e.g., B.Tech, M.Sc)')}, "
    f"{st.text_input(f'Institution {i+1}', placeholder='Institution Name (e.g., ABC University)')}, "
    f"{st.text_input(f'Years {i+1}', placeholder='Years of Study (e.g., 2018-2022)')}, "
    f"Marks: {st.text_input(f'Marks {i+1}', placeholder='Enter marks secured (e.g., 85%)')}"
    for i in range(num_edu_entries)
]

# Section for Skills
st.markdown("---")
st.markdown("## Technical Skills")
data["skills"] = st.text_area(
    "List your technical skills",
    placeholder="Enter one skill per line (e.g., Python, React, SQL)",
).split("\n")

# Section for Experience
st.markdown("---")
st.markdown("## Professional Experience")
data["experience"] = st.text_area(
    "Work Experience",
    placeholder="Describe your experience one line at a time (e.g., Software Engineer at XYZ Corp)",
).split("\n")

# Section for Projects
st.markdown("---")
st.markdown("## Projects")
num_projects = st.number_input("Number of Projects", min_value=1, step=1, value=1)
data["projects"] = [
    {
        "title": st.text_input(f"Project {i+1} Title", placeholder="Project Name (e.g., Resume Builder App)"),
        "description": st.text_area(
            f"Project {i+1} Description", 
            placeholder="Describe the project details (e.g., Developed a tool using Python and Streamlit)"
        ).split("\n"),
    }
    for i in range(num_projects)
]

# Section for Achievements
st.markdown("---")
st.markdown("## Achievements")
data["achievements"] = st.text_area(
    "Your Achievements",
    placeholder="Enter achievements one per line (e.g., Won XYZ Hackathon 2023)",
).split("\n")

# Section for Certifications
st.markdown("---")
st.markdown("## Certifications")
data["certifications"] = st.text_area(
    "Your Certifications",
    placeholder="Enter certifications one per line (e.g., AWS Certified Solutions Architect)",
).split("\n")


# Generate resume
if st.button("Generate Resume"):
    if template == "Template 1 - Classic":
        pdf_path = generate_resume_pdf_template1(data)
    else:
        pdf_path = generate_resume_pdf_template2(data)
    
    # Preview the resume
    if pdf_path:
        # Convert the PDF to base64 for embedding in an iframe
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

    # Download button
    with open(pdf_path, "rb") as pdf_file:
        st.download_button("Download Resume", pdf_file.read(), "enhanced_resume.pdf", "application/pdf")
    os.unlink(pdf_path)