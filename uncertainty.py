import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from predict import get_icd_codes


def monte_carlo_uncertainty(medical_note, n_samples=5, temp_range=(0.1, 0.6)):
    """
    Essential Monte Carlo uncertainty estimation for ICD-10 predictions.
    """
    # Generate predictions with different temperatures
    temperatures = np.linspace(temp_range[0], temp_range[1], n_samples)
    all_codes = []
    
    print(f"Generating {n_samples} samples...")
    for i, temp in enumerate(temperatures):
        codes = get_icd_codes(medical_note, temperature=temp)
        all_codes.extend(codes)
        print(f"Sample {i+1}: T={temp:.2f}, Codes={len(codes)}")
    
    code_counts = Counter(all_codes)
    
    # Code consistency
    code_consistency = {}
    for code, count in code_counts.items():
        consistency = count / n_samples
        code_consistency[code] = consistency
    
    # Reliable codes (appear in >50%)
    reliable_codes = [code for code, consistency in code_consistency.items() 
                     if consistency >= 0.5]
    
    # Overall confidence (average consistency of all codes)
    confidence_score = np.mean(list(code_consistency.values())) if code_consistency else 0
    
    # Confidence level
    if confidence_score >= 0.7:
        confidence_level = "HIGH"
    elif confidence_score >= 0.4:
        confidence_level = "MEDIUM"
    else:
        confidence_level = "LOW"
    
    return {
        'reliable_codes': reliable_codes,
        'confidence_score': confidence_score,
        'confidence_level': confidence_level,
        'code_consistency': code_consistency,
        'all_codes': all_codes,
        'n_samples': n_samples
    }


def plot_uncertainty(results, save_path=None):
    """
    Simple visualization of uncertainty results.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    if results['code_consistency']:
        codes = list(results['code_consistency'].keys())
        consistencies = list(results['code_consistency'].values())
        
        colors = ['green' if c >= 0.7 else 'orange' if c >= 0.4 else 'red' for c in consistencies]
        ax1.bar(codes, consistencies, color=colors, alpha=0.7)
        ax1.set_title('Code Consistency')
        ax1.set_ylabel('Consistency Score')
        ax1.set_xlabel('ICD Codes')
        ax1.tick_params(axis='x', rotation=45)
        ax1.axhline(y=0.5, color='black', linestyle='--', alpha=0.5)
        ax1.grid(True, alpha=0.3)
    
    metrics = {
        'Confidence': results['confidence_score'],
        'Reliable Codes': len(results['reliable_codes']) / max(len(results['code_consistency']), 1),
        'Code Diversity': len(results['code_consistency']) / 10  # Normalized
    }
    
    ax2.bar(metrics.keys(), metrics.values(), color=['blue', 'green', 'purple'], alpha=0.7)
    ax2.set_title('Uncertainty Summary')
    ax2.set_ylabel('Score')
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def quick_uncertainty(medical_note, n_samples=3):
    """
    Uncertainty check
    """
    results = monte_carlo_uncertainty(medical_note, n_samples=n_samples)
    return results['reliable_codes'], results['confidence_level']


if __name__ == "__main__":
    sample_note = """
    Patient presents with chest pain and shortness of breath. 
    EKG shows ST elevation. Cardiac enzymes elevated. 
    Clinical impression: Acute myocardial infarction.
    """

    results = monte_carlo_uncertainty(sample_note, n_samples=5)
    
    print(f"\nResults:")
    print(f"Reliable codes: {results['reliable_codes']}")
    print(f"Confidence: {results['confidence_level']} ({results['confidence_score']:.2f})")
    
    plot_uncertainty(results, save_path='uncertainty.png')
    
    reliable, confidence = quick_uncertainty(sample_note)
    print(f"\nQuick check: {reliable} ({confidence})")