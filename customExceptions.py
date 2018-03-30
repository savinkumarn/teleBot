class DataException(Exception):
    '''
    This is a custom error Class
    '''

    def __init__(self, errorMessage):
        '''
        Constructor
        '''
        self.errorMessage = errorMessage

class finalException(Exception):
    '''
    This is a custom error Class
    '''

    def __init__(self, errorMessage):
        '''
        Constructor
        '''
        self.errorMessage = errorMessage
