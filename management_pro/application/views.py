from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from application.models import MPRO_User, CategoryMaster, Icon, Account, Transaction, TransactionHistory, LoginHistory
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from application import serializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from datetime import datetime, date, time
import json
from json import dumps
from django.db.models import Sum

class Login_Account(APIView):

    def get(self, request):
        data = {}
        if not request.user.is_authenticated:
            return render(request, 'application/base/login.html')
        account_creation = Account()
        user_id = request.user.id
        user_data = MPRO_User.objects.filter(id=user_id)
        # Collect the data for dashboard
        current_month = date.today()
        current_collection = Transaction.objects.values('transaction_type').filter(added_by=user_id, transaction_date__month=current_month.month).annotate(total=Sum('amount'))
        amounts_month = {'income':0,'expense':0}
        for items in current_collection:
            if items['transaction_type'] in amounts_month:
                amounts_month[items['transaction_type']] += items['total']
            else:
                amounts_month[items['transaction_type']] = items['total']
        data['income_month'] = json.dumps(amounts_month['income'])
        data['expense_month'] = json.dumps(amounts_month['expense'])
        max_collection = Transaction.objects.values('transaction_type').filter(added_by=user_id, transaction_date__year=current_month.year).annotate(total=Sum('amount'))
        amounts_year = {'income':0,'expense':0}
        for items in max_collection:
            if items['transaction_type'] in amounts_year:
                amounts_year[items['transaction_type']] += items['total']
            else:
                amounts_year[items['transaction_type']] = items['total']
        data['income_year'] = json.dumps(amounts_year['income'])
        data['expense_year'] = json.dumps(amounts_year['expense'])
        for user in user_data:
            if not Account.objects.filter(account_holder=user_id):
                account_creation.account_holder = user
                account_creation.created_date = user.date_joined
                account_creation.balance = 0
                account_creation.save()
        if request.accepted_renderer.format == 'html':
            return render(request, 'application/base/index.html', {'data': data})
        return Response(data)

class Income_Category(APIView):
    
    def get(self, request, cat_id=None, action=None):
        data = {}
        user_id = request.user.id
        if cat_id:
            category = CategoryMaster.objects.get(id=cat_id)
            if action and action.lower() == 'delete':
                category.delete()
                data['status'] = 'deletion success'
                return HttpResponseRedirect('/management/incomecategory/')
        category = CategoryMaster.objects.filter(categorized_by=user_id)
        data['status'] = 'success'
        data['category'] = category
        if request.accepted_renderer.format == 'html':
            return render(request, 'application/base/income_category.html', {'data': data})
        else:
            print('false')

    def post(self, request, cat_id=None, action=None):
        try:
            data = {}
            category  = CategoryMaster()
            if action and action.lower() =='put':
                print('put')
                category.category_name = request.POST['category_name']
                category.category_type = 'income'
                category.is_child = request.POST['ischild']
                category.parent_category = request.POST['parent_name']
                category.color = 'null'
                user_id = request.user.id
                user_data = MPRO_User.objects.filter(id=user_id)
                for user in user_data:
                    category.categorized_by = user
                category.save()
                data['status'] = 'stored successfully'
                data['category'] = CategoryMaster.objects.filter(categorized_by=user_id)
                return redirect('application:income_category')
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return render(request, 'application/base/income_category.html', {'data':data})
     
class Expense_Category(APIView):
    
    def get(self, request, cat_id=None, action=None):
        data = {}
        user_id = request.user.id
        if cat_id:
            category = CategoryMaster.objects.get(id=cat_id)
            if action and action.lower() == 'delete':
                category.delete()
                data['status'] = 'deletion success'
                return HttpResponseRedirect('/management/expensecategory/')
        category = CategoryMaster.objects.filter(categorized_by=user_id)
        data['status'] = 'success'
        data['category'] = category
        if request.accepted_renderer.format == 'html':
            return render(request, 'application/base/expense_category.html', {'data': data})
        else:
            print('false')

    def post(self, request, cat_id=None, action=None):
        try:
            data = {}
            category  = CategoryMaster()
            if action and action.lower() =='put':
                category.category_name = request.POST['category_name']
                category.category_type = 'expense'
                category.is_child = request.POST['ischild']
                category.parent_category = request.POST['parent_name']
                # category.icon_name = 'null'
                category.color = 'null'
                user_id = request.user.id
                user_data = MPRO_User.objects.filter(id=user_id)
                for user in user_data:
                    category.categorized_by = user
                category.save()
                data['status'] = 'stored successfully'
                data['category'] = CategoryMaster.objects.filter(categorized_by=user_id)
                return redirect('application:expense_category')
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return render(request, 'application/base/expense_category.html', {'data':data})

