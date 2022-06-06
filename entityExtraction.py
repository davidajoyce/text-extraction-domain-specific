
# based off kaggle notebook https://www.kaggle.com/code/sudosharma/quick-and-dirty-entity-extractions

import pandas as pd
import spacy
from spacy.displacy.render import EntityRenderer
from IPython.core.display import display, HTML

pd.set_option('display.max_rows', 10) # edit how jupyter will render our pandas dataframes
pd.options.mode.chained_assignment = None # prevent warning about working on a copy of a dataframe

#nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_lg')

#financeText = "Some basic Economics 101 supply-and-demand analysis can be helpful, in assessing the macroeconomic impact of COVID-19 Note that the second-round impact of a global epidemic will result in moderate to majorcontractions in demand. As supply-side disruptions close factories and places of work,consumers will cut back on their spending, shifting demand curves inward, reducing GDP, boosting unemployment and moderating price rises. Some of this lost demand will be temporary, and when the epidemic recedes, consumers will ‘catch up’ on their spending, such as on vacations. But some of the demand will be lost permanently, thus reducing long-run global economic growth."
financeTextNotTrimmed = "HOME\nMAIL\nNEWS\nFINANCE\nSPORT\nLIFESTYLE\nENTERTAINMENT\nWEATHER\nMORE...\nYahoo Finance\nSign in\nFinance\nWatchlists\nMy Portfolios\nMarkets\nMoney\nWork\nTechnology\nIndustries\nThe New Investors\nAll Markets Summit\nGive Feedback\n\u2026\nAdvertisement\nAustralia markets open in 1 hour 46 minutes\nALL ORDS\n7,472.40\n+71.60 (+0.97%)\n\u00a0\nAUD/USD\n0.7206\n-0.0062 (-0.85%)\n\u00a0\nASX 200\n7,238.80\n+62.90 (+0.88%)\n\u00a0\nOIL\n120.57\n+1.70 (+1.43%)\n\u00a0\nGOLD\n1,853.30\n+3.10 (+0.17%)\n\u00a0\nBTC-AUD\n41,630.62\n-142.61 (-0.34%)\n\u00a0\nCMC Crypto 200\n641.58\n-19.22 (-2.91%)\n\u00a0\n\ud83d\udce9 SIGN UP NOW:\nNews that makes you smarter and richer... For free.\n\nGet Fully Briefed with Yahoo Finance, delivered straight to your inbox.\n\nBloomberg\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n1/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n2/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n3/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n4/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n5/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n6/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n7/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\nCraig Stirling\nSun, 5 June 2022, 4:21 pm\u00b77-min read\n\n(Bloomberg) -- Sign up for the New Economy Daily newsletter, follow us @economics and subscribe to our podcast.\n\nMost Read from Bloomberg\n\n\u2018No Longer Sure Bets\u2019:"
#line = bytes(line, 'utf-8').decode('utf-8', 'ignore')
#original_string.encode("utf-8", "replace").decode()
financeText = financeTextNotTrimmed.encode("utf-8", "replace").decode()
data = [financeText.lower()]
#df = pd.DataFrame(df['Abstract'].apply(lower))
df = pd.DataFrame(data)
df.columns = ['text']
display(df)

def extract_named_ents(text):
    """Extract named entities, and beginning, middle and end idx using spaCy's out-of-the-box model. 
    
    Keyword arguments:
    text -- the actual text source from which to extract entities
    
    """
    return [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in nlp(text).ents]

def add_named_ents(df):
    """Create new column in data frame with named entity tuple extracted.
    
    Keyword arguments:
    df -- a dataframe object
    
    """
    df['named_ents'] = df['text'].apply(extract_named_ents)   

add_named_ents(df)
display(df)

def extract_nouns(text):
    """Extract a few types of nouns, and beginning, middle and end idx using spaCy's POS (part of speech) tagger. 
    
    Keyword arguments:
    text -- the actual text source from which to extract entities
    
    """
    keep_pos = ['PROPN', 'NOUN']
    return [(tok.text, tok.idx, tok.idx+len(tok.text), tok.pos_) for tok in nlp(text) if tok.pos_ in keep_pos]

