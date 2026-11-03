"""
Supported Languages Configuration for Voice Mandi.
Provides metadata, native names, regional state mappings, sample queries,
and localized polite retry prompts for unclear speech across 10 major Indian languages.
"""

from typing import Dict, Any

SUPPORTED_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "hi-IN": {
        "code": "hi-IN",
        "name": "Hindi",
        "native": "हिन्दी",
        "flag": "🇮🇳",
        "script": "Devanagari",
        "state": "Maharashtra",
        "village_tag": "📍 पुणे ग्रामीण (Pune Village)",
        "mic_label": "माईक दबाएं और बोलना शुरू करें",
        "mic_sublabel": "अपनी भाषा में मंडी भाव और मौसम सलाह पूछें",
        "unclear_speech_prompt": "माफ़ कीजिए, आपकी आवाज़ साफ़ सुनाई नहीं दी। कृपया माईक दबाकर दोबारा बोलें।",
        "fallback_advice": "नमस्ते किसान भाई, आपकी फसल का आज मंडी में अच्छा भाव चल रहा है। मौसम की स्थिति जांच कर ही माल ले जाएं।",
        "sample_queries": [
            "आज मंडी में प्याज का क्या भाव है?",
            "टमाटर कहाँ बेचना सबसे फायदेमंद रहेगा?",
            "क्या आज रात बारिश में माल ले जाना सुरक्षित है?"
        ]
    },
    "mr-IN": {
        "code": "mr-IN",
        "name": "Marathi",
        "native": "मराठी",
        "flag": "🚩",
        "script": "Devanagari",
        "state": "Maharashtra",
        "village_tag": "📍 पुणे ग्रामीण (Pune Village)",
        "mic_label": "माईक दाबा आणि बोलायला सुरुवात करा",
        "mic_sublabel": "आपल्या भाषेत बाजारभाव आणि हवामान सल्ला विचारा",
        "unclear_speech_prompt": "माफ करा, तुमचा आवाज स्पष्ट ऐकू आला नाही. कृपया माईक दाबून पुन्हा बोला.",
        "fallback_advice": "नमस्कार शेतकरी बंधू, आज बाजारात तुमच्या पिकाला चांगला भाव मिळत आहे. स्थानिक हवामान पाहूनच माल बाजारात न्या.",
        "sample_queries": [
            "आज बाजारात कांद्याचा काय भाव चालू आहे?",
            "टोमॅटो कोणत्या APMC मध्ये विकणे फायदेशीर ठरेल?",
            "पावसात माल बाजारात नेणे सुरक्षित आहे का?"
        ]
    },
    "gu-IN": {
        "code": "gu-IN",
        "name": "Gujarati",
        "native": "ગુજરાતી",
        "flag": "🌾",
        "script": "Gujarati",
        "state": "Gujarat",
        "village_tag": "📍 રાજકોટ માર્કેટ (Rajkot APMC)",
        "mic_label": "માઇક દબાવો અને બોલવાનું શરૂ કરો",
        "mic_sublabel": "તમારી પોતાની ભાષામાં બજાર ભાવ અને હવામાન સલાહ પૂછો",
        "unclear_speech_prompt": "માફ કરશો, તમારો અવાજ સ્પષ્ટ સંભળાયો નથી. કૃપા કરીને માઇક દબાવીને ફરીથી બોલો.",
        "fallback_advice": "નમસ્તે ખેડૂત મિત્ર, આજના માર્કેટ યાર્ડમાં તમારા પાકનો સારો ભાવ મળી રહ્યો છે. હવામાનની સ્થિતિ જોઈને માલનું પરિવહન કરો.",
        "sample_queries": [
            "આજે માર્કેટ યાર્ડમાં ડુંગળીનો શું ભાવ છે?",
            "ટામેટા ક્યાં વેચવા સૌથી વધુ નફાકારક રહેશે?",
            "શું વરસાદમાં પાકનું પરિવહન કરવું સલામત છે?"
        ]
    },
    "kn-IN": {
        "code": "kn-IN",
        "name": "Kannada",
        "native": "ಕನ್ನಡ",
        "flag": "🌾",
        "script": "Kannada",
        "state": "Karnataka",
        "village_tag": "📍 ಯಶವಂತಪುರ ಮಾರುಕಟ್ಟೆ (Yeshwantpur)",
        "mic_label": "ಮೈಕ್ ಒತ್ತಿ ಮಾತನಾಡಲು ಪ್ರಾರಂಭಿಸಿ",
        "mic_sublabel": "ನಿಮ್ಮ ಸ್ವಂತ ಭಾಷೆಯಲ್ಲಿ ಮಾರುಕಟ್ಟೆ ದರ ಮತ್ತು ಹವಾಮಾನ ಸಲಹೆ ಕೇಳಿ",
        "unclear_speech_prompt": "ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಧ್ವನಿ ಸ್ಪಷ್ಟವಾಗಿ ಕೇಳಿಸಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮೈಕ್ ಒತ್ತಿ ಮತ್ತೊಮ್ಮೆ ಮಾತನಾಡಿ.",
        "fallback_advice": "ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ, ಇಂದು ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಉತ್ತಮ ಬೆಲೆ ದೊರೆಯುತ್ತಿದೆ. ಹವಾಮಾನವನ್ನು ಪರಿಶೀಲಿಸಿ ಬೆಳೆಯನ್ನು ಸಾಗಿಸಿ.",
        "sample_queries": [
            "ಇಂದು ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಈರುಳ್ಳಿ ದರ ಎಷ್ಟಿದೆ?",
            "ಟೊಮೆಟೊ ಎಲ್ಲಿ ಮಾರಾಟ ಮಾಡುವುದು ಹೆಚ್ಚು ಲಾಭದಾಯಕ?",
            "ಮಳೆಯಲ್ಲಿ ಬೆಳೆಯನ್ನು ಸಾಗಿಸುವುದು ಸುರಕ್ಷಿತವೇ?"
        ]
    },
    "ta-IN": {
        "code": "ta-IN",
        "name": "Tamil",
        "native": "தமிழ்",
        "flag": "🌾",
        "script": "Tamil",
        "state": "Tamil Nadu",
        "village_tag": "📍 கோயம்பேடு சந்தை (Koyambedu)",
        "mic_label": "மைக்கை அழுத்தி பேசத் தொடங்குங்கள்",
        "mic_sublabel": "உங்கள் சொந்த மொழியில் மண்டி விலை மற்றும் வானிலை ஆலோசனை கேளுங்கள்",
        "unclear_speech_prompt": "மன்னிக்கவும், உங்கள் குரல் தெளிவாகக் கேட்கவில்லை. தயவுசெய்து மைக்கை அழுத்தி மீண்டும் பேசுங்கள்.",
        "fallback_advice": "வணக்கம் விவசாய நண்பரே, இன்றைய சந்தையில் உங்கள் பயிருக்கு நல்ல விலை கிடைக்கிறது. வானிலை அறிந்து பயிர்களை கொண்டு செல்லுங்கள்.",
        "sample_queries": [
            "இன்று சந்தையில் வெங்காய விலை என்ன?",
            "தக்காளி எங்கு விற்றால் நல்ல லாபம் கிடைக்கும்?",
            "மழையில் பயிர்களை கொண்டு செல்வது பாதுகாப்பானதா?"
        ]
    },
    "te-IN": {
        "code": "te-IN",
        "name": "Telugu",
        "native": "తెలుగు",
        "flag": "🌾",
        "script": "Telugu",
        "state": "Telangana",
        "village_tag": "📍 వరంగల్ మార్కెట్ (Warangal APMC)",
        "mic_label": "మైక్ నొక్కి మాట్లాడటం ప్రారంభించండి",
        "mic_sublabel": "మీ ప్రాంతీయ భాషలో మార్కెట్ ధరలు మరియు వాతావరణ సలహాలు పొందండి",
        "unclear_speech_prompt": "క్షమించండి, మీ స్వరం స్పష్టంగా వినిపించలేదు. దయచేసి మైక్ నొక్కి మళ్ళీ మాట్లాడండి.",
        "fallback_advice": "నమస్కారం రైతు సోదరా, నేటి మార్కెట్లో మీ పంటకు మంచి ధర లభిస్తోంది. వాతావరణాన్ని బట్టి పంట రవాణా చేసుకోండి.",
        "sample_queries": [
            "ఈరోజు మార్కెట్లో ఉల్లిపాయ ధర ఎంత ఉంది?",
            "టమోటాలను ఎక్కడ విక్రయిస్తే ఎక్కువ లాభం వస్తుంది?",
            "వర్షంలో పంటను మార్కెట్‌కు తరలించడం సురక్షితమేనా?"
        ]
    },
    "bn-IN": {
        "code": "bn-IN",
        "name": "Bengali",
        "native": "বাংলা",
        "flag": "🌾",
        "script": "Bengali",
        "state": "West Bengal",
        "village_tag": "📍 বর্ধমান বাজার (Burdwan Market)",
        "mic_label": "মাইক টিপুন এবং কথা বলা শুরু করুন",
        "mic_sublabel": "নিজের ভাষায় মণ্ডির দাম এবং আবহাওয়ার পরামর্শ জানুন",
        "unclear_speech_prompt": "দুঃখিত, আপনার কথা স্পষ্ট শোনা যায়নি। দয়া করে মাইক চেপে আবার বলুন।",
        "fallback_advice": "নমস্কার কৃষক ভাই, আজকের বাজারে আপনার ফসলের ভালো দাম পাওয়া যাচ্ছে। আবহাওয়ার সতর্কতা মেনে মাল পরিবহন করুন।",
        "sample_queries": [
            "আজ বাজারে পেঁয়াজের দর কত চলছে?",
            "টমেটো কোথায় বিক্রি করা সবচেয়ে লাভজনক হবে?",
            "আজ বৃষ্টির মধ্যে ফসল পরিবহন করা কি নিরাপদ?"
        ]
    },
    "pa-IN": {
        "code": "pa-IN",
        "name": "Punjabi",
        "native": "ਪੰਜਾਬੀ",
        "flag": "🌾",
        "script": "Gurmukhi",
        "state": "Punjab",
        "village_tag": "📍 ਖੰਨਾ ਮੰਡੀ (Khanna Mandi)",
        "mic_label": "ਮਾਈਕ ਦਬਾਓ ਅਤੇ ਬੋਲਣਾ ਸ਼ੁਰੂ ਕਰੋ",
        "mic_sublabel": "ਆਪਣੀ ਭਾਸ਼ਾ ਵਿੱਚ ਮੰਡੀ ਦੇ ਭਾਅ ਅਤੇ ਮੌਸਮ ਦੀ ਸਲਾਹ ਪੁੱਛੋ",
        "unclear_speech_prompt": "ਮਾਫ਼ ਕਰਨਾ, ਤੁਹਾਡੀ ਆਵਾਜ਼ ਸਾਫ਼ ਸੁਣਾਈ ਨਹੀਂ ਦਿੱਤੀ। ਕਿਰਪਾ ਕਰਕੇ ਮਾਈਕ ਦਬਾ ਕੇ ਦੁਬਾਰਾ ਬੋਲੋ।",
        "fallback_advice": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਕਿਸਾਨ ਵੀਰੋ, ਅੱਜ ਮੰਡੀ ਵਿੱਚ ਫ਼ਸਲ ਦਾ ਵਧੀਆ ਭਾਅ ਮਿਲ ਰਿਹਾ ਹੈ। ਮੌਸਮ ਦੇਖ ਕੇ ਹੀ ਆਪਣੀ ਫ਼ਸਲ ਮੰਡੀ ਲੈ ਕੇ ਜਾਓ।",
        "sample_queries": [
            "ਅੱਜ ਮੰਡੀ ਵਿੱਚ ਪਿਆਜ਼ ਦਾ ਕੀ ਭਾਅ ਚੱਲ ਰਿਹਾ ਹੈ?",
            "ਟਮਾਟਰ ਕਿਸ ਮੰਡੀ ਵਿੱਚ ਵੇਚਣਾ ਫਾਇਦੇਮੰਦ ਰਹੇਗਾ?",
            "ਕੀ ਅੱਜ ਮੀਂਹ ਵਿੱਚ ਫ਼ਸਲ ਲਿਜਾਣਾ ਠੀਕ ਹੈ?"
        ]
    },
    "ml-IN": {
        "code": "ml-IN",
        "name": "Malayalam",
        "native": "മലയാളം",
        "flag": "🌾",
        "script": "Malayalam",
        "state": "Kerala",
        "village_tag": "📍 കൊച്ചി മാർക്കറ്റ് (Kochi Market)",
        "mic_label": "മൈക്ക് അമർത്തി സംസാരിച്ചു തുടങ്ങൂ",
        "mic_sublabel": "നിങ്ങളുടെ സ്വന്തം ഭാഷയിൽ വിപണി നിരക്കുകളും കാലാവസ്ഥാ ഉപദേശങ്ങളും അറിയൂ",
        "unclear_speech_prompt": "ക്ഷമിക്കണം, താങ്കളുടെ ശബ്ദം വ്യക്തമായി കേട്ടില്ല. ദയവായി മൈക്ക് അമർത്തി വീണ്ടും പറയൂ.",
        "fallback_advice": "നമസ്കാരം കർഷക സുഹൃത്തേ, ഇന്നത്തെ വിപണിയിൽ നല്ല വില ലഭിക്കുന്നുണ്ട്. കാലാവസ്ഥ നിരീക്ഷിച്ച് മാത്രം വിളകൾ വിപണിയിലെത്തിക്കുക.",
        "sample_queries": [
            "ഇന്ന് വിപണിയിൽ ഉള്ളി വില എത്രയാണ്?",
            "തക്കാളി എവിടെ വിൽക്കുന്നതാണ് കൂടുതൽ ലാഭകരം?",
            "മഴയത്ത് വിളകൾ കൊണ്ടുപോകുന്നത് സുരക്ഷിതമാണോ?"
        ]
    },
    "od-IN": {
        "code": "od-IN",
        "name": "Odia",
        "native": "ଓଡ଼ିଆ",
        "flag": "🌾",
        "script": "Odia",
        "state": "Odisha",
        "village_tag": "📍 କଟକ ମଣ୍ଡି (Cuttack Mandi)",
        "mic_label": "ମାଇକ୍ ଦବାନ୍ତୁ ଏବଂ କହିବା ଆରମ୍ଭ କରନ୍ତୁ",
        "mic_sublabel": "ଆପଣଙ୍କ ଭାଷାରେ ମଣ୍ଡି ଦର ଏବଂ ପାଣିପାଗ ପରାମର୍ଶ ପଚାରନ୍ତୁ",
        "unclear_speech_prompt": "କ୍ଷମା କରିବେ, ଆପଣଙ୍କ ସ୍ୱର ସ୍ପଷ୍ଟ ଭାବେ ଶୁଣାଗଲା ନାହିଁ। ଦୟାକରି ମାଇକ୍ ଦବାଇ ପୁଣି କୁହନ୍ତୁ।",
        "fallback_advice": "ନମସ୍କାର ଚାଷୀ ଭାଇ, ଆଜି ମଣ୍ଡିରେ ଆପଣଙ୍କ ଫସଲର ଭଲ ଦର ମିଳୁଛି। ପାଣିପାଗ ସତର୍କତା ଦେଖି ଫସଲ ବିକ୍ରି ପାଇଁ ନିଅନ୍ତୁ।",
        "sample_queries": [
            "ଆଜି ମଣ୍ଡିରେ ପିଆଜ ଦର କେତେ ଅଛି?",
            "ଟମାଟର କେଉଁଠି ବିକିଲେ ଅଧିକ ଲାଭ ମିଳିବ?",
            "ବର୍ଷାରେ ଫସଲ ନେବା ସୁରକ୍ଷିତ କି?"
        ]
    },
    "en-IN": {
        "code": "en-IN",
        "name": "English",
        "native": "English",
        "flag": "🌐",
        "script": "Latin",
        "state": "Maharashtra",
        "village_tag": "📍 Pune Market (India)",
        "mic_label": "Press Mic and Start Speaking",
        "mic_sublabel": "Ask Mandi prices and weather advice in English",
        "unclear_speech_prompt": "Sorry, your voice was not clear. Please tap the mic and speak again clearly.",
        "fallback_advice": "Hello Farmer, current mandi prices are favorable today. Please plan your transport considering the latest local weather forecast.",
        "sample_queries": [
            "What is today's onion rate across nearby mandis?",
            "Where is the best market to sell tomatoes today?",
            "Is it safe to transport crops tonight given the rain alert?"
        ]
    }
}


def get_language_info(code: str) -> Dict[str, Any]:
    """Retrieve metadata for a language code with fallback to Hindi."""
    clean_code = (code or "hi-IN").strip()
    return SUPPORTED_LANGUAGES.get(clean_code, SUPPORTED_LANGUAGES["hi-IN"])
