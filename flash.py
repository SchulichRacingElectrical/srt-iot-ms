from main import app

class Flash:
  def __init__(self):
    pass

  @app.route("/flash/get_version")
  def get_version(self):
    pass

  @app.route("/flash/get_sensors")
  def get_sensors(self):
    pass

  @app.route("/flash/get_diff")
  def get_diff(self, version):
    pass