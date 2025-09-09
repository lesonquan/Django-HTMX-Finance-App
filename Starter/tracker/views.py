from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Transaction
from .filters import TransactionFilter
from .managers import TransactionQuerySet
from .forms import TransactionForm
from django_htmx.http import retarget
from django.core.paginator import Paginator
from django.conf import settings
from .charting import plot_incom_expense_bar_chart, plot_income_expense_pie_chart
# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transaction_list(request):
    # transactions = Transaction.objects.filter(user=request.user)

    # Use select_related('category') is to optimize the sql query for Django 
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.all().select_related('category'))
    # transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user).select_related('category'))

    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)  # Show 5 transactions per page.
    transaction_page = paginator.page(1)  # Get the first page of transactions.
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
        'transactions': transaction_page,
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses
    }
    if request.htmx:
        return render(request, 'tracker/partials/transaction-container.html', context)
    return render(request, 'tracker/transaction-list.html', context)


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': 'Transaction created successfully!'}
            return render(request, 'tracker/partials/transaction-success.html', context)
        
        else:
            context = {'form': form}
            # return render(request, 'tracker/partials/create-transaction.html', context)
            response= render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')


    context = {'form': TransactionForm()}

    return render(request, 'tracker/partials/create-transaction.html', context)


def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            context = {'message': 'Transaction updated successfully!'}
            return render(request, 'tracker/partials/transaction-success.html', context)

        else:
            context = {
                "form": form,
                "transaction": transaction
            }
            response= render(request, 'tracker/partials/update-transaction.html', context)
            return retarget(response, '#transaction-block')

    context = {
        "form": TransactionForm(instance=transaction),
        "transaction": transaction
    }

    return render(request, 'tracker/partials/update-transaction.html', context)


@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    context= {"message": f"Transaction {transaction.id} deleted successfully!"}
    return render(request, 'tracker/partials/transaction-success.html', context)


@login_required
def get_transactions(request):
    page = request.GET.get('page', 1) # ?page=2
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.all().select_related('category'))
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)  # Show 5 transactions per page.
    context = {
        'transactions': paginator.page(page),

    }
    return render(request, 'tracker/partials/transaction-container.html#transaction_list', context)

def transaction_charts(request):
    # Logic for transaction charts
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.all().select_related('category'))
    inconme_expense_chart = plot_incom_expense_bar_chart(transaction_filter.qs)

    income_pie_chart = plot_income_expense_pie_chart(transaction_filter.qs.filter(type='income'))
    expense_pie_chart = plot_income_expense_pie_chart(transaction_filter.qs.filter(type='expense'))

    context = {
        'filter': transaction_filter,
        'income_expense_barchart': inconme_expense_chart.to_html(),
        'income_pie_chart': income_pie_chart.to_html(),
        'expense_pie_chart': expense_pie_chart.to_html()
    }
    if request.htmx:
        return render(request, 'tracker/partials/charts-container.html', context)
    return render(request, 'tracker/charts.html', context)