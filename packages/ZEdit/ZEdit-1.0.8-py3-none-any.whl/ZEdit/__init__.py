name = "ZEdit"

# set current directory to immediate parent
import sys, os
MY_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(MY_DIR) # there. foolproof.

try:
  import main
  run = main.run
except:
  from all_modules import *
  from mainapp import MainApp
  def run(*args, **kwargs):
    window = QApplication(sys.argv)
    QCoreApplication.setApplicationName(APPNAME)
    app = MainApp()
    app.restoreProject()
    sys.exit(window.exec_())
    
