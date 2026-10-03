import sys
import os
import argparse
from generator import SmartNotesGenerator

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SAMPLE_PARAGRAPHS = {
    "1": {
        "topic": "Artificial Intelligence in Modern Healthcare",
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
    "2": {
        "topic": "Renewable Energy and Global Climate Action",
        "text": (
            "The global transition toward renewable energy sources has become one of the most critical imperatives of the 21st century. "
            "As fossil fuels continue to contribute significantly to greenhouse gas emissions and global warming, nations worldwide are "
            "investing heavily in solar, wind, and hydroelectric power infrastructure. Recent technological breakthroughs have dramatically reduced "
            "the manufacturing costs of photovoltaic solar panels and high-capacity battery storage systems, making clean energy economically competitive "
            "with traditional power grids. Nevertheless, integrating intermittent renewable sources into legacy energy infrastructure requires massive "
            "grid modernization, grid-scale storage solutions, and proactive international policy collaboration to achieve zero-carbon targets."
        )
    },
    "3": {
        "topic": "The Psychological Impact of Social Media",
        "text": (
            "Social media platforms have fundamentally altered contemporary human communication, social interaction, and information sharing. "
            "While these digital networks foster unprecedented global connectivity, allow instant knowledge access, and empower community building, "
            "extensive psychological studies highlight emerging concerns regarding mental health. Continuous exposure to curated digital lifestyles "
            "frequently leads to social comparison, anxiety, reduced self-esteem, and sleep disruption among adolescents and young adults. "
            "To mitigate these negative psychological side effects, experts strongly recommend implementing digital wellness practices, setting "
            "daily screen time limits, and cultivating mindful online engagement habits."
        )
    }
}

def print_banner():
    print("=" * 70)
    print("         SMART STUDY NOTES GENERATOR         ")
    print("   Powered by Generative AI (Hugging Face Transformers)   ")
    print("=" * 70)

def display_results(result: dict):
    print("\n" + "-" * 70)
    print("ORIGINAL PARAGRAPH:")
    print(result["original_text"])
    print("-" * 70)
    print("GENERATED SUMMARY:")
    print(result["summary"])
    print("-" * 70)
    print("KEY POINTS:")
    for idx, point in enumerate(result["key_points"], 1):
        print(f"  * {point}")
    print("-" * 70)
    print("WORD COUNT METRICS & TEXT REDUCTION:")
    metrics = result["metrics"]
    print(f"  - Original Word Count : {metrics['original_word_count']} words")
    print(f"  - Summary Word Count  : {metrics['summary_word_count']} words")
    print(f"  - Reduction Percentage: {metrics['reduction_percentage']}%")
    print("=" * 70 + "\n")

def main():
    print_banner()
    
    print("Initializing Generative AI Model Pipeline...")
    generator = SmartNotesGenerator(model_name="sshleifer/distilbart-cnn-12-6")

    while True:
        print("\nChoose an option:")
        print("  [1] Enter your own paragraph")
        print("  [2] Select Sample 1: Artificial Intelligence in Healthcare")
        print("  [3] Select Sample 2: Renewable Energy and Climate Action")
        print("  [4] Select Sample 3: Psychological Impact of Social Media")
        print("  [5] Run All Samples & Compare Results")
        print("  [6] Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            print("\nEnter or paste your paragraph below (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if not line and lines:
                    break
                if line:
                    lines.append(line)
            paragraph = " ".join(lines).strip()
            
            if paragraph:
                print("\nGenerating study notes...")
                res = generator.generate_notes(paragraph)
                display_results(res)
            else:
                print("No text entered. Returning to menu.")

        elif choice in ["2", "3", "4"]:
            sample_key = str(int(choice) - 1)
            sample = SAMPLE_PARAGRAPHS[sample_key]
            print(f"\nProcessing Sample: {sample['topic']}...")
            res = generator.generate_notes(sample["text"])
            display_results(res)

        elif choice == "5":
            print("\nProcessing all sample paragraphs...")
            for k, sample in SAMPLE_PARAGRAPHS.items():
                print(f"\n--- SAMPLE {k}: {sample['topic']} ---")
                res = generator.generate_notes(sample["text"])
                display_results(res)

        elif choice == "6":
            print("Exiting Smart Study Notes Generator. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
