from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Note
from .serializers import NoteSeralizer

@api_view(['GET'])
def getRoutes(req):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def getNotes(req):
    notes = Note.objects.all().order_by('-updated')
    serializers = NoteSeralizer(notes, many=True)
    return Response(serializers.data)   


@api_view(['GET'])
def getNote(req, pk):
    notes = Note.objects.get(id=pk)
    serializers = NoteSeralizer(notes, many=False)
    return Response(serializers.data)   

@api_view(['POST'])
def createNote(req):
    data = req.data
    note = Note.objects.create(
        body = data['body']
    )
    serializer = NoteSeralizer(note, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateNote(req, pk):
    data = req.data 
    notes = Note.objects.get(id=pk)
    serializers = NoteSeralizer(instance=notes, data=data)
    
    if serializers.is_valid():
        serializers.save()    
    
    return Response(serializers.data)

@api_view(['DELETE'])
def deleteNote(req, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')