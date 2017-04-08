#!/usr/bin/python
# coding: utf-8
'''
A library of classes and functions to store and operate on book, chapter
and verse references of biblical texts. It provides conversion between
different systems of bibleutils and abbreviations. The basic concept is one
of work,book,chapter,verse divisions which may vary between languages as do
the Old Greek and the Masoretic systems, or they may simply be different 
abbreviations for the same book. Internally this module defines its own
unique id to each book and all book names from other systems are mapped to 
these ids. Conversions are effected by translating from one name from one
system to the internal id and then to the corresponding name in the output
system. Thus all systems are also known and given a canonical id in this 
module.

In addition to the actual corpus materials having different systems, different
computer software programs also have different systems. These are also handled
in this module. 

Requires Python 2.7+

Created on Jan 21, 2017

@author:     47

@copyright:  2017 47Rooks. All rights reserved.

@license:    MIT

@contact:    47rooks@gmail.com
@deffield    updated: Updated
'''
from inspect import currentframe
import re
from collections import namedtuple

class VersificationException(Exception):
    '''A VersificationException is a simple class containing an error message,
    indicating a fault, a reason indicating why it occurred and an action, which
    may be taken to resolve issue.
    '''
    def __init__(self, message, reason, action):
        self._message = message
        self._reason = reason
        self._action = action
    
    @property
    def message(self):
        return self._message
    
    @property
    def reason(self):
        return self._reason
    
    @property
    def action(self):
        return self._action
        

class Identifier(object):
    '''An Identifier is a set of unique name to value mappings which are
    constant. Values may not be duplicated. Names are expected to be strings
    and values integers. Names are exposed as symbols for use in code where
    their value will be the value in the map. In this sense they are a 
    constant. An Identifier is iterable returning the symbolic name which when
    used will return the value. 
    
    
    FIXME currently a name may also be a value but perhaps even this will be
    prevented.
    '''
    def __init__(self, m):
        self._map = dict()
        for (k, v) in m.items():
            if v in self._map.values():
                raise VersificationException(
                    'duplicate value in supplied map at key {:s}'.format(k),
                    'the value supplied is already in use by another Identifier key',
                    'choose a different value for this Identifier')
            self._map[k] = v
            
    def __iter__(self):
        '''Iterate over the enumeration.
        FIXME It is not clear yet what this should
        return. Should it return the string name, the numeric constant, the
        property function pointer ??
        '''
        for k in self._map.keys():
            yield k      
        
class __VersificationID(Identifier):
    '''Defines the bibleutils system identifiers
    '''
    def __init__(self):
        super().__init__({'ETCBCH' : 1,
                          'ETCBCG' : 2,
                          'IGNTPSinaiticus' : 3,
                          'Accordance' : 4})
 
    @property
    def ETCBCH(self):
        return self._map.get(currentframe().f_code.co_name)
    
    @property
    def ETCBCG(self):
        return self._map.get(currentframe().f_code.co_name)
    
    @property
    def IGNTPSinaiticus(self):
        return self._map.get(currentframe().f_code.co_name)

    @property
    def Accordance(self):
        return self._map.get(currentframe().f_code.co_name)
    
VersificationID = __VersificationID()

