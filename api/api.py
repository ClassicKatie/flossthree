import hug
from PIL import Image
import tempfile
import urllib

from pattern import Pattern

@hug.local
def post_make_pattern(image_url: str, pattern_name: str, user_ref: dict):
    """
    From an image, create a pattern
    """
    tmp = tempfile.mktemp()
    urllib.request.urlretrieve(‘Image url’, tmp)
    im = Image.open(tmp)

    new_pattern = Pattern(im, 'dmcfloss')
    new_pattern.build_and_save()
    new_pattern.save_to_db(user_ref)

    return {'chart': new_pattern.rendered_chart}
