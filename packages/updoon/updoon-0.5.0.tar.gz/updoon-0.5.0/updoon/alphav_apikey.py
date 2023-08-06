
def alphav_apikey_set(apikey, filename=None):
    """Store the Alphavantage Token in $HOME/.updoon_alphav

    Parameters:
    -----------
    apikey : str
        The API Key from the Alphavantage Website.
        See https://www.alphavantage.co/support/#api-key

    filename : str
        Absolute path to the text where the
        Alphavantage API Key is stored (Optional)

    """
    # set default path
    if filename is None:
        import pathlib
        filename = str(pathlib.Path.home()) + "/.updoon_alphav"

    # write string to file
    fileptr = open(filename, 'w')
    fileptr.write(apikey)
    fileptr.close()
    return None


def alphav_apikey(filename=None):
    """Returns the locally store Alphavantage API
    key from $HOME/.updoon_alphav

    Parameters:
    -----------
    filename : str
        Absolute path to the text where the
        Alphavantage API Key is stored (Optional)

    Returns
    -------
    apikey : str
        The API Key from the Alphavantage Website.
        See https://www.alphav.com/account/api

    The function will throw an exception if the
    file $HOME/.updoon_alphav does not exist.
    Use `alphav_apikey_set("mysupersecrettoken")`
    to store your Alphavantage API Key first.

    The function will also throw an exception if
    the file $HOME/.updoon_alphav returns an empty
    string.

    """
    # set default path
    if filename is None:
        import pathlib
        filename = str(pathlib.Path.home()) + "/.updoon_alphav"

    errmsg2 = (
        "Please add your Alphavantage API Key with "
        "alphav_apikey_set('mysupersecrettoken')")
    try:
        fileptr = open(filename, 'r')
        apikey = fileptr.read()
        fileptr.close()
        if apikey:
            if len(apikey) > 0:
                return apikey
        raise Exception('File "$HOME/.updoon_alphav" seems empty. ' + errmsg2)
    except Exception:
        raise Exception('No "$HOME/.updoon_alphav" file found. ' + errmsg2)
