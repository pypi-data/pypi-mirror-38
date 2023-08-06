import pycor.resolver as resolver
import pycor.utils as utils
import pycor.speechmodel as sm


__all__ = ["CollocationResolver"]

class CollocationContext(sm.ContextWrapper):
    def __init__(self, parent):
        super().__init__(parent)
        self.collocations = {}

    def getcollocation(self, text):
        col = self.collocations.get(text)
        if col is None:
            col =  self.parent.getcollocation(text)
        return col
    
    def addcollocation(self, collocation):
        if self.collocations.get(collocation.text) is None:
            self.collocations[collocation.text] = collocation

    def clear(self):
        self.collocations.clear()

class CollocationResolver(resolver.Resolver):
    def resolveDocument(self, sentence_array, context):
        cascadingContext = CollocationContext(context)

        for sentence in sentence_array:
            self.resolveSentence(sentence, cascadingContext)
        
        for colloc in cascadingContext.collocations.values():
            if colloc.frequency > 1:
                # print(colloc, colloc.frequency)
                context.addcollocation(colloc)
    
    def resolveSentence(self,sentence, context):
        end = len(sentence.pairs) - 1 
        index = 0

        while index < end:
            first, index = self.gettext(sentence, index, context)
            
            if first is None:
                continue

            if index >= end:
                break

            second, index2 = self.gettext(sentence, index, context, True)

            if second is None:
                continue

            bigramTxt = ' '.join([second,first])

            bigram = context.getcollocation(bigramTxt)
            if bigram is None:
                bigram = sm.CollocationHead([second,first])
                context.addcollocation(bigram)
            bigram.freq()

            if index < end :
                second2, index2 = self.gettext(sentence, index, context)
                if index2 >= end:
                    break

                third, _ = self.gettext(sentence, index2, context, True)

                if third is None:
                    continue
                
                trigramTxt = ' '.join([third,second2,first])

                trigram = context.getcollocation(trigramTxt)
                if trigram is None:
                    trigram = sm.CollocationHead([third,second2,first])
                    context.addcollocation(trigram)
                trigram.freq()
        return sentence


    def gettext(self, sentence, index, context, islast=False):
        pair = sentence.pairs[index]

        if type(pair) is sm.Sentence :
            self.resolveSentence(pair, context)
            return str(pair), index +1
        elif type(pair) is sm.Quote :
            if(pair.quotetype == sm.QUOTE_TYPE_EQUIV):
                return str(pair.text) , index+1
            else:
                return None, index+1
        else:
            if islast :
                return pair.head.text, index+1
            else:
                return str(pair.text) , index+1
