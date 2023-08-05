import requests


# STRUCTURE = CSV EXPORT of the Google Sheet titled "Kolibri- Content structure"
################################################################################
GSHEETS_BASE = 'https://docs.google.com/spreadsheets/d/'
PRADIGI_SHEET_ID = '1kPOnTVZ5vwq038x1aQNlA2AFtliLIcc2Xk5Kxr852mg'
PRADIGI_STRUCTURE_SHEET_GID = '342105160'
PRADIGI_SHEET_CSV_URL = GSHEETS_BASE + PRADIGI_SHEET_ID + '/export?format=csv&gid=' + PRADIGI_STRUCTURE_SHEET_GID
PRADIGI_SHEET_CSV_PATH = 'chefdata/pradigi_structure.csv'
AGE_GROUP_KEY = 'Age Group'
SUBJECT_KEY = 'Subject'
RESOURCE_TYPE_KEY = 'Resource Type'
GAMENAME_KEY = 'Game Name'
TAKE_FROM_KEY = 'Take From Repo'
USE_ONLY_IN_KEY = 'Use Only In'
PRATHAM_COMMENTS_KEY = 'Pratham'
LE_COMMENTS_KEY = 'LE Comments'
PRADIGI_AGE_GROUPS = ['3-6 years', '6-10 years', '8-14 years', '14 and above']
PRADIGI_SUBJECTS = ['Mathematics', 'Language', 'English', 'Fun', 'Science', 'Health', 'Story',
                    'Beauty', 'Automobile', 'Hospitality', 'Electric',
                    'Healthcare', 'Construction',
                    "CRS128", #  "आदरातिथ्य",      # Hospitality
                    "CRS129", # "ऑटोमोटिव्ह",      # Automobile
                    "CRS130", # "ब्युटी",          # Beauty
                    "CRS131", # "इलेक्ट्रिकल",      # Electric
                    #
                    # Hindi games pages =  खेल
                    "CRS122", # "खेल-बाड़ी",      # Playground
                    "CRS124", # "देखो और करों",   # Look and
                    "CRS123", # "खेल-पुरी",       # Games
                    #
                    # Marathi games pages = खेळ
                    "CRS125", # "खेळ-वाडी",
                    "CRS127", # "बघा आणि शिका",
                    "CRS126", # "खेळ-पुरी",
                    'LanguageAndCommunication']
PRADIGI_RESOURCE_TYPES = ['Game', 'Website Resources']
# Note: can add 'Video Resources', 'Interactive Resoruces' and 'Book Resources'
# as separate categories for more flexibility in the future
PRADIGI_SHEET_CSV_FILEDNAMES = [
    AGE_GROUP_KEY,
    SUBJECT_KEY,
    RESOURCE_TYPE_KEY,
    GAMENAME_KEY,
    TAKE_FROM_KEY,
    USE_ONLY_IN_KEY,
    PRATHAM_COMMENTS_KEY,
    LE_COMMENTS_KEY,
]

# NEW: July 12 load data from separate sheet for English folder structure
PRADIGI_ENGLISH_STRUCTURE_SHEET_GID = '1812185465'
PRADIGI_ENGLISH_SHEET_CSV_URL = GSHEETS_BASE + PRADIGI_SHEET_ID + '/export?format=csv&gid=' + PRADIGI_ENGLISH_STRUCTURE_SHEET_GID
PRADIGI_ENGLISH_SHEET_CSV_PATH = 'chefdata/pradigi_english_structure.csv'




def apply_corrections()
    pass




url = "http://localhost:8080/api/contentnode"

import requests

[{"title":"Topic 1","id":"bc8be361e6be4ada8bc793080b6f24d5", "tags":[], "assessment_items":[], "prerequisite":[], "kind":"topic", "parent":"7463b0d9f11a441b8898ef20f74474ce"}]


payload = "[{\"title\":\"Topic 1\",\"id\":\"bc8be361e6be4ada8bc793080b6f24d5\", \"tags\":[], \"assessment_items\":[], \"prerequisite\":[], \"kind\":\"topic\", \"parent\":\"7463b0d9f11a441b8898ef20f74474ce\"}]\n\n"
headers = {
    'authorization': "Token 26a51f88ae50f4562c075f8031316eff34c58eb8",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "1d8e9f2b-929c-edf8-a561-a0fb41ac9606"
    }

response = requests.request("PATCH", url, data=payload, headers=headers)

print(response.text)
