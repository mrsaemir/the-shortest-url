from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register('encode', views.Encode, basename='encode')
router.register('decode', views.Decode, basename='decode')
