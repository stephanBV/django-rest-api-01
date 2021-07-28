from rest_framework.test import APITestCase
from authentication.models import User


class TestModel(APITestCase):

    def test_creates_user(self):
        # self.assertEqual(1, 1-0)
        user=User.objects.create_user('steph', 'steph@gmail.com', 'password123@!')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'steph@gmail.com')

    def test_creates_super_user(self):
        user=User.objects.create_superuser('steph', 'steph@gmail.com', 'password123@!')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'steph@gmail.com')

    def test_raises_error_when_no_unsername_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username='', email='steph@gmail.com', password='password123@!')

    def test_raises_error_with_message_when_no_username_is_supplied(self): #test that your message has not been changed by somebody else
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(username='', email='steph@gmail.com', password='password123@!')
    
    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username='steph', email='', password='password123@!')

    def test_raises_error_with_message_when_no_email_is_supplied(self): #test that your message has not been changed by somebody else
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(username='steph', email='', password='password123@!')

    # def test_raises_error_when_is_staff_not_passed_as_true(self): CORRECT
    #     self.assertRaises(ValueError, User.objects.create_superuser, username='steph', email='steph@gmail.com', password='password123@!', is_staff=False)

    def test_creates_super_user_with_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username='', email='steph@gmail.com', password='password123@!', is_staff=False)
        
    def test_creates_super_user_with_is_super_user_status(self):    
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username='', email='steph@gmail.com', password='password123@!', is_superuser=False)
    