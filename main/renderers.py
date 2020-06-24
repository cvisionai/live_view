from rest_framework.renderers import BaseRenderer

class JpegRenderer(BaseRenderer):
    media_type = 'image/jpeg'
    charset = None
    format = 'jpg'

    def render(self, data, media_type=None, renderer_context=None):
        return data
