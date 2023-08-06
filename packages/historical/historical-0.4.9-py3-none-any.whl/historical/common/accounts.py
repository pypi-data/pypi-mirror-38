"""
.. module: historical.common.accounts
    :platform: Unix
    :copyright: (c) 2018 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. author:: Kevin Glisson <kglisson@netflix.com>
.. author:: Mike Grima <mgrima@netflix.com>
"""
import os

from swag_client.backend import SWAGManager
from swag_client.util import parse_swag_config_options


def parse_boolean(value):
    """Simple function to get a boolean value from string."""
    if not value:
        return False

    if str(value).lower() == 'true':
        return True

    return False


def get_historical_accounts():
    """Fetches valid accounts from SWAG if enabled or a list accounts."""
    if os.environ.get('SWAG_BUCKET', False):
        swag_opts = {
            'swag.type': 's3',
            'swag.bucket_name': os.environ['SWAG_BUCKET'],
            'swag.data_file': os.environ.get('SWAG_DATA_FILE', 'accounts.json'),
            'swag.region': os.environ.get('SWAG_REGION', 'us-east-1')
        }
        swag = SWAGManager(**parse_swag_config_options(swag_opts))
        search_filter = f"[?provider=='aws' && owner=='{os.environ['SWAG_OWNER']}' && account_status!='deleted'"

        if parse_boolean(os.environ.get('TEST_ACCOUNTS_ONLY')):
            search_filter += " && environment=='test'"

        search_filter += ']'

        accounts = swag.get_service_enabled('historical', search_filter=search_filter)
    else:
        accounts = os.environ['ENABLED_ACCOUNTS']

    return accounts
