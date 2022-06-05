import pandas as pd
import spacy
from spacy.displacy.render import EntityRenderer
from IPython.core.display import display, HTML

def custom_render(doc, df, column, options={}, page=False, minify=False, idx=0):
    """Overload the spaCy built-in rendering to allow custom part-of-speech (POS) tags.
    
    Keyword arguments:
    doc -- a spaCy nlp doc object
    df -- a pandas dataframe object
    column -- the name of of a column of interest in the dataframe
    options -- various options to feed into the spaCy renderer, including colors
    page -- rendering markup as full HTML page (default False)
    minify -- for compact HTML (default False)
    idx -- index for specific query or doc in dataframe (default 0)
    
    """
    renderer, converter = EntityRenderer, parse_custom_ents
    renderer = renderer(options=options)
    parsed = [converter(doc, df=df, idx=idx, column=column)]
    html = renderer.render(parsed, page=page, minify=minify).strip()  
    return display(HTML(html))

def parse_custom_ents(doc, df, idx, column):
    """Parse custom entity types that aren't in the original spaCy module.
    
    Keyword arguments:
    doc -- a spaCy nlp doc object
    df -- a pandas dataframe object
    idx -- index for specific query or doc in dataframe
    column -- the name of of a column of interest in the dataframe
    
    """
    if column in df.columns:
        entities = df[column][idx]
        ents = [{'start': ent[1], 'end': ent[2], 'label': ent[3]} 
                for ent in entities]
    else:
        ents = [{'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_}
            for ent in doc.ents]
    return {'text': doc.text, 'ents': ents, 'title': None}

def render_entities(idx, df, options={}, column='named_ents'):
    """A wrapper function to get text from a dataframe and render it visually in jupyter notebooks
    
    Keyword arguments:
    idx -- index for specific query or doc in dataframe (default 0)
    df -- a pandas dataframe object
    options -- various options to feed into the spaCy renderer, including colors
    column -- the name of of a column of interest in the dataframe (default 'named_ents')
    
    """
    text = df['text'][idx]
    custom_render(nlp(text), df=df, column=column, options=options, idx=idx)


# colors for additional part of speech tags we want to visualize
options = {
    'colors': {'COMPOUND': '#FE6BFE', 'PROPN': '#18CFE6', 'NOUN': '#18CFE6', 'NP': '#1EECA6', 'ENTITY': '#FF8800'}
}

pd.set_option('display.max_rows', 10) # edit how jupyter will render our pandas dataframes
pd.options.mode.chained_assignment = None # prevent warning about working on a copy of a dataframe

#nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_lg')

financeText = "Some basic Economics 101 supply-and-demand analysis can be helpful, in assessing the macroeconomic impact of COVID-19 Note that the second-round impact of a global epidemic will result in moderate to majorcontractions in demand. As supply-side disruptions close factories and places of work,consumers will cut back on their spending, shifting demand curves inward, reducing GDP, boosting unemployment and moderating price rises. Some of this lost demand will be temporary, and when the epidemic recedes, consumers will ‘catch up’ on their spending, such as on vacations. But some of the demand will be lost permanently, thus reducing long-run global economic growth."
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

column = 'named_ents'
# changed from 9 to 0
render_entities(0, df, options=options, column=column) # take a look at one of the abstracts

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

column = 'nouns'
render_entities(0, df, options=options, column=column)

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

column = 'named_nouns'
# changed from 1 to 0
render_entities(0, df, options=options, column=column)


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

def visualize_noun_phrases(text):
    """Create a temporary dataframe to extract and visualize noun phrases. 
    
    Keyword arguments:
    text -- the actual text source from which to extract entities
    
    """
    df = pd.DataFrame([text]) 
    df.columns = ['text']
    add_noun_phrases(df)
    column = 'noun_phrases'
    render_entities(0, df, options=options, column=column)

add_noun_phrases(df)
display(df)

column = 'noun_phrases'
render_entities(0, df, options=options, column=column)

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

column = 'compounds'
render_entities(0, df, options=options, column=column)

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

# take a look at all the nouns again
column = 'named_nouns'
render_entities(0, df, options=options, column=column)

# take a look at all the compound noun phrases again
column = 'compounds'
render_entities(0, df, options=options, column=column)

# take a look at combined entities
df['comp_nouns'][0] 

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

def visualize_entities(df, idx=0):
    """Visualize the entities for a given abstract in the dataframe. 
    
    Keyword arguments:
    df -- a dataframe object
    idx -- the index of interest for the dataframe (default 0)
    
    """
    # store entity start and end index for visualization in dummy df
    ents = []
    abstract = df['text'][idx]
    for ent in df['clean_ents'][idx]:
        i = abstract.find(ent) # locate the index of the entity in the abstract
        ents.append((ent, i, i+len(ent), 'ENTITY')) 
    ents.sort(key=lambda tup: tup[1])

    dummy_df = pd.DataFrame([abstract, ents]).T # transpose dataframe
    dummy_df.columns = ['text', 'clean_ents']
    column = 'clean_ents'
    render_entities(0, dummy_df, options=options, column=column)

visualize_entities(df, 0)