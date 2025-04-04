#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
module: mssql_db_user
version_added: 1.0.0
author:
  - Jim Tarpley (@trippsc2)
short_description: Configures a SQL database user in a Microsoft SQL Server instance.
description:
  - Configures a SQL database user in a Microsoft SQL Server instance.
attributes:
  check_mode:
    support: full
    description:
      - This module supports check mode.
extends_documentation_fragment:
  - trippsc2.mssql.login
options:
  name:
    type: str
    required: true
    description:
      - The name of the SQL Login to configure as a database user.
  database:
    type: str
    required: true
    description:
      - The name of the database for which to configure the SQL Login as a user.
  state:
    type: str
    required: false
    default: present
    choices:
      - present
      - absent
    description:
      - The desired state of the SQL Login.
"""

EXAMPLES = r"""
- name: Create a SQL database user
  trippsc2.mssql.mssql_login:
    login_user: sa
    login_password: password
    login_host: localhost
    name: test
    database: tempdb
    state: present

- name: Remove a SQL database user
  trippsc2.mssql.mssql_login:
    login_user: sa
    login_password: password
    login_host: localhost
    name: test
    database: tempdb
    state: absent
"""

RETURN = r"""
"""

import traceback

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.common.text.converters import to_native

from typing import Optional

try:
    import pymssql
except ImportError:
    HAS_PYMSSQL: bool = False
    PYMSSQL_IMPORT_ERROR: Optional[str] = traceback.format_exc()
else:
    HAS_PYMSSQL: bool = True
    PYMSSQL_IMPORT_ERROR: Optional[str] = None

from ..module_utils._mssql_module import MssqlModule
from ..module_utils._mssql_module_error import MssqlModuleError


def run_module():
    module = MssqlModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            database=dict(type='str', required=True),
            state=dict(type='str', required=False, default='present', choices=['present', 'absent'])
        )
    )

    if not HAS_PYMSSQL:
        module.fail_json(
            msg=missing_required_lib('pymssql'),
            exception=PYMSSQL_IMPORT_ERROR)

    params = module.get_defined_non_connection_params()
    module.initialize_client()
    validate_params(params, module)

    if params['state'] == 'present':
        result = ensure_present(params, module)
    else:
        result = ensure_absent(params, module)

    module.close_client_session()
    module.exit_json(**result)


def validate_params(params: dict, module: MssqlModule) -> None:
    """
    Validate the module parameters.

    Args:
        params (dict): The module parameters.
        module (MssqlModule): The Ansible module.
    """

    query: str = f"SELECT name FROM sys.databases WHERE name = '{params['database']}'"

    try:
        module.cursor.execute(query)
        result: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if result is None:
        module.handle_error(MssqlModuleError(message=f"No database exists with the name '{params['database']}'."))


def ensure_present(params: dict, module: MssqlModule) -> dict:
    """
    Ensure the login is present in the database.

    Args:
        params (dict): The module parameters.
        module (MssqlModule): The Ansible module.

    Returns:
        dict: The module result.
    """

    name: str = params['name']
    database: str = params['database']

    if not get_login(name, module):
        module.handle_error(MssqlModuleError(message=f"No server login exists for '{name}'."))

    if get_user(name, database, module):
        return dict(changed=False)

    if not module.check_mode:
        query: str = f"""
        USE [{database}];
        CREATE USER [{name}] FOR LOGIN [{name}]
        """

        try:
            module.cursor.execute(query)
            module.conn.commit()
        except Exception as e:
            module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return dict(changed=True)


def ensure_absent(params: dict, module: MssqlModule) -> dict:
    """
    Ensure the login is absent in the database.

    Args:
        params (dict): The module parameters.
        module (MssqlModule): The Ansible module.

    Returns:
        dict: The module result.
    """

    name: str = params['name']
    database: str = params['database']

    if not get_user(name, database, module):
        return dict(changed=False)

    if not module.check_mode:
        query: str = f"""
        USE [{database}];
        DROP USER [{name}]
        """

        try:
            module.cursor.execute(query)
            module.conn.commit()
        except Exception as e:
            module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return dict(changed=True)


def get_login(name: str, module: MssqlModule) -> bool:
    """
    Check if the login exists in the database.

    Args:
        name (str): The name of the login.
        module (MssqlModule): The Ansible module.

    Returns:
        bool: True if the login exists, False otherwise.
    """

    query: str = f"SELECT name FROM sys.server_principals WHERE name = '{name}'"

    try:
        module.cursor.execute(query)
        result: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return result is not None


def get_user(name: str, database: str, module: MssqlModule) -> bool:
    """
    Check if the user exists in the database.

    Args:
        name (str): The name of the login.
        database (str): The name of the database.
        module (MssqlModule): The Ansible module.

    Returns:
        bool: True if the user exists, False otherwise.
    """

    query: str = f"SELECT name FROM {database}.sys.database_principals WHERE name = '{name}'"

    try:
        module.cursor.execute(query)
        result: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    return result is not None


def main() -> None:
    run_module()


if __name__ == '__main__':
    main()
