import plotly.express as px
from django.db.models import Sum
from tracker.models import Transaction, Category

def plot_incom_expense_bar_chart(qs):
    x_vals= ['Income', 'Expenses']

    # total_income = qs.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    # total_expenses = qs.filter(transaction_type='expenses').aggregate(total=Sum('amount'))['total'] or 0
    total_income = qs.filter(type='income').aggregate(total=Sum('amount'))['total']
    total_expenses = qs.filter(type='expense').aggregate(total=Sum('amount'))['total']

    y_vals = [total_income, total_expenses]

    fig = px.bar(x=x_vals, y=y_vals, labels={'x': 'Transaction Type', 'y': 'Total Amount'})
    fig.update_layout(
        title='Income vs Expenses',
        xaxis_title='Transaction Type',
        yaxis_title='Total Amount',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def plot_income_expense_pie_chart(qs):
    total_per_category = qs.order_by('category').values('category').annotate(total=Sum('amount'))
    category_pk = total_per_category.values_list('category', flat=True).order_by('category')
    categories = Category.objects.filter(pk__in=category_pk).order_by('pk').values_list('name', flat=True)
    total_final = total_per_category.values_list('total', flat=True)
    fig = px.pie(names=categories, values=total_final)
    fig.update_traces(title='Expenses by Category')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    return fig