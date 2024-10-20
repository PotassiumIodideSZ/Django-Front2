import json
import pickle
from os import path, mkdir

import keras
import numpy as np
import pandas as pd
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist
from keras_preprocessing.text import tokenizer_from_json
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Keyword
from rest_framework import status

from .helpers import get_lower, text_update_key, onlygoodsymbols
from .serializers import UploadFileSerializer, AuthUserSerializer
from .token import create_token, read_token, ReadTokenException


class AuthUserView(APIView):
    def post(self, request: Request):
        serializer = AuthUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            request_body = request.data
            try:
                user: User = User.objects.get(username=request_body["login"])
            except ObjectDoesNotExist:
                return Response(data="User not found", status=404)

            user.save()
            if user.check_password(request_body["password"]):
                payload = {
                    'user_id': user.id
                }

                token = create_token(payload)

                response_body = {
                    'user_id': user.id,
                    'Authorization': token
                }

                return Response(data=response_body, status=200)
            else:
                return Response(data="Unauthorized", status=401)


class UploadFileView(APIView):
    def get(self, request: Request):

        excel_path = "src/excel/output.xlsx"

        response_excel_file = open(excel_path, mode="rb")
        return FileResponse(response_excel_file)

    def post(self, request: Request):
        weight_type = request.data.get('weight_type', None)
        if weight_type not in ['light', 'medium', 'heavy']:
            return Response(data="Invalid weight type. Expected 'light', 'medium', or 'heavy'.", status=400)
        
        token = request.headers.get('Authorization')
        try:
            read_token(token)
        except ReadTokenException:
            return Response(data="Unauthorized", status=401)

        serializer = UploadFileSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            files = request.FILES

            excel_file: InMemoryUploadedFile = files.get('file')
            excel_body: bytes = excel_file.file.getvalue()

            folder_path = "src/excel"
            exel_name = excel_file.name
            if not path.isdir(folder_path):
                mkdir(folder_path)
            excel_path = folder_path + "/" + exel_name

            new_excel_file = open(excel_path, mode="wb")
            new_excel_file.write(excel_body)
            new_excel_file.close()

            # Define different configurations
            # configs = {
            #     'light': {"epochs": 200, "batch_size": 512, "validation_split": 0.2, "verbose": 1},
            #     'medium': {"epochs": 200, "batch_size": 1024, "validation_split": 0.2, "verbose": 1},
            #     'heavy': {"epochs": 200, "batch_size": 512, "validation_split": 0.4, "verbose": 1}
            # }

            # Load and compile the model
            model = keras.models.load_model("main_model")

            # Use the configuration based on weight_type
        # if weight_type in configs:
        #     model.fit(X_train, y_train, **configs[weight_type])

        # Process the Excel file
        df = pd.read_excel(excel_path)
        obrashenie = df['Tекст обращения']
        obrashenie = obrashenie.apply(get_lower).apply(text_update_key).apply(onlygoodsymbols)

        with open('tokenizer.json') as f:
            data = json.load(f)
            t = tokenizer_from_json(data)

        categories = Category.objects.all()
        ly = [category.name for category in categories]
        obr_t = t.texts_to_matrix(obrashenie, mode='binary')
        pred = model.predict(obr_t)
        predicts = [ly[i] for i in np.argmax(pred, axis=-1)]
        df["Категория"] = predicts

        # Save the processed file
        output_excel_file_path = folder_path + "/output.xlsx"
        with pd.ExcelWriter(output_excel_file_path) as writer:
            df.to_excel(writer, index=False)

        return Response(status=201)

class CategoryUpdateView(APIView):
    def get(self, request: Request):
        """
        Получение всех категорий из базы данных.
        """
        categories = Category.objects.all()
        category_names = [category.name for category in categories]
        return Response(data={"categories": category_names}, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """
        Получение одной категории и её почты по имени или удаление категории по имени.
        Ожидается, что в теле запроса будет имя категории и флаг для удаления.
        """
        category_name = request.data.get('category_name', None)
        category_email = request.data.get('email', None)  # Получение почты категории
        delete_flag = request.data.get('delete', False)  # Флаг для удаления категории

        if not category_name:
            return Response(data="Category name is required.", status=status.HTTP_400_BAD_REQUEST)

        if delete_flag:
            try:
                category = Category.objects.get(name=category_name)
                category.delete()
                return Response(data=f'Category "{category_name}" deleted successfully.', status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response(data="Category not found.", status=status.HTTP_404_NOT_FOUND)
        
        if category_email:
            category, created = Category.objects.get_or_create(name=category_name, email=category_email)
            if created:
                return Response(data=f'Category "{category_name}" created successfully.', status=status.HTTP_201_CREATED)
            else:
                return Response(data=f'Category "{category_name}" already exists.', status=status.HTTP_200_OK)

        try:
            category = Category.objects.get(name=category_name)
            response_data = {
                'name': category.name,
                'email': category.email
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(data="Category not found.", status=status.HTTP_404_NOT_FOUND)           
    

class KeywordUpdateView(APIView):
    def get(self, request: Request):
        """
        Получение всех ключевых слов из базы данных.
        """
        keywords = Keyword.objects.all()
        keyword_list = [keyword.word for keyword in keywords]
        return Response(data={"keywords": keyword_list}, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """
        Обновление ключевых слов в базе данных.
        Ожидается, что в теле запроса будет список ключевых слов.
        """
        keywords_data = request.data.get('keywords', [])

        if not isinstance(keywords_data, list):
            return Response(data="Invalid data format. Expected a list of keywords.", status=status.HTTP_400_BAD_REQUEST)

        # Обработка добавления или обновления ключевых слов
        for keyword_word in keywords_data:
            keyword, created = Keyword.objects.get_or_create(word=keyword_word)
            if created:
                print(f'Keyword "{keyword_word}" created')
            else:
                print(f'Keyword "{keyword_word}" already exists')

        # Удаление ключевых слов, которые не были в списке
        existing_keywords = Keyword.objects.all()
        for keyword in existing_keywords:
            if keyword.word not in keywords_data:
                keyword.delete()
                print(f'Keyword "{keyword.word}" deleted')

        return Response(data="Keywords updated successfully.", status=status.HTTP_200_OK)