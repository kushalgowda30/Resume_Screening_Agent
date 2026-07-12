from src.resume_parser import extract_resume_text

resume_path = "sample_data/resumes/Suhas_Gowda.pdf"

text = extract_resume_text(resume_path)

print("=" * 80)
print(text)