from django.http import JsonResponse
from .graph import graph

class PartySimilaritiesJoiner:

    def compare(self, similarities: dict) -> list:
        try:
            results = graph.invoke({"similarities": similarities})

            return JsonResponse(
                {
                    "original": {
                        "id": results["similarities"]["id"],
                        "acronym": results["similarities"]["acronym"],
                        "name": results["similarities"]["name"]
                    },
                    "duplicated": results["result"],
                }, 
                status=200
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    "error": str(e),
                },
                status = 404
            )