class Income(APIView):

    def get(self, request, transaction_id=None, action=None):
        data = {}
        user_id = request.user.id
        category = CategoryMaster.objects.filter(categorized_by=user_id)
        if transaction_id:
            transaction_data = Transaction.objects.get(id=transaction_id)
            data['single_transaction'] = transaction_data
            if action and action.lower() == 'delete':
                transaction_data.delete()
                data['status'] = 'deletion success'
                return HttpResponseRedirect('/management/income/')
        data['status'] = 'get success'
        data['transaction'] = Transaction.objects.filter(added_by=user_id).reverse()[:6]
        data['category'] = category
        if request.accepted_renderer.format == 'html':
            return render(request, 'application/base/income.html', {'data': data})
        else:
            print('false')

    def post(self, request, transaction_id=None, action=None):
        try:
            data = {}
            if action and action.lower() == 'edit':
                transaction_data = Transaction.objects.get(id=transaction_id)
            elif action and action.lower() =='put':
                    transaction_data  = Transaction()
            # foreign key specifications
            user_id = request.user.id
            user_data = MPRO_User.objects.filter(id=user_id)
            for user in user_data:
                transaction_data.added_by = user
            user_acc = Account.objects.filter(id=user_id)
            for acc in user_acc:
                transaction_data.account_id = acc
            category_item = CategoryMaster.objects.filter(id=request.POST['category_name'])
            for cat in category_item:
                transaction_data.category = cat
            transaction_data.transaction_type = 'income'
            transaction_data.amount = request.POST['amount']
            transaction_data.description = request.POST['description']
            transaction_data.payee = request.POST['payee']
            # print(datetime.strptime(request.POST['date'],"YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"))
            # transaction_data.transaction_date = datetime.strptime(request.POST['date'],"YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
            transaction_data.transaction_date = request.POST['date']
            transaction_data.save()
            data['status'] = 'stored successfully'
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return redirect('application:income')

class Expense(APIView):

    def get(self, request, transaction_id=None, action=None):
        data = {}
        user_id = request.user.id
        category = CategoryMaster.objects.filter(categorized_by=user_id)
        if transaction_id:
            transaction_data = Transaction.objects.get(id=transaction_id)
            data['single_transaction'] = transaction_data
            if action and action.lower() == 'delete':
                transaction_data.delete()
                data['status'] = 'deletion success'
                return HttpResponseRedirect('/management/expense/')
        data['status'] = 'get success'
        data['transaction'] = Transaction.objects.all()
        data['category'] = category
        if request.accepted_renderer.format == 'html':
            return render(request, 'application/base/expense.html', {'data': data})
        else:
            print('false')

    def post(self, request, transaction_id=None, action=None):
        try:
            data = {}
            if action and action.lower() == 'edit':
                transaction_data = Transaction.objects.get(id=transaction_id)
            elif action and action.lower() =='put':
                    transaction_data  = Transaction()
            # foreign key specifications
            user_id = request.user.id
            user_data = MPRO_User.objects.filter(id=user_id)
            for user in user_data:
                transaction_data.added_by = user
            user_acc = Account.objects.filter(id=user_id)
            for acc in user_acc:
                transaction_data.account_id = acc
            category_item = CategoryMaster.objects.filter(id=request.POST['category_name'])
            for cat in category_item:
                transaction_data.category = cat
            transaction_data.transaction_type = 'expense'
            transaction_data.amount = request.POST['amount']
            transaction_data.description = request.POST['description']
            transaction_data.payee = request.POST['payee']
            # print(datetime.strptime(request.POST['date'],"YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"))
            # transaction_data.transaction_date = datetime.strptime(request.POST['date'],"YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
            transaction_data.transaction_date = request.POST['date']
            transaction_data.save()
            print('solved')
            data['status'] = 'stored successfully'
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return redirect('application:expense')
            # return render(request, 'application/base/income.html', {'data':data})

class Search_Data(APIView):
    def get(self, request,transaction_id=None, action=None):
        data = {}
        if transaction_id:
            transaction_data = Transaction.objects.get(id=transaction_id)
            data['single_transaction'] = transaction_data
            if action and action.lower() == 'delete':
                transaction_data.delete()
                data['status'] = 'deletion success'
                return HttpResponseRedirect('/management/search_data/')
        user_id = request.user.id
        income = Transaction.objects.filter(added_by=user_id)
        data['income'] = income
        data['status'] = 'success'
        if request.accepted_renderer.format == 'html':
            return render(request, 'application/base/search_data.html', {'data':data})
    def post(self, request):
        pass

