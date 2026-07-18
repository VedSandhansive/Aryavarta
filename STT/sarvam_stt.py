import requests


SARVAM_API_KEY = "sk_99iszh24_42Uil4E1BrhxvkIPxcaoi5Fr"


SARVAM_URL = "https://api.sarvam.ai/speech-to-text"



LANG_CODES = {

    "hindi": "hi-IN",
    "sanskrit": "sa-IN",
    "gujarati": "gu-IN",
    "bengali": "bn-IN",
    "tamil": "ta-IN",
    "telugu": "te-IN",
    "marathi": "mr-IN",
    "kannada": "kn-IN",
    "malayalam": "ml-IN",
    "punjabi": "pa-IN",
    "odia": "od-IN",
    "urdu": "ur-IN",
    "assamese": "as-IN",
    "english": "en-IN"

}



def sarvam_transcribe(filename, language):


    headers = {

        "api-subscription-key":
        SARVAM_API_KEY

    }



    audio_file = open(
        filename,
        "rb"
    )


    files = {

        "file": (

            "audio.wav",

            audio_file,

            "audio/wav"

        )

    }



    data = {

        "model":
        "saaras:v3",


        "language_code":
        LANG_CODES.get(

            language,

            "hi-IN"

        )

    }



    response = requests.post(

        SARVAM_URL,

        headers=headers,

        files=files,

        data=data

    )



    audio_file.close()



    print(
        "Sarvam Response:"
    )


    print(
        response.text
    )



    if response.status_code != 200:

        return ""



    result = response.json()


    return result.get(

        "transcript",

        ""

    )