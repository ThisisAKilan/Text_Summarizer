import os
import re
from typing import Dict, List, Any

class SmartNotesGenerator:
    """
    Smart Study Notes Generator using Hugging Face Transformers pre-trained T5/BART Seq2Seq models.
    """
    def __init__(self, model_name: str = "t5-small"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        """Initializes the Hugging Face AutoModelForSeq2SeqLM & AutoTokenizer."""
        try:
            import warnings
            warnings.filterwarnings("ignore")
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            hf_token = os.environ.get("HF_TOKEN")
            kwargs = {}
            if hf_token:
                kwargs["token"] = hf_token

            print(f"Loading pre-trained model '{self.model_name}'...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, **kwargs)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, **kwargs)
            print("Model & Tokenizer loaded successfully!")
        except Exception as e:
            print(f"Warning: Could not load model '{self.model_name}': {e}")
            self.tokenizer = None
            self.model = None

    def calculate_metrics(self, original_text: str, summary_text: str) -> Dict[str, Any]:
        """
        Calculates word counts and the percentage reduction.
        """
        orig_words = len(re.findall(r'\b\w+\b', original_text))
        summ_words = len(re.findall(r'\b\w+\b', summary_text))
        
        if orig_words > 0:
            reduction_pct = ((orig_words - summ_words) / orig_words) * 100
            reduction_pct = max(0.0, reduction_pct)
        else:
            reduction_pct = 0.0

        return {
            "original_word_count": orig_words,
            "summary_word_count": summ_words,
            "reduction_percentage": round(reduction_pct, 2)
        }

    def generate_notes(self, paragraph: str, min_length: int = 20, max_length: int = 65) -> Dict[str, Any]:
        """
        Generates summary, key points, and word count metrics for a paragraph.
        """
        paragraph = paragraph.strip()
        if not paragraph:
            return {
                "error": "Input text paragraph is empty.",
                "original_text": "",
                "summary": "",
                "key_points": [],
                "metrics": {"original_word_count": 0, "summary_word_count": 0, "reduction_percentage": 0.0}
            }

        orig_word_count = len(re.findall(r'\b\w+\b', paragraph))
        
        # Calculate dynamic max/min tokens for abstractive summarization
        adj_max_len = max(45, min(max_length + 30, int(orig_word_count * 0.8)))
        adj_min_len = max(15, min(min_length, int(adj_max_len * 0.4)))

        if self.model and self.tokenizer:
            try:
                # Add T5 prompt prefix if using T5 model family
                prompt_text = paragraph
                if "t5" in self.model_name.lower():
                    prompt_text = "summarize: " + paragraph

                inputs = self.tokenizer(
                    prompt_text, 
                    return_tensors="pt", 
                    max_length=512, 
                    truncation=True
                )
                summary_ids = self.model.generate(
                    inputs["input_ids"],
                    max_length=adj_max_len,
                    min_length=adj_min_len,
                    num_beams=4,
                    no_repeat_ngram_size=2,
                    early_stopping=True
                )
                summary_text = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()
            except Exception as e:
                print(f"Generative inference error: {e}")
                summary_text = self._fallback_summary(paragraph)
        else:
            summary_text = self._fallback_summary(paragraph)

        # Post-process punctuation spacing (e.g. remove spaces before periods/commas)
        summary_text = re.sub(r'\s+([,.!?])', r'\1', summary_text)
        
        # Ensure summary ends cleanly at sentence boundary if truncated
        if not summary_text.endswith(('.', '!', '?')):
            last_period = max(summary_text.rfind('.'), summary_text.rfind('!'), summary_text.rfind('?'))
            if last_period > len(summary_text) * 0.5:
                summary_text = summary_text[:last_period + 1]
            else:
                summary_text = summary_text + "."

        metrics = self.calculate_metrics(paragraph, summary_text)
        key_points = self._extract_key_points(paragraph, summary_text)

        return {
            "original_text": paragraph,
            "summary": summary_text,
            "key_points": key_points,
            "metrics": metrics
        }

    def _fallback_summary(self, paragraph: str) -> str:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', paragraph) if s.strip()]
        if not sentences:
            return paragraph
        return " ".join(sentences[:max(1, len(sentences)//2)])

    def _extract_key_points(self, paragraph: str, summary: str) -> List[str]:
        """
        Extracts key study bullet points combining neural summary insights and main paragraph facts.
        """
        raw_sentences = re.split(r'(?<=[.!?])\s+', summary + ". " + paragraph)
        sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 15]
        seen = set()
        points = []
        for s in sentences:
            clean_s = re.sub(r'\s+([,.!?])', r'\1', s).rstrip('.').strip()
            key_repr = clean_s.lower()
            if key_repr not in seen:
                seen.add(key_repr)
                points.append(clean_s)
            if len(points) >= 4:
                break
        return points
