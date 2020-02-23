import json
from peewee import *

db = SqliteDatabase('assets.db')


class Base(Model):
    class Meta:
        database = db


class User(Base):
    id = IntegerField(primary_key=True)
    name = TextField()


class Job(Base):
    id = IntegerField(primary_key=True)
    title = TextField()
    company = TextField()


class Tag(Base):
    tag = CharField()


class UserTags(Base):
    tag = ForeignKeyField(Tag)
    user_id = ForeignKeyField(User)

    class Meta:
        primary_key = CompositeKey('tag', 'user_id')


class JobTags(Base):
    tag = ForeignKeyField(Tag)
    job_id = ForeignKeyField(Job)

    class Meta:
        primary_key = CompositeKey('tag', 'job_id')


class Assets:
    """
    A class to represent all the assets

    Attributes
    ---------
    _users: List
        list of users currently loaded
    _jobs: List
        list of jobs currently loaded
    _tags: list
        list of tags currently loaded

    Methods
    ---------
    update_users(users_json=None)
        Get User data.

    update_jobs(jobs_json=None)
        Get Job data.

    """

    def __init__(self):
        self._db = db
        self._users = []
        self._jobs = []
        self._matches = []

    def create_tables(self):
        self._db.create_tables([Job, User, JobTags, UserTags, Tag])

    @property
    def users(self):
        return self._users

    @property
    def jobs(self):
        return self._jobs

    def update_users(self, users_json=None):
        """
        Get User data.
        :param users_json: path of file that contains user data
                        None if not given
        :type users_json: str
        :return: None
        """
        file_name = users_json if users_json is not None else 'data/users.json'
        with open(file_name) as users_json:
            user_data = json.load(users_json)
            for user in user_data:
                user_tags = user['tags']
                user_id = user['id']
                user_name = user['name']
                self._users.append(user_id)
                u, created = User.get_or_create(id=user_id, name=user_name)
                for tag in user_tags:
                    t, created = Tag.get_or_create(tag=tag)
                    UserTags.get_or_create(tag=t, user_id=u)

    def print_users(self):
        """
        Print Users Stored in Database
        """
        users_query = (User.select())
        users = users_query.dicts()
        for user in users:
            print(str(user))

    def update_jobs(self, jobs_json=None):
        """
        Get Job data.
        :param jobs_json: path of file that contains user job None if not given
        :type jobs_json: str
        :return: None
        """
        file_name = (jobs_json if jobs_json is not None else 'data/jobs.json')
        with open(file_name) as jobs_json:
            job_data = json.load(jobs_json)
            for job in job_data:
                job_id = job['id']
                job_name = job['title']
                job_company = job['company']
                job_tags = job['tags']
                self._jobs.append(job_id)
                j, created = Job.get_or_create(id=job_id, title=job_name, company=job_company)
                for tag in job_tags:
                    t, created = Tag.get_or_create(tag=tag)
                    JobTags.get_or_create(tag=t, job_id=j)

    def print_jobs(self):
        """
        Print Jobs Stored in Database
        """
        jobs_query = (Job.select())
        jobs = jobs_query.dicts()
        for job in jobs:
            print(str(job))

    def find_tag_match(self):
        """
        Find number of matches between first_tags and second_tags
        :param first_tags: List of tags for first object
        :type first_tags: list
        :param second_tags: List of tags for second object
        :type second_tags: list
        :return: number of matches
        :rtype: int
        """
        tags_query = (Tag
                      .select(JobTags.job_id, fn.GROUP_CONCAT(Tag.tag).alias("tags"))
                      .join(JobTags, on=(Tag.id == JobTags.tag_id))
                      .group_by(JobTags.job_id)
                      .order_by(JobTags.job_id))
        query = (User
                 .select(User.id.alias("userID"), Job.id, Job.title, Job.company, tags_query.c.tags)
                 .join(UserTags, JOIN.LEFT_OUTER, on=(UserTags.user_id == User.id))
                 .join(JobTags, on=(JobTags.tag_id == UserTags.tag_id))
                 .join(Job, on=(JobTags.job_id == Job.id))
                 .join(tags_query, on=(tags_query.c.job_id == Job.id))
                 .group_by(User.id, Job.id)
                 .having(fn.count(JobTags.tag_id) >= 2))
        q = query.dicts()
        for job in q:
            self._matches.append(job)
            tags = job['tags'].split(',')
            job_string = "'id': '{job_id}', 'title': '{title}', 'company': '{company}', 'tags': {tags}" \
                .format(job_id=job['id'], title=job['title'], company=job['company'], tags=tags)
            print("User " + str(job['userID']) + ' matched to {' + job_string + '}')
