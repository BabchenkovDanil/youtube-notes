from sqladmin import ModelView
from app.models import User, Video, Note



class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.created_at]
    column_searchable_list = [User.email]
    name = 'User'
    name_plural = 'Users'

class VideoAdmin(ModelView, model=Video):
    column_list = [Video.id, Video.title, Video.owner_id, Video.created_at]
    column_searchable_list = [Video.title]
    name = 'Video'
    name_plural = 'Videos'

class NoteAdmin(ModelView, model=Note):
    column_list = [Note.id, Note.text, Note.video_id, Note.owner_id, Note.created_at]
    name = 'Note'
    name_plural = 'Notes'