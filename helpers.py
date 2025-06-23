from prompt_templates import *
import re
import simple_icd_10_cm as cm
import re
from openai import OpenAI
import pandas as pd

CHAPTER_LIST = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"]
ICD_PARAM_REGEX = re.compile(r'\*?\*?(ICD-10 Code):\*?\*? (?P<code>[A-Z0-9.]{3,8})')
ICD_REGEX = r'(^[A-Z0-9.]{3,8})'
client = OpenAI(api_key="sk-proj-......")

VAL_FILE = 'Test_Project_ICD10_Dataset.csv'
MODEL_NAME = "gpt-4o"
TEMPERATURE = 0.2
MAX_TOKENS = 500
# TOP_P = 0.2

def format_code_descriptions(text):
    """
    Removes the last occurrence of content within parentheses from the provided text.
    Remove extra spaces from a given text.
    Format the ICD-10 code descriptions by removing content inside brackets and extra spaces.
    """
    pattern = r'\([^()]*\)(?!.*\([^()]*\))'
    cleaned_text1 = re.sub(pattern, '', text)
    cleaned_text2 = re.sub(r'\s+', ' ', cleaned_text1).strip()
        
    return cleaned_text2


def get_name_and_description(code):
    """
    Retrieve the name and description of an ICD-10 code.
    """
    full_data = cm.get_full_data(code).split("\n")
    return format_code_descriptions(full_data[3]), full_data[1]

def construct_prompt_template(case_note, code_descriptions):
    """
    Construct a prompt template for evaluating ICD-10 code descriptions against a given case note.
    """
    template = prompt_template_dict[MODEL_NAME]

    return template.format(note=case_note, code_descriptions=code_descriptions)

def build_prompt(input_note, descriptions, system_prompt=""):
    """
    Build a zero-shot classification prompt with system and user roles for a language model.
    """
    code_descriptions = "\n".join(descriptions)
    input_prompt = construct_prompt_template(input_note, code_descriptions)

    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": input_prompt}]


def calculate_metrics_simple(true: pd.DataFrame, pred: pd.DataFrame) -> dict:
    """Compute the macro-precision, macro-recall and macro-f1 scores."""
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for i, _ in true.iterrows():
        true_labels = set(true.loc[i, "gold_standard"])
        pred_labels = set(pred.loc[i, "predicted_code"])
        tp = len(pred_labels.intersection(true_labels))
        false_positives += len(pred_labels) - tp
        false_negatives += len(true_labels) - tp
        true_positives += len(pred_labels.intersection(true_labels))
    macro_precision = true_positives / (true_positives + false_positives)
    macro_recall = true_positives / (true_positives + false_negatives)
    macro_f1 = 2 * (macro_precision * macro_recall) / (macro_precision + macro_recall)
    return dict(precision=macro_precision, recall=macro_recall, f1_score=macro_f1)

def get_val_data(file: str):
    """
    Load a validation dataset and extract the icd10 codes
    """
    df = pd.read_csv(file)
    gold_standard = []
    for i, _ in df.iterrows():
        labels = []
        for line in df.loc[i, "reference_answer"].split("\n"):
            labels += re.findall(ICD_REGEX, line)
        gold_standard.append(labels)
    df['gold_standard'] = gold_standard

    return df