from rest_framework_csv.renderers import CSVRenderer

class LenderCSVRenderer(CSVRenderer):
    """
    Overriding & renaming CSV headers to make it human readable
    """
    header = ['name', 'code', 'upfront_commission_rate', 'trial_commission_rate', 'active']
    labels = {
        'name': 'Name',
        'code': 'Code',
        'upfront_commission_rate': 'Upfront Commission Rate',
        'trial_commission_rate': 'Trial Commission Rate',
        'active': 'Active'
    }