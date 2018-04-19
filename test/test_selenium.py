import unittest
import threading
from selenium import webdriver
from app import create_app, db
from app.models import User, Role
import re
from forgery_py import internet, basic


class SeleniumTest(unittest.TestCase):
    client = None
    app_ctx = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Chrome(r"C:\Users\lg\AppData\Local\Google\Chrome\Application\chromedriver.exe")
        except:
            pass
        if cls.client:
            cls.app = create_app("testing")
            cls.app_ctx = cls.app.app_context()
            cls.app_ctx.push()
            db.drop_all()
            db.create_all()
            Role.seed()
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        # cls.client = webdriver.Chrome(r"C:\Users\lg\AppData\Local\Google\Chrome\Application\chromedriver.exe")
        cls.client.get("http://localhost:5000/shutdown")
        cls.client.close()
        # cls.client.quit()
        db.session.remove()
        cls.app_ctx.pop()

    def setUp(self):
        if self.client is None:
            self.skipTest("略过测试")

    def tearDown(self):
        pass

    def test_user_login(self):
        from login_page import LoginPage
        passwd = basic.text()
        username = internet.user_name()
        new_user = User(name=username,
                        email=internet.email_address(),
                        password=passwd)
        db.session.add(new_user)
        db.session.commit()
        # print(username,"+",passwd,"+",new_user)
        page = LoginPage(self.client)

        self.client.get("http://localhost:5000/auth/login")
        self.assertTrue(u"登录" in self.client.title)
        # 因为models 设置
        page.set_user_name(username)
        page.set_pwd(passwd)
        page.submit()
        self.assertTrue(re.search(u'欢迎来到Alan博客', self.client.page_source))
