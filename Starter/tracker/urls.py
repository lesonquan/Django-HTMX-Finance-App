from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions/", views.transaction_list, name='transaction-list'),
    path('transaction/create/', views.create_transaction, name='create-transaction'),

    path('transaction/<int:pk>/update/', views.update_transaction, name='update-transaction'),
    path('transaction/<int:pk>/delete/', views.delete_transaction, name='delete-transaction'),
    path('get-transactions/', views.get_transactions, name='get-transactions'),
    path('transactions/charts/', views.transaction_charts, name='transaction-charts'),
    path('export/', views.export, name='export'),
    path('import/', views.import_transactions, name='import'),
]