class __BookID(Identifier):
    # Internal book IDs
    '''Defines the bibleutils system identifiers
    '''
    def __init__(self):
        super().__init__({
            # Old Testament
            '_GENESIS' : 1,
            '_EXODUS' : 2,
            '_LEVITICUS' : 3,
            '_NUMBERS' : 4,
            '_DEUTERONOMY' : 5,
            '_JOSHUA' : 6,
            '_JUDGES' : 7,
            '_1SAMUEL' : 8,
            '_2SAMUEL' : 9,
            '_1KINGS' : 10,
            '_2KINGS' : 11,
            '_ISAIAH' : 12,
            '_JEREMIAH' : 13,
            '_EZEKIEL' : 14,
            '_HOSEA' : 15,
            '_JOEL' : 16,
            '_AMOS' : 17,
            '_OBADIAH' : 18,
            '_JONAH' : 19,
            '_MICAH' : 20,
            '_NAHUM' : 21,
            '_HABAKKUK' : 22,
            '_ZEPHANIAH' : 23,
            '_HAGGAI' : 24,
            '_ZECHARIAH' : 25,
            '_MALACHI' : 26,
            '_PSALMS' : 27,
            '_JOB' : 28,
            '_PROVERBS' : 29,
            '_RUTH' : 30,
            '_SONG_OF_SONGS' : 31,
            '_ECCLESIASTES' : 32,
            '_LAMENTATIONS' : 33,
            '_ESTHER' : 34,
            '_DANIEL' : 35,
            '_EZRA' : 36,
            '_NEHEMIAH' : 37,
            '_1CHRONICLES' : 38,
            '_2CHRONICLES' : 39,
            
            # Apocrypha
            '_1ESDRAS' : 40,
            '_2ESDRAS' : 41,
            '_TOBIT' : 42,
            '_JUDITH' : 43,
            '_ESTHER_APOC' : 44,
            '_WISDOM' : 45,
            '_SIRACH' : 46,
            '_BARUCH' : 47,
            '_DANIEL_APOC' : 48,  # Apocryphal alternative 3 chapter
            '_MANASSEH' : 49,
            '_1MACABEES' : 50,
            '_2MACABEES' : 51,
            '_3MACABEES' : 52,
            '_4MACABEES' : 53,
            '_SUSANNA' : 54,
            '_BEL' : 55,
            '_LETTER_OF_JEREMIAH' : 56,
            
            # New Testament
            '_MATTHEW' : 57,
            '_MARK' : 58,
            '_LUKE' : 59,
            '_JOHN' : 60,
            '_ACTS' : 61,
            '_ROMANS' : 62,
            '_1CORINTHIANS' : 63,
            '_2CORINTHIANS' : 64,
            '_GALATIANS' : 65,
            '_EPHESIANS' : 66,
            '_PHILIPPIANS' : 67,
            '_COLOSSIANS' : 68,
            '_1THESSALONIANS' : 69,
            '_2THESSALONIANS' : 70,
            '_1TIMOTHY' : 71,
            '_2TIMOTHY' : 72,
            '_TITUS' : 73,
            '_PHILEMON' : 74,
            '_HEBREWS' : 75,
            '_JAMES' : 76,
            '_1PETER' : 77,
            '_2PETER' : 78,
            '_1JOHN' : 79,
            '_2JOHN' : 80,
            '_3JOHN' : 81,
            '_JUDE' : 82,
            '_REVELATION' : 83 })

            # Old Testament
        
    @property
    def _GENESIS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _EXODUS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _LEVITICUS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _NUMBERS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _DEUTERONOMY(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JOSHUA(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JUDGES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1SAMUEL(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2SAMUEL(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1KINGS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2KINGS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ISAIAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JEREMIAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _EZEKIEL(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _HOSEA(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JOEL(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _AMOS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _OBADIAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JONAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _MICAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _NAHUM(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _HABAKKUK(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ZEPHANIAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _HAGGAI(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ZECHARIAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _MALACHI(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _PSALMS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JOB(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _PROVERBS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _RUTH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _SONG_OF_SONGS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ECCLESIASTES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _LAMENTATIONS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ESTHER(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _DANIEL(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _EZRA(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _NEHEMIAH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1CHRONICLES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2CHRONICLES(self):
        return self._map.get(currentframe().f_code.co_name)
    
    # Apocrypha(self):
        
    @property
    def _1ESDRAS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2ESDRAS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _TOBIT(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JUDITH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ESTHER_APOC(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _WISDOM(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _SIRACH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _BARUCH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _DANIEL_APOC(self):  # Apocryphal alternative 3 chapter
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _MANASSEH(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1MACABEES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2MACABEES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _3MACABEES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _4MACABEES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _SUSANNA(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _BEL(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _LETTER_OF_JEREMIAH(self):
        return self._map.get(currentframe().f_code.co_name)
    
    # New Testament
        
    @property
    def _MATTHEW(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _MARK(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _LUKE(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JOHN(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ACTS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _ROMANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1CORINTHIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2CORINTHIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _GALATIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _EPHESIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _PHILIPPIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _COLOSSIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1THESSALONIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2THESSALONIANS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1TIMOTHY(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2TIMOTHY(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _TITUS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _PHILEMON(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _HEBREWS(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JAMES(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1PETER(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2PETER(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _1JOHN(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _2JOHN(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _3JOHN(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _JUDE(self):
        return self._map.get(currentframe().f_code.co_name)
        
    @property
    def _REVELATION(self):
        return self._map.get(currentframe().f_code.co_name)
    
    def fromStr(self, book_name):
        if book_name is not None:
            book_id = self._map.get('_' + str.upper(book_name))
            if book_id is None:
                # search for abbreviations
                for k in self._map.keys():
                    if k.startswith('_' + str.upper(book_name)):
                        return self._map.get(k)
            else:
                return book_id
        return None

BookID = __BookID()

class Versification(object):
    """Defines a bibleutils versification system.
    """
    
    def __init__(self, vid, bk_id_map):
        self._vid = vid
        self._bk_mapping = bk_id_map
        
        # Construct and store the reverse mapping
        self._reverse_mapping = dict()
        for (k, v) in self._bk_mapping.items():
            self._reverse_mapping[v] = k 
        if len(self._bk_mapping) != len(self._reverse_mapping):
            raise VersificationException(f'duplicate values detected '
                                          'forward map size={len(self._bk_mapping)}'
                                          'reverse map size={len(self._reverse_mapping)}',
                                         'a duplicate value was found in this Versification',
                                         'locate the duplicate and assign a unique value'
                                         )
            
    def vid(self):
        '''Get the versification system ID
        '''
        return self._vid
        
    def book_id(self, book_name):
        '''Return the internal book ID for the given name.
        '''
        return self._bk_mapping.get(book_name)
    
    def book_name(self, book_id):
        '''Return the book name as defined in this verisification system for
        the given internal book ID.
        '''
        return self._reverse_mapping.get(book_id)
    
class __ETCBCH(Versification):
    
    def __init__(self):
        super().__init__(
              VersificationID.ETCBCH,
            {   'Genesis' : BookID._GENESIS,
                'Exodus' : BookID._EXODUS,
                'Leviticus' : BookID._LEVITICUS,
                'Numeri' : BookID._NUMBERS,
                'Deuteronomium' : BookID._DEUTERONOMY,
                'Josua' : BookID._JOSHUA,
                'Judices' : BookID._JUDGES,
                'Samuel_I' : BookID._1SAMUEL,
                'Samuel_II' : BookID._2SAMUEL,
                'Reges_I' : BookID._1KINGS,
                'Reges_II' : BookID._2KINGS,
                'Jesaia' : BookID._ISAIAH,
                'Jeremia' : BookID._JEREMIAH,
                'Ezechiel' : BookID._EZEKIEL,
                'Hosea' : BookID._HOSEA,
                'Joel' : BookID._JOEL,
                'Amos' : BookID._AMOS,
                'Obadia' : BookID._OBADIAH,
                'Jona' : BookID._JONAH,
                'Micha' : BookID._MICAH,
                'Nahum' : BookID._NAHUM,
                'Habakuk' : BookID._HABAKKUK,
                'Zephania' : BookID._ZEPHANIAH,
                'Haggai' : BookID._HAGGAI,
                'Sacharia' : BookID._ZECHARIAH,
                'Maleachi' : BookID._MALACHI,
                'Psalmi' : BookID._PSALMS,
                'Iob' : BookID._JOB,
                'Proverbia' : BookID._PROVERBS,
                'Ruth' : BookID._RUTH,
                'Canticum' : BookID._SONG_OF_SONGS,
                'Ecclesiastes' : BookID._ECCLESIASTES,
                'Threni' : BookID._LAMENTATIONS,
                'Esther' : BookID._ESTHER,
                'Daniel' : BookID._DANIEL,
                'Esra' : BookID._EZRA,
                'Nehemia' : BookID._NEHEMIAH,
                'Chronica_I' : BookID._1CHRONICLES,
                'Chronica_II' : BookID._2CHRONICLES
            })

ETCBCHVersification = __ETCBCH()

class __ETCBCG(Versification):
    
    def __init__(self):
        super().__init__(
              VersificationID.ETCBCG,
            {   'Genesis' : BookID._GENESIS,
                'Exodus' : BookID._EXODUS,
                'Matthew' : BookID._MATTHEW,
                'Mark' : BookID._MARK,
                'Luke' : BookID._LUKE,
                'John' : BookID._JOHN,
                'Acts' : BookID._ACTS,
                'Romans' : BookID._ROMANS,
                '1Corinthians' : BookID._1CORINTHIANS,
                '2Corinthians' : BookID._2CORINTHIANS,
                'Galations' : BookID._GALATIANS,
                'Ephesians' : BookID._EPHESIANS,
                'Philippians' : BookID._PHILIPPIANS,
                'Colossians' : BookID._COLOSSIANS,
                '1Thessalonians' : BookID._1THESSALONIANS,
                '2Thessalonians' : BookID._2THESSALONIANS,
                '1Timothy' : BookID._1TIMOTHY,
                '2Timothy' : BookID._2TIMOTHY,
                'Titus' : BookID._TITUS,
                'Philemon' : BookID._PHILEMON,
                'Hebrews' : BookID._HEBREWS,
                'James' : BookID._JAMES,
                '1Peter' : BookID._1PETER,
                '2Peter' : BookID._2PETER,
                '1John' : BookID._1JOHN,
                '2John' : BookID._2JOHN,
                '3John' : BookID._3JOHN,
                'Jude' : BookID._JUDE,
                'Revelation': BookID._REVELATION
            })

ETCBCGVersification = __ETCBCG()

class __ReferenceFormID(Identifier):
    '''Defines the bibleutils system identifiers
    '''
    def __init__(self):
        super().__init__({'BIBLEUTILS' : 0,
                          'ETCBCG' : 1,
                          'ETCBCH' : 2,
                          'IGNTPSinaiticus' : 3})
 
    @property
    def BIBLEUTILS(self):
        return self._map.get(currentframe().f_code.co_name)

    @property
    def ETCBCG(self):
        return self._map.get(currentframe().f_code.co_name)

    @property
    def ETCBCH(self):
        return self._map.get(currentframe().f_code.co_name)

    @property
    def IGNTPSinaiticus(self):
        return self._map.get(currentframe().f_code.co_name)
    
ReferenceFormID = __ReferenceFormID()

class Ref():
    '''A Ref class contains a text reference. It contains reference to a
    single contiguous range of text, as defined in the particular versification
    system.
    '''
    # FIXME there is confusion over verisification system ID and reference form ID
    # I think this here should be reference form ID. Are they really distinct ?
    
    # FIXME Book order is not checked and can only be checked meaningfully when
    # the versification system is fully specified in this module. Sub verses
    # are also not checked and I do not know yet how.
    def __init__(self, v, sb=None, eb=None, sc=None, ec=None, sv=None,
                 ev=None, ssv=None, esv=None):
        if sc is not None and ec is not None and ec < sc:
            raise VersificationException(f'ending chapter {ec} is before the starting chapter {sc}',
                                         'chapter number must be in increasing order'
                                         'reorder chapter numbers to be in numerical order')
        if sv is not None and ev is not None and ev < sv:
            raise VersificationException(f'ending verse {ev} is before the starting verse {sv}',
                                         'verse number must be in increasing order',
                                         'reorder verse numbers to be in numerical order')
        
        self._versification = v
        self._st_book = sb
        self._end_book = eb
        self._st_ch = sc
        self._end_ch = ec
        self._st_vs = sv
        self._end_vs = ev
        self._st_sub_vs = ssv
        self._end_sub_vs = esv
    
    @property
    def versification(self):
        return self._versification
    
    @property
    def st_book(self):
        return self._st_book
    
    @property
    def end_book(self):
        return self._end_book
    
    @property
    def st_ch(self):
        return self._st_ch
    
    @property
    def end_ch(self):
        return self._end_ch
    
    @property
    def st_vs(self):
        return self._st_vs
    
    @property
    def end_vs(self):
        return self._end_vs
    
    @property
    def st_sub_vs(self):
        return self._st_sub_vs
    
    @property
    def end_sub_vs(self):
        return self._end_sub_vs
    
def parse_refs(refs, form):
    '''
    Parses the input string of verse references into a canonical form and
    the returns the requested form.
    
    Parameters
    
    refs - a string of any common form of verse reference such as 'Gen 1:1-12',
           'Gen 1:1-2,6, Ex 17:3'.
    form - specifies the output form, and is basically an indicator of the API
           to which the output will be sent.
           
           ReferenceFormID.ETCBC - ETCBC/TF compliant tuples.

    Returns

    A list of Ref instances.
    
    Issues
    
    The general solution for this problem is complicated by many factors
    including versification system, language, and recognised abbreviations.
    Only some of these issues are dealt with now. 
    '''
    rv = []
    
    # Extract complete discrete references for each book and following chapter
    # and verse references.
    # Delimiter definitions:
    #   <space> book to chapter transition
    #   :       chapter to verse transition
    #   -       book to book, chapter to chapter, verse to verse transitions
    #   ,       end of current reference, transition unclear until next read
    re_book = re.compile('([0-9]{0,1}[a-zA-Z]+)')
    re_delim = re.compile('( *[ +:,-] *)')
    re_ch = re.compile('([0-9]+)')
    re_vs = re.compile('([0-9]+)')
    re_sub_vs = re.compile('([a-z])')
    
    P_INIT = 0 # no processing yet done
    P_BOOK = 1
    P_CH = 2
    P_VS = 3
    P_SUBVS = 4
    P_DELIM = 5 # searching for a delimiter
    P_NEXT = 6 # Finished last ref, do not know what section of a ref will come next
    
    pos = 0   # current position in refs to match at
    #state = P_INIT
    #prev_state = P_INIT
    States = namedtuple('States', ['previous', 'current'])
    state = States(P_INIT, P_BOOK)    
    def update_state(state, new_state):
        return States(state.current, new_state)

    t_st_bk, t_end_bk, t_st_ch, t_end_ch, t_st_vs, t_end_vs, t_st_subvs, \
        t_end_subvs = (None,)*8
    while pos < len(refs):
        if state.current == P_BOOK:
            m = re_book.match(refs, pos)
            if not m:
                raise VersificationException(
                    f'invalid book name at pos {pos} in {refs}',
                    'book name is invalid',
                    'correct the book name and resubmit') 
            pos += len(m.group(1))
            if t_st_bk is None:
                t_st_bk = m.group(1)
            else:
                t_end_bk = m.group(1)
            state = update_state(state, P_DELIM)
        elif state.current == P_CH:
            m = re_ch.match(refs, pos)
            if not m:
                raise VersificationException(
                    f'invalid chapter at pos {pos} in {refs}',
                    'chapter reference is invalid',
                    'correct the chapter and resubmit')            
            pos += len(m.group(1))
            if t_st_ch is None:
                t_st_ch = int(m.group(1))
            else:
                t_end_ch = int(m.group(1))
            state = update_state(state, P_DELIM)
        elif state.current == P_VS:
            m = re_vs.match(refs, pos)
            if not m:
                raise VersificationException(
                    f'invalid verse reference at pos {pos} in {refs}',
                    'verse reference is invalid',
                    'correct the verse and resubmit')            
            pos += len(m.group(1))
            if t_st_vs is None:
                t_st_vs = int(m.group(1))
            else:
                t_end_vs = int(m.group(1))            
            state = update_state(state, P_DELIM)
        elif state.current == P_SUBVS:
            state = update_state(state, P_DELIM)
        elif state.current == P_NEXT:
            pass
        elif state.current == P_DELIM:
            m = re_delim.match(refs, pos)
            if not m:
                raise VersificationException(
                    f'invalid reference delimiter at pos {pos} in {refs}',
                    'reference delimiter is invalid',
                    'correct delimiter (one of ,:- or <space>) and resubmit') 
            pos += len(m.group(1))
            d = m.group(1)
            if ',' in d:
                # End the current contiguous range
                # create Refs object
                # reset temporary vars as required by 
                rv.append(Ref(ReferenceFormID.BIBLEUTILS,
                              BookID.fromStr(t_st_bk),
                              BookID.fromStr(t_end_bk),
                              t_st_ch, t_end_ch,
                              t_st_vs, t_end_vs,
                              t_st_subvs, t_end_subvs))               
                if state.previous == P_BOOK:
                    # reset all temporary vars
                    t_st_bk, t_end_bk, t_st_ch, t_end_ch, t_st_vs, t_end_vs, \
                        t_st_subvs, t_end_subvs = (None,)*8                
                    state = update_state(state, P_BOOK)
                elif state.previous == P_CH:
                    # reset vars chapter and below
                    t_st_ch, t_end_ch, t_st_vs, t_end_vs, \
                        t_st_subvs, t_end_subvs = (None,)*6
                    state = update_state(state, P_CH)
                elif state.previous == P_VS:
                    # reset vars verse and below
                    t_st_vs, t_end_vs, t_st_subvs, t_end_subvs = (None,)*4
                    state = update_state(state, P_VS)
            elif ':' in d:
                if state.previous == P_CH:
                    state = update_state(state, P_VS)
                else:
                    raise VersificationException(
                        f'invalid chapter to verse transition at {pos} in {refs}'
                        'expected to find verse but did not',
                        'examine and correct the reference and resubmit')
            elif '-' in d:
                # We are looking for another of whatever the current
                # state.current is looking for.
                if state.previous == P_BOOK:
                    if t_end_bk is not None:
                        raise VersificationException(
                            f'invalid "-" delimiter at {pos} in {refs}',
                            'found unexpected book designation',
                            'examine and correct the reference and resubmit')
                    state = update_state(state, P_BOOK)
                elif state.previous == P_CH:
                    if t_end_ch is not None:
                        raise VersificationException(
                            f'invalid "-" delimiter at {pos} in {refs}',
                            'found unexpected chapter designation',
                            'examine and correct the reference and resubmit')
                    state = update_state(state, P_CH)
                elif state.previous == P_VS:
                    if t_end_vs is not None:
                        raise VersificationException(
                            f'invalid "-" delimiter at {pos} in {refs}',
                            'found unexpected verse designation',
                            'examine and correct the reference and resubmit')
                    state = update_state(state, P_VS)
            elif d.isspace():
                # Switch state depending upon the current state.
                # book to chapter
                state = update_state(state, P_CH)
            else:
                raise VersificationException(
                    f'invalid delimiter at {pos} in {refs}',
                    'found invalid delimiter',
                    'correct delimiter (one of ,:- or <space>) and resubmit')
        else:
            raise VersificationException(
                f'parsing failure at {pos} in {refs}',
                'general parsing failure',
                'examine and correct the reference and resubmit')
    
    rv.append(Ref(ReferenceFormID.BIBLEUTILS,
                  BookID.fromStr(t_st_bk), BookID.fromStr(t_end_bk),
                  t_st_ch, t_end_ch, t_st_vs, t_end_vs,
                  t_st_subvs, t_end_subvs))
    return rv

def convert_refs(refs, form):
    '''Convert a list of refs from their current forms to specified form
    returning a new list of refs of the right form. At present this is and 
    simple conversion of just the book names.
    '''
    to_internal = False
    if form == ReferenceFormID.ETCBCG:
        ovf = ETCBCGVersification
    elif form == ReferenceFormID.ETCBCH:
        ovf = ETCBCHVersification
    elif form == ReferenceFormID.BIBLEUTILS:
        # This is the internal form. This means convert to internal ID based
        # form. This is a unique conversion and each versification system 
        # supports this by the *_id() converter functions.
        # I am not satisfied with this mapping method here, so it needs
        # to be rethought. FIXME for now this hack will do.
        to_internal = True
    else:
        raise VersificationException(
            'unsupported conversion form {form}',
            'the specified versification system is unknown',
            'specify a support versification system designation')
    rv = []
    for r in refs:
        if r.versification == ReferenceFormID.BIBLEUTILS:
            rv.append(Ref(form,
                          ovf.book_name(r.st_book),
                          ovf.book_name(r.end_book),
                          r.st_ch, r.end_ch,
                          r.st_vs, r.end_vs,
                          r.st_sub_vs, r.end_sub_vs))
        elif r.versification == ReferenceFormID.ETCBCG:
            if to_internal is True:
                rv.append(Ref(form,
                          ETCBCGVersification.book_id(r.st_book),
                          ETCBCGVersification.book_id(r.end_book),
                          r.st_ch, r.end_ch,
                          r.st_vs, r.end_vs,
                          r.st_sub_vs, r.end_sub_vs))
        elif r.versification == ReferenceFormID.ETCBCH:
            if to_internal is True:
                rv.append(Ref(form,
                          ETCBCHVersification.book_id(r.st_book),
                          ETCBCHVersification.book_id(r.end_book),
                          r.st_ch, r.end_ch,
                          r.st_vs, r.end_vs,
                          r.st_sub_vs, r.end_sub_vs))

    return rv    
            
def expand_refs(refs):
    '''Expand each of the refs in the input list into a new list of refs
    each being just a single a ref to a single final point. For example
    a ref for "Gen 1:34-37" will be converted to this list of refs "Gen 1:34,
    Gen 1:35, Gen 1:36, Gen 1:37". This conversion is primarily aimed at the
    section API, nodeFromSection(), of Text-Fabric.
    '''
    # FIXME There is no way to expand references like this without having
    # a knowledge of the internals of the versification system in which the
    # expansion is to be done. It is arguable this is not entirely generalizable
    # or useful but for now we will do the verses.
    rv = []
    for r in refs:
        if r.end_book != None:
            raise VersificationException(
                'reference extends over more than one book',
                'book range expansion not yet implemented',
                'correct reference to be constrained to a single book')
        if r.end_ch != None:
            raise VersificationException(
                'reference extends over more than one chapter',
                'chapter range expansion not yet implemented',
                'correct reference to be constrained to a single chapter')
        #end_ch = r.end_ch if r.end_ch is not None else r.st_ch
        #for ch in range(r.st_ch, end_ch + 1):
        end_vs = r.end_vs if r.end_vs is not None else r.st_vs
        for vs in range(r.st_vs, end_vs + 1):
            rv.append(Ref(r.versification,
                          r.st_book, None,
                          r.st_ch, None,
                          vs, None))
    return rv
                