import pytest
from testing.features.initStructure import test_catExe

prev_enhanced_bom = {
    'bom_json_cid': 'QmXX9wEoRzSeJixp2isrRuLb9KJpprVw1DcJ2eVePzukMW',
    'invoice': {
        'data_cid': 'QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp',
        'order_cid': 'QmangQmYjjrLGEfVZ7yBe2u1eqrnzqSsxVuYSzsyuPCYZv',
        'seed_cid': None
    },
    'invoice_cid': 'QmNRHK4P5kWpsKda8NzpV7c7Qj9L4ppQZbYJc2iFvn7rLf',
    'log_cid': None,
    'order': {
        'function_cid': 'b',
        'invoice_cid': 'QmbUD6XRVS8UbEc9LyBsj7d5M5sQ9WxnquguFEF8AM6wWZ',
        'structure_cid': {
            'Hash': 'QmcrLhZMZMYAhLMz8mWzDriPoB5axwxXeE5JJmPBjAtDFa',
            'Name': 'main.tf',
            'Size': '1886'
        }
    }
}


class Structure:
    def test_init_structure_case(self):
        current_enhanced_bom, current_bom = test_catExe.execute(test_catExe.init_bom_json_cid)
        assert current_enhanced_bom == prev_enhanced_bom
