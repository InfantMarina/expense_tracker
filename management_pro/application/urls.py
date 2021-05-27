from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from application import views

app_name = 'application'

urlpatterns = [
    re_path('^$', views.Login_Account.as_view(), name="dashboard"),
    re_path('^incomecategory/?(?P<cat_id>[0-9]{1,4})?/?(?P<action>(delete|put))?/?$', login_required(views.Income_Category.as_view()), name="income_category"),
    re_path('^expensecategory/?(?P<cat_id>[0-9]{1,4})?/?(?P<action>(delete|put))?/?$', login_required(views.Expense_Category.as_view()), name="expense_category"),
    re_path('^income/?(?P<transaction_id>[0-9]{1,4})?/?(?P<action>(delete|put|edit))?/?$', login_required(views.Income.as_view()), name="income"),
    re_path('^expense/?(?P<transaction_id>[0-9]{1,4})?/?(?P<action>(delete|put|edit))?/?$', login_required(views.Expense.as_view()), name="expense"),
    re_path('^search_data/?(?P<transaction_id>[0-9]{1,4})?/?(?P<action>(delete|put|edit))?/?$', login_required(views.Search_Data.as_view()), name="search_data"),
    re_path('^incomechart/?$',login_required(views.Income_Chart.as_view()), name="income_chart"),
    re_path('^expensechart/?$',login_required(views.Expense_Chart.as_view()), name="expense_chart"),
    re_path('^comparisonchart/?$',login_required(views.Comparison_Chart.as_view()), name="comparison_chart"),
]