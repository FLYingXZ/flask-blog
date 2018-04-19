from flask_script import Manager
from app import create_app, db
#python3 不能侦测到models必须引用进来
from  app.models import Role,User,Post,Comment
from flask_migrate import Migrate, MigrateCommand,upgrade

app = create_app("default")
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    import unittest
    tests=unittest.TestLoader().discover("test")
    unittest.TextTestRunner(verbosity=2).run(tests)
# 自动重新加载
@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch("**/*.*")
    live_server.serve(host="127.0.0.1", open_url_delay=False)
@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post,Comment=Comment)
@manager.command
def deploy():
    upgrade()
    Role.seed()

if __name__ == '__main__':
    # app.run(debug=True,host="0.0.0.0",port=5500)
    manager.run()
