from app import create_app

appliction = create_app("production")

if __name__ == "__main__":
    appliction.run()
