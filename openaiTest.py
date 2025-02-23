from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "Can you give me the time, location, and title of this event?"
                                "( Oo Madhav Valiyaparambil <vpmadhav@gmail.com>"
                                "ee tome +"
                                "Yo Saket,"
                                "Wanna meet up at 12:00 at Krach to Study for a little bit?"
                                ""
                                "Please give me this information in the form"}
    ]
)

print(completion.choices[0].message.content);
