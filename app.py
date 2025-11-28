from flask import Flask, request, render_template, redirect, url_for, session
import joblib
import pandas as pd
import numpy as np

from feature_extractor import extract_features

app = Flask(__name__)
app.secret_key = "SECRET_CHANGE_ME"  # change for production

# Load URL-based phishing model
model = joblib.load('phishguard_rf_model.pkl')

feature_names = [
    'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol',
    'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
    'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL',
    'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL',
    'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain',
    'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page',
    'Statistical_report'
]


def get_top5_features(features, feature_names):
    """
    Use absolute feature value as a simple importance proxy and
    return top 5 (name, importance, value) tuples.
    """
    abs_features = [abs(float(x)) for x in features]
    top5_idxs = np.argsort(abs_features)[-5:][::-1]

    top5 = []
    for idx in top5_idxs:
        name = str(feature_names[idx])
        val = float(features[idx])
        imp = abs(val)
        top5.append((name, imp, val))
    return top5


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        # Basic validation
        if not url or not url.startswith(('http://', 'https://')):
            return render_template(
                'index.html',
                error='Please enter a valid URL starting with http:// or https://'
            )

        try:
            # Extract features and predict
            features = extract_features(url)
            df_features = pd.DataFrame([features], columns=feature_names)

            pred = model.predict(df_features)[0]  # get scalar prediction
            url_label = 'Phishing' if pred == -1 else 'Legitimate'

            top5_pairs = get_top5_features(features, feature_names)

        except Exception as e:
            return render_template('index.html', error=f'Error processing URL: {str(e)}')

        # Cloud version: no visual model
        visual_score = None
        visual_label = "Not available on cloud demo"

        url_score = 1 if url_label == 'Phishing' else 0
        combined_score = float(url_score)  # URL-only score

        # Make sure everything stored in session is JSON-serializable
        safe_top5 = []
        for name, imp, val in top5_pairs:
            safe_top5.append((str(name), float(imp), float(val)))

        session['result'] = {
            'url': str(url),
            'url_label': str(url_label),
            'visual_label': str(visual_label),
            'visual_score': visual_score,
            'combined_score': combined_score,
            'top5_pairs': safe_top5
        }

        return redirect(url_for('result'))

    # GET request
    return render_template('index.html')


@app.route('/result')
def result():
    res = session.get('result')
    if not res:
        return redirect(url_for('index'))

    return render_template(
        'result.html',
        url=res['url'],
        url_label=res['url_label'],
        visual_label=res['visual_label'],
        visual_score=res['visual_score'],
        combined_score=res['combined_score'],
        top5_pairs=res['top5_pairs']
    )


if __name__ == '__main__':
    app.run(debug=True)