class Income_Chart(APIView):
    def get(self, request):
        data = {}
        user_id = request.user.id
        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)
        today_transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='income' , transaction_date__range=(today_min, today_max))
        # chart_data is to retrive data from queryset and storing it in the dictionary
        today_data = {}
        for items in today_transaction:
            if items['category__category_name'] in today_data:
                today_data[items['category__category_name']] += items['amount']
            else:
                today_data[items['category__category_name']] = items['amount']
        data['transaction_keys'] = json.dumps(list(today_data.keys()))
        data['transaction_values'] = json.dumps(list(today_data.values()))
        data['status'] = 'success'
        return render(request, 'application/base/income_chart.html', {'data':data})
    def post(self, request):
        data = {}
        try:
            user_id = request.user.id
            # today's report
            today_min = datetime.combine(date.today(), time.min)
            today_max = datetime.combine(date.today(), time.max)
            today_transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='income' , transaction_date__range=(today_min, today_max))
            today_data = {}
            for items in today_transaction:
                if items['category__category_name'] in today_data:
                    today_data[items['category__category_name']] += items['amount']
                else:
                    today_data[items['category__category_name']] = items['amount']
            data['transaction_keys'] = json.dumps(list(today_data.keys()))
            data['transaction_values'] = json.dumps(list(today_data.values()))
            # custom reports
            if request.POST['datewise_widget']:
                datewise = request.POST['datewise_widget']
                datewise_format = datetime.strptime(datewise, "%m/%d/%Y")
                transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='income', transaction_date__date=datewise_format)
            elif request.POST['monthwise_widget']:
                monthwise = request.POST['monthwise_widget']
                # to slice the month and year alone
                month = monthwise[0:2]
                year = monthwise[6:10]
                transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='income',transaction_date__year=year, transaction_date__month=month)
            else:
                customrange = request.POST['customrange_widget']
                start_date = customrange[0:10]
                stop_date = customrange[13:23]
                start_date_format = datetime.strptime(start_date, "%m/%d/%Y")
                stop_date_format = datetime.strptime(stop_date, "%m/%d/%Y")
                transaction = Transaction.objects.values('category__category_name', 'amount').filter(added_by=user_id, transaction_type='income', transaction_date__range=[start_date_format,stop_date_format])
            chart_data = {}
            for items in transaction:
                if items['category__category_name'] in chart_data:
                    chart_data[items['category__category_name']] += items['amount']
                else:
                    chart_data[items['category__category_name']] = items['amount']
            data['custom_transaction_keys'] = json.dumps(list(chart_data.keys()))
            data['custom_transaction_values'] = json.dumps(list(chart_data.values()))
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return render(request, 'application/base/income_chart.html', {'data':data})
    
class Expense_Chart(APIView):
    def get(self, request):
        data = {}
        user_id = request.user.id
        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)
        today_transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='expense' , transaction_date__range=(today_min, today_max))
        # chart_data is to retrive data from queryset and storing it in the dictionary
        today_data = {}
        for items in today_transaction:
            if items['category__category_name'] in today_data:
                today_data[items['category__category_name']] += items['amount']
            else:
                today_data[items['category__category_name']] = items['amount']
        data['transaction_keys'] = json.dumps(list(today_data.keys()))
        data['transaction_values'] = json.dumps(list(today_data.values()))
        data['status'] = 'success'
        return render(request, 'application/base/expense_chart.html', {'data':data})
    def post(self, request):
        data = {}
        try:
            user_id = request.user.id
            # today's report
            today_min = datetime.combine(date.today(), time.min)
            today_max = datetime.combine(date.today(), time.max)
            transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='expense' , transaction_date__range=(today_min, today_max))
            today_data = {}
            for items in transaction:
                if items['category__category_name'] in today_data:
                    today_data[items['category__category_name']] += items['amount']
                else:
                    today_data[items['category__category_name']] = items['amount']
            data['transaction_keys'] = json.dumps(list(today_data.keys()))
            data['transaction_values'] = json.dumps(list(today_data.values()))
            # custom reports
            if request.POST['datewise_widget']:
                datewise = request.POST['datewise_widget']
                datewise_format = datetime.strptime(datewise, "%m/%d/%Y")
                transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='expense', transaction_date__date=datewise_format)
            elif request.POST['monthwise_widget']:
                monthwise = request.POST['monthwise_widget']
                # to slice the month and year alone
                month = monthwise[0:2]
                year = monthwise[6:10]
                transaction = Transaction.objects.values('category__category_name','amount').filter(added_by=user_id, transaction_type='expense',transaction_date__year=year, transaction_date__month=month)
            else:
                customrange = request.POST['customrange_widget']
                print(customrange)
                start_date = customrange[0:10]
                stop_date = customrange[13:23]
                start_date_format = datetime.strptime(start_date, "%m/%d/%Y")
                stop_date_format = datetime.strptime(stop_date, "%m/%d/%Y")
                transaction = Transaction.objects.values('category__category_name', 'amount').filter(added_by=user_id, transaction_type='expense', transaction_date__range=[start_date_format,stop_date_format])
            chart_data = {}
            for items in transaction:
                if items['category__category_name'] in chart_data:
                    chart_data[items['category__category_name']] += items['amount']
                else:
                    chart_data[items['category__category_name']] = items['amount']
            data['custom_transaction_keys'] = json.dumps(list(chart_data.keys()))
            data['custom_transaction_values'] = json.dumps(list(chart_data.values()))
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return render(request, 'application/base/expense_chart.html', {'data':data})
    
