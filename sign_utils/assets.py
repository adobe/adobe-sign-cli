"""Manipulate assets w/in Adobe Sign"""


class Transfer:
    def __init__(self, sender_session, reciever_session=None):
        self.sender = sender_session
        if reciever_session is not None:
            self.reciever = reciever_session
        else:
            self.reciever = self.sender

    def clone_template(self, id):
        # Fetch Template Data
        template_data = self.sender.get_template(id)
        docs = self.sender.get_template_doc_files(id)
        fields = self.sender.get_template_fields(id)

        # Create new Template
        transient_ids = self.reciever.bulk_create_transient(docs)
        new_template = self.reciever.create_template(template_data, transient_ids)
        self.reciever.update_template_fields(new_template["id"], fields)

        return new_template["id"]

    def bulk_clone(self):
        # get all templates
        ids = []
        for id in ids:
            self.clone_template(id)
