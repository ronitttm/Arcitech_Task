from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from cms_app.models import Content, CustomUser
from cms_app.auth import QueryParameterTokenAuthentication
from cms_app.serializers import UserSerializer, ContentSerializer, CustomAuthTokenSerializer
from cms_app.admin import CustomUserAdmin, ContentAdmin

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import CustomUser, Content


User = get_user_model()

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import CustomUser, Content

class RegisterAuthorViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_register_author(self):
        data = {
            'email': 'newauthor@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'Author',
            'phone': '1234567890',
            'address': '123 Main St',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'pincode': '123456'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Author registered successfully!')

    def test_register_author_invalid(self):
        data = {
            'email': '',
            'password': '',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='password123')
        self.url = reverse('login')

    def test_login(self):
        data = {'email': 'testuser@example.com', 'password': 'password123'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid(self):
        data = {'email': 'testuser@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ContentListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testauthor@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('content-create')

    def test_create_content(self):
        data = {
            'title': 'Test Content',
            'body': 'This is the body of the test content.',
            'summary': 'Test summary',
            'document': 'TestDocument.pdf',
            'categories': 'Category1, Category2',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_content(self):
        Content.objects.create(
            title='Test Content 1',
            body='Body of test content 1',
            summary='Summary 1',
            document='TestDoc1.pdf',
            categories='Cat1, Cat2',
            author=self.user
        )
        Content.objects.create(
            title='Test Content 2',
            body='Body of test content 2',
            summary='Summary 2',
            document='TestDoc2.pdf',
            categories='Cat3, Cat4',
            author=self.user
        )
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ContentDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testauthor@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.content = Content.objects.create(
            title='Test Content',
            body='This is the body of the test content.',
            summary='Test summary',
            document='TestDocument.pdf',
            categories='Category1, Category2',
            author=self.user
        )
        self.url = reverse('content-detail', kwargs={'pk': self.content.pk})

    def test_retrieve_content(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.content.title)

    def test_update_content(self):
        data = {'title': 'Updated Title'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.content.refresh_from_db()
        self.assertEqual(self.content.title, 'Updated Title')

    def test_delete_content(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Content.objects.filter(pk=self.content.pk).exists())

class ContentSearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testauthor@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('content-search')
        self.content1 = Content.objects.create(
            title='Searchable Content 1',
            body='This is searchable content 1.',
            summary='Summary 1',
            document='TestDoc1.pdf',
            categories='Cat1, Cat2',
            author=self.user
        )
        self.content2 = Content.objects.create(
            title='Searchable Content 2',
            body='This is searchable content 2.',
            summary='Summary 2',
            document='TestDoc2.pdf',
            categories='Cat3, Cat4',
            author=self.user
        )

    def test_search_content(self):
        response = self.client.get(self.url, {'query': 'searchable'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class AdminContentListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(email='admin@example.com', password='adminpassword')
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('admin-content-list')
        self.content1 = Content.objects.create(
            title='Admin Content 1',
            body='This is admin content 1.',
            summary='Summary 1',
            document='TestDoc1.pdf',
            categories='Cat1, Cat2',
            author=self.admin_user
        )
        self.content2 = Content.objects.create(
            title='Admin Content 2',
            body='This is admin content 2.',
            summary='Summary 2',
            document='TestDoc2.pdf',
            categories='Cat3, Cat4',
            author=self.admin_user
        )

    def test_list_all_content(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class AdminContentDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(email='admin@example.com', password='adminpassword')
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.content = Content.objects.create(
            title='Admin Content',
            body='This is admin content.',
            summary='Summary',
            document='TestDoc.pdf',
            categories='Cat1, Cat2',
            author=self.admin_user
        )
        self.url = reverse('admin-content-detail', kwargs={'pk': self.content.pk})

    def test_retrieve_admin_content(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.content.title)

    def test_update_admin_content(self):
        data = {'title': 'Updated Admin Title'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.content.refresh_from_db()
        self.assertEqual(self.content.title, 'Updated Admin Title')

    def test_delete_admin_content(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Content.objects.filter(pk=self.content.pk).exists())

class QueryParameterTokenAuthenticationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.auth = QueryParameterTokenAuthentication()

    def test_authenticate_no_token(self):
        request = self.factory.get('/')
        result = self.auth.authenticate(request)
        self.assertIsNone(result)

    def test_authenticate_valid_token(self):
        request = self.factory.get('/', {'token': self.token.key})
        user, token = self.auth.authenticate(request)
        self.assertEqual(user, self.user)
        self.assertEqual(token, self.token)

    def test_authenticate_invalid_token(self):
        request = self.factory.get('/', {'token': 'invalidtoken'})
        with self.assertRaises(AuthenticationFailed):
            self.auth.authenticate(request)

    def test_authenticate_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        request = self.factory.get('/', {'token': self.token.key})
        with self.assertRaises(AuthenticationFailed) as context:
            self.auth.authenticate(request)
        self.assertEqual(str(context.exception), 'User inactive or deleted.')

class CustomUserManagerTest(TestCase):
    def setUp(self):
        self.User = User

    def test_create_user(self):
        email = 'testuser@example.com'
        password = 'testpassword'
        user = self.User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_user(email=None, password='testpassword')
        self.assertEqual(str(context.exception), 'The Email field must be set')

    def test_create_superuser(self):
        email = 'admin@example.com'
        password = 'adminpassword'
        superuser = self.User.objects.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_superuser(email='admin@example.com', password='adminpassword', is_staff=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_staff=True.')

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError) as context:
            self.User.objects.create_superuser(email='admin@example.com', password='adminpassword', is_superuser=False)
        self.assertEqual(str(context.exception), 'Superuser must have is_superuser=True.')

class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            is_admin=True
        )
        self.admin = CustomUserAdmin(CustomUser, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ('email', 'first_name', 'last_name', 'is_admin'))

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ('email', 'first_name', 'last_name'))

class ContentAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_user(
            email='testauthor@example.com',
            password='password',
            first_name='Test',
            last_name='Author',
            is_admin=False
        )
        self.content = Content.objects.create(
            title='Test Content',
            body='This is the body of the test content.',
            summary='Test summary',
            document='TestDocument.pdf',
            categories='Category1, Category2',
            author=self.user
        )
        self.admin = ContentAdmin(Content, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ('title', 'author', 'created_at', 'updated_at'))

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ('title', 'body', 'summary', 'categories'))

class UserSerializerTest(TestCase):
    def test_create_user(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'address': 'Test Address',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'pincode': '123456'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))

class ContentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testauthor@example.com',
            password='password'
        )
        self.content = Content.objects.create(
            title='Test Content',
            body='This is the body of the test content.',
            summary='Test summary',
            document='TestDocument.pdf',
            categories='Category1, Category2',
            author=self.user
        )

    def test_content_serializer(self):
        serializer = ContentSerializer(instance=self.content)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title', 'body', 'summary', 'document', 'categories', 'author', 'created_at', 'updated_at'})
        self.assertEqual(data['title'], self.content.title)
        self.assertEqual(data['body'], self.content.body)
        self.assertEqual(data['summary'], self.content.summary)
        self.assertEqual(data['document'], self.content.document)
        self.assertEqual(data['categories'], self.content.categories)

class CustomAuthTokenSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.factory = APIRequestFactory()
        self.request = self.factory.post('/api/login/')

    def test_valid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        serializer = CustomAuthTokenSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)

    def test_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        serializer = CustomAuthTokenSerializer(data=data, context={'request': self.request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_credentials(self):
        data = {}
        serializer = CustomAuthTokenSerializer(data=data, context={'request': self.request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)