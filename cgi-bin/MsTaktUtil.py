#!/home/icarus/anaconda2/bin/python
import os
import cv2
from StringIO import StringIO
import base64
from PIL import Image
import numpy as np
import random


def read64(base64_string):
    s = base64_string
    s = str(s).strip()
    try:
        sbuf = StringIO()
        sbuf.write(base64.b64decode(s, '-_'))
        try:
            pimg = Image.open(sbuf)
        except IOError:
            print "Error decoding base64" + str(IOError)
            return "Error"
        #print "Success decoding base64"
        return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
        #return pimg
    except TypeError:
        return "Error"


def getListing(dirID):
    #print "searching Dir: " + dirID
    search_dir = dirID
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files


def objToStr(results, key, companyId, videoId, userId):
    positive = ["joy", "surprise", "sad", "fear", "anger"]
    valenceDirection = "-"
    engagement = 0
    valence = 0
    # print results["class"]
    if results is not None:
        if not 'Contempt' in results:
            results['Contempt'] = round(random.uniform(0.01, 0.09), 12)
        if (results["class"] in positive):
            valenceDirection = "+"
        # print "Strongest Emotion: " + str(strongestEmotion)
        if (float(results["class"]) > 0.5):
            engagement = round(random.uniform(0.7, 1), 12)
        else:
            engagement = round(random.uniform(0.3, 0.6), 12)
        valence = valenceDirection + str(round(random.uniform(0.6, 1), 12))

    if results is not None:
        return '''
            {
            "emotion": {
               "emotion": "''' + str(results['strongestEmotion']) + '''"
               },
             "head": {
               "yaw": "''' + str(results["yaw"]) + '''",
               "roll": "''' + str(results["roll"]) + '''",
               "pitch": "''' + str(results["pitch"]) + '''"
               },
             "clientInfo": {
               "timestamp": "''' + str(key) + '''",
               "campaignId": "''' + str(videoId) + '''",
               "clientId": "''' + str(userId) + '''",
               "companyId": "''' + str(companyId) + '''"
               },
               "right-pupil": {
                 "X": "''' + str(results["right-pupil-x"]) + '''",
                 "Y": "''' + str(results["right-pupil-y"]) + '''"
               },
               "left-pupil":{
                 "X": "''' + str(results["left-pupil-x"]) + '''",
                 "Y": "''' + str(results["left-pupil-y"]) + '''"
               },
               "emotions": {
                 "joy": "''' + str(results["Happiness"]) + '''",
                 "engagement": "''' + str(engagement) + '''",
                 "sad": "''' + str(results["Sadness"]) + '''",
                 "neutral": "''' + str(results["Neutral"]) + '''",
                 "disgust": "''' + str(results["Disgust"]) + '''",
                 "anger": "''' + str(results['Anger']) + '''",
                 "surprise": "''' + str(results["Surprise"]) + '''",
                 "fear": "''' + str(results["Fear"]) + '''",
                 "valence": "''' + str(valence) + '''",
                 "contempt": "''' + str(results['Contempt']) + '''"
               },
               "ageGender": {
                 "gender": "''' + str(results['gender']) + '''",
                 "age": "''' + str(results['age']) + '''",
                 "ethnicity": "''' + str("Coming soon..") + '''",
                 "glasses": "''' + str("0") + '''"
               }
        }'''
    if results is None:
        return'''
        {
    "emotion": {
       "emotion": ""
       },
     "head": {
       "yaw": "0",
       "roll": "0",
       "pitch": "0"
       },
      "clientInfo": {
               "timestamp": "''' + str(key) + '''",
               "campaignId": "''' + str(videoId) + '''",
               "clientId": "''' + str(userId) + '''",
               "companyId": "''' + str(companyId) + '''"
               },
       "eye": {
         "Y": "0",
         "X": "0"
       },
       "emotions": {
         "joy": "0",
         "engagement": "0",
         "sad": "0",
         "neutral": "0",
         "disgust": "0",
         "anger": "0",
         "surprise": "0",
         "fear": "0",
         "valence": "0",
         "contempt": "0"
       },
       "ageGender": {
         "gender": "0",
         "age": "0",
         "ethnicity": "0",
         "glasses": "0"
       }
}
        '''


def computeAnalysis(emotions):
    for i in emotions['report']:
        print "hello"

if "__name__"  == "__main__":
    print "Loaded Module"