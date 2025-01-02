from flask import Flask, request, render_template
import base64

app = Flask(__name__)

# Secret word for authentication
SECRET_WORD = "mypassword123"

# Dictionary to store links (encoded in Base64)
links = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        secret_word = request.form.get('secret_word')
        if secret_word == SECRET_WORD:
            return render_template('dashboard.html', links=links)
        else:
            return "<p style='color:red;'>Incorrect Secret Word! Try again.</p><a href='/'>Go back</a>"
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_link():
    secret_word = request.form.get('secret_word')
    link_name = request.form.get('link_name')
    url = request.form.get('url')
    
    if secret_word == SECRET_WORD:
        if link_name and url:
            # Encode URL in Base64
            encoded_url = base64.b64encode(url.encode()).decode()
            links[link_name] = encoded_url
            return f"<p style='color:green;'>Link '{link_name}' saved successfully!</p><a href='/'>Go back</a>"
        else:
            return "<p style='color:red;'>Please provide both Link Name and URL!</p><a href='/'>Try again</a>"
    else:
        return "<p style='color:red;'>Unauthorized access!</p><a href='/'>Go back</a>"

@app.route('/<link_name>')
def get_link(link_name):
    if link_name in links:
        # Decode the Base64 URL
        decoded_url = base64.b64decode(links[link_name]).decode()
        return f"<h3>Saved Link for {link_name}:</h3><p><a href='{decoded_url}' target='_blank'>{decoded_url}</a></p><a href='/'>Go back</a>"
    else:
        return "<p style='color:red;'>Link not found!</p><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)
