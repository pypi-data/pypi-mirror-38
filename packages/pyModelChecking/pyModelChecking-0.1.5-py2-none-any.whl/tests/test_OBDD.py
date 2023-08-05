#!/usr/bin/env python

from pyModelChecking.BDD import *

import unittest

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

class TestOBDD(unittest.TestCase):
    def setUp(self):
        self.a=BDDNode('a',BDDNode(0),BDDNode(True))
        self.b=BDDNode('a',BDDNode(True),BDDNode(False))
        self.c=BDDNode('c',self.b,BDDNode(False))
        self.d=BDDNode('b',BDDNode(1),BDDNode(0))

        self.ordering=['c','a']

    def test_BDD(self):
        for (bdd,text,vars) in [(self.a,'a',['a']),
                                (self.b,'~a',['a']),
                                (self.c,'~c & ~a',['a','c']),
                                (self.d,'~b',['b'])]:

            self.assertEquals('%s' % (bdd),text)
            self.assertEquals(bdd.variables(),set(vars))

        get_ancestors=(lambda :['%s' % BDD for BDD in BDDNode.nodes()])

        before_e=get_ancestors()

        e=BDDNode('r',BDDNode('c',self.d,self.a),BDDNode('h',self.a,self.d))

        with_e=get_ancestors()

        e=None

        after_e=get_ancestors()

        self.assertEquals(before_e,after_e)
        self.assertNotEquals(with_e,after_e)

    def test_OBDD(self):
        oa=OBDD(self.a,self.ordering)
        ob=OBDD(self.c,self.ordering)

        for (obdd,text,vars) in [(oa,'lambda c,a: a',['a']),
                                 (ob,'lambda c,a: ~c & ~a',['a','c']),
                                 (ob.restrict('c',False),'lambda c,a: ~a',['a']),
                                 (ob.restrict('c',1),'lambda c,a: 0',[]),
                                 (ob.restrict('a',0),'lambda c,a: ~c',['c']),
                                 (ob.restrict('a',True),'lambda c,a: 0',[]),
                                 (~ob,'lambda c,a: (~c & a) | (c)',['a','c']),
                                 (oa&ob,'lambda c,a: 0',[]),
                                 (oa|ob,'lambda c,a: (~c) | (c & a)',['a','c']),
                                 (~(oa&ob)|(oa|ob),'lambda c,a: 1',[])]:
            self.assertEquals('%s' % (obdd),text)
            self.assertEquals(obdd.variables(),set(vars))

        self.assertEquals(ob.restrict('a',True),0)
        self.assertEquals(~(oa&ob)|(oa|ob),1)

        with self.assertRaises(RuntimeError):
            OBDD(self.d,self.ordering)

    def test_OBDD_parser(self):
        oa=OBDD(self.a,self.ordering)
        ob=OBDD(self.c,self.ordering)

        for obdd in [oa,ob,~ob,oa&ob, oa|ob, ~(oa&ob)|(oa|ob)]:
            self.assertEquals(OBDD('%s' % (obdd.root),self.ordering),obdd)

        for (a,b) in [('a & ~a','0'),
                      ('a | ~a','1'),
                      ('~a | c','~(a & ~c)'),
                      ('~~~~a','a'),
                      ('~(~a|~c)','a&c')]:
            self.assertEquals(OBDD(a,self.ordering),OBDD(b,self.ordering))

        with self.assertRaises(RuntimeError):
            OBDD('a|~b',self.ordering)

        with self.assertRaises(RuntimeError):
            OBDD('lambda c,a: a|~b')

if __name__ == '__main__':
    unittest.main()
