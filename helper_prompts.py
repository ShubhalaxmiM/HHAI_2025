rephrase_question_prompt = """Given the question below, you need to rephrase it in a more formal self-contained way to make it easier for fact-checkers. Resolve any references to prononuns, dates, and other entities in the question using the claim, speaker and date.
The final generated question must be  with self-contained text with no comments and no other text. Keep original quotes made by someone as much as possible. Remember this will be used as a input for a search engine.

Claim: {}
Question: {}
""" 