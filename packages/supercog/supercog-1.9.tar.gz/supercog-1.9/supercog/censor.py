def censor(text, inCodeBlock = False):
    """Returns a censored version of a string given.

    Parameters:
        text: The text to censor.
        inCodeBlock: Whether or not the text is going into a code block. (Defaults to False)
    
    Returns:
        censoredText (str)
    """

    # The list of profane words
    profaneWords = [
        "asshole", "bastard", "bitch", "cock", "dick", "cunt", "pussy",
        "fuck", "shit", "chode", "choad", "wanker", "twat", "nigger", "nigga",
        "tits", "jizz", "dildo", "douche"
    ]

    profanityUsed = [
        profanity
        for profanity in profaneWords
        if profanity.lower() in text.lower()
    ]

    # Replace text; Keep first and last letters; All middle letters replace with an asterisk (*)
    for profanity in profanityUsed:
        censored = (
            "{}{}{}".format(
                profanity[0],
                "{}".format(
                    "*" if inCodeBlock else "\\*"
                ) * (len(profanity) - 2),
                profanity[len(profanity) - 1]
            )
        )
        text = text.replace(profanity, censored)
    
    return text