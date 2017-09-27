import getopt
import sqlite3
import json
import sys
import re

ARG_LOAD = 'load'
ARG_CALCULATE = 'calculate'
CONST_NONE = 'none'


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

    database = CONST_NONE
    operation = CONST_NONE
    tweet_file = CONST_NONE
    words_file = CONST_NONE
    retweeted = 0

    try:
        opts, args = getopt.getopt(argv, "d:o:t:w:r", ["database=", "operation=", "tweet_file=", "words_file=", "retweeted="])
    except getopt.GetoptError:
        print('test.py -d <database> -o <operation> -t <tweet_file> -w <words_file> -r')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-d", "--database"):
            database = arg
        elif opt in ("-o", "--operation"):
            operation = arg
        elif opt in ("-t", "--tweet_file"):
            tweet_file = arg
        elif opt in ("-w", "--words_file"):
            words_file = arg
        elif opt in ("-r", "--retweeted"):
            retweeted = 1

    if tweet_file == CONST_NONE:
        print('tweet_file was not set!')
        print('test.py -d <database> -o <operation> -t <tweet_file> -w <words_file>')
        sys.exit(2)
    else:
        print('database is "' + database + '"')

    if database == CONST_NONE:
        print('database was not set!')
        print('test.py -d <database> -o <operation> -t <tweet_file> -w <words_file>')
        sys.exit(2)
    else:
        print('database is "' + database + '"')

    if operation == CONST_NONE:
        print('operation was not set!')
        print('test.py -d <database> -o <operation>')
        print(
            'operation = "' + ARG_LOAD + '": only load table; operation = "' + ARG_CALCULATE + '": calculate tweet_sentiment')
        sys.exit(2)
    else:
        print('operation is "' + operation + '"')

    if operation != ARG_CALCULATE and operation != ARG_LOAD:
        print('arguments are wrong!')
        print(
            'operation = "' + ARG_LOAD + '": only load table; operation = "' + ARG_CALCULATE + '": calculate tweet_sentiment')

    if operation == ARG_CALCULATE and words_file == CONST_NONE:
        print('arguments are wrong!')
        print('please set "words_file" argument')
    return database, operation, tweet_file, words_file, retweeted


def loadTweet(json_str, get_retweeted_status):
    name = ""
    country_code = ""
    tweet_id = 0
    tweet_text = ""
    lang = ""
    location = ""
    display_url = ""
    created_at = ""

    tweet_row = []
    #country_codes = []
    #locations = []
    display_urls = []

    if get_retweeted_status == 1:
        json_str_final = json_str['retweeted_status']
    else:
        json_str_final = json_str

    try:
        name = json_str_final['user']['name']
    except:
        pass

    try:
        country_code = json_str_final['place']['country_code']
    except:
        pass

    try:
        tweet_text = json_str_final['text']
    except:
        pass

    try:
        lang = json_str_final['lang']
    except:
        pass

    try:
        location = json_str_final['user']['location']
    except:
        pass

    try:
        # if json has multiple tags display_url store it in collection
        for ent in json_str_final['entities']['media']:
            display_urls.append(ent['display_url'])
    except:
        pass

    try:
        created_at = json_str_final['created_at']
    except:
        pass

    max_rows = len(display_urls)

    if max_rows > 1:
        print(name)

    if max_rows <= 0:
        max_rows = 1

    for i in range(0, max_rows):
        if i <= len(display_urls) and len(display_urls) > 0:
            display_url = display_urls[i]
        else:
            display_url = ""

        tweet = name, tweet_text, country_code, display_url, lang, created_at, location
        tweet_row.append(tweet)

    return tweet_row


def main(argv):
    database, operation, tweet_file, words_file, retweeted = getArgs(argv)
    conn = create_connection(database)

    if operation == ARG_LOAD:

        try:
            f = open(tweet_file, 'r')
        except IOError as e:
            print("I/O error ({0}): {1}".format(e.errno, e.strerror))
            print('Exit')
            sys.exit(2)
        except:
            print('Unresolved error. Exit')
            sys.exit(2)

        sql = ''' insert into tweet(name, tweet_text, country_code, display_url, lang, created_at, location)
                  values(?, ?, ?, ?, ?, ?, ?)  
                      '''

        table = []
        retweeted_rows = []
        tweet_rows = []

        cnt = 0

        # make loop through all lines
        for line in f:
            # get current line and convert to json
            json_str = json.loads(line)

            # skip unnecessary rows
            if 'delete' in json_str:
                continue

            tweet_rows_all = []

            if retweeted == 0:
                # get tweet table rows
                tweet_rows = loadTweet(json_str, 0)

                if len(tweet_rows) > 0:
                    for i in tweet_rows:
                        tweet_rows_all.append(i)
            else:
                # get tweet table rows from retweeted_status tag (additional twitter info)
                try:
                    if json_str['retweeted_status']:
                        retweeted_rows = loadTweet(json_str, 1)
                except:
                    pass

                if len(retweeted_rows) > 0:
                    for j in retweeted_rows:
                        tweet_rows_all.append(j)

            # remove full duplicates and store in table list
            for tra in list(set(tweet_rows_all)):
                table.append(tra)

            # count all rows
            cnt = cnt + len(tweet_rows_all)


        # save to DB
        cur = conn.cursor()
        cur.executemany(sql, table)
        conn.commit()


        print('Inserted {0} rows'.format(cnt))
        f.close()

    if operation == ARG_CALCULATE:
        words_dic = {}

        # load words file
        try:
            words_f = open(words_file, 'r')
        except IOError as e:
            print("I/O error ({0}): {1}".format(e.errno, e.strerror))
            print('Exit')
            sys.exit(2)
        except:
            print('Unresolved error. Exit')
            sys.exit(2)

        # load words to dictionary
        for word in words_f:
            pair = re.split(r'\t+', word.rstrip('\t'))
            words_dic[pair[0]] = int(pair[1])
            words_set = set(words_dic)

        # load tweet text from DB
        sql_norm = 'select id, tweet_text from tweet_norm'
        cur = conn.cursor()
        cur.execute(sql_norm)
        rows = cur.fetchall()

        tweet_sentiment_tab = []
        calc_rows = 0

        # loop through all rows in table
        for row in rows:
            # TODO possible make better trail spaces removing
            sentence = row[1].lower().strip()
            tweet_sentiment = 0
            # loop through all words in twitter text
            for key in sentence.split():
                # find in set to make faster
                if key in words_set:
                    # if found count of word occurrences
                    m = re.findall('\\b' + key + '\\b', sentence, re.IGNORECASE)
                    tweet_sentiment = tweet_sentiment + len(m) * words_dic[key]
                    print('tweet_sentiment {0}'.format(tweet_sentiment))
                    # store update information in table
                    tweet_sentiment_tab_row = int(tweet_sentiment), int(row[0])
                    tweet_sentiment_tab.append(tweet_sentiment_tab_row)

            # debug info
            calc_rows += 1
            print(calc_rows)
        # update field tweet_sentiment
        sql_update = 'update tweet_norm set tweet_sentiment = ? where id = ?'
        cur_update = conn.cursor()
        cur_update.executemany(sql_update, tweet_sentiment_tab)

        conn.commit()
        cur_update.close()

        words_f.close()

    # close file and DB
    conn.close()

if __name__ == '__main__':
    main(sys.argv[1:])
