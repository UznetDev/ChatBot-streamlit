import requests
import streamlit as st
from http.cookies import SimpleCookie
import datetime



def send_request(url, method='GET', data=None):
    try:
        if method.upper() == 'POST':
            response = requests.post(url, json=data)
        elif method.upper() == 'GET':
            response = requests.get(url, params=data)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data)
        else:
            return {"message": "Notog‘ri HTTP usuli"}, 400
        status = response.status_code
        if status == 200:
            return response.json(), response.status_code
        else:
            return {"message": response.json()}, response.status_code
    except Exception as e:
        return {"message": str(e)}, 500
    


def send_request_with_files(url, method='GET', data=None, file=None, headers=None):
    """
    Fayl va boshqa ma'lumotlarni HTTP so'roviga yuborish uchun funktsiya.

    Params:
    - url (str): API endpoint manzili.
    - method (str): HTTP usuli ('POST', 'GET', va h.k.).
    - data (dict, optional): So'rovga yuboriladigan ma'lumotlar (JSON formatida).
    - file (tuple, optional): Fayl (('field_name', file_object)).
    - headers (dict, optional): So'rov uchun sarlavhalar.

    Returns:
    - response (dict): Javob ma'lumotlari yoki xato xabari.
    - status_code (int): HTTP javob kodi.
    """
    try:
        method = method.upper()
        response = None

        if method == 'POST':
            response = requests.post(url, data=data, files=file, headers=headers)
        else:
            return {"message": "Fayllar faqat POST usulida yuborilishi mumkin."}, 400

        if response.status_code in (200, 201):
            return response.json(), response.status_code
        else:
            try:
                error_message = response.json()
            except ValueError:
                error_message = response.text
            return {"message": error_message}, response.status_code

    except requests.exceptions.RequestException as e:
        return {"message": f"Request error: {str(e)}"}, 500
    except Exception as e:
        return {"message": f"Unexpected error: {str(e)}"}, 500

def set_cookie(key, value, days_expiry=2, path="/"):
    """
    Brauzerda cookie yaratish va saqlash.
    Args:
        key (str): Cookie kaliti.
        value (str): Saqlanadigan qiymat.
        days_expiry (int): Cookie amal qilish muddati (kunlarda).
        path (str): Cookie qamrovi.
    """
    expiry_date = datetime.datetime.now() + datetime.timedelta(days=days_expiry)
    cookie = SimpleCookie()
    cookie[key] = value
    cookie[key]["path"] = path
    cookie[key]["expires"] = expiry_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    st.markdown(
        f"""
        <script>
        document.cookie = "{cookie.output(header='', sep='')}";
        </script>
        """,
        unsafe_allow_html=True,
    )


# Cookie o'qish funksiyasi
def get_cookie(key):
    """
    Brauzerdagi cookie qiymatini qaytarish.
    Args:
        key (str): Cookie kaliti.
    Returns:
        str: Cookie qiymati yoki `None` agar mavjud bo'lmasa.
    """
    cookies = SimpleCookie(st.session_state.get("cookie", ""))
    if key in cookies:
        return cookies[key].value
    return None


# Cookie o'chirish funksiyasi
def delete_cookie(key, path="/"):
    """
    Cookie ni o'chirish.
    Args:
        key (str): O'chiriladigan cookie kaliti.
        path (str): Cookie qamrovi.
    """
    expiry_date = datetime.datetime.now() - datetime.timedelta(days=1)
    st.markdown(
        f"""
        <script>
        document.cookie = "{key}=; path={path}; expires={expiry_date.strftime('%a, %d %b %Y %H:%M:%S GMT')}";
        </script>
        """,
        unsafe_allow_html=True,
    )


