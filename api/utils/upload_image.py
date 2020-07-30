""" Module for uploading images """

from os import getenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(cloud_name=getenv('CLOUDINARY_NAME'),
                  api_key=getenv('CLOUDINARY_API_KEY'),
                  api_secret=getenv('CLOUDINARY_API_SECRET'))


def upload_image(file, folder):
    """
    Uploads image to cloudinary
    Args:
        file(file): file
        folder(str): folder name

    Returns:
        result(dict): upload result
    """

    result = cloudinary.uploader.upload(file,
                                        folder=folder,
                                        resource_type='image')
    image = {
        'url': result['url'],
        'public_id': result['public_id']
    }
    return image


def destroy_image(public_id):
    """
    Destroy image from cloudinary
    Args:
        public_id(str): file public id

    """

    cloudinary.uploader.destroy(public_id)
