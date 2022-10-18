from app.libs.MySQL.connector import Connector
from app.settings import Settings
from app.libs.MySQL.db_requests import DBRequests

connector = Connector(Settings())


def insert_paper_with_query(query_id, paper_id):
    connector.execute(
        query=DBRequests.insert_paper_with_query,
        args=[query_id, paper_id],
        commit=True)

def get_not_saved_papers(papers_ids):
    raw_ids = connector.execute(
        query=DBRequests.get_not_saved_papers % (str(papers_ids).replace('[', '(').replace(']', ')')))
    result = [id[0] for id in raw_ids]
    return result

def insert_paper(paper_info):
    connector.execute(
        query=DBRequests.insert_paper_info,
        args=paper_info,
        commit=True,
        many=True
    )

def get_authors_ids():
    ids = connector.execute(
        query=DBRequests.get_authors_ids
    )
    return [id[0] for id in ids]

def get_papers_ids():
    ids = connector.execute(
        query=DBRequests.get_papers_ids
    )
    return [id[0] for id in ids]

def insert_subject_area(area_info):
    connector.execute(
        query=DBRequests.insert_subject_area,
        args=area_info,
        commit=True,
        many=True
    )

def insert_author_subject_areas(area_info):
    connector.execute(
        query=DBRequests.insert_author_subject_area,
        args=area_info,
        commit=True,
        many=True
    )

def update_author_info_db(author_info):
    connector.execute(
        query=DBRequests.update_author_info,
        args=author_info,
        commit=True
    )

def insert_affiliation_history(affil_history_info):
    connector.execute(
        query=DBRequests.insert_affiliation_history,
        args=affil_history_info,
        commit=True,
        many=True
    )

def insert_affiliations(affil_info):
    connector.execute(
        query=DBRequests.insert_affiliation,
        args=affil_info,
        commit=True,
        many=True
    )

def update_paper_last_time(paper_id, last_time):
    connector.execute(
        query=DBRequests.update_paper_last_time,
        args=[last_time, paper_id],
        commit=True
    )

def insert_paper_authors(author_info):
    connector.execute(
        query=DBRequests.insert_paper_author,
        args=author_info,
        commit=True,
        many=True
    )

def insert_paper_keywords(info):
    connector.execute(
        query=DBRequests.insert_paper_keyword,
        args=info,
        commit=True,
        many=True
    )

def insert_author(author_info):
    connector.execute(
        query=DBRequests.insert_author,
        args=author_info,
        commit=True,
        many=True
    )

def insert_keywords(keywords):
    # query_keywords = ["('"+kw+"')" for kw in keywords]
    # query_keywords = ', '.join(query_keywords)
    tuple_keywords = [(k,) for k in keywords]
    connector.execute(
        query=DBRequests.insert_keyword,
        args=tuple_keywords,
        commit=True,
        many=True
    )


def get_top_scopus_authors(query_id: int):
    authors_list = connector.execute(
        query=DBRequests.get_top_scopus_authors_req,
        args=(query_id, )
    )
    return authors_list


def save_pub_author_info(pub_author_info: list):
    connector.execute(
        query=DBRequests.save_pub_info,
        args=pub_author_info,
        commit=True,
        many=True
    )