from transformers import pipeline,BartForConditionalGeneration, BartTokenizer, AutoTokenizer, AutoModelForSequenceClassification
from typing import List
import textwrap
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def summarize(text: str, max_length: int = 95, min_length: int = 50, do_sample: bool = False) -> str:
#     try:
#         chunk_size = 900  # Adjust this value as needed
#         chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
#         summaries: List[str] = []

#         for chunk in chunks:
#             summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=do_sample)[0]['summary_text']
#             summaries.append(summary)

#         return ' '.join(summaries)
#     except Exception as e:
#         return str(e)

def text_summarizer(text):
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs,
        max_length=250,
        min_length=80,
        length_penalty=1.2,
        num_beams=8,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    formatted_summary = "\n".join(textwrap.wrap(summary, width=80))
    return formatted_summary

def summarize(text: str, max_length: int = 100, min_length: int = 50, do_sample: bool = False) -> str:
    try:
        chunk_size = 900  # Adjust this value as needed
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        summaries: List[str] = []

        for chunk in chunks:
            summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=do_sample)[0]['summary_text']
            summaries.append(summary)

        # Paraphrase and merge summaries
        merged_summary = ' '.join(summaries)
        paraphrased_summary = summarizer(merged_summary, max_length=max_length, min_length=min_length, do_sample=do_sample)[0]['summary_text']

        return paraphrased_summary
    except Exception as e:
        return str(e)

from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM, AutoModelForTokenClassification
import torch
def financial_summarizer(text):
    # Use bert-base-NER for key information extraction
    ner_model_name = "dslim/bert-base-NER"
    ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
    ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

    # Tokenize the input text
    ner_inputs = ner_tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    
    # Predict named entities
    with torch.no_grad():
        ner_outputs = ner_model(**ner_inputs)
        ner_predictions = torch.argmax(ner_outputs.logits, dim=2)

    # Extract key information (named entities)
    key_info = []
    for i, label in enumerate(ner_predictions[0]):
        if label != 0:  # Ignore 'O' labels (non-named entities)
            key_info.append(ner_tokenizer.decode(ner_inputs["input_ids"][0][i]))

    key_info = " ".join(key_info)

    print(key_info)
    # Use GPT-2 for summary generation
    gpt2_model_name = "gpt2"
    gpt2_tokenizer = AutoTokenizer.from_pretrained(gpt2_model_name)
    gpt2_model = AutoModelForCausalLM.from_pretrained(gpt2_model_name)

    gpt2_inputs = gpt2_tokenizer.encode("summarize: " + key_info, return_tensors="pt", max_length=1024, truncation=True)
    
    # Create attention mask
    attention_mask = torch.ones_like(gpt2_inputs)
    
    # Set pad_token_id to eos_token_id if pad_token_id is not defined
    pad_token_id = gpt2_tokenizer.eos_token_id if gpt2_tokenizer.pad_token_id is None else gpt2_tokenizer.pad_token_id

    summary_ids = gpt2_model.generate(
        gpt2_inputs,
        max_length=250,
        min_length=80,
        length_penalty=1.2,
        num_beams=8,
        early_stopping=True,
        attention_mask=attention_mask,
        pad_token_id=pad_token_id
    )

    summary = gpt2_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    formatted_summary = "\n".join(textwrap.wrap(summary, width=80))
    return formatted_summary
ARTICLE = """ New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
2010 marriage license application, according to court documents.
Prosecutors said the marriages were part of an immigration scam.
On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
"""

