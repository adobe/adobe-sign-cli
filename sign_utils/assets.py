##########################################################################
# © Copyright 2015-2021 Adobe. All rights reserved.
# Adobe holds the copyright for all the files found in this repository.
# See the LICENSE file for licensing information.
##########################################################################

"""Manipulate assets w/in Adobe Sign"""


class Transfer:
    def __init__(self, sender_session, receiver_session=None):
        self.sender = sender_session
        if receiver_session is not None:
            self.receiver = receiver_session
        else:
            self.receiver = self.sender

    def clone_template(self, id):
        # Fetch Template Data
        template_data = self.sender.get_template(id)
        docs = self.sender.get_template_doc_files(id)
        fields = self.sender.get_template_fields(id)

        # Create new Template
        transient_ids = self.receiver.bulk_create_transient(docs)
        new_template = self.receiver.create_template(template_data, transient_ids)
        self.receiver.update_template_fields(new_template["id"], fields)

        return new_template["id"]

    def bulk_clone(self):
        # get all templates
        ids = []
        for id in ids:
            self.clone_template(id)
