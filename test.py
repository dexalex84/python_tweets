import getopt
import sqlite3, json,sys

ARG_LOAD = 'load'
ARG_CALCULATE = 'calculate'

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None

def getArgs(argv):
    print('Number of arguments:', len(argv), 'arguments.')
    print(argv)

    database = "none"
    operation = "none"

    try:
        opts, args = getopt.getopt(argv, "d:o:", ["database=", "operation="])
    except getopt.GetoptError:
        print('test.py -d <database> -o <operation>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-d", "--database"):
            database = arg
        elif opt in ("-o", "--operation"):
            operation = arg

    if database == "none":
        print('database was not set!')
        print('test.py -d <database> -o <operation>')
        sys.exit(2)
    else:
        print('database is "'+database+'"')

    if operation == "none":
        print('operation was not set!')
        print('test.py -d <database> -o <operation>')
        print('operation = "'+ARG_LOAD+'": only load table; operation = "'+ARG_CALCULATE+'": calculate tweet_sentiment')
        sys.exit(2)
    else:
        print('operation is "'+operation+'"')

    if operation != ARG_CALCULATE and operation != ARG_LOAD:
        print('arguments are wrong!')
        print('operation = "' + ARG_LOAD + '": only load table; operation = "' + ARG_CALCULATE + '": calculate tweet_sentiment')
    return database, operation

def main(argv):
    database, operation = getArgs(argv)

    quit()

    from pprint import pprint

    #with open('C:\\mts\\Documents_\\three_minutes_tweets.json') as data_file:
    #f = open('C:\\mts\\Documents_\\three_minutes_tweets.json.txt','r')
    f = open('C:\\mts\\Documents_\\text.txt','r')


    # name, tweet_text, country_code, display_url, lang, created_at, location

    for line in f:
        json_str = json.loads(line)
        print(json_str)

        name = ""
        country_code = ""
        id = ""
        tweet_text = ""
        lang = ""
        location = ""
        display_url = ""
        created_at = ""

        try:
            name = json_str['user']['name']
        except:
            pass

        try:
            country_code = json_str['place']['country_code']
        except:
            pass

        try:
            id = json_str['id']
        except:
            pass

        try:
            tweet_text = json_str['text']
        except:
            pass

        try:
            lang = json_str['lang']
        except:
            pass

        try:
            location = json_str['location']
        except:
            pass


        try:
            display_url = json_str['url']
        except:
            pass

        try:
            created_at = json_str['created_at']
        except:
            pass

    print(location)


    f.close()

    #data = json.load(data_file)

    #pprint(data)


main(sys.argv[1:])