TEXT = """
What can you tell them about the degree of concern they should have. Well first of all consumers should have whatever degree of concern they have. 
We're not in the business of telling people how they should feel about the economy. It is true that the Michigan sentiment indicator is up 25 percent 
since November. We've seen increases interestingly among Democrats independents Republicans and that's been been good to see. And I think it's tracked 
some of the improvements that we saw in inflation especially the disinflation in the latter half of last year. Now look inflation is still down 60 percent 
from its peak. It was nice to hit the expectations number for the P.C. both headline and core this morning. And in terms of the GDP growth the 3 percent
year over year. It is true that there's some noisy sectors there. Inventories is another one along with net exports. But as long as real consumer spending
fueled by the tight job market and rising real wages continues to help support consumers in their in their spending and their incomes and their rising
disposable incomes even after inflation. I think that's a good sign for consumers and probably behind that improvement that we've seen over the longer 
term sentiment indices. Well take us under the hood for a minute here. Jared it's great to have you back from the North Lawn by the way. The markets had a
bit of a freak out yesterday and we saw some relief today. But the narrative yesterday was that we've plateaued that this this train's running too hot and
inflation is just going to keep on steaming ahead here. Forget interest rate cuts for the rest of the year. And that part may not have changed. But you made 
an interesting point here when you start looking at our trade imbalance net imports and exports and some of the other noise that that created the headline. 
I wonder how you frame the data from yesterday and where we really are here in the fight against inflation. I think it's very important to kind of look at as 
many kind of core or underlying trend indicators as you can. Obviously core inflation fulfills that role. That's why the Fed elevates it so much. But if you 
look at the domestic demand measure PDFP which you know is an acronym for all it means is real consumer spending and real business investment. Now together 
those are more than 80 percent of nominal GDP. But you can think of that as kind of a core GDP. It's actually a fact that that measure though combining those 
two real values predicts where GDP is going better than GDP itself. And that that was up 3.1 percent in the quarter. We have a blog on that by the way on the
C.A. blog this morning. So check it out. A lot of nice graphics on this point. So look I think underlying the economy is still as strong as ever. The job market
continues to put out great numbers. I don't know if you notice the initial claims that got a little bit buried on Thursday. I think it was two hundred and seven 
thousand. I mean that is a really solid job market number when it comes to inflation. I think the question there we should get into it if you want which is is is
the are the forces that helped with the disinflation in the second half of this year. Are they just on a break or are they gone. And obviously we've argued that 
they are that they're still there and that we expect inflation to continue a bumpy path down towards target. Well Mr. Chairman yeah we do want to talk more about
inflation with you because as you as you say there's this question as to whether or not progress is going to continue. And I wonder to what degree you assign 
progress on the fact that we do have tighter monetary policy right now that the Fed embarked. And I know you won't comment directly on that policy itself but 
that we have seen things tighten substantially in a very short period of time. And we did see inflation come down. We're no longer actively tightening. The Fed's
not talking about hiking rates further. So if that doesn't happen how confident are you that the rest of the way of the inflation progress will actually be made.
Well look there's an old kind of rule of thumb that says as as inflation comes down the real interest rate if you hold the Fed policy constant the real interest
rate does get tighter. And we've seen the real interest rate come up significantly over this period. So I think you can't just look at steady as she goes without
taking into account some of the moving variables when it comes to the housing market which is where of course Fed policy always bites first. I mean there is a really
remarkable kind of a gap between the effective mortgage rate which is the average of all the outstanding mortgages. It's in the free 3 to 4 percent range. 
And the mortgage rate you know that 7 percent if you go out and get a new mortgage. That's the lock in effect right there. That that spread. That's a really
important kind of overlook spread. And so I think Fed policy is very much again I won't talk about the granular policy but I think it's it's incorrect to conclude 
that it isn't having an effect or even much an effect on the economy. Now I understand the idea that this is this is another way of saying the neutral interest 
rate must be higher because you know we're posting some great numbers with a relatively high Fed's fund rate. That's a complicated and that's one of those conversations
that involves invisible variables. So that's that's always tricky to talk about. But I do think there's definitely some bite from interest rates. Jared there's reporting
today that some of Donald Trump's allies are suggesting to him that he restructure the Federal Reserve. And in fact if we're elected again I would make the commander in 
chief would make the president actually involved in setting interest rate decisions and Fed policy subject essentially to White House approval. You tend to bend yourself 
into a pretzel to not comment on the Fed which I realize it's kind of the opposite world you're living in right now. But I wonder I just wonder is that is that actually 
something that the president whether it's yours or any other. OK. Watch me try to thread a needle here. So look you've just you've just raised two issues that I can't talk 
about. One is Federal Reserve monetary policy. Other is politics. But I'm not going to stay silent on this because I think it's so important. Let me say the following. 
I am a I am a his. I am a very active reader of the history of monetary policy. And I can spend a long time talking to you about economies that have been brought to their 
knees when the independence of the central bank has been compromised. That's one of the main reasons why this president takes the stance that he does and follows it 
assiduously. And it's one it's a history that people should think about when evaluating the question you just asked me. Let me just leave that there.

"""

