##########################################################################
# Copyright 2020 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
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
        templates = list(self.sender.get_template_list_all())

        for template in templates:
            self.clone_template(template)
            yield template
