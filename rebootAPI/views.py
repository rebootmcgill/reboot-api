from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from machinerequests.models import CPU, OperatingSystem, Preset, Request, Machine
from django.contrib.auth.models import User
from rest_framework.decorators import list_route
from django.utils import timezone
from datetime import datetime

# Data Serializers


class CPUSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CPU
        fields = ('url', 'name', 'cores', 'x64', 'clock')


class OperatingSystemSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ('url', 'name', 'version', 'experimental')


class PresetSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preset
        fields = ('url', 'cpu', 'ram', 'hdd')


class RequestSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Request
        fields = ('url', 'family_name', 'given_name', 'requester_type', 'faculty_and_dept', 'organization', 'preset',
            'os', 'machine_use', 'need_display', 'need_keyboard', 'need_mouse', 'need_ethernet', 'extra_information',
            'amount', 'filled', 'filled_at', 'requested_at')


class MachineSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ('url', 'request', 'fulfiller', 'cpu', 'ram', 'hdd', 'pickedup_at', 'notes', 'picked_up')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'is_staff')


# Views
class StatsAPI(APIView):
    """
    Return a list of request statistics
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        now = timezone.now()
        month = datetime(now.year, now.month, 1, tzinfo=now.tzinfo)
        monthly = {'requests': Request.objects.filter(requested_at__gte=month).count(),
            'fulfill': Request.objects.filter(filled=True, filled_at__gte=month).count(),
            'pickup': Machine.objects.filter(picked_up=True, pickedup_at__gte=month).count()}
        pending = {'fulfill': Request.objects.filter(filled=False).count(),
            'pickup': Machine.objects.filter(picked_up=False).count()}
        return Response({'current': pending, 'month': monthly})


# View Sets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer


class OperatingSystemViewSet(viewsets.ModelViewSet):
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer


class PresetViewSet(viewsets.ModelViewSet):
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @list_route
    def pending(self, request):
        queryset = Request.objects.filter(filled=False)
        page = self.paginate_queryset(queryset)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)


class PendingViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.filter(filled=False)
    serializer_class = RequestSerializer


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    @list_route
    def pending(self, request):
        queryset = Machine.objects.filter(picked_up=False)
        page = self.paginate_queryset(queryset)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)


class PickupViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.filter(picked_up=False)
    serializer_class = MachineSerializer
# The router routes all the routes

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cpus', CPUViewSet)
router.register(r'os', OperatingSystemViewSet)
router.register(r'presets', PresetViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'pending', PendingViewSet, base_name='pending')
router.register(r'pickup', PickupViewSet, base_name='pickup')


def get_router():
    return router