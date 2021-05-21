class QuestionType:
    RADIO = 'RADIO'
    SELECT = 'SELECT'
    DROPBOX = 'CHECKBOX'
    TEXT = 'TEXT'
    RANK = 'RANK'
    RANK_2 = 'RANK_2'

    CHOICES = [
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (DROPBOX, 'dropbox'),
        (TEXT, 'text'),
        (RANK, 'rank'),
        (RANK_2, 'rank_2')
    ]