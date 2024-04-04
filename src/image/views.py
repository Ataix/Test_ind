import io

import torch
from PIL import Image as im

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import ImageModel
from .serializers import ImageSerializer


class ImageCreateView(CreateAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['initial_image']

        # uploaded_img_qs = ImageModel.objects.filter().last()
        uploaded_img_qs = image
        # img_bytes = uploaded_img_qs.initial_image.read()
        img_bytes = uploaded_img_qs.read()
        img = im.open(io.BytesIO(img_bytes))

        path_hubconfig = "yolov5"
        path_weightfile = "yolov5n.pt"  # or any custom trained model

        model = torch.hub.load(path_hubconfig, 'custom',
                               path=path_weightfile, source='local')

        results = model(img, size=640)
        results.render()
        # for img in results.ims:
        #     img_base64 = im.fromarray(img)
        #     img_base64.save(f"images/{image}_res", format="JPEG")
        #
        # inference_img = f"images/{image}_res.jpg"
        result_json = results.pandas().xyxy[0].to_json(orient='records')

        serializer.validated_data['result_json'] = result_json
        # serializer.validated_data['result_image'] = inference_img
        serializer.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


