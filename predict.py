from helpers import *
import pandas as pd


def get_response_obj(messages, temperature=TEMPERATURE, max_tokens=MAX_TOKENS):
    """
    Obtain responses from a specified model via the chat-completions API.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        seed=23,
        temperature=temperature,
        max_completion_tokens=max_tokens
    )
    return response.choices[0].message.content


def get_response(medical_note, temperature=TEMPERATURE):
    """
    Putting together the input prompt and code descriptions to get llm response objects
    """
    candidate_codes = [x for x in CHAPTER_LIST]

    code_descriptions = {}
    for x in candidate_codes:
        description, code = get_name_and_description(x)
        code_descriptions[description] = code

    prompt = build_prompt(medical_note, list(code_descriptions.keys()))
    lm_response = get_response_obj(prompt, temperature=temperature, max_tokens=MAX_TOKENS)
    return lm_response


def get_icd_codes(medical_note, temperature=TEMPERATURE):
    """
    Identifies relevant ICD-10 codes for a given medical note by querying a language model.
    This function implements the tree-search algorithm for ICD coding described in https://openreview.net/forum?id=mqnR8rGWkn.
    """
    lm_response = get_response(medical_note, temperature=TEMPERATURE)
    assigned_codes = [m.groupdict()['code'] for m in ICD_PARAM_REGEX.finditer(lm_response)]

    return assigned_codes


def get_preds_df(df: pd.DataFrame, save_to_file=False):
    """
    Collects the LLM response objects and the ICD10 codes along with the input paramaters
    """
    codes = []
    lm_responses = []
    for i, _ in df.iterrows():
        lm_response = get_response(df.loc[i, "transcript"], temperature=TEMPERATURE)
        code = get_icd_codes(df.loc[i, "transcript"], temperature=TEMPERATURE)
        codes.append(code)
        lm_responses.append(lm_response)

    pred_df = pd.DataFrame({'predicted_code':codes, 'encounter_id':df['encounter_id'], 'llm_response':lm_responses, 'transcript':df['transcript'], 
                            'reference_answer':df['reference_answer'], 'gs_codes':df['gold_standard']})
    if save_to_file:
        pred_df.to_csv('pred_df.csv', index=False)
    return pred_df


if __name__ == "__main__":
    """
    Predict the ICD10 codes for the transcripts in the VAL_FILE and run benchmarks on the same.
    """
    val_df = get_val_data(VAL_FILE)
    pred_df = get_preds_df(val_df)
    print("Validation metrics", calculate_metrics_simple(val_df, pred_df))