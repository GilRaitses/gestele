import os
import random
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from markdownify import markdownify as md_to_plain_text

# Branding and tagline
APP_TITLE = "Gestele"
TAGLINE = "Beauty and Order from Chaos"

# Inject dynamic background CSS
custom_css = """
<style>
body {
    margin: 0;
    overflow: hidden;
    font-family: 'Lato', sans-serif;
}
@keyframes spiral-gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.gradient-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(120deg, #FFB6C1, #FFD700, #87CEEB, #90EE90);
    background-size: 200% 200%;
    animation: spiral-gradient 8s ease infinite;
    z-index: -1;
}
</style>
<div class='gradient-background'></div>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Function to scan the codebase and generate Markdown
def generate_codebase_dump(source_folder):
    toc = []
    content = []
    file_id = 0

    for dirpath, _, filenames in os.walk(source_folder):
        rel_dir = os.path.relpath(dirpath, source_folder)
        folder_id = rel_dir.replace(os.sep, ".") if rel_dir != "." else "1"
        toc.append(f"### 🪰 Folder: {rel_dir} (ID: {folder_id})")
        content.append(f"---\n\n### Folder: {rel_dir} (ID: {folder_id})\n")

        for i, filename in enumerate(filenames, start=1):
            file_id += 1
            file_path = os.path.join(dirpath, filename)
            file_id_str = f"{folder_id}.{i}"
            toc.append(f"  - 🪱 {filename} (ID: {file_id_str})")
            content.append(f"---\n\n### File: {filename} (ID: {file_id_str})\n")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content.append(file.read())
            except Exception as e:
                content.append(f"Could not read file: {e}\n")
    return "\n".join(toc), "\n".join(content)

# Function to apply "Cutieness Filter"
def apply_cutieness_filter(content, color_palette=None, emoji_set=None):
    if color_palette is None:
        color_palette = random.sample(["#FFB6C1", "#FFD700", "#87CEEB", "#90EE90"], 3)
    if emoji_set is None:
        emoji_set = random.sample(["🦄", "🌈", "💖", "🐥", "🐢", "✨"], 2)

    styles = f"""
    <style>
    h1 {{ color: {color_palette[0]}; }}
    h2 {{ color: {color_palette[1]}; }}
    h3 {{ color: {color_palette[2]}; }}
    </style>
    """
    content = content.replace("🪰", emoji_set[0]).replace("🪱", emoji_set[1])
    return styles + content

# Convert HTML to PDF-compatible plain text
def html_to_pdf_plain_text(html_content):
    plain_text = md_to_plain_text(html_content)
    return plain_text

# Export PDF using ReportLab
def export_pdf(content, output_file="codebase_output.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_file)
    story = []

    for paragraph in content.split("\n\n"):  # Split by paragraphs
        story.append(Paragraph(paragraph, styles["Normal"]))
        story.append(Spacer(1, 12))  # Add spacing between paragraphs

    doc.build(story)

# Hermes introduction
def show_hermes_intro():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>🪽 Greetings, Traveler! 🪽</h1>
            <p style="font-size: 18px;">
                I am Hermes, messenger of the gods, and I will guide you to bring order and beauty to your codebase! 🎶✨<br>
                Once, I brought harmony to the world with a simple lyre made from a tortoise shell.<br>
                Now, let’s bring harmony to your projects!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Add Hermes' explanations for each step
def hermes_explains_step(step):
    messages = {
        1: "📂 Paste your folder path below. It’s much easier than inscribing a stele like in my time! ✨",
        2: "🔍 Click 'Generate Preview' to let me analyze your codebase. We’ll create something harmonious together! 🎨",
        3: "🌈 Apply the 'Cutieness Filter' to make your code visually divine. Let's add some flair! 💖",
        4: "📜 Choose how to save your work—Markdown or PDF. Markdown is great for edits, but PDFs are polished and timeless!",
    }
    st.info(messages.get(step, "Let’s proceed!"))

# Streamlit GUI
st.title(APP_TITLE)
st.caption(TAGLINE)
st.sidebar.title("Options")

# Show Hermes intro
if "show_intro" not in st.session_state or st.session_state["show_intro"]:
    show_hermes_intro()
    if st.button("Let's Begin!"):
        st.session_state["show_intro"] = False

if "show_intro" in st.session_state and not st.session_state["show_intro"]:
    # Step 1: Folder path
    hermes_explains_step(1)
    source_folder = st.sidebar.text_input("Enter the source folder path:").strip()

    if source_folder:
        if os.path.exists(source_folder):
            st.sidebar.success(f"Folder found: {source_folder}")

            # Step 2: Generate codebase dump
            hermes_explains_step(2)
            if st.sidebar.button("Generate Preview"):
                toc, content = generate_codebase_dump(source_folder)
                st.session_state["content"] = content
                st.session_state["toc"] = toc
                st.subheader("Markdown Preview")
                st.markdown(f"## Table of Contents\n\n{toc}")
                st.text(content)

            # Step 3: Apply Cutieness Filter
            hermes_explains_step(3)
            if st.sidebar.button("Apply Cutieness"):
                if "content" in st.session_state:
                    cutie_styles = apply_cutieness_filter(st.session_state["content"])
                    st.subheader("HTML Preview with Cutieness")
                    st.markdown(cutie_styles, unsafe_allow_html=True)

            # Step 4: Export Options
            hermes_explains_step(4)

            # Markdown Export
            if st.sidebar.button("Download Markdown"):
                markdown_output = html_to_pdf_plain_text(apply_cutieness_filter(st.session_state["content"]))
                markdown_file = "codebase_output.md"
                with open(markdown_file, "w", encoding="utf-8") as f:
                    f.write(markdown_output)
                st.success(f"Markdown file saved as '{markdown_file}'.")

            # PDF Export
            if st.sidebar.button("Download PDF"):
                plain_text_content = html_to_pdf_plain_text(st.session_state["content"])
                export_pdf(plain_text_content.split("\n"), "codebase_output.pdf")
                st.success("PDF file saved as 'codebase_output.pdf'.")
