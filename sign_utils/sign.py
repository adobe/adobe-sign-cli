import os
from dotenv import load_dotenv

from .session import SignSession


class Sign:
    def __init__(self, integration_key, base_uri, user=None):
        self.session = SignSession(integration_key, base_uri, user)

    def validate(self, resp, code=200):
        if resp.status_code != code:
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
            yield from self.get_template_list_all(next)

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
