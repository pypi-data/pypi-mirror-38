import bottle
import pkg_resources

# BASE VIEW -----------------------------------------------------------------------------

class BaseView():

    def __init__(self):
        self.view_model = {}
        self.view_model["navigation_projects"] = []
        self.view_model["icons"] = []
        self.view_model["breadcrumbs"] = []
        self.set_header_footer()
        self.custom_template = None

    def set_title(self, title):
        self.view_model["title"] = title

    def set_navigation_projects(self, projects):
        for project in projects:
            navigation_project = {}
            navigation_project["name"] = project.name
            navigation_project["id"] = project.id_project
            self.view_model["navigation_projects"].append(navigation_project)

    def add_icon(self, icon):
        self.view_model["icons"].append(icon)

    def add_breadcrumb(self, label, url):
        self.view_model["breadcrumbs"].append({"label": label, "url": url})

    def set_header_footer(self):
        header_path = pkg_resources.resource_filename(__package__, self.template_path("header"))
        self.view_model["header_path"] = header_path
        footer_path = pkg_resources.resource_filename(__package__, self.template_path("footer"))
        self.view_model["footer_path"] = footer_path

    def template_path(self, type):
        # TODO: check if template file exists otherwise raise error
        return "components/html/{}.tpl.html".format(type)

    def render(self):
        pass

    def create(self):
        self.render()
        template = self.custom_template or self.type
        template_path = pkg_resources.resource_filename(__package__, self.template_path(template))
        view = bottle.template(template_path, self.view_model)
        return view

# DASHBOARD VIEW ------------------------------------------------------------------------

class DashboardView(BaseView):

    def __init__(self):
        super().__init__()
        self.type = "dashboard"

    def set_projects(self, projects):
        self.projects = projects

    def set_sessions(self, sessions):
        self.sessions = sessions

    def render(self):
        self.set_title("Dashboard")
        self.add_icon({"type": "create_project"})
        self.add_breadcrumb("Dashboard", "/dashboard")

        self.view_model["number_projects"] = len(self.projects)
        self.view_model["number_running_sessions"] = sum([session.is_active for session in self.sessions])

        self.view_model["list_projects"] = []
        for project in self.projects:
            list_project = {}
            list_project["id"] = project.id_project
            list_project["name"] = project.name
            list_project["number_sessions"] = len([s for s in self.sessions if s.id_project == project.id_project])
            list_project["token"] = project.token
            self.view_model["list_projects"].append(list_project)

        self.view_model["list_last_sessions"] = []
        for i, session in enumerate(sorted(self.sessions, key=lambda s: s.index, reverse=True)[:5]):
            project = next(p for p in self.projects if p.id_project == session.id_project)
            list_session = {}
            list_session["id"] = session.id_session
            list_session["index"] = session.index
            list_session["start_date"] = session.dt_start
            if session.dt_start is not None and session.dt_end is not None:
                list_session["duration"] = session.dt_end - session.dt_start
            list_session["project_name"] = project.name
            list_session["is_active"] = session.is_active
            list_session["is_favorite"] = session.is_favorite
            list_session["id_project"] = session.id_project
            list_session["name"] = "{}: {}".format(project.name, session.index)
            self.view_model["list_last_sessions"].append(list_session)
        self.view_model["number_list_last_sessions"] = len(self.view_model["list_last_sessions"])

# PROJECT VIEWS -------------------------------------------------------------------------

class ProjectView(BaseView):

    def set_project(self, project):
        self.project = project
        
    def set_project_sessions(self, sessions):
        self.sessions = sessions

    def set_project_sessions_epochs(self, sessions_epochs):
        self.sessions_epochs = sessions_epochs

    def render(self):
        icon_display_token = {}
        icon_display_token["type"] = "display_token"
        icon_display_token["token"] = self.project.token
        self.add_icon(icon_display_token)

        icon_delete_project = {}
        icon_delete_project["type"] = "delete_project"
        icon_delete_project["project_name"] = self.project.name
        icon_delete_project["id_project"] = self.project.id_project
        self.add_icon(icon_delete_project)

        self.add_breadcrumb(self.project.name, "/projects/{}".format(self.project.id_project))

        self.view_model["id"] = self.project.id_project

        if len(self.sessions) < 1:
            self.custom_template = "instructions"

