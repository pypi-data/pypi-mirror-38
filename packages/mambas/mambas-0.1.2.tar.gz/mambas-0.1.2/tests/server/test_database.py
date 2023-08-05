import datetime
import os
import pytest

from mambas.server import models
from mambas.server import database

class TestMambasDatabase():

    def create_test_db(self, db):
        mambas_path = db.create_and_get_home()
        db.db_path = os.path.join(mambas_path, "test_database.db")
        self.destroy_test_db(db)
        db.init_tables()

    def destroy_test_db(self, db):
        if os.path.exists(db.db_path):
            os.remove(db.db_path)

    def test_create_project(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        project = db.create_project("Project1", "MyToken")
        assert project.name == "Project1"
        assert project.token == "MyToken"
        self.destroy_test_db(db)
    
    def test_get_project(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id = db.create_project("Project1", "MyToken").id_project
        project = db.get_project(id)
        assert project.name == "Project1"
        assert project.token == "MyToken"
        self.destroy_test_db(db)

    def test_get_project_by_token(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        db.create_project("Project1", "MyToken")
        project = db.get_project_by_token("MyToken")
        assert project.name == "Project1"
        assert project.token == "MyToken"
        self.destroy_test_db(db)

    def test_get_all_projects(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        db.create_project("Project1", "MyToken")
        projects = db.get_all_projects()
        assert len(projects) == 1
        assert projects[0].name == "Project1"
        assert projects[0].token == "MyToken"
        self.destroy_test_db(db)

    def test_increment_project_session_counter(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id = db.create_project("Project1", "MyToken").id_project
        project = db.increment_project_session_counter(id)
        assert project.session_counter == 1
        self.destroy_test_db(db)

    def test_delete_project(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id = db.create_project("Project1", "MyToken").id_project
        result = db.delete_project(id)
        assert result == True
        self.destroy_test_db(db)

    def test_create_session_for_project(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id = db.create_project("Project1", "MyToken").id_project
        session = db.create_session_for_project(1, "127.0.0.1", id)
        assert session.index == 1
        assert session.host == "127.0.0.1"
        assert session.id_project == id
        assert session.is_active == True
        self.destroy_test_db(db)

    def test_get_session(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        session = db.get_session(id)
        assert session.index == 1
        assert session.host == "127.0.0.1"
        assert session.id_project == id
        self.destroy_test_db(db)

    def test_get_sessions_for_project(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id = db.create_project("Project1", "MyToken").id_project
        db.create_session_for_project(1, "127.0.0.1", id)
        sessions = db.get_sessions_for_project(id)
        assert len(sessions) == 1
        assert sessions[0].index == 1
        assert sessions[0].host == "127.0.0.1"
        assert sessions[0].id_project == id
        self.destroy_test_db(db)

    def test_set_session_inactive(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        session = db.set_session_inactive(id)
        assert session.is_active == False
        self.destroy_test_db(db)

    def test_set_session_start_time(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        now = datetime.datetime.now()
        session = db.set_session_start_time(id, now)
        assert session.dt_start.year == now.year
        assert session.dt_start.month == now.month
        assert session.dt_start.day == now.day
        assert session.dt_start.hour == now.hour
        assert session.dt_start.minute == now.minute
        assert session.dt_start.second == now.second
        self.destroy_test_db(db)

    def test_set_session_end_time(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        now = datetime.datetime.now()
        session = db.set_session_end_time(id, now)
        assert session.dt_end.year == now.year
        assert session.dt_end.month == now.month
        assert session.dt_end.day == now.day
        assert session.dt_end.hour == now.hour
        assert session.dt_end.minute == now.minute
        assert session.dt_end.second == now.second
        self.destroy_test_db(db)

    def test_delete_session(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        result = db.delete_session(id)
        assert result == True
        self.destroy_test_db(db)

    def test_create_epoch_for_session(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        now = datetime.datetime.now()
        epoch = db.create_epoch_for_session(0, {}, now, id)
        assert epoch.index == 0
        assert len(epoch.metrics) == 0
        assert epoch.time.strftime("%Y-%m-%d %H:%M:%S") == now.strftime("%Y-%m-%d %H:%M:%S")
        assert epoch.id_session == id
        self.destroy_test_db(db)

    def test_get_epoch(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id_session = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        now = datetime.datetime.now()
        id = db.create_epoch_for_session(0, {}, now, id_session).id_epoch
        epoch = db.get_epoch(id)
        assert epoch.index == 0
        assert len(epoch.metrics) == 0
        assert epoch.time.strftime("%Y-%m-%d %H:%M:%S") == now.strftime("%Y-%m-%d %H:%M:%S")
        assert epoch.id_session == id
        self.destroy_test_db(db)

    def test_get_epochs_for_session(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        now = datetime.datetime.now()
        db.create_epoch_for_session(0, {}, now, id)
        epochs = db.get_epochs_for_session(id)
        assert len(epochs) == 1
        assert epochs[0].index == 0
        assert len(epochs[0].metrics) == 0
        assert epochs[0].time.strftime("%Y-%m-%d %H:%M:%S") == now.strftime("%Y-%m-%d %H:%M:%S")
        assert epochs[0].id_session == id
        self.destroy_test_db(db)

    def test_delete_epoch(self):
        db = database.MambasDatabase()
        self.create_test_db(db)
        id_project = db.create_project("Project1", "MyToken").id_project
        id_session = db.create_session_for_project(1, "127.0.0.1", id_project).id_session
        now = datetime.datetime.now()
        id = db.create_epoch_for_session(0, {}, now, id_session).id_epoch
        result = db.delete_epoch(id)
        assert result == True
        self.destroy_test_db(db)

if __name__ == "__main__":
    pytest.main([__file__])