import json
import os
import sys
import time
from generator import SmartNotesGenerator

# Ensure standard output uses UTF-8 if available
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TEST_PARAGRAPHS = [
    {
        "id": "Paragraph 1",
        "domain": "Artificial Intelligence in Healthcare",
        "text": (
            "Artificial intelligence is rapidly revolutionizing the healthcare industry by enhancing diagnostic precision, "
            "optimizing patient treatment plans, and streamlining administrative workflows. Machine learning algorithms can analyze "
            "vast amounts of medical imaging data, such as MRI scans and X-rays, to detect anomalies like tumors much faster and "
            "often more accurately than human radiologists. Furthermore, AI-powered predictive analytics enable hospitals to forecast "
            "patient admission rates, allocate critical resources efficiently, and customize personalized therapy regimens based on a "
            "patient's unique genetic profile. However, despite these overwhelming technological benefits, challenges regarding data privacy, "
            "algorythmic bias, and the necessity of human oversight remain crucial areas that require rigorous ethical standards and regulations."
        )
    },
    {
        "id": "Paragraph 2",
        "domain": "Renewable Energy and Global Climate Action",
        "text": (
            "The global transition toward renewable energy sources has become one of the most critical imperatives of the 21st century. "
            "As fossil fuels continue to contribute significantly to greenhouse gas emissions and global warming, nations worldwide are "
            "investing heavily in solar, wind, and hydroelectric power infrastructure. Recent technological breakthroughs have dramatically reduced "
            "the manufacturing costs of photovoltaic solar panels and high-capacity battery storage systems, making clean energy economically competitive "
            "with traditional power grids. Nevertheless, integrating intermittent renewable sources into legacy energy infrastructure requires massive "
            "grid modernization, grid-scale storage solutions, and proactive international policy collaboration to achieve zero-carbon targets."
        )
    },
    {
        "id": "Paragraph 3",
        "domain": "The Psychological Impact of Social Media",
        "text": (
            "Social media platforms have fundamentally altered contemporary human communication, social interaction, and information sharing. "
            "While these digital networks foster unprecedented global connectivity, allow instant knowledge access, and empower community building, "
            "extensive psychological studies highlight emerging concerns regarding mental health. Continuous exposure to curated digital lifestyles "
            "frequently leads to social comparison, anxiety, reduced self-esteem, and sleep disruption among adolescents and young adults. "
            "To mitigate these negative psychological side effects, experts strongly recommend implementing digital wellness practices, setting "
            "daily screen time limits, and cultivating mindful online engagement habits."
        )
    }
]

def run_tests():
    print("=" * 80)
    print("      AUTOMATED TEST SUITE FOR SMART STUDY NOTES GENERATOR      ")
    print("=" * 80)
    
    start_time = time.time()
    generator = SmartNotesGenerator(model_name="sshleifer/distilbart-cnn-12-6")
    load_duration = time.time() - start_time
    print(f"Model initialization time: {load_duration:.2f} seconds\n")

    results_data = []

    for test_item in TEST_PARAGRAPHS:
        p_id = test_item["id"]
        domain = test_item["domain"]
        text = test_item["text"]

        sep = "=" * 30
        print(f"\n{sep} {p_id}: {domain} {sep}")
        print(f"Original Text ({len(text.split())} words):\n{text}\n")
        
        t0 = time.time()
        output = generator.generate_notes(text)
        gen_time = time.time() - t0
        
        metrics = output["metrics"]
        print(f"--- Summary ({metrics['summary_word_count']} words, reduced by {metrics['reduction_percentage']}%) ---")
        print(output["summary"])
        print("\n--- Key Points ---")
        for kp in output["key_points"]:
            print(f"  * {kp}")
        print(f"\n[Generation Time: {gen_time:.2f}s]")

        results_data.append({
            "id": p_id,
            "domain": domain,
            "original_text": text,
            "summary": output["summary"],
            "key_points": output["key_points"],
            "original_word_count": metrics["original_word_count"],
            "summary_word_count": metrics["summary_word_count"],
            "reduction_percentage": metrics["reduction_percentage"],
            "generation_time_sec": round(gen_time, 2)
        })

    # Save output to JSON for verification
    json_path = os.path.join(os.path.dirname(__file__), "test_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)

    print("\n" + "=" * 80)
    print(f"[SUCCESS] Test run completed! Results saved to {json_path}")
    print("=" * 80)
    return results_data

if __name__ == "__main__":
    run_tests()
