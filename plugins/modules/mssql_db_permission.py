#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
module: mssql_db_permission
version_added: 1.0.0
author:
  - Jim Tarpley (@trippsc2)
short_description: Configures a SQL database-level permission in a Microsoft SQL Server instance.
description:
  - Configures a SQL database-level permission in a Microsoft SQL Server instance.
attributes:
  check_mode:
    support: full
    description:
      - This module supports check mode.
extends_documentation_fragment:
  - trippsc2.mssql.login
options:
  principal:
    type: str
    required: true
    description:
      - The name of the database user or role for which to configure permissions.
  database:
    type: str
    required: true
    description:
      - The name of the database for which to configure permissions.
  permissions:
    type: list
    required: true
    elements: str
    choices:
      - administer_database_bulk_operations
      - alter
      - alter_any_application_role
      - alter_any_assembly
      - alter_any_asymmetric_key
      - alter_any_certificate
      - alter_any_column_encryption_key
      - alter_any_column_master_key_definition
      - alter_any_contract
      - alter_any_database_audit
      - alter_any_database_ddl_trigger
      - alter_any_database_event_notification
      - alter_any_database_event_session
      - alter_any_database_scoped_configuration
      - alter_any_dataspace
      - alter_any_external_data_source
      - alter_any_external_file_format
      - alter_any_external_library
      - alter_any_fulltext_catalog
      - alter_any_mask
      - alter_any_message_type
      - alter_any_remote_service_binding
      - alter_any_role
      - alter_any_route
      - alter_any_schema
      - alter_any_security_policy
      - alter_any_sensitivity_classification
      - alter_any_service
      - alter_any_symmetric_key
      - alter_any_user
      - authenticate
      - backup_database
      - backup_log
      - checkpoint
      - connect
      - connect_replication
      - control
      - create_aggregate
      - create_any_external_library
      - create_assembly
      - create_asymmetric_key
      - create_certificate
      - create_contract
      - create_database
      - create_database_ddl_event_notification
      - create_default
      - create_fulltext_catalog
      - create_function
      - create_message_type
      - create_procedure
      - create_queue
      - create_remote_service_binding
      - create_role
      - create_route
      - create_rule
      - create_schema
      - create_service
      - create_symmetric_key
      - create_synonym
      - create_table
      - create_type
      - create_view
      - create_xml_schema_collection
      - delete
      - execute
      - execute_any_external_endpoint
      - execute_any_external_script
      - execute_external_script
      - insert
      - kill_database_connection
      - references
      - select
      - showplan
      - subscribe_query_notifications
      - take_ownership
      - unmask
      - update
      - view_any_column_encryption_key_definition
      - view_any_column_master_key_definition
      - view_database_state
      - view_definition
    description:
      - The type of database-level permission to configure.
  state:
    type: str
    required: false
    default: grant
    choices:
      - grant
      - deny
      - grant_with_grant_option
      - revoke
    description:
      - The state of the database-level permission.
"""

EXAMPLES = r"""
- name: Grant SQL database-level permissions
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    database: tempdb
    permissions:
      - connect
      - update
    state: grant

- name: Deny SQL database-level permissions
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    database: tempdb
    permissions:
      - connect
      - update
    state: deny

- name: Grant SQL database-level permissions with grant option
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    database: tempdb
    permissions:
      - connect
      - update
    state: grant_with_grant_option

- name: Remove SQL database-level permissions
  trippsc2.mssql.mssql_db_permission:
    login_user: sa
    login_password: password
    login_host: localhost
    principal: test
    database: tempdb
    permissions:
      - connect
      - update
    state: revoke
"""

RETURN = r"""
current:
  type: dict
  returned: O(state=present)
  description:
    - The configuration of the SQL database-level permissions.
  sample:
    - permission: connect
      state: grant_with_grant_option
    - permission: update
      state: grant_with_grant_option
  contains:
    permission:
      type: str
      description:
        - The database-level permission.
    state:
      type: str
      description:
        - The state of the database-level permission.
previous:
  type: dict
  returned: changed
  description:
    - The previous configuration of the SQL database-level permissions.
  sample:
    - permission: connect
      state: grant
    - permission: update
      state: deny
  contains:
    permission:
      type: str
      description:
        - The database-level permission.
    state:
      type: str
      description:
        - The state of the database-level permission.
