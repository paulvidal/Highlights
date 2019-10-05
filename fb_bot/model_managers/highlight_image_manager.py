from cloudinary_wrapper import uploader
from fb_bot.logger import logger
from fb_highlights.models import HighlightImage
from highlights import env, settings


def add_image_for_highlight(highlight):
    img_link = highlight.img_link

    # No need to upload in debug mode
    if env.DEBUG:
        return

    # No need to upload default images
    if _is_default_highlight_img(img_link):
        return

    # No need to upload if image already exists
    if HighlightImage.objects.filter(match_id=highlight.id, img_link=img_link):
        return

    # Upload the image to the cloud
    try:
        img_uploaded_link = uploader.upload_image(img_link)

        logger.info("Image added for img_link: " + img_link, extra={
            'img_link': img_link,
            'img_uploaded_link': img_uploaded_link
        })

    except:
        logger.error("Image failed uploading: " + img_link)
        return

    HighlightImage.objects.update_or_create(match_id=highlight.id,
                                            img_link=img_link,
                                            img_uploaded_link=img_uploaded_link,
                                            source=highlight.source)


def fetch_best_image_for_highlight(highlight):
    # Use default image in case there are no images found
    best_priority = 0
    best_image_link = settings.STATIC_URL + "img/logo.png"

    images = HighlightImage.objects.filter(match_id=highlight.id)

    for i in images:
        if i.image_source_priority() > best_priority:
            best_priority = i.image_source_priority()
            best_image_link = i.img_uploaded_link

    return best_image_link


def has_images_for_highlight(highlight):
    return len(list(HighlightImage.objects.filter(match_id=highlight.id))) > 0


# Helper
def _is_default_highlight_img(img_link):
    return img_link and any(
        [default_keyword in img_link for default_keyword in [
            'nothumb',
            '/default.jpg',
            '/logo.png'
        ]]
    )