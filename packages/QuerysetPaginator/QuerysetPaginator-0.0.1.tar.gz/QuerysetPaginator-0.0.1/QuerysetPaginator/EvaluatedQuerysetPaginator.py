class EmptyPageException(Exception):
    def __init__(self):
        print("EmptyPageException: Invalid Second Parameter Value")

class EmptyQuerysetException(Exception):
    def __init__(self):
        print("EmptyQuerysetException: Query set is empty")

class EvaluatedQuerysetPaginator():
    def __init__(self, query_set, objects_per_page):
        self.objects_per_page = objects_per_page
        self.query_set = query_set
        self.pages = {}
        self.total_objects = query_set.count()
        if self.total_objects == 0:
            raise EmptyQuerysetException
        if objects_per_page == 0:
            raise EmptyPageException
        self.paginate()

    def page(self, page_number):
        page_number = page_number - 1
        return self.pages[page_number]

    def page_count(self):
        return len(self.pages)

    def paginate(self):
        page_number = 0
        range_value = 0
        if self.objects_per_page > self.total_objects:
            self.objects_per_page = self.total_objects
        if self.total_objects % self.objects_per_page == 0:
            range_value = int(self.total_objects/self.objects_per_page)
        else:
            range_value = int(self.total_objects/self.objects_per_page) + 1
        dup_query_set = [x for x in self.query_set.iterator()]
        self.page_count = range_value
        self.page_range = range(self.page_count)
        for i in range(range_value):
            start_index = i * self.objects_per_page
            end_index = start_index + self.objects_per_page - 1
            self.pages[i] = {}
            self.pages[i]['object_list'] = dup_query_set[start_index : end_index + 1]
            if self.page_count is not 1:
                self.pages[i]['has_other_pages'] = True
            else:
                self.pages[i]['has_other_pages'] = False
            self.pages[i]['number'] = i + 1
            self.pages[i]['page_range'] = range(1,self.page_count + 1)
            if i in self.page_range and i is not 0:
                self.pages[i]['has_previous'] = True
            else:
                self.pages[i]['has_previous'] = False
            if i in self.page_range and i is not self.page_count - 1:
                self.pages[i]['has_next'] = True
            else:
                self.pages[i]['has_next'] = False
            self.pages[i]['previous_page_number'] = i
            self.pages[i]['next_page_number'] = i + 2
