from __future__ import print_function
import phrasefinder as pf

def main():
    # Do queries need a question mark section???
    query = 'This is a ???'

    # Set phrasefinder options
    batch = pf.BatchRequest()

    batch.params = {'key'   : 'ADD API KEY',
                    'corpus': pf.Corpus.AMERICAN_ENGLISH,
                    'topk'  : 3}

    batch.requests.append({'query': 'Item1'})
    batch.requests.append({'query': 'Item2'})


    try:
        result = batch.execute()
        for request, result in zip(batch.requests, results):
            print("query: {}".format(request['query'])

            if result.error_message:
                print('Request was not successful: {}'.format(result.error_message))
                return

            for phrase in result.phrases:
                print("{0:6f}".format(phrase.score), end="")
                for token in phrase.tokens:
                    print(" {}".format(token.text), end="")
                print()

    except Exception as error:
        print('Fatal error: {}'.format(error))

if __name__=='__main__':
    main()
