'''
Created on Jan 22, 2017

@author: Daniel
'''
import unittest
from bibleutils.versification import VersificationID, BookID, Identifier, \
     ReferenceFormID, parse_refs

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
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()