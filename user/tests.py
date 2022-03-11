# Create your tests here.
from rest_framework.test import APITestCase
from user.models import User
# Unit testing for models
class TestModels(APITestCase):
    def test_create_user(self):
        user = User.objects.create_user('ahmed','+213555344484','algeria','Ahmed2001')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.phone, '+213555344484')
    
    def test_whene_unsets_required_informations(self):
        self.assertRaises(ValueError,User.objects.create_user,name='',phone='+213555344484',country='algeria',password='Ahmed2001')
        self.assertRaises(ValueError,User.objects.create_user,name='ahmed',phone='',country='algeria',password='Ahmed2001')
        self.assertRaises(ValueError,User.objects.create_user,name='ahmed',phone='+213555344484',country='',password='Ahmed2001')
        self.assertRaises(ValueError,User.objects.create_user,name='ahmed',phone='+213555344484',country='algeria',password='')
        
    
        
        
        
    def test_create_super_user(self):
        user = User.objects.create_superuser('ahmed','+213555344484','Ahmed2001')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.phone, '+213555344484')    