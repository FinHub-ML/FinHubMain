import time
from bart.bart import financial_summarizer, financial_summarizer_sample_usage
import csv
import random
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments
import torch
model_path = r"bert\model"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
labels = {0: 'Bearish', 1: 'Bullish', 2: 'Neutral'}
start_time = time.time()


def tokenizer_function(input_text):
    return tokenizer(input_text, max_length=128, padding="max_length", truncation=True)


# input news from local file 
# ------- structure: a csv of title, url, content
def read_news_from_file(file_path):
    news_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            title, url, content = row[0], row[1], row[2]
            print("[DEBUG] HERE ARE THE TITLE URL CONTENT IN THE BACKEND ",title, url)
            news_list.append({'title': title, 'url': url, 'content': content})
    return news_list


## bert -> output sentiment analysis 
def bert_get_sentiment(input_text):
    input_token = tokenizer_function(input_text)
    input_ids = torch.tensor(input_token['input_ids']).unsqueeze(0)
    attention_mask = torch.tensor(input_token['attention_mask']).unsqueeze(0)
    model.eval()
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=1).item()
    return predicted_label


def financial_summarizer_placeholder(text):
    return ['This is a placeholder summary'], ['China', 'BYD', 'EV']

news_file_path = 'news.csv'
news_list = read_news_from_file(news_file_path)





def get_processed_news_list():
    
    categories = dict() # categories = { 'China': 10, 'BYD': 5, 'EV': 3, ...}

    processed_news_list = []

    #news_list = [{'title': 'title1', 'url': 'url1', 'content': 'content1'}, {'title': 'title2', 'url': 'url2', 'content': 'content2'}]
    for news in news_list:
        
        ## bart summarize -> output summary and entities
        # summarized_text, entities = financial_summarizer_placeholder(news['content'])
        summarized_text, entities = financial_summarizer_sample_usage(news['content'][:3000])

        ## entity add to category 
        #for ent in entities:
        #    categories[ent] =  1 + categories.get(ent, 0) 

        
        sentiment_list = []
        ## bert sentiment analysis
        sentences = summarized_text
        for sentence in sentences:
            sentiment_list.append(bert_get_sentiment(sentence))
        
        processed_news_list.append({'title': news['title'], 'url': news['url'], 'category': entities, 'sentences': sentences, 'sentiment_list': sentiment_list })
        
    # return a list containing the count of each sentiment category
    def get_market_stats(processed_news_list):
        total_sent = [0, 0, 0]
        # tobe initialized
        
        for i in range(len(processed_news_list)):
            sent = processed_news_list[i]['sentiment']
            for j in range(len(sent)):
                label = sent[j]
                total_sent[label] += 1
        return total_sent
    serializable_news_list = [
        {
            'title': news['title'],
            'url': news['url'],
            'category': news['category'],
            'sentences': news['sentences'],
            'sentiment_list': news['sentiment_list']
        }
        for news in processed_news_list
    ]

    return serializable_news_list

### category implementation: DB/ dict? 
#### dict = { URL: {'title': 'Sample News Title', 'category':['China', 'BYD', 'EV'], 'summary' : ['sentence1', 'sentence2'], 'sentiment': [1,0]}, ... }

# print(get_processed_news_list())



#### Front end plan: 

# 1. Display news list

# 2. for each news - display summary, sentiment of each sentence, category, link to original news, sentiment distribution

# 3. for each category - display news list, sentiment distribution, summary of news