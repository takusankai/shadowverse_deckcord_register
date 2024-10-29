from flask import Flask, redirect, url_for, session, render_template
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'random_secret_key'  # Flaskアプリケーションのセッションを保護するための秘密鍵
app.config['SESSION_TYPE'] = 'filesystem'  # セッションの保存方法をファイルシステムに設定

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='1013698805748-vivoe0aikr85bb19milivoea6fbhemgt.apps.googleusercontent.com',  # Google APIのクライアントID
    consumer_secret='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',  # Google APIのクライアントシークレット
    request_token_params={
        'scope': 'email',  # OAuth認証の際に要求するスコープ（ここではメールアドレス）
    },
    base_url='https://www.googleapis.com/oauth2/v1/',  # Google APIのベースURL
    request_token_url=None,  # リクエストトークンURL（OAuth 1.0aで使用、ここではNone）
    access_token_method='POST',  # アクセストークンを取得するためのHTTPメソッド
    access_token_url='https://accounts.google.com/o/oauth2/token',  # アクセストークンを取得するためのURL
    authorize_url='https://accounts.google.com/o/oauth2/auth',  # ユーザーを認証するためのURL
)

@app.route('/')
def index():
    return render_template('index.html')  # ルートURLにアクセスした際にindex.htmlを表示

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))  # Google OAuth認証を開始し、認証後に/authorizedにリダイレクト

@app.route('/logout')
def logout():
    session.pop('google_token')  # セッションからGoogleトークンを削除
    return redirect(url_for('index'))  # ログアウト後にルートURLにリダイレクト

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()  # Googleからの認証応答を取得
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )  # 認証が失敗した場合のエラーメッセージを表示
    session['google_token'] = (response['access_token'], '')  # アクセストークンをセッションに保存
    user_info = google.get('userinfo')  # ユーザー情報を取得
    return 'Logged in as: ' + user_info.data['email']  # ログインしたユーザーのメールアドレスを表示

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')  # セッションからGoogleトークンを取得

if __name__ == '__main__':
    app.run(debug=True)  # Flaskアプリケーションをデバッグモードで実行