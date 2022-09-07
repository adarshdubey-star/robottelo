"""Test class for Ansible Roles and Variables pages

:Requirement: Ansible

:CaseAutomation: Automated

:CaseLevel: Acceptance

:CaseComponent: Ansible

:Assignee: sbible

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""
from wait_for import wait_for


def test_fetch_and_sync_ansible_playbooks(target_sat):
    """
    Test Ansible Playbooks api for fetching and syncing playbooks

    :id: 17b4e767-1494-4960-bc60-f31a0495c09f

    :Steps:

        1. Install ansible collection with playbooks.
        2. Try to fetch the playbooks via api.
        3. Sync the playbooks.
        4. Assert the count of playbooks fetched and synced are equal.

    :expectedresults:
        1. Playbooks should be fetched and synced successfully.

    :BZ: 2115686

    :CaseAutomation: Automated
    """
    target_sat.execute(
        "ansible-galaxy collection install -p /usr/share/ansible/collections "
        "xprazak2.forklift_collection"
    )
    id = target_sat.api.SmartProxy(name=target_sat.hostname).search()[0].id
    playbook_fetch = target_sat.api.AnsiblePlaybooks().fetch(data={'proxy_id': id})
    playbooks_count = len(playbook_fetch['results']['playbooks_names'])
    playbook_sync = target_sat.api.AnsiblePlaybooks().sync(data={'proxy_id': id})
    assert playbook_sync['action'] == "Sync playbooks"

    wait_for(
        lambda: target_sat.api.ForemanTask()
        .search(query={'search': f'id = {playbook_sync["id"]}'})[0]
        .result
        == 'success',
        timeout=100,
        delay=15,
        silent_failure=True,
        handle_exception=True,
    )
    task_details = target_sat.api.ForemanTask().search(
        query={'search': f'id = {playbook_sync["id"]}'}
    )
    assert len(task_details[0].output['result']['created']) == playbooks_count
