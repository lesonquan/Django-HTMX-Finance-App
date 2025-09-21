from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Transaction, Category


class TransactionResource(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(Category, 'name'))

    class Meta:
        model = Transaction
        fields = ('amount', 'type', 'date', 'description', 'category')
        # fields = ('amount', 'type', 'date', 'description', 'category__name') # --> this also works for foreign key, no need to used ForeignKeyWidget