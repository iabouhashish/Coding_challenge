from lookup import *

if __name__ == "__main__":
    # Setup Assets
    assets = Assets()
    assets.create_tables()
    # import users
    assets.update_users()
    # import jobs
    assets.update_jobs()

    assets.find_tag_match()