TEXT2 = """
Nancy Pelosi, D-Calif., has multiple major accomplishments on her resume. She's been a U.S. Representative for nearly 37 years. She's the first female Speaker of the House and the first woman to lead either chamber of Congress. Is she also a market-beating investor?

The former House Speaker nearly tripled the S&P 500's returns in 2023, giving her the ninth-best returns among members of Congress, according to options trading platform operator Unusual Whales. However, all of Pelosi's disclosures of trades listed her husband, Paul Pelosi, as the owner.

Pelosi's recent purchases
Over the last 12 months, Pelosi has purchased only two stocks. Both are also favorites of many other investors.

On June 15, 2023, the former Speaker's husband exercised 50 call options to buy 5,000 shares of Apple (NASDAQ: AAPL) for $80 per share. Apple's current share price is more than double this purchase price.

Mr. Pelosi has owned Apple stock for years. Other members of Congress or their families have also invested in the tech giant. Apple was second on the list of stocks lawmakers bought the most in 2023.

On the same day of the Apple transaction, Pelosi also exercised 50 call options to purchase 5,000 shares of Microsoft (NASDAQ: MSFT) for $180 per share. As with Apple, Microsoft's current share price is more than twice the strike price of those options.

More options
The initial purchases of the moneymaking call options for Apple and Microsoft were made in 2022. Paul Pelosi has been buying more call options on other stocks in recent months.

On Dec. 22, 2023, Mr. Pelosi bought 50 call options for Nvidia (NASDAQ: NVDA) with a strike price of $120 and an expiration date of Dec. 20. 2024. At the time, Nvidia's share price was around $488.

On Feb. 12, 2024, Pelosi purchased 50 call options for Palo Alto Networks (NASDAQ: PANW) with a strike price of $200 and an expiration date of Jan. 17, 2025. Palo Alto Networks' share price then hovered around $372.

A few days later on Feb. 21, 2024, the former Speaker's husband bought 20 more call options for Palo Alto Networks. Again, the strike price was $200 with an expiration date of Jan. 17, 2025. The stock had fallen significantly, though, to around $262.

Call options with a strike price lower than the current share price are known as "in-the-money" options. Buying in-the-money call options lowers investors' upfront costs and limits the risk of loss while allowing them to profit from upward moves for the underlying stock.
"""

# print(text_summarizer(TEXT))

# print(financial_summarizer(TEXT2))




from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import textwrap
import re


