import requests , time , binascii , json , urllib3 , random
from datetime import datetime
from Black import *
from multiprocessing.dummy import Pool as ThreadPool

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def Ua():
    TmP = "GarenaMSDK/4.0.13 ({}; {}; {};)"
    return TmP.format(random.choice(["iPhone 13 Pro", "iPhone 14", "iPhone XR", "Galaxy S22", "Note 20", "OnePlus 9", "Mi 11"]) , 
                     random.choice(["iOS 17", "iOS 18", "Android 13", "Android 14"]) , 
                     random.choice(["en-SG", "en-US", "fr-FR", "id-ID", "th-TH", "vi-VN"]))

def xGeT(u, p):
    """الدالة المعدلة لاستخدام UID و PW مباشرة من السكريبت الرئيسي"""
    print(f"جاري توليد التوكن لـ UID: {u}")
    try:
        r = requests.Session().post(
            "https://100067.connect.garena.com/oauth/guest/token/grant",
            headers={
                "Host": "100067.connect.garena.com",
                "User-Agent": Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            },
            data={
                "uid": u,
                "password": p,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            },
            verify=False
        )
        
        if r.status_code == 200:
            T = r.json()
            print("تم الحصول على التوكن بنجاح من Garena")
            a, o = T["access_token"], T["open_id"]
            jwt_token = xJwT(a, o)
            if jwt_token:
                print("تم توليد JWT بنجاح")
                return jwt_token
            else:
                print("فشل في توليد JWT")
                return None
        else:
            print(f"خطأ في الاستجابة من Garena: {r.status_code}")
            return None
    except Exception as e:
        print(f"حدث خطأ في xGeT: {str(e)}")
        return None

def xJwT(a, o):
    """دالة توليد JWT باستخدام التوكن المباشر"""
    try:
        dT = bytes.fromhex('1A13323032352D30372D33302031313A30323A3531220966726565206669726528013A07312E3131382E31422C416E64726F6964204F5320372E312E32202F204150492D323320284E32473438482F373030323530323234294A0848616E6468656C645207416E64726F69645A045749464960C00C68840772033332307A1F41524D7637205646507633204E454F4E20564D48207C2032343635207C203480019A1B8A010F416472656E6F2028544D292036343092010D4F70656E474C20455320332E319A012B476F6F676C657C31663361643662372D636562342D343934622D383730622D623164616364373230393131A2010C3139372E312E31322E313335AA0102656EB201203939366136323964626364623339363462653662363937386635643831346462BA010134C2010848616E6468656C64CA011073616D73756E6720534D2D473935354EEA014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261F00101CA0207416E64726F6964D2020457494649CA03203734323862323533646566633136343031386336303461316562626665626466E003DAA907E803899B07F003BF0FF803AE088004999B078804DAA9079004999B079804DAA907C80403D204262F646174612F6170702F636F6D2E6474732E667265656669726574682D312F6C69622F61726DE00401EA044832303837663631633139663537663261663465376665666630623234643964397C2F646174612F6170702F636F6D2E6474732E667265656669726574682D312F626173652E61706BF00403F804018A050233329A050A32303139313138363933A80503B205094F70656E474C455332B805FF7FC00504E005DAC901EA0507616E64726F6964F2055C4B71734854394748625876574C6668437950416C52526873626D43676542557562555551317375746D525536634E30524F3751453141486E496474385963784D614C575437636D4851322B7374745279377830663935542B6456593D8806019006019A060134A2060134B206024000')
        
        # تحديث البيانات الديناميكية
        dT = dT.replace(b'2025-07-30 14:11:20', str(datetime.now())[:-7].encode())
        dT = dT.replace(b'ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a', a.encode())
        dT = dT.replace(b'996a629dbcdb3964be6b6978f5d814db', o.encode())
        
        PyL = bytes.fromhex(EnC_AEs(dT.hex()))
        r = requests.Session().post(
            "https://loginbp.ggwhitehawk.com/MajorLogin",
            headers={
                "Expect": "100-continue",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": "OB51",
                "Authorization": "Bearer ",
                "Host": "loginbp.ggwhitehawk.com"
            },
            data=PyL,
            verify=False
        )
        
        if r.status_code == 200:
            response_data = json.loads(DeCode_PackEt(binascii.hexlify(r.content).decode('utf-8')))
            return response_data['8']['data']
        else:
            print(f"خطأ في MajorLogin: {r.status_code}")
            return None
    except Exception as e:
        print(f"حدث خطأ في xJwT: {str(e)}")
        return None