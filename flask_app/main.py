from init import app, db
from user.api import userBp
#from poi.api import poiBp

app.register_blueprint(userBp, url_prefix='/user')
#app.register_blueprint(poiBp, url_prefix='/poi')

if __name__=='__main__':
   app.run(debug=True, hosts='0.0.0.0')
