from flask import Flask,render_template,request,redirect,url_for,make_response,send_file,abort
from werkzeug.utils import secure_filename
import io,os,tweepy,time,logging

from env import consumer_key,consumer_secret

# Proxy settings(optional)
#os.environ["http_proxy"] = "http://127.0.0.1:18899"
#os.environ["https_proxy"] = "http://127.0.0.1:18899"
# Proxy settings end

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload/'

auth = '' # authグローバル変数　認証用

@app.route('/')
def home_page():  # put application's code here
    if 'access_token' in request.cookies and 'access_token_secret' in request.cookies:
        if 'access_token' in request.cookies and 'access_token_secret' in request.cookies:
            access_token = request.cookies.get('access_token')
            access_token_secret = request.cookies.get('access_token_secret')
        else:
            return redirect(url_for('twi_login'))
        return render_template('mypage.html', access_token=access_token, access_token_secret=access_token_secret)
    else:
        return redirect(url_for('twi_login'))  # もしcookieがなければログインページへ

@app.route('/login.html')
def twi_login():
    global auth
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback='oob')
        auth_url = auth.get_authorization_url(signin_with_twitter=True)
    except:
        logging.error('Tweepy error')
        return abort(403)
    else:
        return render_template('login.html',auth_url=auth_url)

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        global auth
        oauth_pin = request.form['oauth_pin']
        try:
            access_token, access_token_secret = auth.get_access_token(oauth_pin)
        except:
            logging.error('Tweepy error')
            return "<head><title>ログイン失敗しました</title></head><h1>ログイン失敗しました</h1></br><a href='/'>戻る</a>"
        else:
            resp = make_response(redirect(url_for('home_page')))
            resp.set_cookie('access_token', access_token)
            resp.set_cookie('access_token_secret', access_token_secret)
            return resp

@app.route('/setheadpic.html', methods = ['POST', 'GET'])
def setheadpic():
    global auth
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback='oob')
        access_token = request.cookies.get('access_token')
        access_token_secret = request.cookies.get('access_token_secret')
    except:
        logging.error('Tweepy error')
        return abort(403)
    else:
        if request.method == 'POST':
            f = request.files['file']
            filename = str(time.time()) + '_' +secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            try:
                auth.set_access_token(access_token,access_token_secret)
                api = tweepy.API(auth)
                api.update_profile_image(app.config['UPLOAD_FOLDER']+filename)
            except:
                logging.error('Tweepy error')
                return abort(403)
            else:
                os.remove(app.config['UPLOAD_FOLDER']+filename)
                return "<head><title>アップロード完了</title></head><h1>アップロード完了</h1></br><a href='/'>戻る</a>"

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home_page')))
    try:
        resp.delete_cookie('access_token')
        resp.delete_cookie('access_token_secret')
    finally:
        return resp

if __name__ == '__main__':
    app.run()
