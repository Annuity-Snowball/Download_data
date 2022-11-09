class test():
    def __init__(self,name):
        self.name = name
        
    def print_some(self):
        print(self.name)
        
test_object=test('moon')
test_object.print_some()