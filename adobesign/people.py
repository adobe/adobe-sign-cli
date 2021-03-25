##########################################################################
# © Copyright 2015-2021 Adobe. All rights reserved.
# Adobe holds the copyright for all the files found in this repository.
# See the LICENSE file for licensing information.
##########################################################################

"""Work with users and groups"""


class UMG:
    def __init__(self, sign):
        self.sign = sign

    def users_with_default_primary(self):
        default_group = self.sign.get_group_default()
        users = self.sign.get_all_active_users(email=False)
        for user in users:
            user_groups = self.sign.get_user_groups(user)
            for user_group in user_groups["groupInfoList"]:
                is_primary = user_group["isPrimaryGroup"]
                is_default = user_group["id"] == default_group
                has_multiple_groups = len(user_groups["groupInfoList"]) > 1
                if is_primary and is_default and has_multiple_groups:
                    yield user

    def make_default_not_primary(self):
        default_group = self.sign.get_group_default()
        users = self.sign.get_all_active_users(email=False)
        for user_id in users:
            user_groups = self.sign.get_user_groups(user_id)
            if len(user_groups["groupInfoList"]) != 2:
                continue
            for i, user_group in enumerate(user_groups["groupInfoList"]):
                is_primary = user_group["isPrimaryGroup"]
                is_default = user_group["id"] == default_group
                if is_primary and is_default:
                    new_key = int(i == 0)
                    new_group_id = user_groups["groupInfoList"][new_key]["id"]
                    self.sign.set_primary_group(user_id, new_group_id)
                    yield f'Default for user {user_id}: {is_default} -> {new_group_id}'


class Ownership:
    def __init__(self, sign):
        self.sign = sign

    def get_templates_owned_by(self, user, email=False):
        if email:
            key = "ownerEmail"
        else:
            key = "ownerId"

        templates = self.sign.get_template_list_all()
        for template in templates:
            if template[key] == user:
                yield template

    def bulk_change_tmplate_ownership(self, user_old, user_new, email=False):
        if email:
            key = "ownerEmail"
        else:
            key = "ownerId"

        templates = self.get_templates_owned_by(user_old, email)
        for template in templates:
            template_id = template["id"]
            template_data = self.sign.get_template(template_id)
            template_data[key] = user_new

            # TODO: Add this
            # self.sign.update_template(template_id, template_data)
