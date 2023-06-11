from rest_framework.views import APIView, Request, Response, status
from pets.models import Pet
from pets.serializer import PetSerializer
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(instance=result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
      
        group_data = serializer.validated_data.pop('group')

        group, _ = Group.objects.get_or_create(scientific_name=group_data['scientific_name'])

        traits_data = serializer.validated_data.pop('traits')

        pet = Pet.objects.create(group=group, **serializer.validated_data)

        traits = []
        for trait_data in traits_data:
            trait, _ = Trait.objects.get_or_create(trait_name__iexact=trait_data['trait_name'])
            
            traits.append(trait)
            pet.traits.add(*traits)

        serializer = PetSerializer(instance=pet)
        
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


   



       

       

      