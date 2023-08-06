APPLICATION_SETTINGS = {
    'object_language_name': u'',
    'object_language_id': u'',
    'metalanguage_name': u'',
    'metalanguage_id': u'',
    'metalanguage_inventory': u'',
    'orthographic_validation': u'None', # Value should be one of [u'None', u'Warning', u'Error']
    'narrow_phonetic_inventory': u'',
    'narrow_phonetic_validation': u'None',
    'broad_phonetic_inventory': u'',
    'broad_phonetic_validation': u'None',
    'morpheme_break_is_orthographic': u'',
    'morpheme_break_validation': u'None',
    'phonemic_inventory': u'',
    'morpheme_delimiters': u'',
    'punctuation': u'',
    'grammaticalities': u'',
    'unrestricted_users': [],        # A list of user ids
    'storage_orthography': u'',        # An orthography id
    'input_orthography': u'',          # An orthography id
    'output_orthography': u''         # An orthography id
}

COLLECTION = {
    'title': u'',
    'type': u'',
    'url': u'',
    'description': u'',
    'markup_language': u'',
    'contents': u'',
    'speaker': u'',
    'source': u'',
    'elicitor': u'',
    'enterer': u'',
    'date_elicited': u'',
    'tags': [],
    'files': []
}

CORPUS = {
    'name': u'',
    'description': u'',
    'content': u'',
    'form_search': u'',
    'tags': []
}

FILE = {
    'name': u'',
    'description': u'',
    'date_elicited': u'',    # mm/dd/yyyy
    'elicitor': u'',
    'speaker': u'',
    'utterance_type': u'',
    'embedded_file_markup': u'',
    'embedded_file_password': u'',
    'tags': [],
    'forms': [],
    'file': ''      # file data Base64 encoded
}

FILE_BASE64 = {
    'filename': u'',        # Will be filtered out on update requests
    'description': u'',
    'date_elicited': u'',    # mm/dd/yyyy
    'elicitor': u'',
    'speaker': u'',
    'utterance_type': u'',
    'tags': [],
    'forms': [],
    'base64_encoded_file': '' # file data Base64 encoded; will be filtered out on update requests
}

FILE_MPFD = {
    'filename': u'',        # Will be filtered out on update requests
    'description': u'',
    'date_elicited': u'',    # mm/dd/yyyy
    'elicitor': u'',
    'speaker': u'',
    'utterance_type': u'',
    'tags-0': u'',
    'forms-0': u''
}

FILE_SUB_REF = {
    'parent_file': u'',
    'name': u'',
    'start': u'',
    'end': u'',
    'description': u'',
    'date_elicited': u'',    # mm/dd/yyyy
    'elicitor': u'',
    'speaker': u'',
    'utterance_type': u'',
    'tags': [],
    'forms': []
}

FILE_EXT_HOST = {
    'url': u'',
    'name': u'',
    'password': u'',
    'MIME_type': u'',
    'description': u'',
    'date_elicited': u'',    # mm/dd/yyyy
    'elicitor': u'',
    'speaker': u'',
    'utterance_type': u'',
    'tags': [],
    'forms': []
}

FORM = {
    'transcription': u'',
    'phonetic_transcription': u'',
    'narrow_phonetic_transcription': u'',
    'morpheme_break': u'',
    'grammaticality': u'',
    'morpheme_gloss': u'',
    'translations': [],
    'comments': u'',
    'speaker_comments': u'',
    'elicitation_method': u'',
    'tags': [],
    'syntactic_category': u'',
    'speaker': u'',
    'elicitor': u'',
    'verifier': u'',
    'source': u'',
    'status': u'tested',
    'date_elicited': u'',     # mm/dd/yyyy
    'syntax': u'',
    'semantics': u''
}

FORM_SEARCH = {
    'name': u'',
    'search': u'',
    'description': u'',
    'searcher': u''
}

MORPHEME_LANGUAGE_MODEL = {
    'name': u'',
    'description': u'',
    'corpus': u'',
    'vocabulary_morphology': u'',
    'toolkit': u'',
    'order': u'',
    'smoothing': u'',
    'categorial': False
}

MORPHOLOGY = {
    'name': u'',
    'description': u'',
    'lexicon_corpus': u'',
    'rules_corpus': u'',
    'script_type': u'lexc',
    'extract_morphemes_from_rules_corpus': False,
    'rules': u'',
    'rich_upper': True,
    'rich_lower': False,
    'include_unknowns': False
}

MORPHOLOGICAL_PARSER = {
    'name': u'',
    'phonology': u'',
    'morphology': u'',
    'language_model': u'',
    'description': u''
}

ORTHOGRAPHY = {
    'name': u'',
    'orthography': u'',
    'lowercase': False,
    'initial_glottal_stops': True
}

PAGE = {
    'name': u'',
    'heading': u'',
    'markup_language': u'',
    'content': u'',
    'html': u''
}

PHONOLOGY = {
    'name': u'',
    'description': u'',
    'script': u''
}

SOURCE = {
    'file': u'',
    'type': u'',
    'key': u'',
    'address': u'',
    'annote': u'',
    'author': u'',
    'booktitle': u'',
    'chapter': u'',
    'crossref': u'',
    'edition': u'',
    'editor': u'',
    'howpublished': u'',
    'institution': u'',
    'journal': u'',
    'key_field': u'',
    'month': u'',
    'note': u'',
    'number': u'',
    'organization': u'',
    'pages': u'',
    'publisher': u'',
    'school': u'',
    'series': u'',
    'title': u'',
    'type_field': u'',
    'url': u'',
    'volume': u'',
    'year': u'',
    'affiliation': u'',
    'abstract': u'',
    'contents': u'',
    'copyright': u'',
    'ISBN': u'',
    'ISSN': u'',
    'keywords': u'',
    'language': u'',
    'location': u'',
    'LCCN': u'',
    'mrnumber': u'',
    'price': u'',
    'size': u'',
}

SPEAKER = {
    'first_name': u'',
    'last_name': u'',
    'page_content': u'',
    'dialect': u'dialect',
    'markup_language': u'reStructuredText'
}

SYNTACTIC_CATEGORY = {
    'name': u'',
    'type': u'',
    'description': u''
}

USER = {
    'username': u'',
    'password': u'',
    'password_confirm': u'',
    'first_name': u'',
    'last_name': u'',
    'email': u'',
    'affiliation': u'',
    'role': u'',
    'markup_language': u'',
    'page_content': u'',
    'input_orthography': None,
    'output_orthography': None
}

MODELS = {
    'application_settings': APPLICATION_SETTINGS,
    'collection': COLLECTION,
    'corpus': CORPUS,
    'file': FILE,
    'file_base64': FILE_BASE64,
    'file_mpfd': FILE_MPFD,
    'file_sub_ref': FILE_SUB_REF,
    'file_ext_host': FILE_EXT_HOST,
    'form': FORM,
    'form_search': FORM_SEARCH,
    'morpheme_language_model': MORPHEME_LANGUAGE_MODEL,
    'morphology': MORPHOLOGY,
    'morphological_parser': MORPHOLOGICAL_PARSER,
    'orthography': ORTHOGRAPHY,
    'page': PAGE,
    'phonology': PHONOLOGY,
    'source': SOURCE,
    'speaker': SPEAKER,
    'syntactic_category': SYNTACTIC_CATEGORY,
    'user': USER,
}