"""

import traceback

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.common.text.converters import to_native

from typing import List, Optional

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


def run_module() -> None:
    module: MssqlModule = MssqlModule(
        argument_spec=dict(
            principal=dict(type='str', required=True),
            database=dict(type='str', required=True),
            permissions=dict(
                type='list',
                required=True,
                elements='str',
                choices=[
                    'administer_database_bulk_operations',
                    'alter',
                    'alter_any_application_role',
                    'alter_any_assembly',
                    'alter_any_asymmetric_key',
                    'alter_any_certificate',
                    'alter_any_column_encryption_key',
                    'alter_any_column_master_key_definition',
                    'alter_any_contract',
                    'alter_any_database_audit',
                    'alter_any_database_ddl_trigger',
                    'alter_any_database_event_notification',
                    'alter_any_database_event_session',
                    'alter_any_database_scoped_configuration',
                    'alter_any_dataspace',
                    'alter_any_external_data_source',
                    'alter_any_external_file_format',
                    'alter_any_external_library',
                    'alter_any_fulltext_catalog',
                    'alter_any_mask',
                    'alter_any_message_type',
                    'alter_any_remote_service_binding',
                    'alter_any_role',
                    'alter_any_route',
                    'alter_any_schema',
                    'alter_any_security_policy',
                    'alter_any_sensitivity_classification',
                    'alter_any_service',
                    'alter_any_symmetric_key',
                    'alter_any_user',
                    'authenticate',
                    'backup_database',
                    'backup_log',
                    'checkpoint',
                    'connect',
                    'connect_replication',
                    'control',
                    'create_aggregate',
                    'create_any_external_library',
                    'create_assembly',
                    'create_asymmetric_key',
                    'create_certificate',
                    'create_contract',
                    'create_database',
                    'create_database_ddl_event_notification',
                    'create_default',
                    'create_fulltext_catalog',
                    'create_function',
                    'create_message_type',
                    'create_procedure',
                    'create_queue',
                    'create_remote_service_binding',
                    'create_role',
                    'create_route',
                    'create_rule',
                    'create_schema',
                    'create_service',
                    'create_symmetric_key',
                    'create_synonym',
                    'create_table',
                    'create_type',
                    'create_view',
                    'create_xml_schema_collection',
                    'delete',
                    'execute',
                    'execute_any_external_endpoint',
                    'execute_any_external_script',
                    'execute_external_script',
                    'insert',
                    'kill_database_connection',
                    'references',
                    'select',
                    'showplan',
                    'subscribe_query_notifications',
                    'take_ownership',
                    'unmask',
                    'update',
                    'view_any_column_encryption_key_definition',
                    'view_any_column_master_key_definition',
                    'view_database_state',
                    'view_definition'
                ]
            ),
            state=dict(
                type='str',
                required=False,
                default='grant',
                choices=['grant', 'deny', 'grant_with_grant_option', 'revoke']
            )
        )
    )

    if not HAS_PYMSSQL:
        module.fail_json(
            msg=missing_required_lib('pymssql'),
            exception=PYMSSQL_IMPORT_ERROR)

    params: dict = module.get_defined_non_connection_params()
    module.initialize_client()
    validate_params(params, module)

    previous_permissions: dict = get_db_permissions(
        params['principal'],
        params['database'],
        params['permissions'],
        module
    )

    changed: bool = False

    previous: List[dict] = []
    current: List[dict] = []

    for permission, previous_state in previous_permissions.items():
        if previous_state != params['state']:
            changed: bool = True

        if previous_state != 'revoke':
            previous.append(dict(permission=permission, state=previous_state))

        if params['state'] != 'revoke':
            current.append(dict(permission=permission, state=params['state']))

        if not module.check_mode:
            modify_permission(
                params['principal'],
                params['database'],
                permission,
                previous_state,
                params['state'],
                module
            )

    if len(previous) > 0:
        if len(current) > 0:
            result: dict = dict(changed=changed, previous=previous, current=current)
        else:
            result: dict = dict(changed=changed, previous=previous)
    else:
        if len(current) > 0:
            result: dict = dict(changed=changed, current=current)
        else:
            result: dict = dict(changed=changed)

    module.close_client_session()
    module.exit_json(**result)


def validate_params(params: dict, module: MssqlModule) -> None:
    """
    Validates the module parameters.

    Args:
        params (dict): The module parameters.
        module (MssqlModule): The module instance.
    """

    if len(params['permissions']) < 1:
        module.handle_error(MssqlModuleError(message='At least one permission must be specified.'))

    query: str = f"SELECT name FROM sys.databases WHERE name = '{params['database']}'"

    try:
        module.cursor.execute(query)
        result: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if result is None:
        module.handle_error(MssqlModuleError(message=f"No database exists with the name '{params['database']}'."))

    query: str = f"""
    SELECT name FROM {params['database']}.sys.database_principals
    WHERE name = '{params['principal']}'
    """

    try:
        module.cursor.execute(query)
        result: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if result is None:
        module.handle_error(MssqlModuleError(message=f"No database principal exists with the name '{params['principal']}'."))


def get_db_permissions(
        principal: str,
        database: str,
        permissions: List[str],
        module: MssqlModule) -> dict:
    """
    Gets the database-level permissions.

    Args:
        principal (str): The name of the database principal.
        database (str): The name of the database.
        permissions (List[str]): The database-level permissions.
        module (MssqlModule): The module instance.

    Returns:
        dict: The relevant database-level permissions.
    """

    results: dict = {}

    for permission in permissions:
        results = get_db_permission(principal, database, permission, module, results)

    return results


def get_db_permission(
        principal: str,
        database: str,
        permission: str,
        module: MssqlModule,
        results: dict) -> dict:
    """
    Gets the database-level permission.

    Args:
        principal (str): The name of the database principal.
        database (str): The name of the database.
        permission (str): The database-level permission.
        module (MssqlModule): The module instance.
        results (dict): The results of previous operations.

    Returns:
        dict: Results of this and previous operations.
    """

    query: str = f"""
    SELECT principals.name AS name,
            permissions.class_desc AS class,
            permissions.permission_name AS permission,
            permissions.state_desc AS state
    FROM {database}.sys.database_permissions permissions
    JOIN {database}.sys.database_principals principals
    ON permissions.grantee_principal_id = principals.principal_id
    WHERE principals.name = '{principal}'
    AND permissions.class_desc = 'DATABASE'
    AND permissions.permission_name = '{convert_permission_to_query(permission)}'
    """

    try:
        module.cursor.execute(query)
        row: Optional[dict] = module.cursor.fetchone()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))

    if row is None:
        results[permission] = 'revoke'
    else:
        results[permission] = row['state'].lower()

    return results


def convert_permission_to_query(permission: str) -> str:
    """
    Converts the permission to the query string.

    Args:
        permission (str): The permission to convert.

    Returns:
        str: The query string.
    """

    return permission.replace('_', ' ').upper()


def modify_permission(
        principal: str,
        database: str,
        permission: str,
        previous_state: str,
        state: str,
        module: MssqlModule) -> None:
    """
    Modifies the database-level permission.

    Args:
        principal (str): The name of the database principal.
        database (str): The name of the database.
        permission (str): The database-level permission.
        previous_state (str): The previous state of the permission.
        state (str): The desired state of the permission.
        module (MssqlModule): The module instance.
    """

    if previous_state == state:
        return

    if state == 'revoke':
        if previous_state == 'grant_with_grant_option':
            query: str = f"""
            USE [{database}];
            REVOKE {convert_permission_to_query(permission)} TO [{principal}] CASCADE
            """
        else:
            query: str = f"""
            USE [{database}];
            REVOKE {convert_permission_to_query(permission)} TO [{principal}]
            """
    elif state == 'grant':
        if previous_state == 'grant_with_grant_option':
            query: str = f"""
            USE [{database}];
            REVOKE GRANT OPTION FOR {convert_permission_to_query(permission)} TO [{principal}] CASCADE
            """
        else:
            query: str = f"""
            USE [{database}];
            GRANT {convert_permission_to_query(permission)} TO [{principal}]
            """
    elif state == 'deny':
        if previous_state == 'grant_with_grant_option':
            query: str = f"""
            USE [{database}];
            DENY {convert_permission_to_query(permission)} TO [{principal}] CASCADE
            """
        else:
            query: str = f"""
            USE [{database}];
            DENY {convert_permission_to_query(permission)} TO [{principal}]
            """
    elif state == 'grant_with_grant_option':
        query: str = f"""
        USE [{database}];
        GRANT {convert_permission_to_query(permission)} TO [{principal}] WITH GRANT OPTION
        """

    try:
        module.cursor.execute(query)
        module.conn.commit()
    except Exception as e:
        module.handle_error(MssqlModuleError(message=to_native(e), exception=e))


def main() -> None:
    run_module()


if __name__ == '__main__':
    main()
