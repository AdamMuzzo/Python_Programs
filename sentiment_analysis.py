#Creates dictionary of keywords and their values
def read_keywords(keyword_file_name):

    keyword_dict = {}
    try:
        with open(keyword_file_name, "r") as file:
            #loop through each line in the file
            for line in file:
                #Create a temporary list with the keywords and values split at each tab
                temp_list = line.split("\t")
                #update the keyword_dictionary
                keyword_dict[temp_list[0]] = temp_list[1]
    #if file does not exist
    except IOError :
        print("Could not open file", keyword_file_name)


    #Should return a dict of keywords
    return keyword_dict

#Cleans the tweet text by removing unwanted characters
def clean_tweet_text(tweet_text):

    clean_text = ""

    #loop through each character in tweet_text
    for c in tweet_text:
        #if each character is in the alphabet or a space 
        if c.isalpha() or c == " ":
            c = c.lower()
            clean_text += c

    tweet_text = clean_text
    #Should return a string with the cleean tweet text
    return tweet_text

#Calculates sentiment of a tweet text using the keyword dictionary
def calc_sentiment(tweet_text, keyword_dict):

    #Split the text into an list
    new_text = tweet_text.split()
    sentiment = 0

    #loop through the length of the new file
    for i in range(len(new_text)):
        #if the word exists in the keyword dictionary
        if new_text[i] in keyword_dict.keys():
            sentiment += int(keyword_dict[new_text[i]])

    #Should return an integer value
    return sentiment

#Classifies the sentiment score
def classify(score):

    if score > 0:
        return "positive"
    elif score < 0: 
        return "negative"
    else:
        return "neutral"

    #Should return a String
    return

#Reads the tweets and creates a list of dictionaries for each tweet
def read_tweets(tweet_file_name):

    tweet_list = []
    try: 
        #open the file using 'with' for convenience
        with open(tweet_file_name, "r") as file:
            #loop through each line in the tweet file
            for line in file:
                #split at each comma
                mylist = (line.split(","))
                try:
                    tweet_list.append({
                            "city": str(mylist[8]),
                            "country": str(mylist[6]),
                            "date": str(mylist[0]),
                            "favorite": int(mylist[4]),
                            "lang": str(mylist[5]),
                            "lat": float(mylist[9]),
                            "lon": float(mylist[10]),
                            "retweet": int(mylist[3]),
                            "state": str(mylist[7]),
                            "text": str(clean_tweet_text(mylist[1])),  #Use clean tweet function
                            "user": str(mylist[2])
                        }
                    )
                #if the lang or lat given is NULL, must be string casted
                except ValueError:
                    tweet_list.append({
                            "city": str(mylist[8]),
                            "country": str(mylist[6]),
                            "date": str(mylist[0]),
                            "favorite": int(mylist[4]),
                            "lang": str(mylist[5]),
                            "lat": str(mylist[9]),
                            "lon": str(mylist[10]),
                            "retweet": int(mylist[3]),
                            "state": str(mylist[7]),
                            "text": str(clean_tweet_text(mylist[1])),  #Use clean tweet function
                            "user": str(mylist[2])
                        }
                    )
    #if tweet file does not exist
    except IOError :
        print("Could not open file", tweet_file_name)

    #Should return a list with a dictionary for each tweet
    return tweet_list

