
def fred_apikey_set(apikey, filename=None):
    """Store the Fred Token in $HOME/.updoon_fred

    Parameters:
    -----------
    apikey : str
        The API Key from the Fred Website.
        See https://research.stlouisfed.org/useraccount/apikeys

    filename : str
        Absolute path to the text where the
        Fred API Key is stored (Optional)

    """
    # set default path
    if filename is None:
        import pathlib
        filename = str(pathlib.Path.home()) + "/.updoon_fred"

    # write string to file
    fileptr = open(filename, 'w')
    fileptr.write(apikey)
    fileptr.close()
    return None


def fred_apikey(filename=None):
    """ Returns the locally store Fred API key from $HOME/.updoon_fred

    Parameters:
    -----------
    filename : str
        Absolute path to the text where the
        Fred API Key is stored (Optional)

    Returns
    -------
    apikey : str
        The API Key from the Fred Website.
        See https://research.stlouisfed.org/useraccount/apikeys

    The function will throw an exception if the
    file $HOME/.updoon_fred does not exist or is empty.
    Use `fred_apikey_set("mysupersecrettoken")`
    to store your Fred API Key first.
    """
    # set default path
    if filename is None:
        import pathlib
        filename = str(pathlib.Path.home()) + "/.updoon_fred"

    errmsg2 = (
        "Please add your Fred API Key with "
        "fred_apikey_set('mysupersecrettoken')")
    try:
        fileptr = open(filename, 'r')
        apikey = fileptr.read()
        fileptr.close()
        if apikey:
            if len(apikey) > 0:
                return apikey
        raise Exception('File "$HOME/.updoon_fred" seems empty. ' + errmsg2)
    except Exception:
        raise Exception('No "$HOME/.updoon_fred" file found. ' + errmsg2)
