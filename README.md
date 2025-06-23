## ICD10-Prediction

This system automatically assigns appropriate ICD-10 diagnosis codes based on medical transcripts. It uses OpenAI's pre-trained models with structured prompts to identify medical conditions and map them to standardized ICD-10 codes. 

# Installation

1. Clone the repository:

  ```
  git clone <repository-url>
  cd icd10-prediction
  ```

2. Install required dependencies:

  ```
  pip install gradio openai pandas simple-icd-10-cm
  ```

3. Set up your OpenAI API key:

    Replace `sk-proj-......` in helpers.py with your actual OpenAI API key
    OR set it as an environment variable
