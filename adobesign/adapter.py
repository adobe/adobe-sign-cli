##########################################################################
# © Copyright 2015-2021 Adobe. All rights reserved.
# Adobe holds the copyright for all the files found in this repository.
# See the LICENSE file for licensing information.
##########################################################################

"""Sign API Adapter/Helper."""

from .session import SignSession


class Sign:
    def __init__(self, integration_key, base_uri, user=None):
        self.session = SignSession(integration_key, base_uri, user)

    def validate(self, resp, code=200):
        try:
            success = resp.status_code in code
        except TypeError:
            success = resp.status_code != code

        if success:
            raise Exception(
                {
                    "issue": "Bad Response",
                    "status_code": resp.status_code,
                    "data": resp.text,
                }
            )

    def get_template_list(self, cur=None):
        url = f"/libraryDocuments"
        params = {
            "cursor": cur,
            "pageSize": 1000,
        }
        resp = self.session.get(url, params=params)
        self.validate(resp)
        return resp.json()

    def get_template_list_all(self, cur=None):
        data = self.get_template_list(cur)
        yield from [template["id"] for template in data["libraryDocumentList"]]
        if data.get("page", {}).get("nextCursor", None):
            cur = data.get("page", {}).get("nextCursor", None)
            yield from self.get_template_list_all(cur)

    def get_template(self, id):
        url = f"/libraryDocuments/{id}"
        resp = self.session.get(url)
        self.validate(resp)
        return resp.json()

    def get_template_docs(self, id):
        url = f"/libraryDocuments/{id}/documents"
        resp = self.session.get(url)
        self.validate(resp)
        return resp.json()

    def get_template_doc(self, id, doc_id):
        url = f"/libraryDocuments/{id}/documents/{doc_id}"
        resp = self.session.get(url, headers={"Accept": "application/pdf"})
        self.validate(resp)
        return resp.content

    def get_template_doc_files(self, id):
        docs = self.get_template_docs(id)
        for doc in docs["documents"]:
            yield self.get_template_doc(id, doc["id"])

    def get_template_fields(self, id):
        url = f"/libraryDocuments/{id}/formFields"
        resp = self.session.get(url)
        self.validate(resp)
        return resp.json()

    def create_transient(self, doc, mime_type="application/pdf"):
        url = f"/transientDocuments"
        files = {
            "File": doc,
            "Mime-Type": mime_type,
        }
        resp = self.session.post(url, files=files)
        self.validate(resp, code=201)
        return resp.json()

    def bulk_create_transient(self, docs=[]):
        for doc in docs:
            data = self.create_transient(doc)
            yield data["transientDocumentId"]

    def create_template(self, template_data, transient_ids=[]):
        data = {
            "name": template_data["name"],
            "templateTypes": template_data["templateTypes"],
            "sharingMode": "USER",
            "state": "ACTIVE",
            "fileInfos": [{"transientDocumentId": id} for id in transient_ids],
        }
        url = f"/libraryDocuments"
        resp = self.session.post(url, json=data)
        self.validate(resp, code=201)
        return resp.json()

    def update_template_fields(self, id, fields):
        url = f"/libraryDocuments/{id}/formFields"
        resp = self.session.put(url, json=fields)
        self.validate(resp)
        return resp.json()

    def get_users(self, cur=None):
        params = {
            "cursor": cur,
            "pageSize": 1000,
        }
        resp = self.session.get("/users", params=params)
        self.validate(resp)
        data = resp.json()
        return {
            "next": data.get("page", {}).get("nextCursor"),
            "users": [user["id"] for user in data["userInfoList"]],
        }

    def get_all_users(self, cursor=None, users=[]):
        data = self.get_users(cursor)
        users.extend(data["users"])

        if data["next"]:
            return self.get_all_users(data["next"], users)
        return users

    def get_all_active_users(self, email=True):
        users = self.get_all_users()
        for user in users:
            resp = self.session.get(f"/users/{user}")
            data = resp.json()
            if data["status"] == "ACTIVE":
                if email:
                    yield data["email"]
                else:
                    yield user

    def get_user_groups(self, user_id):
        resp = self.session.get(f"/users/{user_id}/groups")
        self.validate(resp)
        return resp.json()

    def update_user_groups(self, user_id, data):
        resp = self.session.put(f"/users/{user_id}/groups", json=data)
        self.validate(resp, (200, 204))
        return resp.json()

    def get_groups(self, cur=None):
        url = f"/groups"
        params = {
            "cursor": cur,
            "pageSize": 100,
        }
        resp = self.session.get(url, params=params)
        self.validate(resp)
        return resp.json()

    def get_groups_all(self, cur=None):
        data = self.get_groups(cur)
        yield from [group["groupId"] for group in data["groupInfoList"]]
        if data.get("page", {}).get("nextCursor", None):
            cur = data.get("page", {}).get("nextCursor", None)
            yield from self.get_groups_all(cur)

    def get_group_default(self, cur=None):
        data = self.get_groups(cur)
        for group in data["groupInfoList"]:
            if group["isDefaultGroup"]:
                return group["groupId"]
        if data.get("page", {}).get("nextCursor", None):
            cur = data.get("page", {}).get("nextCursor", None)
            return self.get_group_default(cur)

    def set_primary_group(self, user_id, group_id):
        user_groups = self.get_user_groups(user_id)
        for group in user_groups["groupInfoList"]:
            primary = group["id"] == group_id
            group["isPrimaryGroup"] = primary
        self.update_user_groups(user_id, user_groups)