class ProjectDashboardView(ProjectView):

    def __init__(self):
        super().__init__()
        self.type = "project_dashboard"

    def render(self):
        super().render()

        self.set_title("{} Dashboard".format(self.project.name))

        # Loss & Accuracy

        self.view_model["graph_sessions_loss"] = []
        for i, session in enumerate(self.sessions[-10:]):
            losses = [epoch.metrics["loss"] for epoch in self.sessions_epochs[i] if "loss" in epoch.metrics]
            if len(losses) > 0:
                graph_sessions_loss_session = {}
                graph_sessions_loss_session["session"] = session.index
                graph_sessions_loss_session["loss"] = min(losses)
                self.view_model["graph_sessions_loss"].append(graph_sessions_loss_session)
        self.view_model["number_graph_sessions_loss"] = len(self.view_model["graph_sessions_loss"])

        last_loss_sessions = self.view_model["graph_sessions_loss"][-2:]
        if(len(last_loss_sessions) > 1):
            if(last_loss_sessions[0]["loss"] - last_loss_sessions[1]["loss"] > 0):
                self.view_model["sessions_loss_state"] = "positive"
            elif(last_loss_sessions[0]["loss"] - last_loss_sessions[1]["loss"] < 0):
                self.view_model["sessions_loss_state"] = "negative"

        self.view_model["graph_sessions_acc"] = []
        for i, session in enumerate(self.sessions[-10:]):
            accs = [epoch.metrics["acc"] for epoch in self.sessions_epochs[i] if "acc" in epoch.metrics]
            if len(accs) > 0:
                graph_sessions_acc_session = {}
                graph_sessions_acc_session["session"] = session.index
                graph_sessions_acc_session["acc"] = min(accs)
                self.view_model["graph_sessions_acc"].append(graph_sessions_acc_session)
        self.view_model["number_graph_sessions_acc"] = len(self.view_model["graph_sessions_acc"])

        last_acc_sessions = self.view_model["graph_sessions_acc"][-2:]
        if(len(last_acc_sessions) > 1):
            if(last_acc_sessions[0]["acc"] - last_acc_sessions[1]["acc"] > 0):
                self.view_model["sessions_acc_state"] = "negative"
            elif(last_acc_sessions[0]["acc"] - last_acc_sessions[1]["acc"] < 0):
                self.view_model["sessions_acc_state"] = "positive"

        # Sessions

        self.view_model["number_sessions"] = len(self.sessions)
        self.view_model["number_running_sessions"] = sum([s.is_active for s in self.sessions])
        self.view_model["number_favorite_sessions"] = sum([s.is_favorite for s in self.sessions])

        self.view_model["list_last_sessions"] = []
        for i, session in enumerate(sorted(self.sessions, key=lambda s: s.index, reverse=True)[:5]):
            list_session = {}
            list_session["id"] = session.id_session
            list_session["index"] = session.index
            list_session["start_date"] = session.dt_start
            if session.dt_start is not None and session.dt_end is not None:
                list_session["duration"] = session.dt_end - session.dt_start
            list_session["is_active"] = session.is_active
            list_session["is_favorite"] = session.is_favorite
            losses = [epoch.metrics["loss"] for epoch in self.sessions_epochs[i] if "loss" in epoch.metrics]
            if len(losses) > 0:
                list_session["loss"] = round(min(losses), 2)
            accs = [epoch.metrics["acc"] for epoch in self.sessions_epochs[i] if "acc" in epoch.metrics]
            if len(accs) > 0:
                list_session["acc"] = round(max(accs), 2)
            list_session["id_project"] = self.project.id_project
            list_session["name"] = "{}: {}".format(self.project.name, session.index)
            self.view_model["list_last_sessions"].append(list_session)
        self.view_model["number_list_last_sessions"] = len(self.view_model["list_last_sessions"])

class ProjectSessionsView(ProjectView):

    def __init__(self):
        super().__init__()
        self.type = "project_sessions"

    def render(self):
        super().render()

        self.set_title("{} Sessions".format(self.project.name))

        self.view_model["list_sessions"] = []
        for i, session in enumerate(sorted(self.sessions, key=lambda s: s.index, reverse=True)):
            list_session = {}
            list_session["id"] = session.id_session
            list_session["index"] = session.index
            list_session["start_date"] = session.dt_start
            if session.dt_start is not None and session.dt_end is not None:
                list_session["duration"] = session.dt_end - session.dt_start
            list_session["is_active"] = session.is_active
            list_session["is_favorite"] = session.is_favorite
            losses = [epoch.metrics["loss"] for epoch in self.sessions_epochs[i] if "loss" in epoch.metrics]
            if len(losses) > 0:
                min_loss = min(losses)
                list_session["loss"] = round(min_loss, 2)
                if(i > 0):
                    last_losses = [epoch.metrics["loss"] for epoch in self.sessions_epochs[i-1] if "loss" in epoch.metrics]
                    if(len(last_losses) > 0):
                        if(min(last_losses) - min_loss > 0):
                            list_session["loss_state"] = "positive"
                        elif(min(last_losses) - min_loss < 0):
                            list_session["loss_state"] = "negative"
            accs = [epoch.metrics["acc"] for epoch in self.sessions_epochs[i] if "acc" in epoch.metrics]
            if len(accs) > 0:
                max_acc = max(accs)
                list_session["acc"] = round(max_acc, 2)
                if(i > 0):
                    last_accs = [epoch.metrics["acc"] for epoch in self.sessions_epochs[i-1] if "acc" in epoch.metrics]
                    if(len(last_accs) > 0):
                        if(min(last_accs) - max_acc > 0):
                            list_session["acc_state"] = "negative"
                        elif(min(last_accs) - max_acc < 0):
                            list_session["acc_state"] = "positive"
            list_session["id_project"] = self.project.id_project
            list_session["name"] = "{}: {}".format(self.project.name, session.index)
            self.view_model["list_sessions"].append(list_session)

        self.add_breadcrumb("Sessions", "/projects/{}/sessions".format(self.project.id_project))

