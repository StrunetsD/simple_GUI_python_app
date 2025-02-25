class Pagination:
    def __init__(self, total_items, page_size=10):
        self.page_size = page_size
        self.current_page = 1
        self.total_items = total_items
        self.total_pages = (total_items + page_size - 1) // page_size

    def get_current_page_data(self, data):
        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        return data[start_index:end_index]

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def first_page(self):
        self.current_page = 1

    def last_page(self):
        self.current_page = self.total_pages

    def set_page_size(self, size):
        self.page_size = size
        self.total_pages = (self.total_items + size - 1) // size
        self.current_page = 1

    def update_total(self, total_items):
        self.total_items = total_items
        self.total_pages = (total_items + self.page_size - 1) // self.page_size
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        elif self.current_page < 1:
            self.current_page = 1
