"""
JSON message formatter
"""

def create_message(text):
    return {
        "text": text
    }


def create_quick_text_reply_message(text, quick_replies):
    formatted_quick_replies = []

    for quick_reply in quick_replies:
        formatted_quick_replies.append({
            "content_type": "text",
            "title": quick_reply,
            "payload": "NO_PAYLOAD"
        })

    return {
        "text": text,
        "quick_replies": formatted_quick_replies
    }


def create_list_attachment(elements):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "list",
                "top_element_style": "compact",
                "elements": elements
            }
        }
    }


def create_generic_attachment(elements):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }


def create_image_attachment_from_saved_asset(asset_id):
    return {
        "attachment": {
            "type": "image",
            "payload": {
                "attachment_id": str(asset_id)
            }
        }
    }


def create_image_attachment_from_url(url):
    return {
        "attachment":{
            "type":"image",
            "payload": {
                "url": url,
                "is_reusable": True
            }
        }
    }