class DBRequests:
    insert_paper_with_query = '''
        INSERT INTO scopus_paper_query
        (query_id, scopus_paper_id)
        VALUES (%s, %s)
    '''

    get_not_saved_papers = '''
        SELECT DISTINCT id FROM scopus_paper WHERE id IN %s
    '''

    insert_paper_info = '''
        INSERT IGNORE INTO scopus_paper (id, title, cited_by_count, cover_date, doi, eid, url)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    '''

    get_authors_ids = '''
        SELECT id FROM scopus_author WHERE last_update IS NULL
    '''

    get_papers_ids = '''
        SELECT id FROM scopus_paper WHERE last_update IS NULL
    '''

    insert_subject_area = '''
        INSERT IGNORE INTO scopus_subject_area (id, name, abbr)
        VALUES (%s, %s, %s)
    '''

    insert_author_subject_area = '''
        INSERT INTO scopus_author_subject_area (author_id, subject_area_id)
        VALUES (%s, %s)
    '''

    update_author_info = '''
            UPDATE scopus_author
            SET eid = "%s",
                documents_count = %s,
                cited_by_count = %s,
                citation_count = %s,
                h_index = %s,
                coauthors_count = %s,
                created_account = %s,
                initials = %s,
                indexed_name = %s,
                publication_start = %s,
                publication_end = %s,
                current_affiliation_id = %s,
                last_update = %s,
                orcid_id = %s
            WHERE id = %s
        '''

    insert_affiliation = '''
        INSERT IGNORE INTO scopus_affiliation (id, url, name, country, city, state, postal_code, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''

    insert_affiliation_history = '''
        INSERT INTO scopus_author_affiliation_history (author_id, affiliation_id)
        VALUES (%s, %s)
    '''

    update_paper_last_time = '''
        UPDATE scopus_paper SET last_update=%s WHERE id=%s
    '''

    insert_paper_author = '''
        INSERT IGNORE INTO scopus_paper_author (paper_id, author_id)
        VALUES (%s, %s)
    '''

    insert_paper_keyword = '''
        INSERT INTO scopus_paper_keyword (paper_id, keyword)
        VALUES (%s, %s)
    '''

    insert_author = '''
        INSERT IGNORE INTO scopus_author (id, first_name, last_name, url)
        VALUES (%s,%s,%s,%s)
    '''

    insert_keyword = '''
        INSERT IGNORE INTO scopus_keyword (name)
        VALUES (%s)
    '''

    get_top_scopus_authors_req = """
        SELECT scopus_author.id
        from scopus_author
        INNER JOIN top_authors
            on top_authors.scopus_id = scopus_author.id
        where top_authors.query_id = %s
    """

    save_pub_info = """
        INSERT INTO scopus_publication_author(id, year, count, type)
        VALUES (%s, %s, %s, %s)

    """  # ON DUPLICATE KEY UPDATE id=%s