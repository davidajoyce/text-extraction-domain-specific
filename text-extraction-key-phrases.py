key = ""
endpoint = ""

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def key_phrase_extraction_example(client):

    try:
        documents = ["(Bloomberg) -- Asian shares followed their US peers higher Friday ahead of a" + 
        "key jobs report as traders weighed the outlook for inflation and growth. Most Read from Bloomberg." + 
        " One-Third of Americans Making $250,000 Live Paycheck-to-Paycheck, Survey Finds Elon Musk’s Ultimatum to Tesla Execs:" +
        "Return to the Office or Get Out Jamie Dimon Says JPMorgan Is Bracing Itself for Economic Hurricane" + 
        "Stks Decline as Data Show a Still-Hot Economy: Markets Wrap" + 
        "Fed Starts Experiment of Letting $8.9 Trillion Portfolio Shrink" + 
        "Stocks rose in Japan, Korea and Australia while US futures fluctuated. On Thursday, the S&P 500 rose 1.8%, led by gains in consumer discretionary shares, while the tech-heavy Nasdaq 100 added 2.8%." + 
        "Markets are shut in Hong Kong and China, where officials have vowed to carry out a slew of government policies to stimulate the economy. The offshore yuan rose amid thin trading in Asia." + 
        "A Bloomberg gauge of the dollar steadied after overnight losses, while the yen held near the psychologically important 130 level against the greenback. Benchmark Treasury yields edged up to 2.92%." + 
        "Investors remain on edge as some fear the pace of US monetary tightening could throw the world’s largest economy into a recession. Friday’s May labor report is likely to show the smallest gain in jobs since April 2021 alongside a down shift in average hourly earnings growth, Bloomberg Economics said." + 
        "We really do just need a lot more data, not one data point, not just the jobs data,” Carol Schleif, BMO Family Office LLC deputy chief investment officer, said on Bloomberg TV. “The potential range of outcomes is wider than it has been. We do think that you are going to see a lot of volatility through the summer." + 
        "Federal Reserve Vice Chair Lael Brainard said it was hard to see a case for a September pause in rate hikes and that increases of 50 basis points in June and July seemed reasonable." + 
        "We believe a slight lean toward defensive sectors and away from the growth-oriented areas of this market still make sense,” said Scott Brown, technical market strategist at LPL Financial. “Outside of this recent rally, very little about this market has changed from a technical standpoint and that makes us wary of calling the all-clear."
        ]
        

        response = client.extract_key_phrases(documents = documents)[0]

        count = 1
        if not response.is_error:
            print("\tKey Phrases:")
            for phrase in response.key_phrases:
                print("\t\t", phrase + " " + str(count))
                count = count + 1
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))
        
key_phrase_extraction_example(client)