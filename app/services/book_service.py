
import json
from abc import ABCMeta, abstractmethod

import requests

from app.services.error import OpenBD404NotFoundError, OpenBDConnectionError


class ExternalBookInformationServiceInterface(metaclass=ABCMeta):

    @abstractmethod
    def retrive(self, isbn: str):
        raise NotImplementedError()


class BookServiceOpenBD(ExternalBookInformationServiceInterface):

    def __init__(self, openbd_api_endpoint: str) -> None:
        """初期化処理

        Parameters
        ----------
        openbd_api_endpoint : str
            openBDのAPIエンドポイント
        """
        self.openbd_api_endpoint = openbd_api_endpoint

    def retrive(self, isbn: str) -> dict:
        """書籍情報の取得処理

        Parameters
        ----------
        isbn : str
            isbn番号

        Returns
        -------
        book_info : dict
            取得した書籍情報

        Raises
        ------
        OpenBDConnectionError
            requests connection error
        OpenBD404NotFoundError
            apiの404 error
        """

        url = f'{self.openbd_api_endpoint}?isbn={isbn}'

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as connection_error:
            raise OpenBDConnectionError() from connection_error
        if response.status_code == 404:
            raise OpenBD404NotFoundError()

        response_json = json.loads(response.content)

        book_info = {}

        if response_json != [None]:
            book_info["title"] = response_json[0]['summary']['title']
            book_info["author"] = response_json[0]['summary']['author']
            book_info["cover"] = response_json[0]['summary']['cover']
            book_info["published_at"] = response_json[0]['summary']['pubdate']

        return book_info