# SESSION VIEW --------------------------------------------------------------------------

class SessionView(BaseView):

    def __init__(self):
        super().__init__()
        self.type = "session"

    def set_project(self, project):
        self.project = project
      
    def set_session(self, session):
        self.session = session

    def set_session_epochs(self, epochs):
        self.epochs = epochs

    def render(self):
        self.set_title("{}: Session {}".format(self.project.name, self.session.index))
        self.add_breadcrumb(self.project.name, "/projects/{}".format(self.project.id_project))
        self.add_breadcrumb("Sessions", "/projects/{}/sessions".format(self.project.id_project))
        self.add_breadcrumb("Session {}".format(self.session.index),
            "/projects/{}/sessions/{}".format(self.project.id_project, self.session.id_session))

        self.view_model["graphs"] = {}

        for epoch in self.epochs:
            for k, v in epoch.metrics.items():
                if "loss" in k:
                    graph_name = "loss"
                    if not graph_name in self.view_model["graphs"].keys():
                        self.view_model["graphs"][graph_name] = {}
                        name = "{}-Session{}-{}".format(self.project.name, self.session.index, "loss")
                        self.view_model["graphs"][graph_name]["name"] = name.lower()
                        self.view_model["graphs"][graph_name]["data"] = []
                    if not any(d["epoch"] == epoch.index for d in self.view_model["graphs"][graph_name]["data"]):
                        self.view_model["graphs"][graph_name]["data"].append({"epoch": epoch.index, "time": epoch.time.strftime("%Y-%m-%d %H:%M:%S")})
                    next(d for d in self.view_model["graphs"][graph_name]["data"] if d["epoch"] == epoch.index)[k] = v
                elif "acc" in k:
                    graph_name = "acc"
                    if not graph_name in self.view_model["graphs"].keys():
                        self.view_model["graphs"][graph_name] = {}
                        name = "{}-Session{}-{}".format(self.project.name, self.session.index, "accuracy")
                        self.view_model["graphs"][graph_name]["name"] = name.lower()
                        self.view_model["graphs"][graph_name]["data"] = []
                    if not any(d["epoch"] == epoch.index for d in self.view_model["graphs"][graph_name]["data"]):
                        self.view_model["graphs"][graph_name]["data"].append({"epoch": epoch.index, "time": epoch.time.strftime("%Y-%m-%d %H:%M:%S")})
                    next(d for d in self.view_model["graphs"][graph_name]["data"] if d["epoch"] == epoch.index)[k] = v
                else:
                    graph_name = k
                    if not graph_name in self.view_model["graphs"].keys():
                        self.view_model["graphs"][graph_name] = {}
                        name = "{}-Session{}-{}".format(self.project.name, self.session.index, graph_name)
                        self.view_model["graphs"][graph_name]["name"] = name.lower()
                        self.view_model["graphs"][graph_name]["data"] = []
                    if not any(d["epoch"] == epoch.index for d in self.view_model["graphs"][graph_name]["data"]):
                        self.view_model["graphs"][graph_name]["data"].append({"epoch": epoch.index, "time": epoch.time.strftime("%Y-%m-%d %H:%M:%S")})
                    next(d for d in self.view_model["graphs"][graph_name]["data"] if d["epoch"] == epoch.index)[k] = v

        self.view_model["is_active"] = self.session.is_active
        self.view_model["number_epochs"] = len(self.epochs)
        if self.session.dt_start is not None and self.session.dt_end is not None:
            self.view_model["duration"] = self.session.dt_end - self.session.dt_start

        icon_mark_favorite = {}
        icon_mark_favorite["type"] = "mark_favorite"
        icon_mark_favorite["is_favorite"] = self.session.is_favorite
        icon_mark_favorite["id_project"] = self.session.id_project
        icon_mark_favorite["id_session"] = self.session.id_session
        self.add_icon(icon_mark_favorite)

        icon_delete_session = {}
        icon_delete_session["type"] = "delete_session"
        icon_delete_session["session_name"] = "{}: {}".format(self.project.name, self.session.index)
        icon_delete_session["id_session"] = self.session.id_session
        icon_delete_session["id_project"] = self.session.id_project
        self.add_icon(icon_delete_session)