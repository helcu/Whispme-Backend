from flask import Flask
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
#from flask_restful_swagger import swagger

mysql = MySQL()
app = Flask(__name__)
PORT = 5000

# Cadena de coneccion de la base de datos

app.config['MYSQL_DATABASE_USER'] = 'bf64964c115591'
app.config['MYSQL_DATABASE_PASSWORD'] = '2f69db32'
app.config['MYSQL_DATABASE_DB'] = 'heroku_c975115db73d434'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-03.cleardb.net'

mysql.init_app(app)

api = Api(app)


class CreateUser(Resource):
    def post(self):

        try:
            parser = reqparse.RequestParser()

            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            parser.add_argument('user_name', type=str, help='user name to create user')

            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']
            _userName = args['user_name']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('WM_sp_CreateUser', (_userName, _userPassword, _userEmail))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode': '200', 'Message': 'User creation success'}
            else:
                return {'StatusCode': '1000', 'Message': str(data[0])}

            return {'Email': args['email'], 'Password': args['password'], 'User Name': args['user_name']}

        except Exception as e:

            return {'error': str(e)}


class Authenticate(Resource):

    def post(self):

        try:

            parser = reqparse.RequestParser()
            parser.add_argument('user_name', type=str, help='user name to create user')
            parser.add_argument('password', type=str, help='Password to create user')

            args = parser.parse_args()
            _userPassword = args['password']
            _userName = args['user_name']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('WM_sp_Authenticate', (_userName, _userPassword))
            data = cursor.fetchall()

            if len(data) > 0:

                return {'status': 200, 'UserId': str(data[0][0])}

            else:
                return {'status': 203, 'UserId': 'no existe'}

        except Exception as e:

            return {'error': str(e)}


class Test(Resource):
    def get(self):
        return {'mensaje':'pruebaWindoes'}

class Followers(Resource):

    def get(self, userid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('WM_sp_GetFollowers', [userid,])
            data = cursor.fetchall()

            items_list = []

            for item in data:
                i = {
                    'IDUser': item[0],
                    'UserName': item[1],
                    'UrlPhoto': item[2],
                    'Description': item[3],
                }
                items_list.append(i)

            return {'StatusCode': '200', 'Items': items_list}
        except Exception as e:
            return {'StatusCode': '200', 'Items': str(e)}


class Whispers(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('latitude', type=float, help='latitude position')
            parser.add_argument('longitude', type=float, help='longitude position ')
            args = parser.parse_args()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('WM_sp_GetWhisper', (args['latitude'], args['longitude']))
            data = cursor.fetchall()
            items_list = []

            for item in data:
                i = {
                    'IdWhisp': item[0],
                    'Latitude': item[1],
                    'Longitude': item[2],
                    'Distance': item[3],
                }
                items_list.append(i)

            return {'StatusCode': '200', 'Items': items_list}
        except Exception as e:
            return {'StatusCode': '200', 'Error': e}
class WhispersPost(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        #parser.add_argument('idWhisp', type=str, help='Email address to create user')
        parser.add_argument('idUser', type=str, help='Password to create user')
        parser.add_argument('title', type=str, help='user name to create user')
        parser.add_argument('dateCreation', type=str, help='user name to create user')
        parser.add_argument('latitude', type=float, help='user name to create user')
        parser.add_argument('longitude', type=float, help='user name to create user')
        parser.add_argument('urlAudio', type=str, help='user name to create user')
        parser.add_argument('place', type=str, help='user name to create user')
        parser.add_argument('text', type=str, help='user name to create user')
        parser.add_argument('urlPhoto', type=str, help='user name to create user')
        args = parser.parse_args()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('WM_sp_PostWhisper', (args['idUser'], args['title'],args['dateCreation'],args['latitude'],args['longitude'],args['urlAudio'],args['place'],args['text'],args['urlPhoto']))
        data = cursor.execute()
        conn.commit()
        return {'StatusCode': '200', 'Message': 'Whisp upload'}


class WhispersDetail(Resource):
    def get(self,whispId):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('WM_sp_GetWhisperDetail', [whispId,])
            data = cursor.fetchall()
            items_list = []

            for item in data:
                i = {
                    'idWhisp': item[0],
                    'idUser': item[1],
                    'title': item[2],
                    'dateCreation': str(item[3]),
                    'latitude': item[4],
                    'longitude': item[5],
                    'urlAudio': item[6],
                    'place': item[7],
                    'text': item[8],
                    'urlPhoto': item[9],
                }
                items_list.append(i)
            return {'StatusCode': '200', 'Items': items_list}
        except Exception as e:
            return {'StatusCode': '200', 'Error': e}


class AccountDetail(Resource):
    def get(self, whispId):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('WM_sp_GetWhisperDetail', [whispId, ])
            data = cursor.fetchall()
            items_list = []

            for item in data:
                i = {
                    'idWhisp': item[0],
                    'idUser': item[1],
                    'title': item[2],
                    'dateCreation': str(item[3]),
                    'latitude': item[4],
                    'longitude': item[5],
                    'urlAudio': item[6],
                    'place': item[7],
                    'text': item[8],
                    'urlPhoto': item[9],
                }
                items_list.append(i)
            return {'StatusCode': '200', 'Items': items_list}
        except Exception as e:
            return {'StatusCode': '200', 'Error': e}

#Declaracion de la ruta y agregado al recurso

api.add_resource(CreateUser, '/CreateUser')
api.add_resource(Authenticate, '/AuthenticateUser')
api.add_resource(Followers, '/Followers/<userid>')
api.add_resource(Whispers, '/Whispers')
api.add_resource(WhispersPost, '/WhispersPost')
api.add_resource(WhispersDetail, '/WhispersDeteail/<whispId>')
api.add_resource(AccountDetail, '/AccountDetail/<userId>')

api.add_resource(Test, '/')

if __name__ == '__main__':
    app.run(debug=False)