class Comparison_Chart(APIView):
    def get(self, request):
        data = {}
        user_id = request.user.id
        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)
        today_transaction = Transaction.objects.values('transaction_type').filter(added_by=user_id, transaction_date__range=(today_min, today_max)).annotate(total=Sum('amount'))
        # today_data is to retrive data from queryset and storing it in the dictionary
        today_data = {}
        for items in today_transaction:
            if items['transaction_type'] in today_data:
                today_data[items['transaction_type']] += items['total']
            else:
                today_data[items['transaction_type']] = items['total']
        data['transaction_keys'] = json.dumps(list(today_data.keys()))
        data['transaction_values'] = json.dumps(list(today_data.values()))
        data['status'] = 'success'
        return render(request, 'application/base/comparison_chart.html', {'data':data})
    def post(self, request):
        data = {}
        print('post')
        try:
            user_id = request.user.id
            # today's report
            today_min = datetime.combine(date.today(), time.min)
            today_max = datetime.combine(date.today(), time.max)
            today_transaction = Transaction.objects.values('transaction_type').filter(added_by=user_id, transaction_date__range=(today_min, today_max)).annotate(total=Sum('amount'))
            today_data = {}
            for items in today_transaction:
                if items['transaction_type'] in today_data:
                    today_data[items['transaction_type']] += items['total']
                else:
                    today_data[items['transaction_type']] = items['total']
            data['transaction_keys'] = json.dumps(list(today_data.keys()))
            data['transaction_values'] = json.dumps(list(today_data.values()))
            # custom reports
            if request.POST['datewise_widget']:
                datewise = request.POST['datewise_widget']
                datewise_format = datetime.strptime(datewise, "%m/%d/%Y")
                transaction = Transaction.objects.values('transaction_type').filter(added_by=user_id, transaction_date__date=datewise_format).annotate(total=Sum('amount'))
            elif request.POST['monthwise_widget']:
                monthwise = request.POST['monthwise_widget']
                # to slice the month and year alone
                month = monthwise[0:2]
                year = monthwise[6:10]
                transaction = Transaction.objects.values('transaction_type').filter(added_by=user_id, transaction_date__year=year, transaction_date__month=month).annotate(total=Sum('amount'))
                print(transaction)
            else:
                customrange = request.POST['customrange_widget']
                start_date = customrange[0:10]
                stop_date = customrange[13:23]
                start_date_format = datetime.strptime(start_date, "%m/%d/%Y")
                stop_date_format = datetime.strptime(stop_date, "%m/%d/%Y")
                transaction = Transaction.objects.values('transaction_type').filter(added_by=user_id, transaction_date__range=[start_date_format,stop_date_format]).annotate(total=Sum('amount'))
            chart_data = {}
            for items in transaction:
                if items['transaction_type'] in chart_data:
                    chart_data[items['transaction_type']] += items['total']
                else:
                    chart_data[items['transaction_type']] = items['total']
            data['custom_transaction_keys'] = json.dumps(list(chart_data.keys()))
            data['custom_transaction_values'] = json.dumps(list(chart_data.values()))
            print(chart_data)
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return render(request, 'application/base/comparison_chart.html', {'data':data})