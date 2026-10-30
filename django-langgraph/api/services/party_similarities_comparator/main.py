from django.http import JsonResponse
from .graph import graph

class PartySimilaritiesComparatorService:

    def compare(self, coincidences: dict) -> list:

        try:
            similarities = graph.invoke({"coincidences": coincidences})
            #print(similarities)
            return JsonResponse(
                {
                    "results": similarities['results']
                }, 
                status=200
            )
        except Exception as e:
            return JsonResponse(
                {
                    "results": str(e),
                },
                status = 404
            )
