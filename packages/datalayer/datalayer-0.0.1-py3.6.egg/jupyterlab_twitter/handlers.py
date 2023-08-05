"""
This is a Handler Module with all the individual handlers for Twitter-Plugin.
"""
import json

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import APIHandler

import logging, os, sys
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, tornado.gen, tornado.auth
from tornado.options import define, options

class BaseHandler(APIHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("twitter_user")
        if user_json == None:
            return None
        return tornado.escape.json_decode(user_json)

class MainHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        self.render('index.html')

class TwitterAuthHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            twitter_user = {'name': user['name'], 'screen_name': user['screen_name'], 'username': user['screen_name']}
            self.set_secure_cookie("twitter_user", tornado.escape.json_encode(twitter_user))
            self.set_secure_cookie("twitter_user_access", tornado.escape.json_encode(user['access_token']))
            self.redirect("/")
        else:
            yield self.authorize_redirect(callback_uri=self.request.protocol+'://'+self.request.host+'/twitter/auth')

class TwitterAuthPopupHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            twitter_user = {'name': user['name'], 'screen_name': user['screen_name'], 'username': user['screen_name']}
            self.set_secure_cookie("twitter_user", tornado.escape.json_encode(twitter_user))
            self.set_secure_cookie("twitter_user_access", tornado.escape.json_encode(user['access_token']))
            self.write("""
                <!doctype html>
                <html lang="en">
                    <head>
                        <title>Close Me</title>
                        <script type="text/javascript">
                            window.opener.postMessage({twitterAuth: true}, '*');
                            window.close();
                        </script>
                    </head>
                    <body>
                    </body>
                </html>
            """)
        else:
#            yield self.authorize_redirect(callback_uri=self.request.protocol+'://'+self.request.host+'/twitter/auth/popup')
            yield self.authorize_redirect(callback_uri=self.request.protocol+'://'+self.request.host+'/services/twitter/auth/popup')

class TwitterSignoutHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def post(self):
        self.clear_cookie("twitter_user")
        self.clear_cookie("twitter_user_access")
        self.write(json.dumps("""{ 'success': 'true' }""", indent=1, sort_keys=True))

class TwitterInfoHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def post(self):
        if not self.get_current_user():
            self.write({'name': '', 'screen_name': '', 'username': ''})
            return
        self.write(json.dumps(self.get_current_user(), indent=1, sort_keys=True))
        
class TwitterPostHandler(BaseHandler, tornado.auth.TwitterMixin):
#    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.write({'name': '', 'screen_name': '', 'username': ''})
            return
        try:
            status = tornado.escape.json_decode(self.request.body)
            new_entry = yield self.twitter_request(
                "/statuses/update",
                post_args={"status": status['status']},
                access_token=tornado.escape.json_decode(self.get_secure_cookie('twitter_user_access'))
                )
            print(new_entry)
            if not new_entry:
                # Call failed; perhaps missing permission?
                self.write(json.dumps("""{ 'success': 'false' }""", indent=1, sort_keys=True))
                return
            res={}
            res['success']='true'
            res['status']=new_entry
            self.write(json.dumps(res, indent=1, sort_keys=True))
        except:
            self.write(json.dumps("""{ 'success': 'false' }""", indent=1, sort_keys=True))

class Twitter_handler(APIHandler):
    """
    Twitter Parent Handler.
    """
    @property
    def twitter(self):
        return self.settings['twitter']

class Twitter_API_handler(Twitter_handler):
    """
    A single class to give you 4 twitter commands combined:
    1. twitter showtoplevel
    2. twitter branch
    3. twitter log
    4. twitter status
    Class is used in the refresh method
    """

    def post(self):
        """
        Function used  to apply POST(REST_API) method to 'Twitter_API_handler'.
        API handler gives you:
        1. twitter showtoplevel
        2. twitter branch
        3. twitter log
        4. twitter status
        """
        """self.log.warning(self.request.body)"""
        my_data = json.loads(self.request.body.decode('utf-8'))
        current_path = my_data["current_path"]
        showtoplevel = self.twitter.showtoplevel(current_path)
        if(showtoplevel['code'] != 0):
            self.finish(json.dumps(showtoplevel))
        else:
            branch = self.twitter.branch(current_path)
            log = self.twitter.log(current_path)
            status = self.twitter.status(current_path)

            result = {
                "code": showtoplevel['code'],
                'data': {
                    'showtoplevel': showtoplevel,
                    'branch': branch,
                    'log': log,
                    'status': status}}
            self.finish(json.dumps(result))


class Twitter_showtoplevel_handler(Twitter_handler):
    """
    A class used to show the twitter root directory inside a repository.
    The twitter command used in here is 'twitter rev-parse --show-toplevel'
    """

    def post(self):
        """
        Function used  to apply POST  method to 'Twitter_showtoplevel_handler'.
        show toplevel gives you the root directory in your twitter repository.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        current_path = my_data["current_path"]
        result = self.twitter.showtoplevel(current_path)
        self.finish(json.dumps(result))


class Twitter_showprefix_handler(Twitter_handler):
    """
    A class used to show the prefix path of a directory in a repository
    The twitter command used in here is 'twitter rev-parse --show-prefix'
    """

    def post(self):
        """
        Function used  to apply POST method to 'Twitter_showprefix_handler'.
        show prefix gives you the prefix with respect to root directory
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        current_path = my_data["current_path"]
        result = self.twitter.showprefix(current_path)
        self.finish(json.dumps(result))


class Twitter_status_handler(Twitter_handler):
    """
    A class used to show the twitter status.
    The twitter command used in here is 'twitter status --porcelain'
    """

    def get(self):
        """
        Function used to apply GET method to 'Twitter_status_handler'.
        We need GET method to return the status to refresh method & show file
        status.
        """
        self.finish(
            json.dumps({
                "add_all": "check",
                "filename": "filename",
                "top_repo_path": "path"
            })
        )

    def post(self):
        """
        Function used to apply POST method to 'Twitter_status_handler'.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        current_path = my_data["current_path"]
        result = self.twitter.status(current_path)
        self.finish(json.dumps(result))


class Twitter_log_handler(Twitter_handler):
    """
    A class used to get Commit SHA, Author Name, Commit Date & Commit Message.
    The twitter command used here is 'twitter log --pretty=format:%H-%an-%ar-%s'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_log_handler'.
        log handler is used to get Commit SHA, Author Name, Commit Date &
        Commit Message.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        current_path = my_data["current_path"]
        result = self.twitter.log(current_path)
        self.finish(json.dumps(result))


class Twitter_log_1_handler(Twitter_handler):
    """
    A class used to get file names of committed files, Number of insertions &
    deletions in that commit.  The twitter command used here is
        'twitter log -1 --stat --numstat --oneline'
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_log_1_handler'.
        log 1 handler is used to get file names of committed files, Number of
        insertions & deletions in that commit.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        selected_hash = my_data["selected_hash"]
        current_path = my_data["current_path"]
        result = self.twitter.log_1(selected_hash, current_path)
        self.finish(json.dumps(result))


class Twitter_diff_handler(Twitter_handler):
    """
    A class used to show changes between commits & working tree.
    The twitter command used here is 'twitter diff --numstat'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_diff_handler'.
        twitter diff is used to get differences between commits & current working
        tree.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        top_repo_path = my_data["top_repo_path"]
        my_output = self.twitter.diff(top_repo_path)
        self.finish(my_output)
        print("GIT DIFF")
        print(my_output)


class Twitter_branch_handler(Twitter_handler):
    """
    A class used to change between different branches.
    The twitter command used here is 'twitter branch -a'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_branch_handler'.
        twitter branch is used to get all the branches present.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        current_path = my_data["current_path"]
        result = self.twitter.branch(current_path)
        self.finish(json.dumps(result))


class Twitter_add_handler(Twitter_handler):
    """
    A class used to add files to the staging area.
    The twitter command used here is 'twitter add <filename>'.
    """

    def get(self):
        """
        Function used to apply GET method of 'Twitter_add_handler'.
        twitter add is used to add files in the staging area.
        """
        self.finish(
            json.dumps({
                "add_all": "check",
                "filename": "filename",
                "top_repo_path": "path"
            })
        )

    def post(self):
        """
        Function used to apply POST method of 'Twitter_add_handler'.
        twitter add is used to add files in the staging area.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        top_repo_path = my_data["top_repo_path"]
        if(my_data["add_all"]):
            my_output = self.twitter.add_all(top_repo_path)
        else:
            filename = my_data["filename"]
            my_output = self.twitter.add(filename, top_repo_path)
        self.finish(my_output)


class Twitter_reset_handler(Twitter_handler):
    """
    A class used to move files from staged to unstaged area.
    The twitter command used here is 'twitter reset <filename>'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_reset_handler'.
        twitter reset is used to reset files from staging to unstage area.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        top_repo_path = my_data["top_repo_path"]
        if(my_data["reset_all"]):
            my_output = self.twitter.reset_all(top_repo_path)
        else:
            filename = my_data["filename"]
            my_output = self.twitter.reset(filename, top_repo_path)
        self.finish(my_output)


class Twitter_checkout_handler(Twitter_handler):
    """
    A class used to changes branches.
    The twitter command used here is 'twitter checkout <branchname>'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_checkout_handler'.
        twitter checkout is used to changes between branches.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        top_repo_path = my_data["top_repo_path"]
        if (my_data["checkout_branch"]):
            if(my_data["new_check"]):
                print("to create a new branch")
                my_output = self.twitter.checkout_new_branch(
                    my_data["branchname"], top_repo_path)
            else:
                print("switch to an old branch")
                my_output = self.twitter.checkout_branch(
                    my_data["branchname"], top_repo_path)
        elif(my_data["checkout_all"]):
            my_output = self.twitter.checkout_all(top_repo_path)
        else:
            my_output = self.twitter.checkout(my_data["filename"], top_repo_path)
        self.finish(my_output)


class Twitter_commit_handler(Twitter_handler):
    """
    A class used to commit files.
    The twitter command used here is 'twitter commit -m <message>'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_commit_handler'.
        twitter commit is used to commit files.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        top_repo_path = my_data["top_repo_path"]
        commit_msg = my_data["commit_msg"]
        my_output = self.twitter.commit(commit_msg, top_repo_path)
        self.finish(my_output)


class Twitter_pull_handler(Twitter_handler):
    """
    A class used to pull files from a remote branch.
    The twitter command used here is 'twitter pull <first-branch> <second-branch>'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_pull_handler'.
        twitter pull is used to pull files from a remote branch to your current
        work.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        origin = my_data["origin"]
        master = my_data["master"]
        curr_fb_path = my_data["curr_fb_path"]
        my_output = self.twitter.pull(origin, master, curr_fb_path)
        self.finish(my_output)
        print("You Pulled")


class Twitter_push_handler(Twitter_handler):
    """
    A class used to push files to a remote branch.
    The twitter command used here is 'twitter push <first-branch> <second-branch>'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_push_handler'.
        twitter push is used to push files from a remote branch to your current
        work.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        origin = my_data["origin"]
        master = my_data["master"]
        curr_fb_path = my_data["curr_fb_path"]
        my_output = self.twitter.push(origin, master, curr_fb_path)
        self.finish(my_output)
        print("You Pushed")


class Twitter_init_handler(Twitter_handler):
    """
    A class used to initialize a repository.
    The twitter command used here is 'twitter init'.
    """

    def post(self):
        """
        Function used to apply POST method of 'Twitter_init_handler'.
        twitter init is used to initialize a repository.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        current_path = my_data["current_path"]
        my_output = self.twitter.init(current_path)
        self.finish(my_output)


class Twitter_add_all_untracked_handler(Twitter_handler):
    """
    A class used to add and ONLY add all the untracked files.
    The twitter command used here is 'echo "a\n*\nq\n" | twitter add -i'.
    """
    def post(self):
        """
        Function used to apply POST method of 'Twitter_add_all_untracked_handler'.
        twitter add_all_untracked is used to add all the untracked files.
        """
        my_data = json.loads(self.request.body.decode('utf-8'))
        top_repo_path = my_data["top_repo_path"]
        my_output = self.twitter.add_all_untracked(top_repo_path)
        print(my_output)
        self.finish(my_output)


def setup_handlers(web_app):
    """
    Function used to setup all of the Twitter_Handlers used in the file.
    Every handler is defined here, to be used in twitter.py file.
    """

    twitter_handlers = [
        ('/twitter/showtoplevel', Twitter_showtoplevel_handler),
        ('/twitter/showprefix', Twitter_showprefix_handler),
        ('/twitter/add', Twitter_add_handler),
        ('/twitter/status', Twitter_status_handler),
        ('/twitter/branch', Twitter_branch_handler),
        ('/twitter/reset', Twitter_reset_handler),
        ('/twitter/checkout', Twitter_checkout_handler),
        ('/twitter/commit', Twitter_commit_handler),
        ('/twitter/pull', Twitter_pull_handler),
        ('/twitter/push', Twitter_push_handler),
        ('/twitter/diff', Twitter_diff_handler),
        ('/twitter/log', Twitter_log_handler),
        ('/twitter/log_1', Twitter_log_1_handler),
        ('/twitter/init', Twitter_init_handler),
        ('/twitter/API', Twitter_API_handler),
        ('/twitter/add_all_untracked', Twitter_add_all_untracked_handler),

        (r"/twitter/info", TwitterInfoHandler),
        (r"/twitter/auth", TwitterAuthHandler),
        (r"/twitter/auth/popup", TwitterAuthPopupHandler),
        (r"/services/twitter/auth/popup", TwitterAuthPopupHandler),
        (r"/twitter/signout", TwitterSignoutHandler),
        (r"/twitter/post", TwitterPostHandler),

    ]

    # add the baseurl to our paths
    base_url = web_app.settings['base_url']
    twitter_handlers = [
        (ujoin(base_url, x[0]), x[1])
        for x in twitter_handlers
    ]
    print("base_url: {}".format(base_url))
    print(twitter_handlers)

    web_app.add_handlers('.*', twitter_handlers)


def print_handlers():
    twitter_handlers = [
        ('/twitter/showtoplevel', Twitter_showtoplevel_handler),
        ('/twitter/showprefix', Twitter_showprefix_handler),
        ('/twitter/add', Twitter_add_handler),
        ('/twitter/status', Twitter_status_handler),
        ('/twitter/branch', Twitter_branch_handler),
        ('/twitter/reset', Twitter_reset_handler),
        ('/twitter/checkout', Twitter_checkout_handler),
        ('/twitter/commit', Twitter_commit_handler),
        ('/twitter/pull', Twitter_pull_handler),
        ('/twitter/push', Twitter_push_handler),
        ('/twitter/diff', Twitter_diff_handler),
        ('/twitter/log', Twitter_log_handler),
        ('/twitter/log_1', Twitter_log_1_handler),
        ('/twitter/init', Twitter_init_handler),
        ('/twitter/API', Twitter_API_handler),
        ('/twitter/add_all_untracked', Twitter_add_all_untracked_handler),

        (r"/twitter/info", TwitterInfoHandler),
        (r"/twitter/auth", TwitterAuthHandler),
        (r"/twitter/auth/popup", TwitterAuthPopupHandler),
        (r"/services/twitter/auth/popup", TwitterAuthPopupHandler),
        (r"/twitter/signout", TwitterSignoutHandler),
        (r"/twitter/post", TwitterPostHandler),

    ]

    # add the baseurl to our paths
    base_url = ''
    twitter_handlers = [
        (ujoin(base_url, x[0]), x[1])
        for x in twitter_handlers
    ]
