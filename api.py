from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
from client import analyze_text
from calendarTest import create_event
from ocr import get_text
import cv2
import requests
import re

app = Flask(__name__)

def validate_google_token(token):
    """Checks if the Google OAuth token is valid"""
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=" + token
    )
    return response.status_code == 200 


def create_google_calendar_event(event_data, token):
    """Creates an event in Google Calendar"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        json=event_data,
        headers=headers
    )

    if response.status_code == 200 or response.status_code == 201:
        return response.json()  # Success!
    else:
        return {"error": response.json()}  # Handle error properly
    
def clean_extracted_text(text):
    """Cleans extracted text by removing labels"""
    return re.sub(r"(Name= |Location= |StartTime= |EndTime= |StartDate= |EndDate= )", "", text)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        image_b64 = data['image']
        image = Image.open(BytesIO(base64.b64decode(image_b64)))
        token = data['token']
        # Process the image (e.g., save, analyze, etc.)
        image.save("received_image.png")

        if not validate_google_token(token):
            return jsonify({'error': 'Invalid or expired OAuth token'}), 401
        
        extracted_text = get_text(cv2.imread('received_image.png'))
        print(token)
        print("Start analysis")
        formatted_text = analyze_text(extracted_text)
        print(formatted_text)
        formatted_text = clean_extracted_text(formatted_text)
        items = formatted_text.split("\n")
        final_start_date = items[4] + "T" + items[2] + ":00"
        final_end_date = items[5] + "T" + items[3] + ":00"
        # print(f"title={items[0]}, location={items[1]}, description=None, start_date={final_start_date}, end_date={final_end_date}, guests=['email': 'madhavsv05@gmail.com'], recurring='WEEKLY', amountRecur='COUNT=3'")
        
        event_data=create_event(
            title=items[0], 
            location=items[1], 
            description=' ', 
            start_date=final_start_date, 
            end_date=final_end_date, 
            guests=[{'email': 'madhavsv05@gmail.com'},],
            recurring='WEEKLY', 
            amountRecur='COUNT=3'
        )

        print(event_data)


        calendar_response = create_google_calendar_event(event_data, token)

        return jsonify({
            'message': 'Event created successfully!',
            'calendar_response': calendar_response
        }), 200

    except Exception as e:
        print("FAILED")
        print(e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)