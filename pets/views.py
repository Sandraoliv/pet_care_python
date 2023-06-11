from rest_framework.views import APIView, Request, Response, status
from pets.models import Pet
from pets.serializer import PetSerializer
from groups.models import Group
from traits.models import Trait
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        trait = request.query_params.get('trait', None)
        if trait:
            pets = pets.filter(traits__trait_name__iexact=trait)

        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(instance=result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
      
        group_data = serializer.validated_data.pop('group')
        traits_data = serializer.validated_data.pop('traits')
        pets_data = serializer.validated_data

        instance_group, _ = Group.objects.get_or_create(scientific_name=group_data['scientific_name'])
        
        instance_pet = Pet.objects.create(group=instance_group, **pets_data)

        for trait_data in traits_data:
            
            instance_trait, _ = Trait.objects.get_or_create(trait_name__iexact=trait_data['trait_name'])
            
            instance_trait.traits.add(instance_pet)

        serializer = PetSerializer(instance_pet)
        
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        

class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
       
        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request: Request, pet_id: int) -> Response:
        serializer = PetSerializer(data=request.data, partial=True)
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)
        pet.save()

        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    

    


    


       

       

      