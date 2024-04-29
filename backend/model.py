from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments
import torch
model_path = r"bert\model"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


def tokenizer_function(input_text):
    return tokenizer(input_text, max_length=128, padding="max_length", truncation=True)


def sentiment(input_text):
    input_token = tokenizer_function(input_text)
    input_ids = torch.tensor(input_token['input_ids']).unsqueeze(0)
    attention_mask = torch.tensor(input_token['attention_mask']).unsqueeze(0)
    model.eval()
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=1).item()
    return predicted_label


if __name__ == "__main__":
    print(sentiment("Stock market crashed today."))
    print(sentiment("Stock market is good today."))
    print(sentiment("Stock market is ok today."))
    print(sentiment("Stock market is not bad today."))
    print(sentiment("Stock market is desperate today."))
    print(sentiment("Stock market is the same."))

