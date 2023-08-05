import skil_client


class WorkSpace:

    def __init__(self, skil=None, name=None, labels=None, verbose=False, create=True):
        if not create:
            return
        self.skil = skil
        self.printer = self.skil.printer
        self.name = name if name else 'skil_workspace'

        self.workspace = self.skil.api.add_model_history(
            self.skil.server_id,
            skil_client.AddModelHistoryRequest(name, labels)
        )
        self.id = self.workspace.model_history_id

        if verbose:
            self.printer.pprint(self.workspace)

    def delete(self):
        try:
            api_response = self.skil.api.delete_model_history(
                self.skil.server_id, self.workspace.id)
            self.skil.printer.pprint(api_response)
        except skil_client.rest.ApiException as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_model_history: %s\n" % e)

def get_workspace_by_id(self, skil, id):
    server_id = skil.server_id
    response = skil.api.get_model_history(server_id, id)
    ws = WorkSpace(create=False)
    ws.skil = skil
    ws.printer = skil.printer
    ws.workspace = response
    ws.id = id
    return ws
