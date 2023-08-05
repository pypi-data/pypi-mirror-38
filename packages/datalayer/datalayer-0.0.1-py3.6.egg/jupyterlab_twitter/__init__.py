"""
Python module to initialize Server Extension & Notebook Extension
"""
import os
from jupyterlab_twitter.handlers import setup_handlers
from jupyterlab_twitter.twitter import Twitter

def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [{
        'module': 'jupyterlab_twitter',
    }]

def _jupyter_nbextension_paths():
    """
    Function to declare Jupyter Notebook Extension Paths.
    """
    return [{"section": "notebook", "dest": "jupyterlab_twitter"}]

def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """

    twitter = Twitter()
    nbapp.web_app.settings['twitter'] = twitter

    nbapp.web_app.settings['xsrf_cookies'] = False

    nbapp.web_app.settings['twitter_consumer_key'] = os.environ['DATALAYER_TWITTER_CONSUMER_KEY']
    nbapp.web_app.settings['twitter_consumer_secret'] = os.environ['DATALAYER_TWITTER_CONSUMER_SECRET']
    nbapp.web_app.settings['cookie_secret'] = "32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
    nbapp.web_app.settings['login_url'] = "/twitter/auth/popup"
    nbapp.web_app.settings['debug'] = True

    setup_handlers(nbapp.web_app)
