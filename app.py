import gradio as gr
from predict import get_icd_codes, get_response
from uncertainty import monte_carlo_uncertainty

def predict_with_uncertainty(transcript, n_samples=5):
    """
    Get ICD codes with uncertainty analysis including LLM response.
    """
    try:
        icd_codes = get_icd_codes(transcript)
        llm_response = get_response(transcript)
        uncertainty = monte_carlo_uncertainty(transcript, n_samples=n_samples)
        result = f"""ICD CODES: {', '.join(icd_codes)}

LLM RESPONSE:
{llm_response}

UNCERTAINTY ANALYSIS:
• Reliable Codes: {', '.join(uncertainty['reliable_codes'])}
• Confidence: {uncertainty['confidence_level']} ({uncertainty['confidence_score']:.2f})
• Samples: {n_samples}

RISK: {'✅ LOW' if uncertainty['confidence_score'] >= 0.7 else '⚠️ MEDIUM' if uncertainty['confidence_score'] >= 0.4 else '❌ HIGH'}"""
        
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio
demo = gr.Interface(
    fn=predict_with_uncertainty,
    inputs=[
        gr.Textbox(label="Medical Transcript", lines=8, placeholder="Enter medical transcript..."),
        gr.Slider(3, 10, 5, label="Samples")
    ],
    outputs=gr.Textbox(label="Results", lines=10),
    title="ICD-10 Prediction with Uncertainty",
    description="Predict ICD-10 codes with Monte Carlo uncertainty estimation"
)

if __name__ == "__main__":
    demo.launch()