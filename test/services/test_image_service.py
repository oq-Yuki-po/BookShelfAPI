from PIL import Image

from app.services.image_service import ImageBase64Service


class TestImageService:

    def test_encode(self, encode_image_base64):
        """
        Test encode
        """
        # Prepare
        test_image_path = "app/static/images/no_image.jpg"
        # Execute
        encoded_image = ImageBase64Service.encode(test_image_path)
        # Assert
        assert isinstance(encoded_image, bytes)
        assert encoded_image == encode_image_base64(test_image_path)

    def test_decode(self, encode_image_base64):
        """
        Test decode
        """
        # Prepare
        test_image_path = "app/static/images/no_image.jpg"
        encoded_image = encode_image_base64(test_image_path)
        # Execute
        decoded_image = ImageBase64Service.decode(encoded_image)
        # Assert
        assert isinstance(decoded_image, Image.Image)
