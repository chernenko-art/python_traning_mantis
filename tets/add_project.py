from model.project import Project


def test_add_project(app):
    project = Project(name="Project999", status="stable", view_state="private",
                      description="!!some description")
    if not app.project.add_project_page_is_view():
        app.project.open_add_project_page()
    old_list = app.project.get_project_list()
    app.project.add_new(project)
    new_list = app.project.get_project_list()
    old_list.append(project)
    assert sorted(old_list, key=Project.id_or_max) == sorted(new_list, key=Project.id_or_max)
