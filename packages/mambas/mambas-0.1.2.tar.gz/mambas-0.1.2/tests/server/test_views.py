import datetime
import pytest

from mambas.server import models
from mambas.server import views

class TestBaseView():

    def test_set_title(self):
        base_view = views.BaseView()
        base_view.set_title("MyTitle")
        assert base_view.view_model["title"] == "MyTitle"

    def test_set_navigation_projects(self):
        base_view = views.BaseView()
        projects = [models.Project(1, "Project1", 0, "token")]
        base_view.set_navigation_projects(projects)
        assert base_view.view_model["navigation_projects"][0]["id"] == 1
        assert base_view.view_model["navigation_projects"][0]["name"] == "Project1"

    def test_add_icon(self):
        base_view = views.BaseView()
        base_view.add_icon({"type": "create_project"})
        assert base_view.view_model["icons"][0]["type"] == "create_project"

    def test_add_breadcrumb(self):
        base_view = views.BaseView()
        base_view.add_breadcrumb("Dashboard", "/dashboard")
        assert base_view.view_model["breadcrumbs"][0]["label"] == "Dashboard"
        assert base_view.view_model["breadcrumbs"][0]["url"] == "/dashboard"

    def test_set_header_footer(self):
        base_view = views.BaseView()
        base_view.set_header_footer()
        assert base_view.view_model["header_path"].endswith("components/html/header.tpl.html")
        assert base_view.view_model["footer_path"].endswith("components/html/footer.tpl.html")

    def test_template_path(self):
        base_view = views.BaseView()
        template_path = base_view.template_path("template")
        assert template_path == "components/html/template.tpl.html"

class TestDashboardView():

    def test_init(self):
        dashboard_view = views.DashboardView()
        assert dashboard_view.type == "dashboard"

    def test_render(self):
        dashboard_view = views.DashboardView()
        dashboard_view.set_projects([models.Project(1, "Project1", 0, "token")])
        dashboard_view.set_sessions([models.Session(1, 1, None, None, True, False, "127.0.0.1", 1)])
        dashboard_view.render()
        assert dashboard_view.view_model["title"] == "Dashboard"
        assert dashboard_view.view_model["number_projects"] == 1
        assert dashboard_view.view_model["number_running_sessions"] == 1
        assert dashboard_view.view_model["icons"][0]["type"] == "create_project"
        assert dashboard_view.view_model["breadcrumbs"][0]["label"] == "Dashboard"
        assert dashboard_view.view_model["breadcrumbs"][0]["url"] == "/dashboard"

class TestProjectView():

    def test_set_project(self):
        project_view = views.ProjectView()
        project = models.Project(1, "Project1", 0, "token")
        project_view.set_project(project)
        assert project_view.project == project

    def test_set_project_sessions(self):
        project_view = views.ProjectView()
        sessions = [models.Session(1, 1, None, None, True, False, "127.0.0.1", 1)]
        project_view.set_project_sessions(sessions)
        assert project_view.sessions[0] == sessions[0]

    def test_render(self):
        project_view = views.ProjectView()
        project = models.Project(1, "Project1", 0, "token")
        project_view.set_project(project)
        sessions = [models.Session(1, 1, None, None, True, False, "127.0.0.1", 1)]
        project_view.set_project_sessions(sessions)
        project_view.render()
        assert any(d["type"] == "display_token" for d in project_view.view_model["icons"])
        assert any(d["type"] == "delete_project" for d in project_view.view_model["icons"])
        assert project_view.view_model["breadcrumbs"][0]["label"] == "Project1"
        assert project_view.view_model["breadcrumbs"][0]["url"] == "/projects/1"

    def test_render_instructions(self):
        project_view = views.ProjectView()
        project = models.Project(1, "Project1", 0, "token")
        project_view.set_project(project)
        project_view.set_project_sessions([])
        project_view.render()
        assert project_view.custom_template == "instructions"

