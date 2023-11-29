class MockCursor:
    INVALID_RESULT = 2

    def execute(self, sql):
        pass

    def fetchone(self):
        return (MockCursor.INVALID_RESULT,)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
