================================================================================
  Online Linguistic Database (OLD) Client
================================================================================

This package is a client module for OLD web services. It facilitates making
HTTP requests to interact with one or more OLD instances.

Installation::

    $ pip install oldclient

For example usage, see the src/example.py file. In summary::

    >>> from oldclient import OLDClient
    >>> options = {
    ...     'url': '<URL_TO_AN_OLD_INSTANCE>',
    ...     'username': '<YOUR_USERNAME>',
    ...     'password': '<YOUR_PASSWORD>'}
    >>> old_client = OLDClient(options['url'])
    >>> old_client.login(options['username'], options['password'])
    True
    >>> form = old_client.models['form'].copy()
    >>> form['transcription'] = 'Arma virumque cano.'
    >>> form['translations'].append({
    ...     'transcription': 'I sing of arms and a man.',
    ...     'grammaticality': ''})
    >>> response = old_client.create(
    ...     'forms',
    ...     data=form)
    >>> print(response['id'])
    1061

The src/example.py file will create a stock form on an OLD you specify and have
access to::

    $ python src/example.py \
          -o <URL_TO_AN_OLD_INSTANCE> \
          -u <YOUR_USERNAME> \
          -p <YOUR_PASSWORD>
    John Doe created a new form with id 1059 on 2018-11-20T07:05:58.
    See https://app.dative.ca/#form/1059.

If you are logged in to your OLD instance in Dative, you should be able to see
the form just created (the first three words from Virgil's Aeneid) at the above
URL.
