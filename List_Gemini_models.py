import google.generativeai as genai

genai.configure(api_key="AIzaSyDlzD8SWJpGi-Jw6uxP6DLsb4vtkU7Jb90")

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)