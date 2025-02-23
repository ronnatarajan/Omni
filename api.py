from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
from client import analyze_text
from calendarTest import create_event

app = Flask(__name__)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        image_b64 = data['image']
        image = Image.open(BytesIO(base64.b64decode(image_b64)))
        token = data['token']

        # Process the image (e.g., save, analyze, etc.)
        image.save("received_image.png")

        extracted_text = ("( Oo Madhav Valiyaparambil <vpmadhav@gmail.com>"
                        "ee tome +"
                        "Yo Saket,"
                        "Wanna meet up at 12:00 at Krach to Study for a little bit")
        print("Start analysis")
        formatted_text = analyze_text(extracted_text)
        print(formatted_text)
        formatted_text = formatted_text.replace("Name= ", "")
        formatted_text = formatted_text.replace("Location= ", "")
        formatted_text = formatted_text.replace("StartTime= ", "")
        formatted_text = formatted_text.replace("EndTime= ", "")
        formatted_text = formatted_text.replace("StartDate= ", "")
        formatted_text = formatted_text.replace("EndDate= ", "")
        items = formatted_text.split("\n")
        final_start_date = items[4] + "T" + items[2] + ":00"
        final_end_date = items[5] + "T" + items[3] + ":00"
        print(f"title={items[0]}, location={items[1]}, description=None, start_date={final_start_date}, end_date={final_end_date}, guests=['email': 'madhavsv05@gmail.com'], recurring='WEEKLY', amountRecur='COUNT=3'")
        create_event(title=items[0], location=items[1], description=' ', start_date=final_start_date, end_date=final_end_date, guests=[{'email': 'madhavsv05@gmail.com'},], recurring='WEEKLY', amountRecur='COUNT=3')


        return jsonify({'message': 'Image uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)