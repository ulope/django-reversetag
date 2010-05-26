from django.test import TestCase
from django.template import Template
from django.template.context import Context
from django.core.urlresolvers import NoReverseMatch


class ReversetagTest(TestCase):
    def test_base(self):        
        t1 = Template("""{% load reversetag %}{% reverse "URL1" %}""")
        self.assertEqual(t1.render(Context()), u"/T1/")

        t2 = Template("""{% load reversetag %}{% reverse "URL2" 1 %}""")
        self.assertEqual(t2.render(Context()), u"/T2/1/")

        t3 = Template("""{% load reversetag %}{% reverse "URL3" x=1,y=2,z=3 %}""")
        self.assertEqual(t3.render(Context()), u"/T3/1/2/3/")

        t4 = Template("""{% load reversetag %}{% with "URL1" as somevar %}{% reverse somevar %}{% endwith %}""")
        self.assertEqual(t4.render(Context()), u"/T1/")

    def test_failures(self):
        t1 = Template("""{% load reversetag %}{% reverse "NOURL1" %}""")
        self.assertRaises(NoReverseMatch, t1.render, Context())
    
        t2 = Template("""{% load reversetag %}{% reverse "URL2" x %}""")
        self.assertRaises(NoReverseMatch, t2.render, Context())

        t3 = Template("""{% load reversetag %}{% reverse "URL3" x=a,y=b,z=c %}""")
        self.assertRaises(NoReverseMatch, t3.render, Context())


    def test_partial(self):
        t1 = Template("""{% load reversetag %}{% reverse partial "URL1" as P1 %}{% reverse P1 %}""")
        self.assertEqual(t1.render(Context()), u"/T1/")

        t2 = Template("""{% load reversetag %}{% reverse partial "URL3" as P3 %}{% reverse P3 x=1,y=2,z=3 %}""")
        self.assertEqual(t2.render(Context()), u"/T3/1/2/3/")

        t3 = Template("""{% load reversetag %}{% reverse partial "URL3" as P3 %}{% reverse partial P3 x=1 as P3_1 %}{% reverse partial P3_1 y=2 as P3_2 %}{% reverse P3_2 z=3 %}""")
        self.assertEqual(t3.render(Context()), u"/T3/1/2/3/")

    def test_loop(self):
        t3 = Template("""{% load reversetag %}{% reverse partial "URL3" as P3 %}{% reverse partial P3 x=1 as P3_1 %}{% reverse partial P3_1 y=2 as P3_2 %}{% for VAR_X in values %}{% reverse P3_2 z=VAR_X %} {% endfor %}""")
        self.assertEqual(t3.render(Context({'values': [3,4,5]})), u"/T3/1/2/3/ /T3/1/2/4/ /T3/1/2/5/ ")
        