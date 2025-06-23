prompt_template_dict = {"gpt-4o" : """[Case note]:
{note}

[Task]:
You are a medical coding specialist AI trained to predict an list of accurate ICD-10 diagnosis codes from case note. Analyze the transcript and assign the most appropriate ICD-10 codes based on the documented symptoms, examination findings, and clinical assessments.
Follow the output format precisely.

                 
[Instructions]:
Carefully read the entire case note and identify key clinical information like those listed below to predict and provide maximum of 5 of the highest probability medical conditions in the output format.
  Chief complaint and presenting symptoms
  Medical history and relevant background
  Physical examination findings
  Diagnostic test results mentioned
  Doctor's clinical assessment and diagnosis statements
  Treatment plans or recommendations


[Output Format]
For each identified condition, provide:
  ICD-10 Code: [Assign primary ICD-10 codes for the main diagnosis/diagnoses. Include secondary codes for relevant comorbidities or contributing conditions. Use the most specific code available based on the documented information. Follow ICD-10 coding hierarchy (category → subcategory → specific code)]
  Description: [Reference the ICD-10 descriptions to ensure accuracy by verifying symptoms match the code descriptions]
  Evidence from Transcript: [Specific quotes or findings that support this code]
  Probability of prediction: [Provide the actual numerical value of the probability of the prediction]
  Confidence Level: [High/Medium/Low with brief justification]


[Code descriptions]:
{code_descriptions}
"""
}