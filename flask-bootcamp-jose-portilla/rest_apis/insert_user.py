
from simple_example_api import db, User
import getpass


def useradd(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return User.query.filter_by(username=username).first()


def main():
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    result = useradd(username, password)
    print(result)


if __name__ == "__main__":
    main()
