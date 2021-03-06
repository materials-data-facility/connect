import re

import mdf_toolbox


def list_acls(endpoint, count_only=False, re_match=None):
    """List or count the ACLs on an endpoint, optionally matching some regex.

    Arguments:
        endpoint (str): The endpoint ID to check for ACLs.
        count_only (bool): When True, will only return the total count of ACLs found.
                When False, will print each ACL found.
                Default False.
        re_match (str): A regular expression to test the ACL's path. Any ACL rule
                that has a path matching this regex will be counted.
                Default None, to match all ACLs.
    Returns:
        int: The total ACLs matched.

    Note:
        You must be an Access Manager or higher on the target endpoint to list ACLs.
    """
    tc = mdf_toolbox.login(services="transfer")["transfer"]
    count = 0
    for rule in tc.endpoint_acl_list(endpoint):
        if re_match is None or re.match(re_match, rule["path"]):
            count += 1
            if not count_only:
                print(rule)
    return count


def delete_acls(endpoint, re_match, dry_run=True):
    """Delete ACLs from an endpoint matching some regex on the rule path.

    Arguments:
        endpoint (str): The endpoint ID to delete ACLs from.
        re_match (str): A regular expression to test the ACL's path. Any ACL rule
                that has a path matching this regex will be deleted.
        dry_run (bool): When True, will not actually delete anything, and instead
                will print the ACL rules that would have been deleted.
                When False, will permanently delete the ACL rules.
                Default True.

    Returns:
        int: The number of ACL rules matched for deletion.

    Caution:
            This function deletes ACL rules, which removes permissions.
            You must be an Access Manager or higher on the target endpoint,
            and you must exercise caution.
    """
    tc = mdf_toolbox.login(services="transfer")["transfer"]
    count = 0
    for rule in tc.endpoint_acl_list(endpoint):
        if re.match(re_match, rule["path"]):
            count += 1
            if dry_run:
                print(rule)
            else:
                tc.delete_endpoint_acl_rule(endpoint, rule["id"])
    return count
