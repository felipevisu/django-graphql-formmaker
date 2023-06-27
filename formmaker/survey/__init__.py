class QuestionType:
    PLAIN_TEXT = "PLAIN_TEXT"
    SELECT = "SELECT"
    MULTISELECT = "MULTISELECT"

    choices = [
        (PLAIN_TEXT, "plain text"),
        (SELECT, "select"),
        (MULTISELECT, "multIselect"),
    ]
