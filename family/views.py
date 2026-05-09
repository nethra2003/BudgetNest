from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from family.models import FamilyData, Expenses

@login_required
@never_cache
# Create your views here.
def addmember(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        income = request.POST.get('income')
        income = 0 if income == '' else income
        new_mem = FamilyData.objects.create(name=name,age=age,income=income,family_lead=request.user)
        return redirect('familydata')
    return render(request,'addmember.html')


@login_required
@never_cache
def familydata(request):
    family_members = FamilyData.objects.all()
    return render(request,'familydata.html',
                  {'family_members':family_members})

@login_required
@never_cache
def addexpenses(request):
    family_mem = FamilyData.objects.filter(family_lead=request.user)
    if request.method == 'POST':
        name_input = request.POST.get('name')
        try:
            person_name=FamilyData.objects.get(family_lead = request.user,name = name_input)
        except FamilyData.DoesNotExist:
            return render(request,'addexpenses.html',{
                'data': family_mem,
                'error':'Invalid family member selected'
            })

        family_lead=request.user
        purpose = request.POST.get('purpose')
        expense = request.POST.get('expense')
        date = request.POST.get('date')
        date=datetime.strptime(date,'%Y-%m-%d')
        exp=Expenses.objects.create(family_lead=family_lead,name=person_name,purpose=purpose,expense=expense,date=date)

        return redirect('viewexpenses')

    return render(request,'addexpenses.html',{'data':family_mem})

@login_required
@never_cache
def viewexpenses(request):
    # Fetch all expenses for the current user only
    expenses = Expenses.objects.filter(family_lead=request.user).order_by('-date')

    # Calculate total expenses
    total_expense = sum(exp.expense for exp in expenses)

    context = {
        'expenses': expenses,
        'total_expense': total_expense
    }
    return render(request, 'viewexpenses.html', context)

@login_required
@never_cache
def update_expense(request, id):
    expense = get_object_or_404(Expenses, id=id, family_lead=request.user)
    if request.method == 'POST':
        expense.purpose = request.POST['purpose']
        expense.expense = float(request.POST['expense'])
        date_from_user = request.POST.get('date')
        expense.date = datetime.strptime(date_from_user, '%Y-%m-%d')
        expense.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('viewexpenses')
    return render(request, 'update_expense.html', {'data': expense})

@login_required
@never_cache
def delete_expense(request,id):
    expense = get_object_or_404(Expenses, id=id, family_lead=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')

    return redirect('viewexpenses')

@login_required
@never_cache
def monthly(request):
    from django.utils import timezone
    now = timezone.now()

    # Default to current month/year
    selected_year = now.year
    selected_month = now.month

    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        selected_month = int(request.POST.get('month'))

    expenses = Expenses.objects.filter(
        family_lead=request.user,
        date__year=selected_year,
        date__month=selected_month
    ).order_by('-date')

    total_expense = sum(exp.expense for exp in expenses)
    # Form data
    years = range(2020, now.year + 1)
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'report_type': 'Monthly',
        'start_year': selected_year,
        'years': years,
        'start_month': selected_month,
        'months': months,
        'records': expenses,  # For template compatibility
        'norecords': 'No records found' if not expenses else ''
    }
    return render(request, 'monthly.html', context)

@login_required
@never_cache
def yearly(request):
    from django.utils import timezone
    now = timezone.now()

    # Default to current year
    selected_year = now.year

    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))

    expenses = Expenses.objects.filter(
        family_lead=request.user,
        date__year=selected_year
    ).order_by('-date')

    total_expense = sum(exp.expense for exp in expenses)

    # Form data
    years = range(2020, now.year + 1)

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'report_type': 'Yearly',
        'start_year': selected_year,
        'years': years,
        'records': expenses,  # For template compatibility
        'norecords': 'No records found' if not expenses else ''
    }
    return render(request, 'yearly.html', context)

@login_required
@never_cache
def total(request):
    from django.utils import timezone
    now = timezone.now()

    # Default to current month/year
    selected_year = now.year
    selected_month = now.month

    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        selected_month = int(request.POST.get('month'))

    # Filter expenses for selected month/year
    expenses = Expenses.objects.filter(
        family_lead=request.user,
        date__year=selected_year,
        date__month=selected_month
    ).order_by('-date')

    # Calculate monthly total
    total_expense = sum(exp.expense for exp in expenses)

    # Calculate yearly total for the selected year
    yearly_expenses = Expenses.objects.filter(
        family_lead=request.user,
        date__year=selected_year
    )
    year_total = sum(exp.expense for exp in yearly_expenses)

    # Form data
    years = range(2020, now.year + 1)
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    dict1 = {
        'expenses': expenses,
        'total_expense': total_expense,
        'year_total': year_total,
        'years': years,
        'months': months,
        'start_year': selected_year,
        'start_month': selected_month,
        'records': expenses,  # For template compatibility
        'norecords': 'No records found' if not expenses else ''
    }

    return render(request, 'total.html', dict1)

@login_required
@never_cache
def update_data(request,id):
    family_mem=FamilyData.objects.get(id=id)
    if request.method == 'POST':
        family_mem.name = request.POST.get('firstname')
        family_mem.age = request.POST.get('age')
        family_mem.income = request.POST.get('income')
        family_mem.save()
        return redirect('familydata')
    return render(request,'update_data.html',{'data':family_mem})

@login_required
@never_cache
def delete_data(request,id):
    mem = get_object_or_404(FamilyData, id=id)
    mem.delete()
    return redirect('familydata')
