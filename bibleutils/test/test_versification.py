'''
Created on Jan 22, 2017

@author: Daniel
'''
import unittest
from bibleutils.versification import VersificationID, BookID, Identifier, \
     ReferenceFormID, parse_refs, ETCBCHVersification, Ref, convert_refs, \
     expand_refs

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testVersificationIDs(self):
        '''Verify that ids can be referred to by the property methods
        '''
        assert VersificationID.ETCBCH == 1
        assert VersificationID.ETCBCG == 2
        assert VersificationID.IGNTPSinaiticus == 3
        assert VersificationID.Accordance == 4

    def testVersificationIDsImmutable(self):
        with self.assertRaises(AttributeError):
            VersificationID.ETCBCH = 12
        
    def testVersificationIDsCannotBeAdded(self):
        # FIXME I cannot prevent an attribute being added.
        with self.assertRaises(AttributeError):
            VersificationID.FOO = 15
        
    def testVersificationIter(self):
        for k in VersificationID:
            print('key={:s}'.format(k))
            
    def testBookNameFromBookId(self):
        self.assertEqual(ETCBCHVersification.book_name(BookID._NUMBERS), 'Numeri',
                         f'Incorrect name from book_id {ETCBCHVersification.book_id(BookID._NUMBERS)}')

    def testBookIdFromBookName(self):
        self.assertEqual(ETCBCHVersification.book_id('Numeri'),
                         BookID._NUMBERS,
                         f"Incorrect ID from book_name {ETCBCHVersification.book_name('Numeri')}")
        
    def testIDValuesUnique(self):
        '''Verify that duplicates cannot be created in the Identifier class
        ''' 
        chk = {'_GENESIS':1, '_EXODUS':2, '_LEVITICUS':3,
               '_NUMBERS':4, '_DEUTERONOMY':5, '_DEUTERONOMYA':5}
        with self.assertRaises(Exception) as expected_ex:
            Identifier(chk)

        ex = expected_ex.exception
        self.assertEqual(str(ex)[:51],
                         'duplicate value in supplied map at key _DEUTERONOMY',
                         'Unexpected mesg in exception : {:s}'.format(str(ex)))

    def testBookIDSmoker(self):
        '''Just a quick smoker
        '''
        self.assertEqual(BookID._1CHRONICLES, 38, 'Unexpected value {:d}')
        
    def testParseBookOnly(self):
        r = parse_refs("Exodus", ReferenceFormID.BIBLEUTILS)
        self.assertEquals(len(r), 1)
        self.assertEqual(r[0].versification, ReferenceFormID.BIBLEUTILS,
                         'wrong versification system {}'.format(r[0].versification))
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertIsNone(r[0].end_book,
                         'ending book is wrong {}'.format(r[0].end_book))
        self.assertIsNone(r[0].st_ch, 'st_ch not None {}'.format(r[0].st_ch))
        self.assertIsNone(r[0].end_ch, 'end_ch not None {}'.format(r[0].end_ch))
        self.assertIsNone(r[0].st_vs, 'st_vs not None {}'.format(r[0].st_vs))
        self.assertIsNone(r[0].end_vs, 'end_vs not None {}'.format(r[0].end_vs))
        self.assertIsNone(r[0].st_sub_vs, 'st_sub_vs not None {}'.format(r[0].st_sub_vs))
        self.assertIsNone(r[0].end_sub_vs, 'end_sub_vs not None {}'.format(r[0].end_sub_vs))
        
    def testParseNumBookOnly(self):
        r = parse_refs("1Kings", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._1KINGS,
                         'wrong book id {}'.format(r[0].st_book))
        
    def testParseBookRangeOnly(self):
        r = parse_refs("Exodus-Numbers", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].end_book, BookID._NUMBERS,
                         'wrong book id {}'.format(r[0].end_book))
        
    def testParseBookRangeTwoDelims(self):
        with self.assertRaises(Exception) as expected_ex:
            parse_refs("Exodus--Numbers", ReferenceFormID.BIBLEUTILS)

        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'Parsing failed at pos 7 in Exodus--Numbers',
                         'Unexpected mesg in exception : {:s}'.format(str(ex)))        
 
    def testParseChVsRangeTwoDelims(self):
        with self.assertRaises(Exception) as expected_ex:
            parse_refs("Exodus 12::13", ReferenceFormID.BIBLEUTILS)

        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'Parsing failed at pos 10 in Exodus 12::13',
                         'Unexpected mesg in exception : {:s}'.format(str(ex)))        
 
    def testParseTwoCommas(self):
        with self.assertRaises(Exception) as expected_ex:
            parse_refs("Exodus 12-13,,15", ReferenceFormID.BIBLEUTILS)

        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'Parsing failed at pos 13 in Exodus 12-13,,15',
                         'Unexpected mesg in exception : {:s}'.format(str(ex)))        
 
    def testParseMixedDelims(self):
        with self.assertRaises(Exception) as expected_ex:
            parse_refs("Exodus 12-13,:-15", ReferenceFormID.BIBLEUTILS)

        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'Parsing failed at pos 13 in Exodus 12-13,:-15',
                         'Unexpected mesg in exception : {:s}'.format(str(ex)))        

    def testParseBookRangeTooManyBooks(self):
        with self.assertRaises(Exception) as expected_ex:
            parse_refs("Exodus-Numbers-Deuteronomy", ReferenceFormID.BIBLEUTILS)

        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'invalid "-" delimiter at 15 in Exodus-Numbers-Deuteronomy')
                         
    def testParseMultiBookRangeOnly(self):
        r = parse_refs("Exodus-Numbers,Matt-Mark", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].end_book, BookID._NUMBERS,
                         'wrong book id {}'.format(r[0].end_book))
        self.assertEqual(r[1].st_book, BookID._MATTHEW,
                         'wrong book id {}'.format(r[1].st_book))
        self.assertEqual(r[1].end_book, BookID._MARK,
                         'wrong book id {}'.format(r[1].end_book))
        
    def testParseNumBookRangeOnly(self):
        r = parse_refs("1Kings-2Kings", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._1KINGS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].end_book, BookID._2KINGS,
                         'wrong book id {}'.format(r[0].end_book))
        
    def testParseBookChapter(self):
        r = parse_refs("Exodus 12", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertIsNone(r[0].end_book,
                         'book id is not None {}'.format(r[0].end_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect chapter {}'.format(r[0].st_ch))  
        self.assertIsNone(r[0].end_ch, 'chapter is not None')  

    def testParseBookChapterRange(self):
        r = parse_refs("Exodus 12-15", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].end_ch, 15,
                         'incorrect ending chapter {}'.format(r[0].end_ch))

    def testParseBookMultiChapterRange(self):
        r = parse_refs("Exodus 12-15, 17-25", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].end_ch, 15,
                         'incorrect ending chapter {}'.format(r[0].end_ch))
        self.assertEqual(r[1].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[1].st_book))
        self.assertEqual(r[1].st_ch, 17,
                         'incorrect starting chapter {}'.format(r[1].st_ch))  
        self.assertEqual(r[1].end_ch, 25,
                         'incorrect ending chapter {}'.format(r[1].end_ch))
        
    def testParseBookAbbrevCh(self):
        r = parse_refs("Ex 12", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        
    def testParseBookAbbrevWithDot(self):
        r = parse_refs("Ex. 12", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        
    def testParseBookChVs(self):
        r = parse_refs("Gen 12:1", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].st_vs, 1,
                         'incorrect starting chapter {}'.format(r[0].st_vs))  
        
    def testParseBookChVsRange(self):
        r = parse_refs("Gen 12:1-12", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].st_vs, 1,
                         'incorrect starting chapter {}'.format(r[0].st_vs))  
        self.assertEqual(r[0].end_vs, 12,
                         'incorrect starting chapter {}'.format(r[0].end_vs))
         
    def testParseBookChVsRangeSeq(self):
        r = parse_refs("Gen 12:1-12,13", ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].st_vs, 1,
                         'incorrect starting chapter {}'.format(r[0].st_vs))  
        self.assertEqual(r[0].end_vs, 12,
                         'incorrect starting chapter {}'.format(r[0].end_vs))
        self.assertEqual(r[1].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[1].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[1].st_ch))  
        self.assertEqual(r[1].st_vs, 13,
                         'incorrect starting chapter {}'.format(r[1].st_vs))        

    def testParseGen1_3(self):
        r = parse_refs('Gen 1:1-2,6-23', ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 1,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].st_vs, 1,
                         'incorrect starting chapter {}'.format(r[0].st_vs))  
        self.assertEqual(r[0].end_vs, 2,
                         'incorrect starting chapter {}'.format(r[0].end_vs))
        self.assertEqual(r[1].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[1].st_ch, 1,
                         'incorrect starting chapter {}'.format(r[1].st_ch))  
        self.assertEqual(r[1].st_vs, 6,
                         'incorrect starting chapter {}'.format(r[1].st_vs))        
        self.assertEqual(r[1].end_vs, 23,
                         'incorrect starting chapter {}'.format(r[1].st_vs))        
        
    def testParseBookChVsChVs(self):
        r = parse_refs('Gen 1:1-2,6-23,2:23', ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 1,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].st_vs, 1,
                         'incorrect starting chapter {}'.format(r[0].st_vs))  
        self.assertEqual(r[0].end_vs, 2,
                         'incorrect starting chapter {}'.format(r[0].end_vs))
        self.assertEqual(r[1].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[1].st_ch, 1,
                         'incorrect starting chapter {}'.format(r[1].st_ch))  
        self.assertEqual(r[1].st_vs, 6,
                         'incorrect starting chapter {}'.format(r[1].st_vs))        
        self.assertEqual(r[1].end_vs, 23,
                         'incorrect starting chapter {}'.format(r[1].st_vs))        
        self.assertEqual(r[2].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[2].st_book))
        self.assertEqual(r[2].st_ch, 2,
                         'incorrect starting chapter {}'.format(r[2].st_ch))  
        self.assertEqual(r[2].st_vs, 23,
                         'incorrect starting chapter {}'.format(r[2].st_vs))  

    def testParseComplexRefString(self):
        r = parse_refs('Gen 1:1-2,6, Ex 17:3, Deut 12,13', ReferenceFormID.BIBLEUTILS)
        self.assertEqual(r[0].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[0].st_ch, 1,
                         'incorrect starting chapter {}'.format(r[0].st_ch))  
        self.assertEqual(r[0].st_vs, 1,
                         'incorrect starting chapter {}'.format(r[0].st_vs))  
        self.assertEqual(r[0].end_vs, 2,
                         'incorrect starting chapter {}'.format(r[0].end_vs))
        self.assertEqual(r[1].st_book, BookID._GENESIS,
                         'wrong book id {}'.format(r[0].st_book))
        self.assertEqual(r[1].st_ch, 1,
                         'incorrect starting chapter {}'.format(r[1].st_ch))  
        self.assertEqual(r[1].st_vs, 6,
                         'incorrect starting chapter {}'.format(r[1].st_vs))        
        self.assertEqual(r[2].st_book, BookID._EXODUS,
                         'wrong book id {}'.format(r[2].st_book))
        self.assertEqual(r[2].st_ch, 17,
                         'incorrect starting chapter {}'.format(r[2].st_ch))  
        self.assertEqual(r[2].st_vs, 3,
                         'incorrect starting chapter {}'.format(r[2].st_vs))  
        self.assertEqual(r[3].st_book, BookID._DEUTERONOMY,
                         'wrong book id {}'.format(r[3].st_book))
        self.assertEqual(r[3].st_ch, 12,
                         'incorrect starting chapter {}'.format(r[3].st_ch))  
        self.assertEqual(r[4].st_book, BookID._DEUTERONOMY,
                         'wrong book id {}'.format(r[4].st_book))
        self.assertEqual(r[4].st_ch, 13,
                         'incorrect starting chapter {}'.format(r[4].st_vs))  
            
    def testConvertInternalToETCBCH(self):
        refs = [Ref(ReferenceFormID.BIBLEUTILS,
                    BookID._DEUTERONOMY, sc=3, sv=4),
                Ref(ReferenceFormID.BIBLEUTILS,
                    BookID._EXODUS, BookID._EXODUS, 1, sv=12, ev=15)]
        c_refs = convert_refs(refs, ReferenceFormID.ETCBCH)
        self.assertEqual(c_refs[0].versification, ReferenceFormID.ETCBCH,
                         f'Incorrect reference form {c_refs[0].versification}')
        self.assertEqual(c_refs[0].st_book, 'Deuteronomium',
                         f'Conversion returned wrong name {c_refs[0].st_book}')
        self.assertEqual(c_refs[0].st_ch, 3,
                         f'Conversion returned wrong ch {c_refs[0].st_ch}')
        self.assertEqual(c_refs[0].st_vs, 4,
                         f'Conversion returned wrong vs {c_refs[0].st_vs}')
        self.assertEqual(c_refs[1].versification, ReferenceFormID.ETCBCH,
                         f'Incorrect reference form {c_refs[0].versification}')
        self.assertEqual(c_refs[1].st_book, 'Exodus',
                         f'Conversion returned wrong name {c_refs[1].st_book}')
        self.assertEqual(c_refs[1].st_ch, 1,
                         f'Conversion returned wrong ch {c_refs[1].st_ch}')
        self.assertEqual(c_refs[1].st_vs, 12,
                         f'Conversion returned wrong vs {c_refs[1].st_vs}')
        self.assertEqual(c_refs[1].end_vs, 15,
                         f'Conversion returned wrong vs {c_refs[1].end_vs}')
        
    def testConvertETCBCHToInternal(self):
        refs = [Ref(ReferenceFormID.ETCBCH,
                    'Deuteronomium', sc=3, sv=4),
                Ref(ReferenceFormID.ETCBCH,
                    'Exodus', 'Exodus', 1, sv=12, ev=15)]
        c_refs = convert_refs(refs, ReferenceFormID.BIBLEUTILS)
        self.assertEqual(c_refs[0].versification, ReferenceFormID.BIBLEUTILS,
                         f'Incorrect reference form {c_refs[0].versification}')
        self.assertEqual(c_refs[0].st_book, BookID._DEUTERONOMY,
                         f'Conversion returned wrong name {c_refs[0].st_book}')
        self.assertEqual(c_refs[0].st_ch, 3,
                         f'Conversion returned wrong ch {c_refs[0].st_ch}')
        self.assertEqual(c_refs[0].st_vs, 4,
                         f'Conversion returned wrong vs {c_refs[0].st_vs}')
        self.assertEqual(c_refs[1].versification, ReferenceFormID.BIBLEUTILS,
                         f'Incorrect reference form {c_refs[1].versification}')
        self.assertEqual(c_refs[1].st_book, BookID._EXODUS,
                         f'Conversion returned wrong name {c_refs[1].st_book}')
        self.assertEqual(c_refs[1].st_ch, 1,
                         f'Conversion returned wrong ch {c_refs[1].st_ch}')
        self.assertEqual(c_refs[1].st_vs, 12,
                         f'Conversion returned wrong vs {c_refs[1].st_vs}')
        self.assertEqual(c_refs[1].end_vs, 15,
                         f'Conversion returned wrong vs {c_refs[1].end_vs}')
    
    def testConvertInternalToETCBCG(self):
        refs = [Ref(ReferenceFormID.BIBLEUTILS,
                    BookID._LUKE, sc=3, sv=4),
                Ref(ReferenceFormID.BIBLEUTILS,
                    BookID._MARK, BookID._MARK, 1, sv=12, ev=15)]
        c_refs = convert_refs(refs, ReferenceFormID.ETCBCG)
        self.assertEqual(c_refs[0].versification, ReferenceFormID.ETCBCG,
                         f'Incorrect reference form {c_refs[0].versification}')
        self.assertEqual(c_refs[0].st_book, 'Luke',
                         f'Conversion returned wrong name {c_refs[0].st_book}')
        self.assertEqual(c_refs[0].st_ch, 3,
                         f'Conversion returned wrong ch {c_refs[0].st_ch}')
        self.assertEqual(c_refs[0].st_vs, 4,
                         f'Conversion returned wrong vs {c_refs[0].st_vs}')
        self.assertEqual(c_refs[1].versification, ReferenceFormID.ETCBCG,
                         f'Incorrect reference form {c_refs[0].versification}')
        self.assertEqual(c_refs[1].st_book, 'Mark',
                         f'Conversion returned wrong name {c_refs[1].st_book}')
        self.assertEqual(c_refs[1].st_ch, 1,
                         f'Conversion returned wrong ch {c_refs[1].st_ch}')
        self.assertEqual(c_refs[1].st_vs, 12,
                         f'Conversion returned wrong vs {c_refs[1].st_vs}')
        self.assertEqual(c_refs[1].end_vs, 15,
                         f'Conversion returned wrong vs {c_refs[1].end_vs}')
        
    def testConvertETCBCGToInternal(self):
        refs = [Ref(ReferenceFormID.ETCBCG,
                    'Luke', sc=3, sv=4),
                Ref(ReferenceFormID.ETCBCG,
                    'Mark', 'Mark', 1, sv=12, ev=15)]
        c_refs = convert_refs(refs, ReferenceFormID.BIBLEUTILS)
        self.assertEqual(c_refs[0].versification, ReferenceFormID.BIBLEUTILS,
                         f'Incorrect reference form {c_refs[0].versification}')
        self.assertEqual(c_refs[0].st_book, BookID._LUKE,
                         f'Conversion returned wrong name {c_refs[0].st_book}')
        self.assertEqual(c_refs[0].st_ch, 3,
                         f'Conversion returned wrong ch {c_refs[0].st_ch}')
        self.assertEqual(c_refs[0].st_vs, 4,
                         f'Conversion returned wrong vs {c_refs[0].st_vs}')
        self.assertEqual(c_refs[1].versification, ReferenceFormID.BIBLEUTILS,
                         f'Incorrect reference form {c_refs[1].versification}')
        self.assertEqual(c_refs[1].st_book, BookID._MARK,
                         f'Conversion returned wrong name {c_refs[1].st_book}')
        self.assertEqual(c_refs[1].st_ch, 1,
                         f'Conversion returned wrong ch {c_refs[1].st_ch}')
        self.assertEqual(c_refs[1].st_vs, 12,
                         f'Conversion returned wrong vs {c_refs[1].st_vs}')
        self.assertEqual(c_refs[1].end_vs, 15,
                         f'Conversion returned wrong vs {c_refs[1].end_vs}')

    def testExpandVerse(self):
        refs = [Ref(ReferenceFormID.ETCBCH,
                    'Deuteronomium', sc=3, sv=4, ev=6)]
        e_refs = expand_refs(refs)
        self.assertEqual(len(e_refs), 3, 'incorrect number of expanded refs')
        self.assertEqual(e_refs[0].st_book, 'Deuteronomium', 'st_book is not Deuteronomium')
        self.assertIsNone(e_refs[0].end_book, 'end_book is not None')
        self.assertEqual(e_refs[0].st_ch, 3, 'wrong chapter')
        self.assertIsNone(e_refs[0].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[0].st_vs, 4, 'wrong verse')
        self.assertIsNone(e_refs[0].end_vs, 'end_vs is not None')

        self.assertEqual(e_refs[1].st_book, 'Deuteronomium', 'st_book is not Deuteronomium')
        self.assertIsNone(e_refs[1].end_book, 'end_book is not None')
        self.assertEqual(e_refs[1].st_ch, 3, 'wrong chapter')
        self.assertIsNone(e_refs[1].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[1].st_vs, 5, 'wrong verse')
        self.assertIsNone(e_refs[1].end_vs, 'end_vs is not None')
        
        self.assertEqual(e_refs[2].st_book, 'Deuteronomium', 'st_book is not Deuteronomium')
        self.assertIsNone(e_refs[2].end_book, 'end_book is not None')
        self.assertEqual(e_refs[2].st_ch, 3, 'wrong chapter')
        self.assertIsNone(e_refs[2].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[2].st_vs, 6, 'wrong verse')
        self.assertIsNone(e_refs[2].end_vs, 'end_vs is not None')

    def testExpandList(self):
        refs = [Ref(ReferenceFormID.ETCBCH,
                    'Deuteronomium', sc=3, sv=4, ev=6),
                Ref(ReferenceFormID.ETCBCH,
                    'Exodus', sc=6, sv=1, ev=7)]
        e_refs = expand_refs(refs)
        self.assertEqual(len(e_refs), 10, 'incorrect number of expanded refs')
        self.assertEqual(e_refs[0].st_book, 'Deuteronomium', 'st_book is not Deuteronomium')
        self.assertIsNone(e_refs[0].end_book, 'end_book is not None')
        self.assertEqual(e_refs[0].st_ch, 3, 'wrong chapter')
        self.assertIsNone(e_refs[0].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[0].st_vs, 4, 'wrong verse')
        self.assertIsNone(e_refs[0].end_vs, 'end_vs is not None')

        self.assertEqual(e_refs[1].st_book, 'Deuteronomium', 'st_book is not Deuteronomium')
        self.assertIsNone(e_refs[1].end_book, 'end_book is not None')
        self.assertEqual(e_refs[1].st_ch, 3, 'wrong chapter')
        self.assertIsNone(e_refs[1].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[1].st_vs, 5, 'wrong verse')
        self.assertIsNone(e_refs[1].end_vs, 'end_vs is not None')
        
        self.assertEqual(e_refs[2].st_book, 'Deuteronomium', 'st_book is not Deuteronomium')
        self.assertIsNone(e_refs[2].end_book, 'end_book is not None')
        self.assertEqual(e_refs[2].st_ch, 3, 'wrong chapter')
        self.assertIsNone(e_refs[2].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[2].st_vs, 6, 'wrong verse')
        self.assertIsNone(e_refs[2].end_vs, 'end_vs is not None')
    
        self.assertEqual(e_refs[3].st_book, 'Exodus', 'st_book is not Exodus')
        self.assertIsNone(e_refs[3].end_book, 'end_book is not None')
        self.assertEqual(e_refs[3].st_ch, 6, 'wrong chapter')
        self.assertIsNone(e_refs[3].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[3].st_vs, 1, 'wrong verse')
        self.assertIsNone(e_refs[3].end_vs, 'end_vs is not None')
    
        self.assertEqual(e_refs[4].st_book, 'Exodus', 'st_book is not Exodus')
        self.assertIsNone(e_refs[4].end_book, 'end_book is not None')
        self.assertEqual(e_refs[4].st_ch, 6, 'wrong chapter')
        self.assertIsNone(e_refs[4].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[4].st_vs, 2, 'wrong verse')
        self.assertIsNone(e_refs[4].end_vs, 'end_vs is not None')
    
        self.assertEqual(e_refs[9].st_book, 'Exodus', 'st_book is not Exodus')
        self.assertIsNone(e_refs[9].end_book, 'end_book is not None')
        self.assertEqual(e_refs[9].st_ch, 6, 'wrong chapter')
        self.assertIsNone(e_refs[9].end_ch, 'end_ch is not None')
        self.assertEqual(e_refs[9].st_vs, 7, 'wrong verse')
        self.assertIsNone(e_refs[9].end_vs, 'end_vs is not None')
    
    def testExpandChapter(self):
        with self.assertRaises(Exception) as expected_ex:
            refs = [Ref(ReferenceFormID.ETCBCH,
                        'Deuteronomium', sc=3, ec=4, sv=4, ev=6)]
            expand_refs(refs)

        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'chapter range expansion not yet implemented')        
    
    def testExpandEndBook(self):
        with self.assertRaises(Exception) as expected_ex:
            refs = [Ref(ReferenceFormID.ETCBCH,
                        'Deuteronomium', 'Exodus', sc=3, sv=4)]
            expand_refs(refs)
            
        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'book range expansion not yet implemented')        
             
    def testRefBadCh(self):
        with self.assertRaises(Exception) as expected_ex:
            Ref(ReferenceFormID.ETCBCH,
                'Deuteronomium', 'Exodus', sc=3, ec=2)
            
        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'ending vs 2 is before the starting vs 3')        

    def testRefBadVs(self):
        with self.assertRaises(Exception) as expected_ex:
            Ref(ReferenceFormID.ETCBCH,
                'Deuteronomium', 'Exodus', sv=3, ev=2)
            
        ex = expected_ex.exception
        self.assertEqual(str(ex),
                         'ending vs 2 is before the starting vs 3')        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()