def add_nouns(df):
    """Create new column in data frame with nouns extracted.
    
    Keyword arguments:
    df -- a dataframe object
    
    """
    df['nouns'] = df['text'].apply(extract_nouns)

add_nouns(df)
display(df)

def extract_named_nouns(row_series):
    """Combine nouns and non-numerical entities. 
    
    Keyword arguments:
    row_series -- a Pandas Series object
    
    """
    ents = set()
    idxs = set()
    # remove duplicates and merge two lists together
    for noun_tuple in row_series['nouns']:
        for named_ents_tuple in row_series['named_ents']:
            if noun_tuple[1] == named_ents_tuple[1]: 
                idxs.add(noun_tuple[1])
                ents.add(named_ents_tuple)
        if noun_tuple[1] not in idxs:
            ents.add(noun_tuple)
    
    return sorted(list(ents), key=lambda x: x[1])

def add_named_nouns(df):
    """Create new column in data frame with nouns and named ents.
    
    Keyword arguments:
    df -- a dataframe object
    
    """
    df['named_nouns'] = df.apply(extract_named_nouns, axis=1)

add_named_nouns(df)
display(df)

def extract_noun_phrases(text):
    """Combine noun phrases. 
    
    Keyword arguments:
    text -- the actual text source from which to extract entities
    
    """
    return [(chunk.text, chunk.start_char, chunk.end_char, chunk.label_) for chunk in nlp(text).noun_chunks]

def add_noun_phrases(df):
    """Create new column in data frame with noun phrases.
    
    Keyword arguments:
    df -- a dataframe object
    
    """
    df['noun_phrases'] = df['text'].apply(extract_noun_phrases)

add_noun_phrases(df)
display(df)

def extract_compounds(text):
    """Extract compound noun phrases with beginning and end idxs. 
    
    Keyword arguments:
    text -- the actual text source from which to extract entities
    
    """
    comp_idx = 0
    compound = []
    compound_nps = []
    tok_idx = 0
    for idx, tok in enumerate(nlp(text)):
        if tok.dep_ == 'compound':

            # capture hyphenated compounds
            children = ''.join([c.text for c in tok.children])
            if '-' in children:
                compound.append(''.join([children, tok.text]))
            else:
                compound.append(tok.text)

            # remember starting index of first child in compound or word
            try:
                tok_idx = [c for c in tok.children][0].idx
            except IndexError:
                if len(compound) == 1:
                    tok_idx = tok.idx
            comp_idx = tok.i

        # append the last word in a compound phrase
        if tok.i - comp_idx == 1:
            compound.append(tok.text)
            if len(compound) > 1: 
                compound = ' '.join(compound)
                compound_nps.append((compound, tok_idx, tok_idx+len(compound), 'COMPOUND'))

            # reset parameters
            tok_idx = 0 
            compound = []

    return compound_nps

def add_compounds(df):
    """Create new column in data frame with compound noun phrases.
    
    Keyword arguments:
    df -- a dataframe object
    
    """
    df['compounds'] = df['text'].apply(extract_compounds)

add_compounds(df)
display(df)

def extract_comp_nouns(row_series, cols=[]):
    """Combine compound noun phrases and entities. 
    
    Keyword arguments:
    row_series -- a Pandas Series object
    
    """
    return {noun_tuple[0] for col in cols for noun_tuple in row_series[col]}

def add_comp_nouns(df, cols=[]):
    """Create new column in data frame with merged entities.
    
    Keyword arguments:
    df -- a dataframe object
    cols -- a list of column names that need to be merged
    
    """
    df['comp_nouns'] = df.apply(extract_comp_nouns, axis=1, cols=cols)

cols = ['nouns', 'compounds']
add_comp_nouns(df, cols=cols)
display(df)

def drop_duplicate_np_splits(ents):
    """Drop any entities that are already captured by noun phrases. 
    
    Keyword arguments:
    ents -- a set of entities
    
    """
    drop_ents = set()
    for ent in ents:
        if len(ent.split(' ')) > 1:
            for e in ent.split(' '):
                if e in ents:
                    drop_ents.add(e)
    return ents - drop_ents

