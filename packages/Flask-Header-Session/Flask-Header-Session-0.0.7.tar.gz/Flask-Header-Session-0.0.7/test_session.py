import unittest
import tempfile

import flask
from flask_header_session import Session
import redis
import os

import time
time.sleep(2)

class FlaskSessionTestCase(unittest.TestCase):

    def test_null_session(self):
        app = flask.Flask(__name__)
        Session(app)

        def expect_exception(f, *args, **kwargs):
            try:
                f(*args, **kwargs)
            except RuntimeError as e:
                self.assertTrue(e.args and 'session is unavailable' in e.args[0])
            else:
                self.assertTrue(False, 'expected exception')
        with app.test_request_context():
            self.assertTrue(flask.session.get('missing_key') is None)
            expect_exception(flask.session.__setitem__, 'foo', 42)
            expect_exception(flask.session.pop, 'foo')

    def test_redis_session(self):
        app = flask.Flask(__name__)
        app.debug = True
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_HEADER_NAME'] = 'X-TEST-SESSION'
        # Session, put into redis db 0
        app.config['SESSION_REDIS'] = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)
        Session(app)

        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'

        @app.route('/get')
        def get():
            return flask.session['value']

        @app.route('/delete', methods=['POST'])
        def delete():
            del flask.session['value']
            return 'value deleted'

        c = app.test_client()
        # Set the session by calling /set endpoint
        temp_session_id = c.post('/set', data={'value': '42'}).headers['X-TEST-SESSION']
        # Test the session by calling the /get endpoint with a header set as session identifier
        self.assertEqual(c.get('/get', headers={'X-TEST-SESSION': str(temp_session_id)}).data, b'42')
        # c.post('/delete')

    # def test_memcached_session(self):
    #     app = flask.Flask(__name__)
    #     app.config['SESSION_TYPE'] = 'memcached'
    #     Session(app)

    #     @app.route('/set', methods=['POST'])
    #     def set():
    #         flask.session['value'] = flask.request.form['value']
    #         return 'value set'

    #     @app.route('/get')
    #     def get():
    #         return flask.session['value']

    #     @app.route('/delete', methods=['POST'])
    #     def delete():
    #         del flask.session['value']
    #         return 'value deleted'

    #     c = app.test_client()
    #     self.assertEqual(c.post('/set', data={'value': '42'}).data, b'value set')
    #     self.assertEqual(c.get('/get').data, b'42')
    #     c.post('/delete')

    # def test_filesystem_session(self):
    #     app = flask.Flask(__name__)
    #     app.config['SESSION_TYPE'] = 'filesystem'
    #     app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
    #     Session(app)

    #     @app.route('/set', methods=['POST'])
    #     def set():
    #         flask.session['value'] = flask.request.form['value']
    #         return 'value set'

    #     @app.route('/get')
    #     def get():
    #         return flask.session['value']

    #     @app.route('/delete', methods=['POST'])
    #     def delete():
    #         del flask.session['value']
    #         return 'value deleted'

    #     c = app.test_client()
    #     self.assertEqual(c.post('/set', data={'value': '42'}).data, b'value set')
    #     self.assertEqual(c.get('/get').data, b'42')
    #     c.post('/delete')

    # def test_mongodb_session(self):
    #     app = flask.Flask(__name__)
    #     app.testing = True
    #     app.config['SESSION_TYPE'] = 'mongodb'
    #     Session(app)

    #     @app.route('/set', methods=['POST'])
    #     def set():
    #         flask.session['value'] = flask.request.form['value']
    #         return 'value set'

    #     @app.route('/get')
    #     def get():
    #         return flask.session['value']

    #     @app.route('/delete', methods=['POST'])
    #     def delete():
    #         del flask.session['value']
    #         return 'value deleted'

    #     c = app.test_client()
    #     self.assertEqual(c.post('/set', data={'value': '42'}).data, b'value set')
    #     self.assertEqual(c.get('/get').data, b'42')
    #     c.post('/delete')

    def test_flasksqlalchemy_session(self):
        app = flask.Flask(__name__)
        app.debug = True
        app.config['SESSION_TYPE'] = 'sqlalchemy'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://businesscarduser:changemeifyoucan@db:3306/businesscard'
        app.config['SESSION_HEADER_NAME'] = 'X-TEST-SESSION'
        
        # Create Session in Python
        session = Session(app)
        # Create Table in SQLAlchemy database
        session.app.session_interface.db.create_all()

        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'

        @app.route('/get')
        def get():
            return flask.session['value']

        @app.route('/delete', methods=['POST'])
        def delete():
            del flask.session['value']
            return 'value deleted'

        c = app.test_client()
        temp_session_id = c.post('/set', data={'value': '42'}).headers['X-TEST-SESSION']
        self.assertEqual(c.get('/get', headers={'X-TEST-SESSION': str(temp_session_id)}).data, b'42')
        # c.post('/delete', headers={'X-TEST-SESSION': str(temp_session_id)})

    def test_flasksqlalchemy_session_with_signer(self):
        app = flask.Flask(__name__)
        app.debug = True
        app.secret_key = 'test_secret_key'
        app.config['SESSION_TYPE'] = 'sqlalchemy'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://businesscarduser:changemeifyoucan@db:3306/businesscard'
        app.config['SESSION_HEADER_NAME'] = 'X-TEST-SESSION'
        app.config['SESSION_USE_SIGNER'] = True
        
        # Create Session in Python
        session = Session(app)
        # Create Table in SQLAlchemy database
        session.app.session_interface.db.create_all()

        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'

        @app.route('/get')
        def get():
            return flask.session['value']

        @app.route('/delete', methods=['POST'])
        def delete():
            del flask.session['value']
            return 'value deleted'

        c = app.test_client()
        temp_session_id = c.post('/set', data={'value': '42'}).headers['X-TEST-SESSION']
        self.assertEqual(c.get('/get', headers={'X-TEST-SESSION': str(temp_session_id)}).data, b'42')
        # c.post('/delete', headers={'X-TEST-SESSION': str(temp_session_id)})

    def test_redis_session_use_signer(self):
        app = flask.Flask(__name__)
        app.secret_key = 'test_secret_key'
        app.debug = True
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_HEADER_NAME'] = 'X-TEST-SESSION'
        # Session, put into redis db 0
        app.config['SESSION_REDIS'] = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)
        Session(app)

        @app.route('/set', methods=['POST'])
        def set():
            flask.session['value'] = flask.request.form['value']
            return 'value set'

        @app.route('/get')
        def get():
            return flask.session['value']

        c = app.test_client()
        # Set the session by calling /set endpoint
        temp_session_id = c.post('/set', data={'value': '42'}).headers['X-TEST-SESSION']
        # Test the session by calling the /get endpoint with a header set as session identifier
        self.assertEqual(c.get('/get', headers={'X-TEST-SESSION': str(temp_session_id)}).data, b'42')


if __name__ == "__main__":
    unittest.main()
