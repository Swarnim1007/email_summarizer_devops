from transformers import BartForConditionalGeneration, BartTokenizer

class EmailSummarizer:
    def __init__(self):
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

    def summarize_email(self, email_content):
        inputs = self.tokenizer([email_content], max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = self.model.generate(inputs['input_ids'])
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
