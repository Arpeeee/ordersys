from storages.backends.gcloud import GoogleCloudStorage


class ProtectedGCSStorage(GoogleCloudStorage):
    def url(self, name):
        return f'/protected-media/{name}'
