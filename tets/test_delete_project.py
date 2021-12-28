import random
from model.project import Project
from data.project import rand_test_data


def test_delete_project(app):
    if len(app.project.get_project_list()) == 0:
        project = rand_test_data()
        app.project.add_new(project)
    old_list = app.project.get_project_list()
    project = random.choice(old_list)
    app.project.delete_by_index(project.id)
    new_list = app.project.get_project_list()
    old_list.remove(project)
    assert sorted(old_list, key=Project.id_or_max) == sorted(new_list, key=Project.id_or_max)