class TestProjectDashboardView():

    def test_init(self):
        project_dashboard_view = views.ProjectDashboardView()
        assert project_dashboard_view.type == "project_dashboard"

class TestProjectSessionView():

    def test_init(self):
        project_sessions_view = views.ProjectSessionsView()
        assert project_sessions_view.type == "project_sessions"

    def test_render(self):
        project_sessions_view = views.ProjectSessionsView()
        project = models.Project(1, "Project1", 0, "token")
        project_sessions_view.set_project(project)
        sessions = [models.Session(1, 1, None, None, True, False, "127.0.0.1", 1)]
        project_sessions_view.set_project_sessions(sessions)
        sessions_epochs = [[models.Epoch(1, 0, {"loss": 0, "acc": 1, "custom": 2}, datetime.datetime.now(), 1)]]
        project_sessions_view.set_project_sessions_epochs(sessions_epochs)
        project_sessions_view.render()
        assert project_sessions_view.view_model["list_sessions"][0]["id"] == 1
        assert project_sessions_view.view_model["list_sessions"][0]["index"] == 1
        assert project_sessions_view.view_model["list_sessions"][0]["is_active"] == True
        assert project_sessions_view.view_model["list_sessions"][0]["loss"] == 0
        assert project_sessions_view.view_model["list_sessions"][0]["acc"] == 1
        assert project_sessions_view.view_model["breadcrumbs"][1]["label"] == "Sessions"
        assert project_sessions_view.view_model["breadcrumbs"][1]["url"] == "/projects/1/sessions"

class TestSessionView():

    def test_init(self):
        session_view = views.SessionView()
        assert session_view.type == "session"

    def test_set_project(self):
        session_view = views.SessionView()
        project = models.Project(1, "Project1", 0, "token")
        session_view.set_project(project)
        assert session_view.project == project

    def test_set_session(self):
        session_view = views.SessionView()
        session = models.Session(1, 1, None, None, True, False, "127.0.0.1", 1)
        session_view.set_session(session)
        assert session_view.session == session

    def test_set_session_epochs(self):
        session_view = views.SessionView()
        epochs = [models.Epoch(1, 0, None, None, 1)]
        session_view.set_session_epochs(epochs)
        assert session_view.epochs[0] == epochs[0]

    def test_render(self):
        session_view = views.SessionView()
        project = models.Project(1, "Project1", 0, "token")
        session_view.set_project(project)
        session = models.Session(1, 1, None, None, True, False, "127.0.0.1", 1)
        session_view.set_session(session)
        epochs = [models.Epoch(1, 0, {"loss": 0, "acc": 1, "custom": 2}, datetime.datetime.now(), 1)]
        session_view.set_session_epochs(epochs)
        session_view.render()
        assert session_view.view_model["breadcrumbs"][0]["label"] == "Project1"
        assert session_view.view_model["breadcrumbs"][0]["url"] == "/projects/1"
        assert session_view.view_model["breadcrumbs"][1]["label"] == "Sessions"
        assert session_view.view_model["breadcrumbs"][1]["url"] == "/projects/1/sessions"
        assert session_view.view_model["breadcrumbs"][2]["url"] == "/projects/1/sessions/1"
        assert session_view.view_model["graphs"]["loss"]["data"][0]["epoch"] == 0
        assert session_view.view_model["graphs"]["loss"]["data"][0]["loss"] == 0
        assert session_view.view_model["graphs"]["acc"]["data"][0]["epoch"] == 0
        assert session_view.view_model["graphs"]["acc"]["data"][0]["acc"] == 1
        assert session_view.view_model["graphs"]["custom"]["data"][0]["epoch"] == 0
        assert session_view.view_model["graphs"]["custom"]["data"][0]["custom"] == 2
        assert session_view.view_model["is_active"] == True
        assert session_view.view_model["number_epochs"] == 1
        assert any(d["type"] == "delete_session" for d in session_view.view_model["icons"])

if __name__ == "__main__":
    pytest.main([__file__])