def preprocess_text(text):
    # Remove filler words and repetitions
    text = re.sub(r'\b(um|uh|you know)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)
    
    # Remove incomplete sentences
    sentences = re.findall(r'[^.!?]+[.!?]', text)
    text = ' '.join([sentence for sentence in sentences if len(sentence.split()) > 5])
    
    return text

def postprocess_summary(summary):
    # Remove repetitions and filler words
    summary = re.sub(r'\b(um|uh|you know)\b', '', summary, flags=re.IGNORECASE)
    summary = re.sub(r'\b(\w+)( \1\b)+', r'\1', summary)
    
    # Improve coherence and structure
    sentences = re.findall(r'[^.!?]+[.!?]', summary)
    sentences = [sentence.strip() for sentence in sentences]
    summary = ' '.join(sentences)
    
    return summary

# def financial_summarizer(text):
#     preprocessed_text = preprocess_text(text)
#     model_name = "facebook/bart-large-cnn"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#     inputs = tokenizer.encode("summarize: " + preprocessed_text, return_tensors="pt", max_length=1024, truncation=True)
#     input_length = len(inputs[0])

#     def adjust_summary_length(input_length):
#         base_max_length = 150
#         base_min_length = 75
#         length_factor = 0.3
#         max_length = min(base_max_length + int(input_length * length_factor), 1024)
#         min_length = min(base_min_length + int(input_length * length_factor * 0.5), max_length)
#         return max_length, min_length

#     max_length, min_length = adjust_summary_length(input_length)
#     summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, num_beams=6, length_penalty=1.5, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     postprocessed_summary = postprocess_summary(summary)
#     formatted_summary = "\n".join(textwrap.wrap(postprocessed_summary, width=80))
#     return formatted_summary

def adjust_summary_length(input_length):
    base_max_length = 100
    base_min_length = 50
    length_factor = 0.2
    max_length = min(base_max_length + int(input_length * length_factor), 1024)
    min_length = min(base_min_length + int(input_length * length_factor * 0.5), max_length)
    return max_length, min_length

from transformers import pipeline


# Load NER model
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

# Load topic modeling pipeline
# topic_model = pipeline('text-generation', model='facebook/bart-large-cnn')


def generate_query(text):
    # Perform Named Entity Recognition
    entities = ner_pipeline(text)

    # Extract entity names and types
    entity_names_types = []
    current_entity = ""
    for ent in entities:
        if ent['entity'].startswith('B-'):
            if current_entity:
                entity_names_types.append(current_entity)
            current_entity = (ent['word'], ent['entity'].split('-')[1])
        elif ent['entity'].startswith('I-'):
            current_entity = (current_entity[0] + ent['word'], current_entity[1])
    if current_entity:
        entity_names_types.append(current_entity)

    return entity_names_types

def financial_summarizer(text):
    preprocessed_text = preprocess_text(text)

    # Generate entities
    entity_names_types = generate_query(preprocessed_text)

    # Use query for summarization
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    query = f"Summarize the key points involving {', '.join([f'{name} ({entity_type})' for name, entity_type in entity_names_types])}."
    print("query", query)
    inputs = tokenizer.encode(query + ": " + preprocessed_text, return_tensors="pt", max_length=1024, truncation=True)
    input_length = len(inputs[0])

    max_length, min_length = adjust_summary_length(input_length)
    summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, num_beams=4, length_penalty=1.5, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    key_points = summary.split('. ')
    print("Generated key points: ", key_points)
    return key_points, entity_names_types

def financial_summarizer_sample_usage(text):
    res = summarizer(text, max_length=130, min_length=30, do_sample=False)
    summary = res[0]['summary_text']
    tokenizer2 = AutoTokenizer.from_pretrained("dslim/bert-base-NER", use_fast=True)
    model2 = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", aggregation_strategy='simple')
    ner_results = nlp(text)
    summary = summary.split('. ')
    print(ner_results)

    def filter_unwanted_names(item):
        name = item['word']
        return len(name) > 1 and '#' not in name

    unique_names = set()
    filtered_result = [{'name': entry['word'], 'type': entry['entity_group']} for entry in ner_results if filter_unwanted_names(entry) and entry['word'] not in unique_names and not unique_names.add(entry['word'])]
    
    return summary, filtered_result


#test = "This morning's GDP report showed the U.S. economy growing by 1.6 percent. That's well weaker than the 2.5 percent that was expected. But with consumer spending remaining strong, what does that mean for inflationary pressures and potential rate cuts? Joining us now to discuss, former Federal Reserve Board economist Claudia Somme. Claudia, great to have you here on the program with us. You know, maybe I'm just flabbergasted trying to figure out what this print means for the Fed and how it changes the tenor of their conversation at the next meeting, if at all. The Fed's going to look at data big picture, right? So one number, particularly thinking about, oh, it was a surprise on what the markets thought. That is not, you know, enough to really move their thinking. And in particular, and you mentioned this, consumer spending looks really good under the hood, business fixed investment. So set aside those inventories, the investment business making are really good considering interest rates are a lot higher. And so that's what we think of as kind of the underlying pace. The where do we think GDP is headed? Today we got hit by imports had a bigger drag. That's a very noisy series. Inventories were a little in the play. These are not things that should change our view on the economy. It's been strong. It continues. The underlying pace continues to be strong. That's not bad for the Fed. We had a strong pace last year. Inflation came down. Frankly, the Fed thinks it can lean on a strong economy a little bit, get it some time to get comfortable with inflation. Claudia, when you take a look at this number, when you take a look at the fact that maybe PCE is going to surprise here to the upside, if we do see any sort of elevated print here tomorrow before the bell from PCE, what does that signal just in terms of what the Fed is then likely to do? How far out could we potentially be pushing that first rate cut? As Ben said, and absolutely the Fed, Jay Powell, when he's been out talking towards the end of last year, there had been some real progress last year, but it was going to be a bumpy ride. Well, we got our bumpy ride in the first quarter and the progress really slowed. There has been progress. It's just been really slow. The target index for them, the personal consumption expenditure index has looked a little better, but still it's slow. They want to build confidence. Confidence takes time. So they are pushing out, I think, where the Fed probably will start their cutting. And yet we are set up for them to cut this year and probably more than once. But you know what? They're going to be driven by the data and there's a lot of data we don't have yet. Yeah, and Claudia, that's a good point. And I want to bring up the move that we're seeing, the action that we're seeing in the yield market today, because that bump higher in yield is obviously tied to that pricing data that we're getting in this GDP print. But you say that it is likely that the Fed is still going to cut before the end of the year. What do you think then is going to, what does the Fed need to see in order to be confident to make that first cut? And when we talk about the improvement, I would guess that you're expecting then to see on the inflation front. Where do you see inflation then trending between now and year end? There is a very clear path. Given what we know now, there is a clear path for inflation to slow. And in all likelihood, we're going to see a pickup in that disinflation, maybe not as much as last year, but we're going to get moving. The Fed's target price index is within a percentage point, less than a percentage point of the 2% target. And they have told us over and over again, and it is good practice, they will not wait until 2% to cut. So we've got to see more progress to 2%. Things can't stall out. And goodness, they cannot inflation pick up. Again, the Fed is going to be driven by what it sees happening in the world. And yet we know things like the shelter prices, the owner's equivalent rent. We got more data on the rent people, like the contracts they're signing now have really come down. So it's in train. We see it, but we have gotten surprised. And there could be other surprises down the road. So I understand why markets are having a hard time getting a read on the data. And yet we should remember that the Fed doesn't wake up, look at one release and go, wow, we have to totally change our thinking. What do you think the data, especially on that housing front, needs to continue to trend towards in order for the Fed to feel confident with its cut decision when they do make that? The Fed is looking for things back to normal, which doesn't mean it has to look exactly like before the pandemic, say in terms of inflation. But if you look at the pieces of the, quote unquote, excess inflation, so like what pieces of spending are running above the inflation before the pandemic? The leader is the shelter, particularly the owner's equivalent rent. We have every reason to believe we're pointed in the right direction of that slowing. Do we know how much or how fast? No. I mean, it's coming much slower than we had expected. The other piece, I mean, there are some other pieces of services and some of it's pretty eclectic and echoes of COVID. I mean, in the Consumer Price Index, motor vehicle insurance is another big excess. That isn't as much in the PCE, but it just shows we've got we have far fewer enemies in the fight on inflation than we did in 2022. And yet they are still here. And some of them are going to be tough. Claudia Assam, we really appreciate your insight, especially on a day like today. Thanks so much for hopping on early with us here on Yahoo Finance. Claudia Assam, Assam Consulting founder. Thank you."
# print(financial_summarizer(test))



# t = """

# Equities in Australia and South Korea rose at the open, while the Japanese stock market is shut for a holiday. US contracts nudged higher after the S&P 500 rose 1% on Friday. Yen traders remain alert to efforts to support the currency that’s at its weakest in more than three decades. Australian bond yields fell, following US Treasuries on Friday. Chinese shares will be closely watched after industrial companies’ profits slumped in March as exports flagged and deflationary pressures persisted. The weakness in the latest data “casts doubts on whether the economic recovery seen early this year can be sustained,” Commerzbank strategists including Charlie Lay wrote in a note to clients. “It is important now that the government will follow through with their fiscal stimulus plan outlined in the National People’s Congress annual meeting back in March.” Asian technology stocks may move in early trading after earnings from Microsoft Corp. and Google’s parent Alphabet Inc. last week sent a clear message that spending on artificial intelligence and cloud computing is paying off. The rally in tech shares has helped trim the drop in global stocks this month to 2.7%, the first monthly loss since October, amid concerns over lingering inflation pressures and conflict in the Middle East. While the correction could be over, “there is a significant risk that it’s just a bounce from oversold conditions,” said Shane Oliver, chief economist and head of investment strategy at AMP Ltd. Still, any further selloff is unlikely to be deep and stocks will see more gains “as disinflation resumes, central banks ultimately cut interest rates and recession is avoided or proves mild,” he wrote in a note to clients. Traders will also be focusing on the Fed’s policy meeting on Wednesday after the central bank’s preferred measure of inflation rose at a brisk pace in March, though roughly in line with estimates. With officials likely to hold rates steady at a more than two-decade high, much of the focus will be on any pivot in the tone of the post-meeting statement and Chair Jerome Powell’s press conference. “With all measures of US consumer prices showing a steep acceleration over the past three to four months, the FOMC is bound to row back hard from its earlier predictions of meaningful policy easing this year,” Societe Generale economists including Klaus Baader wrote in a note to clients. “That said, markets have already scaled back pricing of rate cuts drastically, so unless Chair Powell plays up the possibility of rate hikes, the market damage is likely to be modest.” A gauge of US Treasury returns has slumped 2.3% this month, set for the biggest monthly drop since February last year, as hawkish Fedspeak and strong economic data pushed back rate-cut bets. Swaps traders now see only one Fed reduction for all of 2024, well below the roughly six quarter-point cuts they expected at the start of 2024.
# """

#print(financial_summarizer_sample_usage("Elon Musk is doing great. Coca-Cola is doing bad. Tesla price is up."))
