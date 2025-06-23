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

    Replace `sk-proj-......` in helpers.py with your actual OpenAI API key<br>
    OR set it as an environment variable

# Usage

1. Web Interface
   Launch the Gradio web interface for interactive testing:
   ```
   python app.py
   ```
   This will start a web server where you can input medical transcripts and get ICD-10 code predictions.
2. Command Line
   Run predictions on a validation dataset:
   ```
   python predict.py
   ```
   For uncertainty estimates:
   ```
   from uncertainty_estimation import monte_carlo_uncertainty

   results = monte_carlo_uncertainty(transcript, n_samples=5)
   print(f"Reliable codes: {results['reliable_codes']}")
   print(f"Confidence: {results['confidence_level']}")

   # for visualization
   plot_uncertainty(results, save_path='uncertainty.png')
   
   ```

# Configuration

   Key parameters can be modified in helpers.py:

  `MODEL_NAME`: OpenAI model to use (default: "gpt-4o")<br>
  `TEMPERATURE`: Model temperature for randomness (default: 0.2)<br>
  `MAX_TOKENS`: Maximum response length (default: 500)<br>
  `CHAPTER_LIST`: ICD-10 chapters to consider<br>

# Data Format

1. Input: Medical transcripts should be provided as plain text
2. Output:<br>
    **ICD-10 Code**: Primary and secondary diagnosis codes <br>
    **Description**: Human-readable description of the condition <br>
    **Evidence**: Supporting quotes from the transcript<br>
    **Probability**: Numerical confidence score<br>
    **Confidence Level**: High/Medium/Low classification<br>
3. Evaluation:<br>
    **Precision**: Accuracy of predicted codes<br>
    **Recall**: Coverage of relevant codes<br>
    **F1-Score**: Harmonic mean of precision and recall<br>

