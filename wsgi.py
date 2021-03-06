from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

#basedir = os.path.abspat(os.paat.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mmp!tR1t@localhost/states'
app.config['SQLALCHMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class State(db.Model):
  __tablename__ = 'states'
  did = db.Column(db.String(4), primary_key=True)
  timestamp = db.Column(db.String(32), primary_key=True)
  state = db.Column(db.String(16))

  def __init__(self, did, timestamp, state):
    self.did = did
    self.timestamp = timestamp
    self.state = state

  def __refr__(self):
    return '<State %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    # Add to the database and display updated values
    state = State(request.json['deviceId'], request.json['timestamp'],
		  request.json['operationalState'])
    db.session.add(state)
    db.session.commit()
    return jsonify({'success': 'state change added'}), 201
  else:
    # Display last 10 updates
    states = State.query.order_by(State.timestamp.desc()).limit(10).all()
    return render_template('index.html', states=states)
    
if __name__ == '__main__':
  app.run(debug=True)
