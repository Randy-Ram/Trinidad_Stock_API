from google.cloud import language

client = language.Client()

content = "Hello, I absolutely love and adore your dress!"

document = client.document_from_text(content)

sentiment = document.analyze_sentiment()

print sentiment.magnitude
