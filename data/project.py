from model.project import Project
import random
import string


# generate random string
def random_string(prefix, maxlen):
    # generate string on letters, numbers symbols and spaces
    symbol = string.ascii_letters
    # generate string on random symbols and length
    return prefix + "".join([random.choice(symbol) for i in range(random.randrange(maxlen))])


def rand_test_data():
    rand_name = random_string("name", 10)
    rand_status = random.choice(("development", "release", "stable", "obsolete"))
    rand_inherit_global = random.choice(("True", "False"))
    rand_view_state = random.choice(("public", "private"))
    description = random_string("description", 20)
    return (Project(name=rand_name, status=rand_status, inherit_global=rand_inherit_global, view_state=rand_view_state,
                    description=description))
