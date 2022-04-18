import pytest

from app.services.book_service import BookServiceOpenBD
from app.services.error import OpenBD404NotFoundError, OpenBDConnectionError


class TestBookServiceOpenBD():

    @pytest.fixture
    def openbd_api_endpoint(self):
        return "https://api.openbd.jp/v1/get"

    def test_retrive_book_info_success(self, openbd_api_endpoint):
        """書籍情報が取得できる場合のテスト
        """

        test_isbn = "9784047914742"

        book_service = BookServiceOpenBD(openbd_api_endpoint)
        book_info = book_service.retrive(test_isbn)

        expected_title = "ダ・ヴィンチ・コード"
        expected_author = "Brown,Dan／著 越前敏弥／翻訳 ブラウンダン／著"
        expected_cover = "https://cover.openbd.jp/9784047914742.jpg"
        expected_published_at = "2004-05"

        assert book_info["title"] == expected_title
        assert book_info["author"] == expected_author
        assert book_info["cover"] == expected_cover
        assert book_info["published_at"] == expected_published_at

    def test_retrive_book_info_failed_result_is_null(self, openbd_api_endpoint):
        """openBDに登録されていない書籍の場合のテスト
        """

        test_isbn = "9781847942678"

        book_service = BookServiceOpenBD(openbd_api_endpoint)
        book_info = book_service.retrive(test_isbn)

        expected_book_info = {}

        assert book_info == expected_book_info

    def test_retrive_book_info_failed_result_is_not_found(self):
        """APIエンドポイントが存在しない場合のテスト
        """

        test_isbn = "9784047914742"

        invalid_api_endpoint = "https://api.openbd.jp/v2/get"

        book_service = BookServiceOpenBD(invalid_api_endpoint)
        with pytest.raises(OpenBD404NotFoundError) as e:

            _ = book_service.retrive(test_isbn)

        assert str(e.value.message) == "OpenBD API endpoint is 404 not found."

    def test_retrive_book_info_failed_connection_error(self):
        """接続エラーが発生した場合のテスト
        """

        test_isbn = "9784047914742"

        invalid_api_endpoint = "https://api.open.jp/v1/get"

        book_service = BookServiceOpenBD(invalid_api_endpoint)

        with pytest.raises(OpenBDConnectionError) as e:

            _ = book_service.retrive(test_isbn)

        assert str(e.value.message) == "OpenBD API endpoint is connection error."