#Calculates the report values and stores them in a dictionary
def make_report(tweet_list, keyword_dict):

    report_dict = {
        'avg_favorite': 0,
        'avg_retweet': 0,
        'avg_sentiment': 0,
        'num_favorite': 0,
        'num_negative': 0,
        'num_neutral': 0,
        'num_positive': 0,
        'num_retweet': 0,
        'num_tweets': 0,
        'top_five': ""
    }

    #Saves a current score for the classification of each tweets (positive, negative, neutral)
    current_score = 0

    #Num Tweets
    report_dict['num_tweets'] = len(tweet_list)

    #loop through the length of the tweet list
    for i in range(len(tweet_list)):

        #Avg Sentiment of all tweets [float]
        report_dict['avg_sentiment'] += round(calc_sentiment(tweet_list[i]['text'], keyword_dict),2)

        #Num of positive,negative, or neutral tweets [int]
        current_score = calc_sentiment(tweet_list[i]['text'], keyword_dict)
        result = classify(current_score)
        #num positive tweets
        if result == "positive":
            report_dict['num_positive'] += 1
        #num negative tweets
        elif result == "negative":
            report_dict['num_negative'] += 1
        #num neutral tweets
        else :
            report_dict['num_neutral'] += 1

        #Num of favorited tweets [int]
        if tweet_list[i]['favorite'] > 0:
            #stores a total for avg_favorite tweets
            report_dict['avg_favorite'] += calc_sentiment(tweet_list[i]['text'], keyword_dict)
            report_dict['num_favorite'] += 1

        #Num of rewteeted tweets [int]
        if tweet_list[i]['retweet'] > 0:
            #stores a total for avg_retweeted tweets
            report_dict['avg_retweet'] += calc_sentiment(tweet_list[i]['text'], keyword_dict)
            report_dict['num_retweet'] += 1
    
    #Avg favorited tweets
    try:
        report_dict['avg_favorite'] = round(report_dict['avg_favorite']/report_dict['num_favorite'],2)
    #if an attempt to divide by 0 is made
    except ZeroDivisionError:
        report_dict['avg_favorite'] = "NAN"

    #Avg Sentiment
    try:
        report_dict['avg_sentiment'] = round(report_dict['avg_sentiment']/report_dict['num_tweets'],2)
    #if an attempt to divide by 0 is made
    except ZeroDivisionError:
        report_dict['avg_sentiment'] = "NAN"

    #Avg retweets
    try:
        report_dict['avg_retweet'] = round(report_dict['avg_retweet']/report_dict['num_retweet'],2)
    #if an attempt to divide by 0 is made
    except ZeroDivisionError:
        report_dict['avg_retweet'] = "NAN"

    #top five countries 
    countries_dict = {}

    #loop through the length of the tweet list
    for i in range(len(tweet_list)):
        #if country does not exist
        if tweet_list[i]['country'] not in countries_dict:
            #first update the dictionary by adding a new country
            countries_dict.update({tweet_list[i]['country']: [0,0]})
            #then update the calc sentiment total and counter (the counter will later be used to calculate the average)
            countries_dict[tweet_list[i]['country']][0] += calc_sentiment(tweet_list[i]['text'], keyword_dict)
            countries_dict[tweet_list[i]['country']][1] += 1
            
        #if country does exist
        else :
            countries_dict[tweet_list[i]['country']][0] += calc_sentiment(tweet_list[i]['text'], keyword_dict)
            countries_dict[tweet_list[i]['country']][1] += 1

    #loop through the keys of the countries dictionary
    for k in countries_dict.keys():    
        #append a third element to the list inside the dictionary which stores the average sentiment for each country   
        countries_dict[k].append(round(countries_dict[k][0]/countries_dict[k][1],2))

    #Remove the Key titled 'NULL' along with its values
    countries_dict.pop("NULL", None)

    #stores a sorted dictionary 
    sorted_countries = dict(sorted(countries_dict.items(), key = lambda x: x[1][2], reverse = True))
    #stores a list of keys of the sorted dictionary
    sorted_countries_list = list(sorted_countries.keys())

    #removes elements of the list whose index is greater than 4
    while len(sorted_countries_list) > 5:
        sorted_countries_list.pop()
    
    countries_string = ', '.join(sorted_countries_list)

    #store the string in the report dictionary
    report_dict['top_five'] = countries_string


    #Should return a dictionary containing the report values
    return report_dict

#Writes the values of the dictionary to a file
def write_report(report, output_file):

    #attempt to write all the values to the file given by the user
    try:
        with open(output_file, "w") as outfile:
            outfile.write("Average sentiment of all tweets: " + str(report['avg_sentiment']) + "\n")
            outfile.write("Total number of tweets: " + str(report['num_tweets']) + "\n")
            outfile.write("Number of positive tweets: " + str(report['num_positive']) + "\n")
            outfile.write("Number of negative tweets: " + str(report['num_negative']) + "\n")
            outfile.write("Number of neutral tweets: " + str(report['num_neutral']) + "\n")
            outfile.write("Number of favorited tweets: " + str(report['num_favorite']) + "\n")
            outfile.write("Average sentiment of favorited tweets: " + str(report['avg_favorite']) + "\n")
            outfile.write("Number of retweeted tweets: " + str(report['num_retweet']) + "\n")
            outfile.write("Average sentiment of retweeted tweets: " + str(report['avg_retweet']) + "\n")
            outfile.write("Top five countries by average sentiment: " + str(report['top_five']))

            print("Wrote report to", output_file)
    #if file does not exist
    except IOError :
        print("Could not open file", output_file)

    #Should write the report to the output_file.
    return
