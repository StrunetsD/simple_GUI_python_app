import tkinter as tk
from model.db_requests import DBRequests


class Controller:
    def __init__(self):
        self.db = DBRequests()
        self.deleted_count = 0
        self.found_count = 0

    def get_students(self):
        return self.db.get_query_of_students()

    def delete_by_income_of_parents(self, min_income=None, max_income=None):
        count = self.db.delete_by_income_of_parents(min_income, max_income)
        self.deleted_count += count
        return f"Удалено {count} записей"

    def search_by_income_of_parents(self, min_income=None, max_income=None):
        results = self.db.search_by_income_of_parents(min_income, max_income)
        self.found_count += len(results)
        return results

    def delete_by_count_of_brothers_or_sisters(self, count):
        count = self.db.delete_by_count_of_brothers_or_sisters(count)
        self.deleted_count += count
        return f"Удалено {count} записей"

    def search_by_count_of_brothers_or_sisters(self, count):
        results = self.db.search_by_count_of_brothers_or_sisters(count)
        self.found_count += len(results)
        return results

    def search_parents_by_name(self, search_item):
        results = self.db.search_parents_by_name(search_item)
        self.found_count += len(results)
        return results

    def delete_parent_by_name(self, search_term):
        self.db.delete_parent_by_name(search_term)
        self.deleted_count += 1
        return f"Удалена 1 запись {search_term}"

    def delete_student_by_name(self, search_term):
        self.db.delete_student_by_name(search_term)
        self.deleted_count += 1
        return f"Удалена 1 запись {search_term}"

    def search_students_by_name(self, search_term):
        results = self.db.search_students_by_name(search_term)
        self.found_count += len(results)
        return results

    def get_counts(self):
        return self.deleted_count, self.found_count



