from django.shortcuts import render
from movie.models import Movie
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

def get_embedding(text, client, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        
        
        load_dotenv('../api_keys_1 1.env')
        client = OpenAI(api_key=os.environ.get('openai-apikey'))
        
    
        emb_req = get_embedding(prompt, client)
        
    
        movies = Movie.objects.all()
        
        similarities = []
        for movie in movies:
            emb = np.frombuffer(movie.emb)
            similarity = cosine_similarity(emb, emb_req)
            similarities.append((movie, similarity))
        
        
        recommended_movie = max(similarities, key=lambda x: x[1])[0]
        
        return render(request, 'suggestions.HTML', {'recommended_movie': recommended_movie})
    
    return render(request, 'suggestions.HTML')
