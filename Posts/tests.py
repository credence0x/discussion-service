from django.test import TestCase, Client
from .models import Post
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from rest_framework.reverse import reverse



class PostTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        # create 2 user objects and 3 post objects
        u1 = User.objects.create_user(username="ojetokun",first_name="Lanre",last_name="ojetokun",password="1234")
        u2 = User.objects.create_user(username="Hannah",first_name="Hannah",last_name="Roosevelt",password="1234")
        Post.objects.create(id=1,creator=u1,content="In the affirmative")
        Post.objects.create(id=2,creator=u2,content="Thats what I said")
        Post.objects.create(id=3,creator=u1,content="tHIS IS THE THIRD COMMENT")
        super(PostTestCase, self).setUpClass()
        


    def test_GET_posts_and_confirm_ordering_by_date_created(self):
        c = Client()
        c.login(username="ojetokun",password="1234")
        res = c.get(reverse("Posts:post-list"))
        self.assertEqual(res.status_code,200)


        #confirm ordering
        post_list = res.data
        last_datetime = ""

        for post in post_list:
            if not last_datetime:
                last_datetime = post['date_created']
                continue
            current_datetime = post['date_created']

            # assert that posts with the earlier time come first
            assert last_datetime <= current_datetime
            last_datetime = current_datetime



    

    def test_POST_post_by_authenticated_user(self):
        c = Client()
        c.login(username="ojetokun",password="1234")

        # the creator field is automatically filled in as the authenticated user and other field are taken care of automatically also
        res = c.post(reverse("Posts:post-list"),{"content":"This conversation really hits"})
        self.assertEqual(res.status_code,201)


    




    def test_POST_post_by_unauthenticated_user(self):
        c = Client()
        # c.login(username="ojetokun",password="1234")
        res = c.post(reverse("Posts:post-list"),{"content":"This conversation really hits"})
        self.assertEqual(res.status_code,403)





    def test_PUT_edit_by_wrong_user(self):
        c = Client()
        c.login(username="ojetokun",password="1234")
        res = c.put(reverse("Posts:post-detail" , args=[2]),{"content":"This is a change"},content_type='application/json')
        self.assertEqual(res.status_code,403)
        
   
   
   
    def test_PUT_edit_by_correct_user(self):
        c = Client()
        c.login(username="Hannah",password="1234")        
        res = c.put(reverse("Posts:post-detail" , args=[2]),{"content":"This is a change"},content_type='application/json')
        self.assertEqual(res.status_code,200)

   
   
   
   
   
    def test_PATCH_to_like_post(self):
        c1 = Client()
        c2 = Client()

        c1.login(username="ojetokun",password="1234") 
        c2.login(username="Hannah",password="1234")        

        c1.patch(reverse("Posts:post-like" , args=[2]),{},content_type='application/json')
        res = c2.patch(reverse("Posts:post-like" , args=[2]),{},content_type='application/json')
        likes = res.data['likes']
        num_people_who_liked = len(res.data['users_who_liked'])
        self.assertEqual(likes,2)
        self.assertEqual(num_people_who_liked,2)
        self.assertEqual(likes,num_people_who_liked)
        self.assertEqual(res.status_code,200)






    def test_PATCH_to_unlike_post(self):
        c1 = Client()
        c2 = Client()

        c1.login(username="ojetokun",password="1234") 
        c2.login(username="Hannah",password="1234")        

        #give two likes
        c1.patch(reverse("Posts:post-like" , args=[3]),{},content_type='application/json')
        res = c2.patch(reverse("Posts:post-like" , args=[3]),{},content_type='application/json')

        likes = res.data['likes']
        num_people_who_liked = len(res.data['users_who_liked'])
        self.assertEqual(likes,2)

        # remove one like
        res = c1.patch(reverse("Posts:post-unlike" , args=[3]),{},content_type='application/json')
        likes = res.data['likes']
        num_people_who_liked = len(res.data['users_who_liked'])
        self.assertEqual(likes,1)
        self.assertEqual(num_people_who_liked,1)
        self.assertEqual(likes,num_people_who_liked)
        self.assertEqual(res.status_code,200)



    def test_GET_posts_ordered_by_likes(self):
        c = Client()
        c.login(username="ojetokun",password="1234")
        

        ############# pre-processing #########
        # add likes to some posts
        c2 = Client()
        c2.login(username="Hannah",password="1234")        

        c.patch(reverse("Posts:post-like" , args=[2]),{},content_type='application/json')
        c.patch(reverse("Posts:post-like" , args=[1]),{},content_type='application/json')

        post2 = c2.patch(reverse("Posts:post-like" , args=[2]),{},content_type='application/json')
        likes = post2.data['likes']
        num_people_who_liked = len(post2.data['users_who_liked'])
        self.assertEqual(likes,2)
        self.assertEqual(num_people_who_liked,2)
        self.assertEqual(likes,num_people_who_liked)


        ######### END pre-processing #########

        #confirm ordering by likes
        res = c.get(reverse("Posts:post-order-by-likes"))
        self.assertEqual(res.status_code,200)
        post_list = res.data
        last_like_item = 0

        for post in post_list:
            if not last_like_item:
                last_like_item = post['likes']
                continue
            current_like_item = post['likes']
            assert last_like_item >= current_like_item
            last_like_item = current_like_item





       
    def test_DELETE_post_by_wrong_user(self):
        c = Client()
        c.login(username="ojetokun",password="1234")
        res = c.delete(reverse("Posts:post-detail" , args=[2]))
        self.assertEqual(res.status_code,403)






    def test_DELETE_post_by_correct_user(self):
        c = Client()
        c.login(username="Hannah",password="1234")
        res = c.delete(reverse("Posts:post-detail" , args=[2]))
        exists = Post.objects.filter(id=2).exists()
        self.assertEqual(False,exists)
        self.assertEqual(res.status_code,204)
       

            




