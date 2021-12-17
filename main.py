import streamlit as st
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

st.title('顔認識アプリ')

subscription_key='https://key-manager.vault.azure.net/secrets/WebApp--FaceCheck/21f6601cbbdc41e894f4c27902bf5005'
assert subscription_key

face_api_url = 'https://202112116-kubo.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file = st.file_uploader("Choose an image...",type=['jpg','jpeg','png','gif','bmp'])

if uploaded_file is not None:

    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        binary_img=output.getvalue()
        
    headers= {
        'content-Type':'application/octet-stream',
        'Ocp-Apim-subscription-Key': subscription_key}

    params = {
        'returnFaceId':'True',
        'returnFaceAttributes':'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    res = requests.post(face_api_url, params=params,headers=headers, data = binary_img)


    results = res.json()
    for result in results:
            rect = result['faceRectangle']
            gender = result['faceAttributes']['gender']
            age = result['faceAttributes']['age']
            text = gender + '\n'+str(age)
            draw = ImageDraw.Draw(img)
            draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline ='green',width=5)
            
            textcolor = (255, 255, 255)
            textsize=round(rect['width']/5)
            font = ImageFont.truetype(font = "Arial Unicode.ttf", size=textsize)
            
            txpos = (rect['left'], rect['top']-textsize*2.5)
            draw.text(txpos, text, font=font ,fill=textcolor)
    st.image(img, caption='Uploaded Image.', use_column_width=True)

