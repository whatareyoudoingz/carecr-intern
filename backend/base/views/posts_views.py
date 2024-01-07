from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from base.models import Post, Review
from base.serializers import PostSerializer, ReviewSerializer
from rest_framework import status
from datetime import datetime
import openai
import os 
from dotenv import load_dotenv
import psycopg2
import pandas as pd

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
PORT = "5432"
DB_NAME = "postgres"

# set api key
load_dotenv(dotenv_path="../../../../../.env.local") #.env.local에 openai.api_key가 저장되어 있음. 환경변수로 사용함.
openai.api_key = os.getenv("OPENAI_API_KEY")

# Call the chat GPT API
def completion(chattime):
    name='김진아'
    conn = psycopg2.connect(
                    host=DB_HOST, port=PORT, database=DB_NAME,
                    user=DB_USER, password=DB_PASSWORD
                )
                
    cur = conn.cursor()
    cur.execute("SELECT * FROM chatlog WHERE username = (%s) AND chattime = (%s);", (name, chattime))
    result_rows = cur.fetchall()
        
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(result_rows, columns=columns)
    all_text = "\n".join([f"(person: {row['person']}, chatbot: {row['chatbot']})" for index, row in df.iterrows()])     

    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo-1106',
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"다음 내용을 한글로 요약해서 일기형식으로 말해줘 => {all_text}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

@api_view(['GET'])
def getPosts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    posts = Post.objects.filter(user_id=request.user, title__icontains=query)
    serializer = PostSerializer(posts, many=True) 
    return Response({'posts': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPosts(request):
    data = request.data
    user = request.user
    now = data['title']
    posts=Post.objects.create(
        title= data['title'],
        body= data['body'],
        user_id=user,
        status=True,
        created_at=now,
    )
    serializer=PostSerializer(posts, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getPostsReview(request,pk):
    reviews = Review.objects.filter(post_id=pk)    
    serializer = ReviewSerializer(reviews, many=True) 
    return Response(serializer.data)

@api_view(['POST'])
def createPostsReview(request,pk):
    post = Post.objects.get(id=pk)
    comment = completion(chattime) 
    print(comment)
    data = request.data
    now = datetime.now()
    if comment:
        content = {'detail':'아직 안 풀렸구나. 새로운 문장을 만들어줄게.'}
        review = Review.objects.filter(post_id=pk).delete() 
        review = Review.objects.create(
            post = post, 
            name = 'chatgpt',
            comment = comment,
            createdAt = now,
        )
        serializer = ReviewSerializer(review, many=False)
        return Response(serializer.data)
    else: 
        review = Review.objects.create(
            post = post,
            name = 'chatgpt',
            comment = comment,
            createdAt = now,
        )
        serializer = ReviewSerializer(review, many=False)
        return Response(serializer.data)

@api_view(['GET'])
def getPost(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePosts(request, pk):
    data = request.data
    post = Post.objects.get(id=pk) 
    post.title = data['title']
    post.body = data['body']
    post.save()
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deletePosts(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response('Post Deleted')