def drop_single_char_nps(ents):
    """Within an entity, drop single characters. 
    
    Keyword arguments:
    ents -- a set of entities
    
    """
    return {' '.join([e for e in ent.split(' ') if not len(e) == 1]) for ent in ents}

def drop_double_char(ents):
    """Drop any entities that are less than three characters. 
    
    Keyword arguments:
    ents -- a set of entities
    
    """
    drop_ents = {ent for ent in ents if len(ent) < 3}
    return ents - drop_ents

def keep_alpha(ents):
    """Keep only entities with alphabetical unicode characters, hyphens, and spaces. 
    
    Keyword arguments:
    ents -- a set of entities
    
    """
    keep_char = set('-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
    drop_ents = {ent for ent in ents if not set(ent).issubset(keep_char)}
    return ents - drop_ents

def add_clean_ents(df, funcs=[]):
    """Create new column in data frame with cleaned entities.
    
    Keyword arguments:
    df -- a dataframe object
    funcs -- a list of heuristic functions to be applied to entities
    
    """
    col = 'clean_ents'
    df[col] = df['comp_nouns']
    for f in funcs:
        df[col] = df[col].apply(f)


funcs = [drop_duplicate_np_splits, drop_double_char, keep_alpha, drop_single_char_nps]
add_clean_ents(df, funcs)
display(df)
#df['comp_nouns'][0] 
print(df['clean_ents'][0])


def findFinanceTerms(financeTermNotTrimmed):
    pd.set_option('display.max_rows', 10) 
    pd.options.mode.chained_assignment = None 
    financeText = financeTextNotTrimmed.encode("utf-8", "replace").decode()
    data = [financeText.lower()]
    #df = pd.DataFrame(df['Abstract'].apply(lower))
    df = pd.DataFrame(data)
    df.columns = ['text']
    add_named_ents(df)
    add_nouns(df)
    add_named_nouns(df)
    add_noun_phrases(df)
    add_compounds(df)
    cols = ['nouns', 'compounds']
    add_comp_nouns(df, cols=cols)
    funcs = [drop_duplicate_np_splits, drop_double_char, keep_alpha, drop_single_char_nps]
    add_clean_ents(df, funcs)
    return df['clean_ents'][0]

def main():
    financeTextNotTrimmed = "HOME\nMAIL\nNEWS\nFINANCE\nSPORT\nLIFESTYLE\nENTERTAINMENT\nWEATHER\nMORE...\nYahoo Finance\nSign in\nFinance\nWatchlists\nMy Portfolios\nMarkets\nMoney\nWork\nTechnology\nIndustries\nThe New Investors\nAll Markets Summit\nGive Feedback\n\u2026\nAdvertisement\nAustralia markets open in 1 hour 46 minutes\nALL ORDS\n7,472.40\n+71.60 (+0.97%)\n\u00a0\nAUD/USD\n0.7206\n-0.0062 (-0.85%)\n\u00a0\nASX 200\n7,238.80\n+62.90 (+0.88%)\n\u00a0\nOIL\n120.57\n+1.70 (+1.43%)\n\u00a0\nGOLD\n1,853.30\n+3.10 (+0.17%)\n\u00a0\nBTC-AUD\n41,630.62\n-142.61 (-0.34%)\n\u00a0\nCMC Crypto 200\n641.58\n-19.22 (-2.91%)\n\u00a0\n\ud83d\udce9 SIGN UP NOW:\nNews that makes you smarter and richer... For free.\n\nGet Fully Briefed with Yahoo Finance, delivered straight to your inbox.\n\nBloomberg\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n1/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n2/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n3/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n4/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n5/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n6/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\n7/7\nECB Is Ready to Tighten Just as Global Peers Speed Up: Eco Week\nCraig Stirling\nSun, 5 June 2022, 4:21 pm\u00b77-min read\n\n(Bloomberg) -- Sign up for the New Economy Daily newsletter, follow us @economics and subscribe to our podcast.\n\nMost Read from Bloomberg\n\n\u2018No Longer Sure Bets\u2019:"
    findFinanceTerms(financeTextNotTrimmed)

if __name__ == "__main__":
    main()