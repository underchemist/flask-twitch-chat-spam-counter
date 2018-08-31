import json


def load_emotes():
    fname = 'app/emotes.json'

    return json.load(open(fname, 'r'))


def txt_to_emote(df):
    """
    Parse dataset for str matches for twitch global emotes and replace with img src for said emote.
    """
    emotes = load_emotes()
    replace_dict = {'Spam': emotes}
    return df.replace(replace_dict, regex=True)
