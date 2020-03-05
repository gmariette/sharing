import requests
import feedparser
import json

def getMediumInfo(blogPosts):
    # https://github.com/kurtmckee/feedparser/issues/84
    import ssl
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    ######## MEDIUM PART

    # Medium token
    mediumToken = "yourmediumtoken"

    # Set the headers
    headers = {
        'Authorization': "Bearer " + mediumToken,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    # Who is behind the token ?
    base_url = "https://api.medium.com/v1/"
    r = requests.get(base_url+'me', headers=headers)
    myUserJson = (r.json())

    # Get the feed with rss parsing
    newsFeed = feedparser.parse('https://medium.com/feed/@'+myUserJson['data']['username'])

    # List for all the blog posts
    for entry in newsFeed.entries:
        tags = []
        for tag in entry['tags']:
            tags.append(tag['term'])
        blogPosts.append({"title": entry['title'], "link": entry['id'], "published": entry['published'], "tags": tags})

    return blogPosts

def ShareContentOnLinkedin(myposttitle, myposturl, myposttags):

    ######## LINKEDIN PART

    # First generated a client_id and a client_secret within the app page on your linkedin account
    # Then follow this procedure to generate a code https://medium.com/@ellesmuse/how-to-get-a-linkedin-access-token-a53f9b62f0ce
    # Following code will allow you to get an access token ! use only once (token as to be generated every 60 days)

    # code = 'AQRcv5xzBHnY3E4yW4q961ZlRMVmt0MoBK_Cxx4nkueidU3fgri6lkN-8-irY9wc_l_HWMqdHhizIi6jTnrSa1JyctKKvk1Vp8XnftTLYWGQJgHVaIX4E9dO-XIfzCCxPHt9K3hjwPj8yTgwb8u1mrDlB9IvaYnbx5Z28o5b4xr_u70DOox3RrQ63mwqVg'

    # url = 'https://www.linkedin.com/oauth/v2/accessToken'
    # data = {"client_id": "yourclientid", "client_secret": "yourclientsecret", "grant_type": "authorization_code", "redirect_uri": "https://movingmarseille.wordpress.com/", "code": code}
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # r = requests.post(url, data=data, headers=headers)
    # print(r.content)

    # Then you will be able to post on linkedin

    access_token = "youraccesstoken"

    linkedinBaseUrl = 'https://api.linkedin.com/v2/'
    headers = {'Authorization': 'Bearer ' + access_token}
    r = requests.get(linkedinBaseUrl+'me?projection=(id)', headers=headers)
    linkedInProfile = r.json()

    #create the author variable in linkedin urn format
    author = "urn:li:person:"+linkedInProfile['id']

    api_url = linkedinBaseUrl+'ugcPosts'

    #concat all tags extracted from medium with an hashtag
    myTagsstr = ' #'.join(map(str, myposttags))

    post_data = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Check out my new Medium post : " + myposttitle + "\n" + myposturl + "\n #" + myTagsstr + "\n \n This was automaticaly posted from AWS Lambda"
                },
                "shareMediaCategory": "NONE"
            },
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }

    response = requests.post(api_url, headers=headers, json=post_data)

    if response.status_code == 201:
        print("Success")
        print(response.content)
    else:
        print(response.content)

def lambdaHandler(event, context):

    #Create an array variable to collect all medium informations
    blogPosts = []
    #Run the medium function, pass as parameter our empty list
    getMediumInfo(blogPosts)
    # Post on linkedin the latest result
    # Could be improved with a for loop - linkedin will answer a 4xx status code if you try to post a duplicate content
    ShareContentOnLinkedin(blogPosts[0]['title'], blogPosts[0]['link'], blogPosts[0]['tags'])

