
#from collections.abc import MutableSet
#import collections
#from nlglib.realisation.simplenlg.realisation import Realiser
#from nlglib.microplanning import *

#realise_en = Realiser(host='nlg.kutlak.info', port=40000)


"""def main():
    p = Clause("User", "create", "report")
    p['TENSE'] = 'PAST'
    # expected = 'María persigue un mono.'
    print(realise_en(p))
    p = Clause(NP("user"), VP("create"), NP("report"))
    subject = NP("user")
    objekt = NP("report")
    verb = VP("create")
    p.subject = subject
    p.predicate = verb
    p.object = objekt
    print(realise_en(p))
    p = Clause(NP('this', 'example'), VP('show', 'how cool simplenlg is'))
    # expected = This example shows how cool simplenlg is.
    print(realise_en(p))"""


#main()


#-------------------------------------------------

import inflect

p = inflect.engine()
word = "university"


print("Did you want ", p.a(word), " or ", p.an(word))
word = "employee"
print("Did you want ", p.a(word), " or ", p.an(word))
